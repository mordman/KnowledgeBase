В **PostgreSQL** обработка ошибок реализована с помощью механизмов **исключений** (exceptions) и **блоков обработки ошибок** в процедурном языке **PL/pgSQL**. Это позволяет контролировать выполнение кода, перехватывать ошибки и выполнять корректные действия (например, откат транзакций, логирование, повторные попытки).

---

## **1. Основные механизмы обработки ошибок**

### **1.1. Блок `BEGIN ... EXCEPTION ... END`**
В **PL/pgSQL** можно использовать блоки `BEGIN ... EXCEPTION` для перехвата и обработки ошибок.

#### **Синтаксис:**
```sql
BEGIN
    -- Код, который может вызвать ошибку
    ...
EXCEPTION
    WHEN <условие ошибки> THEN
        -- Обработка ошибки
    WHEN OTHERS THEN
        -- Обработка всех остальных ошибок
END;
```

---

### **1.2. Типы ошибок**
PostgreSQL поддерживает множество типов ошибок, которые можно перехватывать. Некоторые из них:

| Тип ошибки                     | Описание                                                                                     |
|--------------------------------|---------------------------------------------------------------------------------------------|
| `SQLSTATE '23505'`             | Нарушение уникальности (`unique_violation`).                                               |
| `SQLSTATE '23503'`             | Нарушение ограничения внешнего ключа (`foreign_key_violation`).                            |
| `SQLSTATE '23502'`             | Нарушение ограничения `NOT NULL`.                                                           |
| `SQLSTATE '42P01'`             | Несуществующая таблица (`undefined_table`).                                                |
| `SQLSTATE '42703'`             | Несуществующая колонка (`undefined_column`).                                               |
| `SQLSTATE '22003'`             | Числовое значение вне диапазона (`numeric_value_out_of_range`).                            |
| `SQLSTATE '22012'`             | Ошибка деления на ноль (`division_by_zero`).                                                |
| `SQLSTATE '40001'`             | Взаимоблокировка (`serialization_failure`).                                                |
| `SQLSTATE '40P01'`             | Взаимоблокировка (`deadlock_detected`).                                                     |
| `SQLSTATE 'P0001'`             | Пользовательская ошибка (`raise_exception`).                                               |

---

## **2. Примеры обработки ошибок**

### **2.1. Простая обработка ошибок в блоке `DO`**

```sql
DO $$
BEGIN
    -- Пытаемся вставить дубликат
    INSERT INTO users (id, name, email)
    VALUES (1, 'Иван Иванов', 'ivan@example.com');

EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'Пользователь с таким id уже существует!';
END $$;
```

---

### **2.2. Обработка ошибок в функции**

```sql
CREATE OR REPLACE FUNCTION safe_insert_user(
    user_id INT,
    user_name TEXT,
    user_email TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    -- Пытаемся вставить пользователя
    INSERT INTO users (id, name, email)
    VALUES (user_id, user_name, user_email);

    RETURN TRUE;

EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'Пользователь с id=% уже существует!', user_id;
    RETURN FALSE;

WHEN OTHERS THEN
    RAISE NOTICE 'Ошибка при вставке пользователя: %', SQLERRM;
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова функции
SELECT safe_insert_user(1, 'Иван Иванов', 'ivan@example.com');
```

---

### **2.3. Обработка ошибок в транзакции**

```sql
DO $$
BEGIN
    -- Начало транзакции
    BEGIN
        -- Пытаемся обновить несуществующего пользователя
        UPDATE users
        SET email = 'new_email@example.com'
        WHERE id = 999;

        -- Если запись не найдена, выбрасывается исключение
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Пользователь с id=999 не найден!';
        END IF;

        -- Фиксируем транзакцию
        COMMIT;
        RAISE NOTICE 'Email пользователя успешно обновлён!';

    EXCEPTION WHEN OTHERS THEN
        -- Откат транзакции в случае ошибки
        ROLLBACK;
        RAISE NOTICE 'Ошибка при обновлении email: %', SQLERRM;
    END;
END $$;
```

---

### **2.4. Обработка ошибок с использованием `SQLSTATE`**

```sql
DO $$
BEGIN
    -- Пытаемся удалить пользователя с зависимыми записями
    DELETE FROM users
    WHERE id = 1;

EXCEPTION WHEN SQLSTATE '23503' THEN -- foreign_key_violation
    RAISE NOTICE 'Нельзя удалить пользователя: у него есть зависимые записи!';

WHEN OTHERS THEN
    RAISE NOTICE 'Ошибка при удалении пользователя: %', SQLERRM;
END $$;
```

