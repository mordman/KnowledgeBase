Миграция кода с **Oracle PL/SQL** на **PostgreSQL PL/pgSQL** — это не просто синтаксическая замена, а смена парадигмы работы с данными, сессиями и оптимизатором. Ниже собраны ключевые точки, где чаще всего возникают баги, с конкретными примерами и рекомендациями по исправлению.

---
### 🔍 1. `NULL` vs пустая строка `''` (Топ-1 причина багов)
| Oracle | PostgreSQL |
|--------|------------|
| `''` автоматически превращается в `NULL` | `''` — это строка длины 0, `NULL` — отсутствие значения |
| `LENGTH('')` → `NULL` | `LENGTH('')` → `0` |
| `WHERE col = ''` работает как `IS NULL` | `WHERE col = ''` ищет реально пустую строку |
| `'A' \|\| ''` → `'A'` | `'A' \|\| ''` → `'A'` (совпадает, но логика разная) |

**Баг:** `COALESCE(col, 'default')` в Oracle заменит и `NULL`, и `''` (т.к. `''` стал `NULL`). В PG заменит только `NULL`.
**Fix:** 
- Явно приводить к единой семантике: `NULLIF(col, '')` или `NULLIF(TRIM(col), '')`
- В `WHERE` писать `col IS NULL OR col = ''`
- При миграции legacy-кода добавить проверку: `IF col = '' THEN col := NULL; END IF;`

---
### 📦 2. Типы данных и неявные преобразования
| Oracle | PostgreSQL | Комментарий |
|--------|------------|-------------|
| `NUMBER` | `NUMERIC` / `DECIMAL` | PG строже к масштабам: `NUMERIC(10,2)` не примет `10.123` без округления |
| `DATE` | `DATE` | В Oracle `DATE` хранит **дату+время до секунд**. В PG `DATE` только дата. Аналог: `TIMESTAMP(0)` или `TIMESTAMPTZ` |
| Нет `BOOLEAN` в SQL | `BOOLEAN` (`true`/`false`) | Oracle использует `CHAR(1)` с `'Y'/'N'` или `0/1`. В PG `IF flag = 'Y'` → `IF flag` |
| `VARCHAR2` | `VARCHAR` / `TEXT` | В PG `VARCHAR` и `TEXT` идентичны. `CHAR(n)` избегайте |

**Баг:** `WHERE char_col = 5` работает в Oracle (неявный каст), в PG → `ERROR: operator does not exist: character varying = integer`.
**Fix:** Явные касты: `char_col::int` или `CAST(char_col AS int)`. Включите `standard_conforming_strings = on` (по умолчанию в PG 9.1+).

---
### ⚠️ 3. `SELECT INTO` и исключения `NO_DATA_FOUND`
| Oracle | PostgreSQL |
|--------|------------|
| `SELECT col INTO var FROM t WHERE id=1;` → нет строк → `RAISE NO_DATA_FOUND` | → нет строк → `var := NULL`, **исключение не кидается** |
| `TOO_MANY_ROWS` при >1 строке | Берёт первую строку (или `ERROR: query returned more than one row` в зависимости от контекста) |

**Баг:** Логика `EXCEPTION WHEN NO_DATA_FOUND THEN ...` в PG никогда не сработает.
**Fix:**
```plpgsql
SELECT col INTO var FROM t WHERE id = 1;
IF NOT FOUND THEN
   -- аналог NO_DATA_FOUND
   var := NULL; -- или другая логика
END IF;
```
Или используйте `GET DIAGNOSTICS row_count = ROW_COUNT;` после `UPDATE/DELETE/SELECT`.

---
### 🔧 4. Синтаксис и встроенные функции (Шпаргалка)
| Oracle | PostgreSQL | Примечание |
|--------|------------|------------|
| `DECODE(col, v1, r1, default)` | `CASE col WHEN v1 THEN r1 ELSE default END` | |
| `NVL(a, b)` | `COALESCE(a, b)` | |
| `SYSDATE` | `CURRENT_TIMESTAMP` / `NOW()` | `CURRENT_DATE` если нужна только дата |
| `TRUNC(date_col)` | `DATE_TRUNC('day', date_col)` | или `date_col::date` |
| `seq_name.NEXTVAL` | `nextval('seq_name')` | В PG нельзя писать `seq.CURRVAL`, только `currval('seq_name')` |
| `SELECT 1 FROM DUAL` | `SELECT 1` | `DUAL` не нужен |
| `DBMS_OUTPUT.PUT_LINE` | `RAISE NOTICE` | |
| `RAISE_APPLICATION_ERROR(-20001, 'msg')` | `RAISE EXCEPTION 'msg' USING ERRCODE = 'P0001';` | Кастомные SQLSTATE: `P0000`–`P9999` |

---
### 📦 5. Пакеты, сессия и глобальные переменные
- **Oracle:** `PACKAGE` группирует процедуры/функции, поддерживает **пакетные переменные**, сохраняющие состояние между вызовами в рамках сессии.
- **PG:** Пакетов нет. Используйте `SCHEMA` для логической группировки.
- **Баг:** Код, полагающийся на `g_pkg_var := 10;`, теряет состояние или работает некорректно при использовании пула соединений (PgBouncer, connection recycling).
- **Fix:**
  - Передавать состояние через параметры функции
  - Использовать `current_setting('myapp.var')` + `set_config('myapp.var', '10', false)`
  - Временные таблицы (`CREATE TEMP TABLE`) для сложных состояний
  - ⚠️ `current_setting` **не совместим с session-based пулами** (режим `transaction` в PgBouncer сбрасывает сессию). Для таких окружений используйте только параметры/таблицы.

