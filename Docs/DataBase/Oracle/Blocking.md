В Oracle (PL/SQL) информация о блокировках хранится в динамических представлениях производительности (`V$`-views). Сами блокировки управляются ядром БД, но вы можете запросить их состояние из SQL или PL/SQL.

### 🔍 Основной запрос для поиска блокировок на таблице
```sql
SELECT 
    o.owner           AS table_owner,
    o.object_name     AS table_name,
    o.object_type,
    s.sid,
    s.serial#,
    s.username        AS db_user,
    s.osuser,
    s.machine,
    s.program,
    s.status          AS session_status,
    l.lmode,
    CASE l.lmode
        WHEN 0 THEN 'None'
        WHEN 1 THEN 'Null'
        WHEN 2 THEN 'Row-S (SS)'
        WHEN 3 THEN 'Row-X (SX)'
        WHEN 4 THEN 'Share'
        WHEN 5 THEN 'S/Row-X (SSX)'
        WHEN 6 THEN 'Exclusive'
        ELSE 'Unknown'
    END               AS lock_mode,
    CASE l.block
        WHEN 1 THEN '🔴 BLOCKING (удерживает блокировку)'
        ELSE '🟢 WAITING / IDLE'
    END               AS lock_role
FROM v$lock l
JOIN v$session s   ON l.sid = s.sid
JOIN dba_objects o ON l.id1 = o.object_id
WHERE l.type = 'TM'                  -- TM = DML/Table lock
  AND o.object_name = UPPER('ВАША_ТАБЛИЦА')
  AND o.owner       = UPPER('ВАША_СХЕМА');
```

### 📖 Расшифровка ключевых полей
| Поле | Значение |
|------|----------|
| `l.type = 'TM'` | Блокировка уровня таблицы (DML: `INSERT/UPDATE/DELETE/SELECT ... FOR UPDATE`) |
| `l.lmode` | Режим блокировки, удерживаемый сессией (2–6 см. выше) |
| `l.block = 1` | Сессия **блокирует** другие сессии |
| `s.status` | `ACTIVE` (выполняет запрос) / `INACTIVE` (ожидает действий пользователя) |
| `s.blocking_session` | SID сессии, которая блокирует текущую (если запросить через `V$SESSION`) |

### 💻 Как использовать внутри PL/SQL
```plsql
DECLARE
    CURSOR c_table_locks IS
        SELECT o.owner, o.object_name, s.sid, s.serial#, s.username, 
               l.lmode, l.block
        FROM v$lock l
        JOIN v$session s ON l.sid = s.sid
        JOIN dba_objects o ON l.id1 = o.object_id
        WHERE l.type = 'TM'
          AND o.object_name = 'EMPLOYEES'
          AND o.owner       = 'HR';
          
    TYPE t_lock IS TABLE OF c_table_locks%ROWTYPE;
    v_locks t_lock;
BEGIN
    OPEN c_table_locks;
    FETCH c_table_locks BULK COLLECT INTO v_locks;
    CLOSE c_table_locks;

    IF v_locks.COUNT = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Блокировок на таблице не обнаружено.');
    ELSE
        FOR i IN 1 .. v_locks.COUNT LOOP
            DBMS_OUTPUT.PUT_LINE(
                'Session: ' || v_locks(i).sid || ',' || v_locks(i).serial# ||
                ' | User: ' || v_locks(i).username ||
                ' | Lmode: ' || v_locks(i).lmode ||
                ' | Block: ' || CASE WHEN v_locks(i).block = 1 THEN 'YES' ELSE 'NO' END
            );
        END LOOP;
    END IF;
END;
/
```

### 🔑 Необходимые привилегии
Для выполнения запросов нужны права на `V$`-представления:
```sql
-- Для DBA или администратора
GRANT SELECT ON sys.v_$lock    TO ваш_пользователь;
GRANT SELECT ON sys.v_$session TO ваш_пользователь;
GRANT SELECT ON dba_objects    TO ваш_пользователь;
-- Или проще:
GRANT SELECT_CATALOG_ROLE TO ваш_пользователь;
```
> ⚠️ Если нет доступа к `DBA_OBJECTS`, замените на `ALL_OBJECTS`, но тогда увидите только таблицы, к которым у вас есть права.

### 🛠 Практические рекомендации
1. **Как снять блокировку?**  
   Обычно достаточно выполнить `COMMIT;` или `ROLLBACK;` в блокирующей сессии.  
   Если сессия "зависла", можно принудительно завершить её:
   ```sql
   ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;
   ```
2. **`V$LOCKED_OBJECT` vs `V$LOCK`**  
   `V$LOCKED_OBJECT` проще, но показывает только факт блокировки объекта. `V$LOCK` даёт детализацию по режимам и флагам блокировки (`block=1`).
3. **Row-level блокировки**  
   Oracle не хранит информацию о заблокированных строках в системных представлениях. Чтобы узнать, какие строки заблокированы, нужно попробовать `SELECT ... FOR UPDATE NOWAIT` или использовать `DBMS_LOCK` / трассировку.
4. **Мониторинг в реальном времени**  
   Для постоянного отслеживания используйте Oracle Enterprise Manager, `ASH` (`V$ACTIVE_SESSION_HISTORY`) или настройте оповещения через `DBMS_SCHEDULER`.

Вот готовый, production-ready скрипт для построения **дерева блокировок** (кто кого блокирует, включая цепочки). Он работает в Oracle 11.2+ и выводит иерархию в читаемом виде.

