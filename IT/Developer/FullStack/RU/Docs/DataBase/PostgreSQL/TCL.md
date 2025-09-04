## **TCL (Transaction Control Language)**

**TCL (Transaction Control Language)** — это набор команд для управления **транзакциями** в базе данных. Транзакции позволяют группировать несколько операций в одну логическую единицу, обеспечивая **атомарность**, **согласованность**, **изолированность** и **долговечность** (ACID).

---

### **Основные команды TCL в PostgreSQL**

| Команда            | Описание                                                                                     |
|--------------------|---------------------------------------------------------------------------------------------|
| **`BEGIN`**        | Начало транзакции.                                                                           |
| **`COMMIT`**       | Фиксация транзакции (сохранение изменений).                                                 |
| **`ROLLBACK`**     | Откат транзакции (возврат к состоянию до начала транзакции).                                 |
| **`SAVEPOINT`**    | Создание точки сохранения внутри транзакции.                                                 |
| **`RELEASE SAVEPOINT`** | Удаление точки сохранения.                                                                  |
| **`ROLLBACK TO SAVEPOINT`** | Откат к точке сохранения (без отката всей транзакции).                                      |

---

## **1. Базовые примеры использования TCL**

### **1.1. Простая транзакция**

```sql
-- Начало транзакции
BEGIN;

-- Вставляем нового пользователя
INSERT INTO users (name, email, age)
VALUES ('Иван Иванов', 'ivan@example.com', 30);

-- Обновляем баланс пользователя
UPDATE accounts
SET balance = balance - 100
WHERE user_id = 1;

-- Проверяем баланс
SELECT balance FROM accounts WHERE user_id = 1;

-- Если всё хорошо, фиксируем транзакцию
COMMIT;

-- Если ошибка, откатываем транзакцию
-- ROLLBACK;
```

---

### **1.2. Транзакция с обработкой ошибок**

```sql
BEGIN;

-- Вставляем нового пользователя
INSERT INTO users (name, email, age)
VALUES ('Иван Иванов', 'ivan@example.com', 30);

-- Пытаемся обновить баланс
UPDATE accounts
SET balance = balance - 1000
WHERE user_id = 1;

-- Проверяем, не ушёл ли баланс в минус
IF (SELECT balance FROM accounts WHERE user_id = 1) < 0 THEN
    -- Откат транзакции
    ROLLBACK;
    RAISE NOTICE 'Недостаточно средств на счёте!';
ELSE
    -- Фиксация транзакции
    COMMIT;
    RAISE NOTICE 'Транзакция успешно завершена!';
END IF;
```

---

## **2. Использование точек сохранения (`SAVEPOINT`)**

Точки сохранения позволяют откатывать часть транзакции, не отменяя её полностью.

### **2.1. Создание и использование точек сохранения**

```sql
BEGIN;

-- Вставляем нового пользователя
INSERT INTO users (name, email, age)
VALUES ('Иван Иванов', 'ivan@example.com', 30);

-- Создаём точку сохранения
SAVEPOINT after_user_insert;

-- Обновляем баланс пользователя
UPDATE accounts
SET balance = balance - 100
WHERE user_id = 1;

-- Проверяем баланс
IF (SELECT balance FROM accounts WHERE user_id = 1) < 0 THEN
    -- Откат к точке сохранения
    ROLLBACK TO SAVEPOINT after_user_insert;
    RAISE NOTICE 'Недостаточно средств на счёте! Откат к точке после вставки пользователя.';
ELSE
    -- Фиксируем транзакцию
    COMMIT;
    RAISE NOTICE 'Транзакция успешно завершена!';
END IF;

-- Удаляем точку сохранения
RELEASE SAVEPOINT after_user_insert;
```

---

## **3. Уровни изоляции транзакций**

PostgreSQL поддерживает **четыре уровня изоляции транзакций**, которые определяют, как транзакции взаимодействуют друг с другом.

| Уровень изоляции       | Описание                                                                                     | Проблемы                                                                                   |
|------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **`READ UNCOMMITTED`** | Чтение незафиксированных данных (грязное чтение).                                           | Грязное чтение, неповторяющееся чтение, фантомное чтение.                                  |
| **`READ COMMITTED`**   | Чтение только зафиксированных данных (уровень по умолчанию в PostgreSQL).                     | Неповторяющееся чтение, фантомное чтение.                                                  |
| **`REPEATABLE READ`**  | Гарантирует, что повторное чтение в рамках транзакции вернёт те же данные.                   | Фантомное чтение (но не в PostgreSQL благодаря **MVCC**).                                  |
| **`SERIALIZABLE`**    | Самый строгий уровень: транзакции выполняются так, как будто последовательно.                | Нет проблем с согласованностью, но возможны **deadlock**.                                 |

---

### **3.1. Установка уровня изоляции**

```sql
-- Установить уровень изоляции для текущей транзакции
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN;
    -- Запросы в транзакции
    SELECT * FROM accounts WHERE user_id = 1;
COMMIT;
```

---

## **4. Примеры использования TCL в реальных сценариях**

### **4.1. Перевод денег между счетами**

