## **Взаимоблокировки (Deadlocks)**

**Взаимоблокировка (deadlock)** — это ситуация, когда две или более транзакций блокируют друг друга, ожидая освобождения ресурсов, удерживаемых другой транзакцией. В результате ни одна из транзакций не может завершиться, и PostgreSQL вынужден прервать одну из них с ошибкой.

---

## **1. Как возникают взаимоблокировки?**

### **1.1. Пример взаимоблокировки**
Рассмотрим две транзакции, которые блокируют друг друга:

| **Транзакция 1**                     | **Транзакция 2**                     |
|--------------------------------------|--------------------------------------|
| `BEGIN;`                             | `BEGIN;`                             |
| `UPDATE accounts SET balance = balance - 100 WHERE id = 1;` |  |
|                                      | `UPDATE accounts SET balance = balance + 100 WHERE id = 2;` |
| `UPDATE accounts SET balance = balance + 100 WHERE id = 2;` |  |
|                                      | `UPDATE accounts SET balance = balance - 100 WHERE id = 1;` |
| **Ожидает освобождения строки 2**    | **Ожидает освобождения строки 1**    |

В этом случае:
- **Транзакция 1** заблокировала строку с `id = 1` и пытается заблокировать строку с `id = 2`.
- **Транзакция 2** заблокировала строку с `id = 2` и пытается заблокировать строку с `id = 1`.

PostgreSQL обнаруживает взаимоблокировку и **прерывает одну из транзакций** с ошибкой:
```
ERROR:  deadlock detected
DETAIL:  Process 1234 waits for ShareLock on transaction 5678; blocked by process 5678.
Process 5678 waits for ShareLock on transaction 1234; blocked by process 1234.
HINT:  See server log for query details.
```

---

## **2. Почему возникают взаимоблокировки?**

Взаимоблокировки возникают из-за **неправильного порядка блокировок** и **конкуренции за ресурсы**. Основные причины:

1. **Неправильный порядок обновления таблиц**:
   - Если транзакции обновляют таблицы в **разном порядке**, это может привести к взаимоблокировке.

2. **Длительные транзакции**:
   - Чем дольше транзакция удерживает блокировки, тем выше вероятность взаимоблокировки.

3. **Отсутствие индексов**:
   - Если запрос блокирует много строк из-за отсутствия индексов, это увеличивает вероятность конфликтов.

4. **Явные блокировки (`SELECT FOR UPDATE`)**:
   - Если транзакции используют явные блокировки и захватывают ресурсы в разном порядке, это может привести к взаимоблокировке.

---

## **3. Как избежать взаимоблокировок?**

### **3.1. Соблюдайте одинаковый порядок доступа к ресурсам**
Если все транзакции обновляют таблицы в **одном и том же порядке**, вероятность взаимоблокировки снижается.

**Пример:**
```sql
-- Транзакция 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Сначала строка 1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Потом строка 2
COMMIT;

-- Транзакция 2
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Сначала строка 1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Потом строка 2
COMMIT;
```

---

### **3.2. Сокращайте время выполнения транзакций**
- **Держите транзакции короткими** — чем быстрее транзакция завершается, тем меньше вероятность взаимоблокировки.
- **Избегайте длительных операций** внутри транзакций (например, ожидание пользовательского ввода).

---

### **3.3. Используйте правильные уровни изоляции**
PostgreSQL поддерживает несколько уровней изоляции транзакций:
- **`READ COMMITTED`** (по умолчанию) — минимальный уровень блокировок.
- **`REPEATABLE READ`** — блокирует строки от изменений другими транзакциями.
- **`SERIALIZABLE`** — самый строгий уровень, может увеличивать вероятность взаимоблокировок.

**Рекомендация:** Используйте `READ COMMITTED`, если не требуется более строгая изоляция.

---

### **3.4. Избегайте явных блокировок (`SELECT FOR UPDATE`)**
Если возможно, используйте **оптимистичные блокировки** вместо пессимистичных (`SELECT FOR UPDATE`).

**Пример оптимистичной блокировки:**
```sql
-- Вместо:
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- ... некоторые операции ...
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- Используйте:
BEGIN;
-- Проверяем версию записи (например, по полю version)
SELECT balance, version FROM accounts WHERE id = 1;
-- ... некоторые операции ...
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = <предыдущая версия>;
COMMIT;
```

---

### **3.5. Добавляйте индексы**
Если запрос блокирует много строк из-за отсутствия индексов, добавьте индексы, чтобы уменьшить количество блокируемых строк.

**Пример:**
```sql
-- Если запрос блокирует много строк из-за отсутствия индекса:
SELECT * FROM accounts WHERE user_id = 123 FOR UPDATE;

-- Добавьте индекс:
CREATE INDEX idx_accounts_user_id ON accounts(user_id);
```

---

### **3.6. Используйте `ON CONFLICT` для вставок**
Если несколько транзакций пытаются вставить одни и те же данные, используйте `ON CONFLICT` вместо явной проверки и обновления.