### 📜 Скрипт: Дерево блокировок
```sql
WITH relevant_locks AS (
    -- Оставляем только значимые блокировки (TX/TM), которые либо удерживаются с флагом block=1, либо запрашиваются
    SELECT sid, type, lmode, request, id1, id2
    FROM v$lock
    WHERE type IN ('TM', 'TX')
      AND (block = 1 OR request > 0)
),
session_hierarchy AS (
    SELECT 
        s.sid,
        s.serial#,
        s.username,
        s.status,
        s.osuser,
        s.machine,
        s.program,
        s.sql_id,
        s.blocking_session,
        s.seconds_in_wait,
        s.event,
        rl.type,
        rl.lmode,
        rl.request,
        CASE WHEN rl.type = 'TM' THEN o.owner || '.' || o.object_name END AS locked_object
    FROM v$session s
    LEFT JOIN relevant_locks rl ON s.sid = rl.sid
    LEFT JOIN dba_objects o ON rl.id1 = o.object_id
    WHERE s.blocking_session IS NOT NULL 
       OR s.sid IN (SELECT blocking_session FROM v$session WHERE blocking_session IS NOT NULL)
)
SELECT 
    LPAD(' ', 4 * (LEVEL - 1)) || h.sid || ',' || h.serial# AS "Session Chain",
    h.username,
    h.status,
    h.machine,
    h.program,
    CASE h.type WHEN 'TM' THEN 'TABLE' WHEN 'TX' THEN 'ROW/TRANS' ELSE h.type END AS "Lock Type",
    CASE h.lmode 
        WHEN 2 THEN 'Row-S' WHEN 3 THEN 'Row-X' 
        WHEN 4 THEN 'Share' WHEN 6 THEN 'Exclusive' 
        ELSE TO_CHAR(h.lmode) END AS "Held Mode",
    CASE h.request 
        WHEN 2 THEN 'Row-S' WHEN 3 THEN 'Row-X' 
        WHEN 4 THEN 'Share' WHEN 6 THEN 'Exclusive' 
        ELSE TO_CHAR(h.request) END AS "Requested Mode",
    h.locked_object,
    sql.sql_text,
    h.seconds_in_wait AS "Wait (sec)",
    h.event
FROM session_hierarchy h
LEFT JOIN v$sql sql ON h.sql_id = sql.sql_id
CONNECT BY NOCYCLE PRIOR h.sid = h.blocking_session
START WITH h.blocking_session IS NULL 
           AND h.sid IN (SELECT DISTINCT blocking_session FROM v$session WHERE blocking_session IS NOT NULL)
ORDER SIBLINGS BY h.sid;
```

### 🔍 Как читать вывод
| Колонка | Значение |
|---------|----------|
| `Session Chain` | Иерархия с отступами. Корень (без отступа) → блокирует следующих, те блокируют дальше |
| `Held Mode` | Режим блокировки, который **удерживает** сессия |
| `Requested Mode` | Режим, который **ждет** сессия |
| `Wait (sec)` | Сколько секунд сессия уже ждет |
| `Event` | Ожидание (обычно `enq: TX - row lock contention` или `enq: TM - contention`) |

Пример вывода:
```
Session Chain    | USERNAME | Held  | Requested | Object          | SQL Text
-----------------+----------+-------+-----------+-----------------+------------------
45,1023          | HR       | Excl  | -         | HR.EMPLOYEES    | UPDATE employees...
    78,5542      | SALES    | -     | Excl      | HR.EMPLOYEES    | SELECT ... FOR UPDATE
    91,3310      | REPORT   | -     | Row-X     | HR.DEPARTMENTS  | DELETE departments...
```
Здесь сессия `45` блокирует `78`, а `78` косвенно держит `91` (через другую таблицу или цепочку транзакций).

### ⚠️ Важные нюансы
1. **RAC (кластер)**: Замените `V$SESSION` → `GV$SESSION`, `V$LOCK` → `GV$LOCK`, добавьте колонку `INST_ID` и в `START WITH` учитывайте инстансы.
2. **Динамичность**: Блокировки живут миллисекунды. Если дерево пустое, скорее всего, все уже закоммитилось/откатилось.
3. **Дубликаты строк**: У одной сессии может быть несколько строк (разные блокировки). Это нормально. Фильтр `relevant_locks` оставляет только те, что участвуют в contention.
4. **Права**: `SELECT_CATALOG_ROLE` или `SELECT ANY DICTIONARY`. Без них замените `dba_objects` на `all_objects`.

### 🗑 Как безопасно снять блокировку
1. **Предпочтительно**: Попросить владельца сессии выполнить `COMMIT;` или `ROLLBACK;`.
2. **Если сессия "зависла"**:
   ```sql
   ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;
   ```
   > 🔸 `IMMEDIATE` не ждет отката транзакции, но оставляет её в состоянии `MARKED FOR KILL`. Для полного завершения лучше сначала сделать `ALTER SYSTEM DISCONNECT SESSION ... POST_TRANSACTION`.

3. **Автоматическое обнаружение deadlock**: Oracle сам разрушает deadlock через ~3 сек, выбирая сессию с наименьшим rollback-объемом. В alert.log будет `ORA-00060`.

### 💡 Бонус: Быстрый поиск только "корневых" блокировщиков
Если нужно только найти инициаторов проблем (без цепочек):
```sql
SELECT s.sid, s.serial#, s.username, s.machine, s.program,
       s.seconds_in_wait, s.event, sql.sql_text
FROM v$session s
LEFT JOIN v$sql sql ON s.sql_id = sql.sql_id
WHERE s.sid IN (SELECT blocking_session FROM v$session WHERE blocking_session IS NOT NULL)
  AND s.status = 'ACTIVE';
```