---

### **2.5. Обработка ошибок в процедуре**

```sql
CREATE OR REPLACE PROCEDURE safe_delete_user(user_id INT)
AS $$
BEGIN
    -- Пытаемся удалить пользователя
    DELETE FROM users
    WHERE id = user_id;

    -- Проверяем, было ли удаление
    IF NOT FOUND THEN
        RAISE NOTICE 'Пользователь с id=% не найден!', user_id;
    ELSE
        RAISE NOTICE 'Пользователь с id=% успешно удалён!', user_id;
    END IF;

EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'Нельзя удалить пользователя с id=%: у него есть зависимые записи!', user_id;

WHEN OTHERS THEN
    RAISE NOTICE 'Ошибка при удалении пользователя с id=%: %', user_id, SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова процедуры
CALL safe_delete_user(1);
```

---

## **3. Использование `RAISE` для генерации ошибок**

В **PL/pgSQL** можно явно выбрасывать ошибки с помощью команды `RAISE`.

### **3.1. Генерация пользовательских ошибок**

```sql
DO $$
DECLARE
    user_balance DECIMAL;
BEGIN
    -- Получаем баланс пользователя
    SELECT balance INTO user_balance
    FROM accounts
    WHERE user_id = 1;

    -- Проверяем баланс
    IF user_balance < 0 THEN
        RAISE EXCEPTION 'Недостаточно средств на счёте! Текущий баланс: %', user_balance;
    END IF;

    RAISE NOTICE 'Баланс пользователя: %', user_balance;
END $$;
```

---

### **3.2. Генерация ошибок с указанием `SQLSTATE`**

```sql
DO $$
BEGIN
    -- Проверяем условие
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = 1) THEN
        RAISE EXCEPTION SQLSTATE 'P0001', 'Пользователь с id=1 не найден!';
    END IF;
END $$;
```

---

## **4. Логирование ошибок**

Для логирования ошибок в PostgreSQL можно использовать:
- **`RAISE NOTICE`** — для вывода сообщений в клиент.
- **Таблицы логов** — для сохранения информации об ошибках в базе данных.

---

### **4.1. Логирование ошибок в таблицу**

```sql
-- Создаём таблицу для логов
CREATE TABLE error_logs (
    id SERIAL PRIMARY KEY,
    error_time TIMESTAMP DEFAULT NOW(),
    error_message TEXT,
    error_detail TEXT,
    error_hint TEXT,
    error_context TEXT
);

-- Пример функции с логированием ошибок
CREATE OR REPLACE FUNCTION safe_divide(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    result NUMERIC;
BEGIN
    BEGIN
        result := a / b;
        RETURN result;

    EXCEPTION WHEN division_by_zero THEN
        -- Логируем ошибку
        INSERT INTO error_logs (error_message, error_detail)
        VALUES ('Деление на ноль', 'Попытка разделить ' || a || ' на 0');

        RAISE NOTICE 'Деление на ноль! Ошибка записана в лог.';
        RETURN NULL;

    WHEN OTHERS THEN
        -- Логируем ошибку
        INSERT INTO error_logs (error_message, error_detail)
        VALUES ('Ошибка при делении', SQLERRM);

        RAISE NOTICE 'Ошибка при делении: %', SQLERRM;
        RETURN NULL;
    END;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова функции
SELECT safe_divide(10, 0);
```

---

## **5. Повторное выполнение операций при ошибках**

### **5.1. Повторное выполнение операции с ограничением по количеству попыток**

```sql
CREATE OR REPLACE FUNCTION retry_insert_user(
    user_id INT,
    user_name TEXT,
    user_email TEXT,
    max_retries INT DEFAULT 3
) RETURNS BOOLEAN AS $$
DECLARE
    retry_count INT := 0;
BEGIN
    WHILE retry_count < max_retries LOOP
        BEGIN
            -- Пытаемся вставить пользователя
            INSERT INTO users (id, name, email)
            VALUES (user_id, user_name, user_email);

            RETURN TRUE;

        EXCEPTION WHEN unique_violation THEN
            retry_count := retry_count + 1;
            RAISE NOTICE 'Попытка %: Пользователь с id=% уже существует!', retry_count, user_id;
            -- Задержка перед повторной попыткой
            PERFORM pg_sleep(1);
        END;
    END LOOP;

    RAISE NOTICE 'Не удалось вставить пользователя после % попыток!', max_retries;
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова функции
SELECT retry_insert_user(1, 'Иван Иванов', 'ivan@example.com', 3);
```