---
### 🔄 6. Динамический SQL и курсоры
| Oracle | PostgreSQL |
|--------|------------|
| `EXECUTE IMMEDIATE 'SQL' INTO var USING bind;` | `EXECUTE 'SQL' INTO var USING bind;` |
| `DBMS_SQL` | Нет аналога. Используйте `EXECUTE` + `format()` |
| `OPEN cur FOR SELECT ...` | `OPEN cur FOR EXECUTE format('...') USING ...` |

**Баг:** Конкатенация строк для SQL → SQL-инъекции и ошибки парсинга.
**Fix:**
```plpgsql
-- ✅ Правильно
EXECUTE format('UPDATE t SET val = %L WHERE id = $1', new_val) USING rec_id;

-- ❌ Опасно
EXECUTE 'UPDATE t SET val = ''' || new_val || ''' WHERE id = ' || rec_id;
```
Используйте `%I` (идентификатор), `%L` (литерал), `%s` (сырая строка) в `format()`.

---
### 🧩 7. Функции vs Процедуры, `OUT`-параметры, `PIPELINED`
- **Oracle:** `PROCEDURE` (действия), `FUNCTION` (возврат), `PIPELINED FUNCTION` (стриминг).
- **PG:** Исторически всё через `FUNCTION`. `PROCEDURE` (с PG 11) поддерживает `COMMIT`/`ROLLBACK` внутри, но для миграции проще оставить `FUNCTION`.
- **OUT-параметры:** 
  - Oracle: `PROCEDURE p(p1 IN, p2 OUT, p3 OUT)`
  - PG: `FUNCTION f(p1 IN, OUT p2, OUT p3) RETURNS RECORD` или `RETURNS TABLE(p2 type, p3 type)`
- **PIPELINED:** 
  ```plpgsql
  -- PG аналог
  CREATE OR REPLACE FUNCTION gen_rows()
  RETURNS TABLE(id int, val text) AS $$
  BEGIN
     RETURN QUERY SELECT id, val FROM source;
     -- или RETURN NEXT в цикле
  END;
  $$ LANGUAGE plpgsql;
  ```

---
### ⚡ 8. Производительность и волатильность функций
PG кэширует планы вызовов PL/pgSQL, но **не заглядывает внутрь** функции, если не указана волатильность.

| Атрибут | Когда использовать | Риск |
|---------|-------------------|------|
| `IMMUTABLE` | Только аргументы, нет БД, нет времени | Если использует `NOW()` или `SELECT` → планы кэшируются навсегда, возвращаются старые данные |
| `STABLE` | Читает БД, не меняет, результат одинаковый в транзакции | Оптимизатор может вынести вызов в `WHERE`/`JOIN` |
| `VOLATILE` | По умолчанию. DML, `RANDOM()`, `NOW()` | Не кэшируется, безопасно, но медленнее |

**Баг:** Функция помечена `IMMUTABLE`, но делает `SELECT count(*) FROM t`. После `INSERT` результат не меняется.
**Fix:** Всегда ставьте `STABLE` для `SELECT`-функций, `VOLATILE` для модификаций. Проверяйте через `EXPLAIN (ANALYZE, BUFFERS)`.

---
### ✅ Чек-лист миграции PL/SQL → PL/pgSQL
- [ ] Заменить `''` на `NULL` или явно обрабатывать `NULLIF(col, '')`
- [ ] `DATE` → `TIMESTAMP`/`TIMESTAMPTZ` (проверить все `TRUNC`, `SYSDATE`, арифметику дат)
- [ ] `DECODE` → `CASE`, `NVL` → `COALESCE`, `SYSDATE` → `NOW()`
- [ ] Убрать `FROM DUAL`
- [ ] `seq.NEXTVAL` → `nextval('seq')`
- [ ] Переписать логику `NO_DATA_FOUND` → `IF NOT FOUND THEN`
- [ ] Пакетные переменные → `current_setting` / temp tables / параметры
- [ ] Динамический SQL → `EXECUTE ... USING` + `format()`
- [ ] `OUT`-параметры → `RETURNS TABLE` или `OUT` в `FUNCTION`
- [ ] Проверить волатильность функций (`IMMUTABLE`/`STABLE`/`VOLATILE`)
- [ ] Протестировать в целевом пуле соединений (PgBouncer mode `transaction` сбрасывает сессию!)
- [ ] Запустить `pg_upgrade` / `ora2pg` с флагом `--check-only` и разобрать отчёт

---
### 💡 Итог
Основные баги при миграции возникают не из-за синтаксиса, а из-за **разной семантики**:
1. `''` vs `NULL`
2. `NO_DATA_FOUND` отсутствует в PG
3. Сессионное состояние пакетов не переносится автоматически
4. Неправильная волатильность функций ломает кэширование планов

Рекомендую использовать инструмент **`ora2pg`** (open source) для автоматической конвертации, но **всегда ревьюить** сгенерированный код вручную, особенно блоки `EXCEPTION`, динамический SQL и работу с датами.