**Пример:**
```sql
-- Вместо:
BEGIN;
SELECT 1 FROM users WHERE email = 'test@example.com' FOR UPDATE;
-- Если не существует, вставляем
INSERT INTO users (email, name) VALUES ('test@example.com', 'Иван');
COMMIT;

-- Используйте:
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Иван')
ON CONFLICT (email) DO NOTHING;
```

---

### **3.7. Логируйте и анализируйте взаимоблокировки**
PostgreSQL записывает информацию о взаимоблокировках в лог. Настройте логирование, чтобы анализировать причины:

```sql
-- В файле postgresql.conf:
log_lock_waits = on
log_statement = 'all'
deadlock_timeout = 1s
```

**Пример лога взаимоблокировки:**
```
2023-01-01 12:00:00 UTC [1234] ERROR:  deadlock detected
2023-01-01 12:00:00 UTC [1234] DETAIL:  Process 1234 waits for ShareLock on transaction 5678; blocked by process 5678.
Process 5678 waits for ShareLock on transaction 1234; blocked by process 1234.
2023-01-01 12:00:00 UTC [1234] HINT:  See server log for query details.
2023-01-01 12:00:00 UTC [1234] STATEMENT:  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
```

---

## **4. Как обрабатывать взаимоблокировки в коде?**

### **4.1. Повторный запуск транзакции**
Если транзакция завершилась с ошибкой взаимоблокировки, её можно **повторить**.

**Пример на Python (с использованием `psycopg2`):**
```python
import psycopg2
from psycopg2 import OperationalError

def transfer_money(sender_id, receiver_id, amount):
    while True:
        try:
            with connection.cursor() as cursor:
                cursor.execute("BEGIN;")
                cursor.execute(
                    "UPDATE accounts SET balance = balance - %s WHERE id = %s;",
                    (amount, sender_id)
                )
                cursor.execute(
                    "UPDATE accounts SET balance = balance + %s WHERE id = %s;",
                    (amount, receiver_id)
                )
                cursor.execute("COMMIT;")
                break
        except OperationalError as e:
            if "deadlock detected" in str(e):
                print("Взаимоблокировка. Повторяем транзакцию...")
                continue
            else:
                raise
```

---

### **4.2. Ограничение количества повторов**
Чтобы избежать бесконечных повторов, ограничьте количество попыток:

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN;")
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s;", (amount, sender_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s;", (amount, receiver_id))
            cursor.execute("COMMIT;")
            break
    except OperationalError as e:
        if "deadlock detected" in str(e) and attempt < max_retries - 1:
            print(f"Взаимоблокировка. Попытка {attempt + 1} из {max_retries}...")
            time.sleep(0.1)  # Пауза перед повтором
            continue
        else:
            raise
```

---

## **5. Итоговые рекомендации**
| Рекомендация                          | Описание                                                                                     |
|---------------------------------------|---------------------------------------------------------------------------------------------|
| Соблюдайте порядок доступа к ресурсам | Все транзакции должны обновлять таблицы в одном и том же порядке.                            |
| Сокращайте время транзакций           | Держите транзакции короткими.                                                               |
| Используйте оптимистичные блокировки   | Вместо `SELECT FOR UPDATE` используйте проверку версии.                                     |
| Добавляйте индексы                    | Уменьшайте количество блокируемых строк.                                                   |
| Логируйте взаимоблокировки            | Настройте логирование для анализа причин.                                                   |
| Повторяйте транзакции                 | Если произошла взаимоблокировка, повторяйте транзакцию с паузой.                            |
| Используйте `ON CONFLICT`             | Для вставок с возможными конфликтами.                                                       |

---

## **6. Пример оптимизации кода**
**Исходный код (проблемный):**
```python
def transfer_money(sender_id, receiver_id, amount):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        cursor.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE id = {sender_id};")
        cursor.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = {receiver_id};")
        cursor.execute("COMMIT;")
```
**Проблемы:**
- Нет обработки взаимоблокировок.
- Порядок обновления таблиц не фиксирован.

**Оптимизированный код:**
```python
def transfer_money(sender_id, receiver_id, amount, max_retries=3):
    for attempt in range(max_retries):
        try:
            with connection.cursor() as cursor:
                cursor.execute("BEGIN;")
                # Всегда обновляем сначала отправителя, потом получателя
                cursor.execute(
                    "UPDATE accounts SET balance = balance - %s WHERE id = %s;",
                    (amount, min(sender_id, receiver_id))  # Фиксированный порядок
                )
                cursor.execute(
                    "UPDATE accounts SET balance = balance + %s WHERE id = %s;",
                    (amount, max(sender_id, receiver_id))
                )
                cursor.execute("COMMIT;")
                break
        except OperationalError as e:
            if "deadlock detected" in str(e) and attempt < max_retries - 1:
                time.sleep(0.1 * (attempt + 1))  # Экспоненциальная задержка
                continue
            else:
                raise
```

---