---

## **6. Обработка ошибок в триггерах**

### **6.1. Пример триггера с обработкой ошибок**

```sql
CREATE OR REPLACE FUNCTION check_user_age()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем возраст пользователя
    IF NEW.age < 18 THEN
        RAISE EXCEPTION 'Пользователь должен быть старше 18 лет!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаём триггер
CREATE TRIGGER user_age_check
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION check_user_age();

-- Пример вставки, которая вызовет ошибку
INSERT INTO users (id, name, email, age)
VALUES (1, 'Иван Иванов', 'ivan@example.com', 16);
```

---

## **7. Обработка ошибок в анонимных блоках**

### **7.1. Пример анонимного блока с обработкой ошибок**

```sql
DO $$
DECLARE
    user_record RECORD;
BEGIN
    -- Пытаемся получить пользователя
    SELECT * INTO user_record
    FROM users
    WHERE id = 1;

    -- Если пользователь не найден
    IF NOT FOUND THEN
        RAISE NOTICE 'Пользователь с id=1 не найден!';
    ELSE
        RAISE NOTICE 'Пользователь найден: %', user_record.name;
    END IF;

EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Ошибка при получении пользователя: %', SQLERRM;
END $$;
```

---

## **8. Обработка ошибок в курсорах**

### **8.1. Пример использования курсора с обработкой ошибок**

```sql
DO $$
DECLARE
    user_record RECORD;
    user_cursor CURSOR FOR
        SELECT id, name, email FROM users;
BEGIN
    OPEN user_cursor;

    LOOP
        BEGIN
            FETCH user_cursor INTO user_record;
            EXIT WHEN NOT FOUND;

            -- Обработка каждой записи
            RAISE NOTICE 'Обработка пользователя: %', user_record.name;

            -- Пример операции, которая может вызвать ошибку
            UPDATE accounts
            SET balance = balance + 100
            WHERE user_id = user_record.id;

        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'Ошибка при обработке пользователя %: %', user_record.id, SQLERRM;
        END;
    END LOOP;

    CLOSE user_cursor;
END $$;
```

---

## **Вывод**
- **PostgreSQL** предоставляет мощные механизмы обработки ошибок с помощью **исключений** и **блоков `BEGIN ... EXCEPTION`**.
- **`RAISE`** позволяет генерировать пользовательские ошибки.
- **Логирование ошибок** можно реализовать с помощью **таблиц логов** или **`RAISE NOTICE`**.
- **Транзакции** и **точки сохранения** (`SAVEPOINT`) позволяют управлять откатом изменений при ошибках.
- **Функции, процедуры, триггеры и анонимные блоки** поддерживают обработку ошибок для различных сценариев.

---

## **Пример вложенной обработки ошибок**

### **Сценарий:**
1. Начало транзакции.
2. Вставка пользователя.
3. Обновление счёта пользователя.
4. Если ошибка при обновлении счёта, откат к точке сохранения.
5. Если ошибка на любом этапе, полный откат транзакции.

---

### **1. Вложенная обработка ошибок в анонимном блоке**

```sql
DO $$
DECLARE
    user_balance DECIMAL;
BEGIN
    -- Начало транзакции
    BEGIN
        -- Вставляем пользователя
        INSERT INTO users (id, name, email)
        VALUES (1, 'Иван Иванов', 'ivan@example.com');

        -- Создаём точку сохранения
        SAVEPOINT after_user_insert;

        -- Вложенный блок для обновления счёта
        BEGIN
            -- Получаем текущий баланс
            SELECT balance INTO user_balance
            FROM accounts
            WHERE user_id = 1;

            -- Проверяем баланс
            IF user_balance < 100 THEN
                RAISE EXCEPTION 'Недостаточно средств на счёте!';
            END IF;

            -- Обновляем баланс
            UPDATE accounts
            SET balance = balance - 100
            WHERE user_id = 1;

            -- Логируем успешное обновление
            RAISE NOTICE 'Баланс успешно обновлён!';

        EXCEPTION WHEN OTHERS THEN
            -- Откат к точке сохранения при ошибке обновления счёта
            ROLLBACK TO SAVEPOINT after_user_insert;
            RAISE NOTICE 'Ошибка при обновлении счёта: %', SQLERRM;

            -- Продолжаем выполнение без обновления счёта
        END;

        -- Фиксируем транзакцию
        COMMIT;
        RAISE NOTICE 'Транзакция успешно завершена!';

    EXCEPTION WHEN OTHERS THEN
        -- Полный откат транзакции при любой другой ошибке
        ROLLBACK;
        RAISE NOTICE 'Ошибка в транзакции: %', SQLERRM;
    END;
END $$;
```