```sql
BEGIN;

-- Снимаем деньги со счёта отправителя
UPDATE accounts
SET balance = balance - 100
WHERE user_id = 1;

-- Проверяем, не ушёл ли баланс в минус
IF (SELECT balance FROM accounts WHERE user_id = 1) < 0 THEN
    ROLLBACK;
    RAISE NOTICE 'Недостаточно средств на счёте отправителя!';
ELSE
    -- Зачисляем деньги на счёт получателя
    UPDATE accounts
    SET balance = balance + 100
    WHERE user_id = 2;

    -- Фиксируем транзакцию
    COMMIT;
    RAISE NOTICE 'Перевод успешно выполнен!';
END IF;
```

---

### **4.2. Бронирование билетов**

```sql
BEGIN;

-- Проверяем наличие свободных мест
IF (SELECT available_seats FROM flights WHERE flight_id = 1) > 0 THEN
    -- Бронируем место
    UPDATE flights
    SET available_seats = available_seats - 1
    WHERE flight_id = 1;

    -- Создаём запись о бронировании
    INSERT INTO bookings (user_id, flight_id, booking_time)
    VALUES (1, 1, NOW());

    -- Фиксируем транзакцию
    COMMIT;
    RAISE NOTICE 'Билет успешно забронирован!';
ELSE
    -- Откат транзакции
    ROLLBACK;
    RAISE NOTICE 'Нет свободных мест на рейсе!';
END IF;
```

---

### **4.3. Обновление данных с проверкой условий**

```sql
BEGIN;

-- Обновляем данные пользователя
UPDATE users
SET email = 'new_email@example.com'
WHERE id = 1;

-- Проверяем, было ли обновление
IF NOT FOUND THEN
    ROLLBACK;
    RAISE NOTICE 'Пользователь с id=1 не найден!';
ELSE
    -- Создаём точку сохранения
    SAVEPOINT after_email_update;

    -- Обновляем дополнительные данные
    UPDATE user_profiles
    SET preferences = '{"theme": "dark"}'
    WHERE user_id = 1;

    -- Проверяем, было ли обновление профиля
    IF NOT FOUND THEN
        -- Откат к точке сохранения
        ROLLBACK TO SAVEPOINT after_email_update;
        RAISE NOTICE 'Профиль пользователя не найден! Откат к точке после обновления email.';
    END IF;

    -- Фиксируем транзакцию
    COMMIT;
    RAISE NOTICE 'Данные пользователя успешно обновлены!';
END IF;
```

---

## **5. Использование TCL в функциях и процедурах**

### **5.1. Пример функции с транзакцией**

```sql
CREATE OR REPLACE FUNCTION transfer_funds(
    sender_id INT,
    receiver_id INT,
    amount DECIMAL
) RETURNS BOOLEAN AS $$
DECLARE
    sender_balance DECIMAL;
    receiver_balance DECIMAL;
BEGIN
    -- Начало транзакции
    BEGIN
        -- Проверяем баланс отправителя
        SELECT balance INTO sender_balance
        FROM accounts
        WHERE user_id = sender_id;

        IF sender_balance < amount THEN
            RAISE EXCEPTION 'Недостаточно средств на счёте отправителя!';
            RETURN FALSE;
        END IF;

        -- Снимаем деньги со счёта отправителя
        UPDATE accounts
        SET balance = balance - amount
        WHERE user_id = sender_id;

        -- Зачисляем деньги на счёт получателя
        UPDATE accounts
        SET balance = balance + amount
        WHERE user_id = receiver_id;

        -- Фиксируем транзакцию
        COMMIT;
        RETURN TRUE;
    EXCEPTION WHEN OTHERS THEN
        -- Откат транзакции в случае ошибки
        ROLLBACK;
        RAISE NOTICE 'Ошибка при переводе средств: %', SQLERRM;
        RETURN FALSE;
    END;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова функции
SELECT transfer_funds(1, 2, 100);
```

---

### **5.2. Пример процедуры с транзакцией**

```sql
CREATE OR REPLACE PROCEDURE update_user_email(
    user_id INT,
    new_email TEXT
) AS $$
BEGIN
    -- Начало транзакции
    BEGIN
        -- Обновляем email пользователя
        UPDATE users
        SET email = new_email
        WHERE id = user_id;

        -- Проверяем, было ли обновление
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Пользователь с id=% не найден!', user_id;
        END IF;

        -- Фиксируем транзакцию
        COMMIT;
        RAISE NOTICE 'Email пользователя успешно обновлён!';
    EXCEPTION WHEN OTHERS THEN
        -- Откат транзакции в случае ошибки
        ROLLBACK;
        RAISE NOTICE 'Ошибка при обновлении email: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова процедуры
CALL update_user_email(1, 'new_email@example.com');
```

---

## **Вывод**
- **TCL** позволяет управлять транзакциями, обеспечивая **целостность данных**.
- **`BEGIN`**, **`COMMIT`**, **`ROLLBACK`** — основные команды для работы с транзакциями.
- **Точки сохранения (`SAVEPOINT`)** позволяют откатывать часть транзакции.
- **Уровни изоляции** определяют, как транзакции взаимодействуют друг с другом.
- **Функции и процедуры** позволяют инкапсулировать логику транзакций для повторного использования.