---

### **2. Вложенная обработка ошибок в функции**

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
        -- Вложенный блок для проверки отправителя
        BEGIN
            -- Получаем баланс отправителя
            SELECT balance INTO sender_balance
            FROM accounts
            WHERE user_id = sender_id;

            -- Проверяем баланс
            IF sender_balance < amount THEN
                RAISE EXCEPTION 'Недостаточно средств на счёте отправителя!';
            END IF;

        EXCEPTION WHEN NO_DATA_FOUND THEN
            RAISE EXCEPTION 'Отправитель с id=% не найден!', sender_id;
        END;

        -- Вложенный блок для проверки получателя
        BEGIN
            -- Получаем баланс получателя
            SELECT balance INTO receiver_balance
            FROM accounts
            WHERE user_id = receiver_id;

        EXCEPTION WHEN NO_DATA_FOUND THEN
            RAISE EXCEPTION 'Получатель с id=% не найден!', receiver_id;
        END;

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
        -- Откат транзакции при любой ошибке
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

### **3. Вложенная обработка ошибок в процедуре**

```sql
CREATE OR REPLACE PROCEDURE update_user_profile(
    user_id INT,
    new_email TEXT,
    new_age INT
) AS $$
BEGIN
    -- Начало транзакции
    BEGIN
        -- Вложенный блок для обновления email
        BEGIN
            UPDATE users
            SET email = new_email
            WHERE id = user_id;

            -- Проверяем, было ли обновление
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Пользователь с id=% не найден!', user_id;
            END IF;

        EXCEPTION WHEN unique_violation THEN
            RAISE NOTICE 'Email % уже используется!', new_email;
        END;

        -- Вложенный блок для обновления возраста
        BEGIN
            -- Проверяем возраст
            IF new_age < 18 THEN
                RAISE EXCEPTION 'Возраст должен быть не менее 18 лет!';
            END IF;

            -- Обновляем возраст
            UPDATE users
            SET age = new_age
            WHERE id = user_id;

        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'Ошибка при обновлении возраста: %', SQLERRM;
        END;

        -- Фиксируем транзакцию
        COMMIT;
        RAISE NOTICE 'Профиль пользователя успешно обновлён!';

    EXCEPTION WHEN OTHERS THEN
        -- Откат транзакции при любой ошибке
        ROLLBACK;
        RAISE NOTICE 'Ошибка при обновлении профиля: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова процедуры
CALL update_user_profile(1, 'new_email@example.com', 25);
```

---

### **4. Вложенная обработка ошибок в триггере**

```sql
CREATE OR REPLACE FUNCTION validate_user_age()
RETURNS TRIGGER AS $$
BEGIN
    -- Вложенный блок для проверки возраста
    BEGIN
        -- Проверяем возраст
        IF NEW.age < 18 THEN
            RAISE EXCEPTION 'Возраст пользователя должен быть не менее 18 лет!';
        END IF;

    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Ошибка при проверке возраста: %', SQLERRM;
        RETURN NULL; -- Отменяем операцию
    END;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаём триггер
CREATE TRIGGER user_age_validation
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION validate_user_age();

-- Пример вставки, которая вызовет ошибку
INSERT INTO users (id, name, email, age)
VALUES (1, 'Иван Иванов', 'ivan@example.com', 16);
```

---

## **Вывод**
- **Вложенные блоки `BEGIN ... EXCEPTION`** позволяют гибко управлять ошибками на разных уровнях логики.
- **Точки сохранения (`SAVEPOINT`)** помогают откатывать только часть транзакции.
- **Функции, процедуры и триггеры** поддерживают вложенную обработку ошибок.
- **Логирование ошибок** с помощью `RAISE NOTICE` или таблиц логов позволяет отслеживать проблемы.