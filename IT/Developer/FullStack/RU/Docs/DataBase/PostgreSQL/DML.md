**DML (Data Manipulation Language)** — это набор команд для работы с данными в таблицах. Он включает в себя не только базовые операции (`INSERT`, `UPDATE`, `DELETE`, `SELECT`), но и более сложные конструкции, такие как работа с **массивами**, **временными таблицами**, **CTE (Common Table Expressions)**, **оконными функциями** и другими расширенными возможностями.

---

## **1. Основные команды DML**

### **1.1. `INSERT`**
**Описание:** Добавление новых строк в таблицу.

#### **Простой пример:**
```sql
INSERT INTO users (name, email, age)
VALUES ('Иван Иванов', 'ivan@example.com', 30);
```

#### **Множественная вставка:**
```sql
INSERT INTO users (name, email, age)
VALUES
    ('Петр Петров', 'petr@example.com', 25),
    ('Сидор Сидоров', 'sidor@example.com', 40);
```

#### **Вставка данных из другой таблицы:**
```sql
INSERT INTO users_backup (name, email, age)
SELECT name, email, age
FROM users
WHERE age > 30;
```

---

### **1.2. `UPDATE`**
**Описание:** Изменение существующих строк.

#### **Простой пример:**
```sql
UPDATE users
SET email = 'new_email@example.com'
WHERE id = 1;
```

#### **Обновление с использованием данных из другой таблицы:**
```sql
UPDATE users u
SET age = u.age + 1
FROM departments d
WHERE u.department_id = d.id AND d.name = 'IT';
```

---

### **1.3. `DELETE`**
**Описание:** Удаление строк из таблицы.

#### **Простой пример:**
```sql
DELETE FROM users
WHERE id = 1;
```

#### **Удаление с использованием подзапроса:**
```sql
DELETE FROM users
WHERE department_id IN (
    SELECT id
    FROM departments
    WHERE name = 'HR'
);
```

---

### **1.4. `SELECT`**
**Описание:** Выборка данных из таблиц.

#### **Простой пример:**
```sql
SELECT id, name, email
FROM users
WHERE age > 25;
```

#### **Выборка с сортировкой и ограничением:**
```sql
SELECT id, name, email
FROM users
ORDER BY age DESC
LIMIT 10;
```

---

## **2. Сложные запросы DML**

### **2.1. Использование `WITH` (CTE, Common Table Expressions)**
**Описание:** Позволяет создавать временные наборы данных внутри запроса.

#### **Пример с CTE:**
```sql
WITH active_users AS (
    SELECT id, name
    FROM users
    WHERE last_login > CURRENT_DATE - INTERVAL '30 days'
)
SELECT u.id, u.name, o.order_count
FROM active_users u
JOIN (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

---

### **2.2. Оконные функции**
**Описание:** Позволяют выполнять вычисления по группам строк, сохраняя при этом исходные данные.

#### **Пример с оконными функциями:**
```sql
SELECT
    id,
    name,
    age,
    RANK() OVER (ORDER BY age DESC) AS age_rank,
    AVG(age) OVER (PARTITION BY department_id) AS avg_department_age
FROM users;
```

---

### **2.3. Работа с массивами**
**Описание:** PostgreSQL поддерживает массивы, что позволяет хранить и обрабатывать списки значений в одной ячейке.

#### **Создание таблицы с массивом:**
```sql
CREATE TABLE user_tags (
    user_id INT,
    tags TEXT[]
);
```

#### **Вставка данных с массивом:**
```sql
INSERT INTO user_tags (user_id, tags)
VALUES
    (1, ARRAY['admin', 'moderator']),
    (2, ARRAY['user', 'guest']);
```

#### **Запрос с использованием массивов:**
```sql
-- Найти пользователей с тегом 'admin'
SELECT user_id
FROM user_tags
WHERE 'admin' = ANY(tags);

-- Найти пользователей, у которых есть все указанные теги
SELECT user_id
FROM user_tags
WHERE tags @> ARRAY['admin', 'moderator'];
```

---

### **2.4. Временные таблицы**
**Описание:** Временные таблицы существуют только в рамках сессии и полезны для промежуточных вычислений.

#### **Создание временной таблицы:**
```sql
CREATE TEMPORARY TABLE temp_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Вставка данных
INSERT INTO temp_users (name, email)
SELECT name, email
FROM users
WHERE age > 30;

-- Использование временной таблицы в запросе
SELECT * FROM temp_users;
```

---

### **2.5. Использование `JSON` и `JSONB`**
**Описание:** PostgreSQL поддерживает типы данных `JSON` и `JSONB` для работы с неструктурированными данными.

#### **Создание таблицы с JSON:**
```sql
CREATE TABLE user_profiles (
    user_id INT,
    profile JSONB
);
```

#### **Вставка данных в JSON:**
```sql
INSERT INTO user_profiles (user_id, profile)
VALUES (
    1,
    '{"name": "Иван", "preferences": {"theme": "dark", "notifications": true}}'
);
```

#### **Запрос с извлечением данных из JSON:**
```sql
-- Извлечение имени пользователя
SELECT
    user_id,
    profile->>'name' AS user_name,
    profile->'preferences'->>'theme' AS theme
FROM user_profiles;
```

---

### **2.6. Рекурсивные запросы с `WITH RECURSIVE`**
**Описание:** Позволяет выполнять рекурсивные запросы, например, для работы с иерархическими данными.

#### **Пример рекурсивного запроса:**
```sql
WITH RECURSIVE employee_hierarchy AS (
    -- Базовый запрос: начальные данные
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Рекурсивный запрос: присоединяем подчинённых
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy
ORDER BY level, name;
```

---

### **2.7. Использование `UNION`, `INTERSECT`, `EXCEPT`**
**Описание:** Комбинирование результатов нескольких запросов.

#### **Пример с `UNION`:**
```sql
-- Объединение результатов двух запросов
SELECT name FROM users
UNION
SELECT name FROM admins;
```

#### **Пример с `INTERSECT`:**
```sql
-- Найти общие имена в двух таблицах
SELECT name FROM users
INTERSECT
SELECT name FROM admins;
```

#### **Пример с `EXCEPT`:**
```sql
-- Найти имена, которые есть в users, но нет в admins
SELECT name FROM users
EXCEPT
SELECT name FROM admins;
```

---

### **2.8. Транзакции и блоки `BEGIN`/`COMMIT`/`ROLLBACK`**
**Описание:** Управление транзакциями для обеспечения целостности данных.

#### **Пример транзакции:**
```sql
BEGIN;

-- Вставляем заказ
INSERT INTO orders (user_id, product_id, quantity)
VALUES (1, 5, 2);

-- Обновляем запасы продукта
UPDATE products
SET stock = stock - 2
WHERE id = 5;

-- Проверяем, не ушли ли запасы в минус
IF (SELECT stock FROM products WHERE id = 5) < 0 THEN
    ROLLBACK;
    RAISE NOTICE 'Недостаточно товара на складе!';
ELSE
    COMMIT;
    RAISE NOTICE 'Заказ успешно оформлен!';
END IF;
```

---

### **2.9. Использование `RETURNING`**
**Описание:** Позволяет вернуть данные, изменённые в результате `INSERT`, `UPDATE` или `DELETE`.

#### **Пример с `RETURNING`:**
```sql
-- Вставка с возвратом идентификатора
INSERT INTO users (name, email)
VALUES ('Иван Иванов', 'ivan@example.com')
RETURNING id;

-- Обновление с возвратом изменённых данных
UPDATE users
SET email = 'new_email@example.com'
WHERE id = 1
RETURNING id, name, email;
```

---

## **3. Примеры сложных запросов**

### **3.1. Агрегация с фильтрацией (`HAVING`)**
```sql
-- Найти отделы, где средний возраст сотрудников больше 30
SELECT
    department_id,
    AVG(age) AS avg_age
FROM users
GROUP BY department_id
HAVING AVG(age) > 30;
```

---

### **3.2. Подзапросы в `FROM`**
```sql
-- Использование подзапроса как таблицы
SELECT subquery.user_id, subquery.order_count
FROM (
    SELECT
        user_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) AS subquery
WHERE subquery.order_count > 5;
```

---

### **3.3. Обновление с использованием `FROM`**
```sql
-- Обновление данных с использованием другой таблицы
UPDATE users u
SET age = u.age + 1
FROM departments d
WHERE u.department_id = d.id AND d.name = 'IT';
```

---

### **3.4. Использование `LATERAL` для коррелированных подзапросов**
```sql
-- Найти последнюю покупку каждого пользователя
SELECT
    u.id AS user_id,
    u.name,
    last_order.order_date,
    last_order.amount
FROM users u,
LATERAL (
    SELECT order_date, amount
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY order_date DESC
    LIMIT 1
) AS last_order;
```

---

### **3.5. Работа с `ARRAY_AGG` и `STRING_AGG`**
```sql
-- Агрегация массивов и строк
SELECT
    department_id,
    ARRAY_AGG(name) AS employee_names,
    STRING_AGG(name, ', ') AS employee_names_string
FROM users
GROUP BY department_id;
```

---

### **3.6. Использование `WITH` для сложных вычислений**
```sql
WITH user_stats AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spent
    FROM orders
    GROUP BY user_id
),
department_stats AS (
    SELECT
        d.id AS department_id,
        AVG(u.age) AS avg_age
    FROM departments d
    JOIN users u ON d.id = u.department_id
    GROUP BY d.id
)
SELECT
    u.id,
    u.name,
    u.department_id,
    us.order_count,
    us.total_spent,
    ds.avg_age AS department_avg_age
FROM users u
JOIN user_stats us ON u.id = us.user_id
JOIN department_stats ds ON u.department_id = ds.department_id;
```

---

## **Вывод**
PostgreSQL предоставляет мощные инструменты для работы с данными:
- **Базовые команды DML** (`INSERT`, `UPDATE`, `DELETE`, `SELECT`).
- **Сложные запросы** с использованием `CTE`, оконных функций, массивов, JSON.
- **Временные таблицы** для промежуточных вычислений.
- **Рекурсивные запросы** для работы с иерархическими данными.
- **Транзакции** для обеспечения целостности данных.

---
В **PostgreSQL** **DML (Data Manipulation Language)** — это набор команд для работы с данными в таблицах. Он включает в себя не только базовые операции (`INSERT`, `UPDATE`, `DELETE`, `SELECT`), но и более сложные конструкции, такие как работа с **массивами**, **временными таблицами**, **CTE (Common Table Expressions)**, **оконными функциями** и другими расширенными возможностями.

---

## **1. Основные команды DML**

### **1.1. `INSERT`**
**Описание:** Добавление новых строк в таблицу.

#### **Простой пример:**
```sql
INSERT INTO users (name, email, age)
VALUES ('Иван Иванов', 'ivan@example.com', 30);
```

#### **Множественная вставка:**
```sql
INSERT INTO users (name, email, age)
VALUES
    ('Петр Петров', 'petr@example.com', 25),
    ('Сидор Сидоров', 'sidor@example.com', 40);
```

#### **Вставка данных из другой таблицы:**
```sql
INSERT INTO users_backup (name, email, age)
SELECT name, email, age
FROM users
WHERE age > 30;
```

---

### **1.2. `UPDATE`**
**Описание:** Изменение существующих строк.

#### **Простой пример:**
```sql
UPDATE users
SET email = 'new_email@example.com'
WHERE id = 1;
```

#### **Обновление с использованием данных из другой таблицы:**
```sql
UPDATE users u
SET age = u.age + 1
FROM departments d
WHERE u.department_id = d.id AND d.name = 'IT';
```

---

### **1.3. `DELETE`**
**Описание:** Удаление строк из таблицы.

#### **Простой пример:**
```sql
DELETE FROM users
WHERE id = 1;
```

#### **Удаление с использованием подзапроса:**
```sql
DELETE FROM users
WHERE department_id IN (
    SELECT id
    FROM departments
    WHERE name = 'HR'
);
```

---

### **1.4. `SELECT`**
**Описание:** Выборка данных из таблиц.

#### **Простой пример:**
```sql
SELECT id, name, email
FROM users
WHERE age > 25;
```

#### **Выборка с сортировкой и ограничением:**
```sql
SELECT id, name, email
FROM users
ORDER BY age DESC
LIMIT 10;
```

---

## **2. Сложные запросы DML**

### **2.1. Использование `WITH` (CTE, Common Table Expressions)**
**Описание:** Позволяет создавать временные наборы данных внутри запроса.

#### **Пример с CTE:**
```sql
WITH active_users AS (
    SELECT id, name
    FROM users
    WHERE last_login > CURRENT_DATE - INTERVAL '30 days'
)
SELECT u.id, u.name, o.order_count
FROM active_users u
JOIN (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

---

### **2.2. Оконные функции**
**Описание:** Позволяют выполнять вычисления по группам строк, сохраняя при этом исходные данные.

#### **Пример с оконными функциями:**
```sql
SELECT
    id,
    name,
    age,
    RANK() OVER (ORDER BY age DESC) AS age_rank,
    AVG(age) OVER (PARTITION BY department_id) AS avg_department_age
FROM users;
```

---

### **2.3. Работа с массивами**
**Описание:** PostgreSQL поддерживает массивы, что позволяет хранить и обрабатывать списки значений в одной ячейке.

#### **Создание таблицы с массивом:**
```sql
CREATE TABLE user_tags (
    user_id INT,
    tags TEXT[]
);
```

#### **Вставка данных с массивом:**
```sql
INSERT INTO user_tags (user_id, tags)
VALUES
    (1, ARRAY['admin', 'moderator']),
    (2, ARRAY['user', 'guest']);
```

#### **Запрос с использованием массивов:**
```sql
-- Найти пользователей с тегом 'admin'
SELECT user_id
FROM user_tags
WHERE 'admin' = ANY(tags);

-- Найти пользователей, у которых есть все указанные теги
SELECT user_id
FROM user_tags
WHERE tags @> ARRAY['admin', 'moderator'];
```

---

### **2.4. Временные таблицы**
**Описание:** Временные таблицы существуют только в рамках сессии и полезны для промежуточных вычислений.

#### **Создание временной таблицы:**
```sql
CREATE TEMPORARY TABLE temp_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Вставка данных
INSERT INTO temp_users (name, email)
SELECT name, email
FROM users
WHERE age > 30;

-- Использование временной таблицы в запросе
SELECT * FROM temp_users;
```

---

### **2.5. Использование `JSON` и `JSONB`**
**Описание:** PostgreSQL поддерживает типы данных `JSON` и `JSONB` для работы с неструктурированными данными.

#### **Создание таблицы с JSON:**
```sql
CREATE TABLE user_profiles (
    user_id INT,
    profile JSONB
);
```

#### **Вставка данных в JSON:**
```sql
INSERT INTO user_profiles (user_id, profile)
VALUES (
    1,
    '{"name": "Иван", "preferences": {"theme": "dark", "notifications": true}}'
);
```

#### **Запрос с извлечением данных из JSON:**
```sql
-- Извлечение имени пользователя
SELECT
    user_id,
    profile->>'name' AS user_name,
    profile->'preferences'->>'theme' AS theme
FROM user_profiles;
```

---

### **2.6. Рекурсивные запросы с `WITH RECURSIVE`**
**Описание:** Позволяет выполнять рекурсивные запросы, например, для работы с иерархическими данными.

#### **Пример рекурсивного запроса:**
```sql
WITH RECURSIVE employee_hierarchy AS (
    -- Базовый запрос: начальные данные
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Рекурсивный запрос: присоединяем подчинённых
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy
ORDER BY level, name;
```

---

### **2.7. Использование `UNION`, `INTERSECT`, `EXCEPT`**
**Описание:** Комбинирование результатов нескольких запросов.

#### **Пример с `UNION`:**
```sql
-- Объединение результатов двух запросов
SELECT name FROM users
UNION
SELECT name FROM admins;
```

#### **Пример с `INTERSECT`:**
```sql
-- Найти общие имена в двух таблицах
SELECT name FROM users
INTERSECT
SELECT name FROM admins;
```

#### **Пример с `EXCEPT`:**
```sql
-- Найти имена, которые есть в users, но нет в admins
SELECT name FROM users
EXCEPT
SELECT name FROM admins;
```

---

### **2.8. Транзакции и блоки `BEGIN`/`COMMIT`/`ROLLBACK`**
**Описание:** Управление транзакциями для обеспечения целостности данных.

#### **Пример транзакции:**
```sql
BEGIN;

-- Вставляем заказ
INSERT INTO orders (user_id, product_id, quantity)
VALUES (1, 5, 2);

-- Обновляем запасы продукта
UPDATE products
SET stock = stock - 2
WHERE id = 5;

-- Проверяем, не ушли ли запасы в минус
IF (SELECT stock FROM products WHERE id = 5) < 0 THEN
    ROLLBACK;
    RAISE NOTICE 'Недостаточно товара на складе!';
ELSE
    COMMIT;
    RAISE NOTICE 'Заказ успешно оформлен!';
END IF;
```

---

### **2.9. Использование `RETURNING`**
**Описание:** Позволяет вернуть данные, изменённые в результате `INSERT`, `UPDATE` или `DELETE`.

#### **Пример с `RETURNING`:**
```sql
-- Вставка с возвратом идентификатора
INSERT INTO users (name, email)
VALUES ('Иван Иванов', 'ivan@example.com')
RETURNING id;

-- Обновление с возвратом изменённых данных
UPDATE users
SET email = 'new_email@example.com'
WHERE id = 1
RETURNING id, name, email;
```

---

## **3. Примеры сложных запросов**

### **3.1. Агрегация с фильтрацией (`HAVING`)**
```sql
-- Найти отделы, где средний возраст сотрудников больше 30
SELECT
    department_id,
    AVG(age) AS avg_age
FROM users
GROUP BY department_id
HAVING AVG(age) > 30;
```

---

### **3.2. Подзапросы в `FROM`**
```sql
-- Использование подзапроса как таблицы
SELECT subquery.user_id, subquery.order_count
FROM (
    SELECT
        user_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) AS subquery
WHERE subquery.order_count > 5;
```

---

### **3.3. Обновление с использованием `FROM`**
```sql
-- Обновление данных с использованием другой таблицы
UPDATE users u
SET age = u.age + 1
FROM departments d
WHERE u.department_id = d.id AND d.name = 'IT';
```

---

### **3.4. Использование `LATERAL` для коррелированных подзапросов**
```sql
-- Найти последнюю покупку каждого пользователя
SELECT
    u.id AS user_id,
    u.name,
    last_order.order_date,
    last_order.amount
FROM users u,
LATERAL (
    SELECT order_date, amount
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY order_date DESC
    LIMIT 1
) AS last_order;
```

---

### **3.5. Работа с `ARRAY_AGG` и `STRING_AGG`**
```sql
-- Агрегация массивов и строк
SELECT
    department_id,
    ARRAY_AGG(name) AS employee_names,
    STRING_AGG(name, ', ') AS employee_names_string
FROM users
GROUP BY department_id;
```

---

### **3.6. Использование `WITH` для сложных вычислений**
```sql
WITH user_stats AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_spent
    FROM orders
    GROUP BY user_id
),
department_stats AS (
    SELECT
        d.id AS department_id,
        AVG(u.age) AS avg_age
    FROM departments d
    JOIN users u ON d.id = u.department_id
    GROUP BY d.id
)
SELECT
    u.id,
    u.name,
    u.department_id,
    us.order_count,
    us.total_spent,
    ds.avg_age AS department_avg_age
FROM users u
JOIN user_stats us ON u.id = us.user_id
JOIN department_stats ds ON u.department_id = ds.department_id;
```

---

## **Вывод**
PostgreSQL предоставляет мощные инструменты для работы с данными:
- **Базовые команды DML** (`INSERT`, `UPDATE`, `DELETE`, `SELECT`).
- **Сложные запросы** с использованием `CTE`, оконных функций, массивов, JSON.
- **Временные таблицы** для промежуточных вычислений.
- **Рекурсивные запросы** для работы с иерархическими данными.
- **Транзакции** для обеспечения целостности данных.
---
В PostgreSQL можно выполнить **вставку данных с выводом записей, которые не были вставлены** из-за конфликтов или условий. Для этого используются конструкции с **`EXCLUDE`**, **`ON CONFLICT`**, **`RETURNING`** и **`EXCEPTION`**.

---

## **1. Использование `ON CONFLICT` с `RETURNING` для вывода невставленных записей**

### **1.1. Вставка с игнорированием дубликатов и выводом невставленных записей**

**Задача:** Вставить данные, игнорируя дубликаты по уникальному ключу, и вывести те записи, которые не были вставлены.

```sql
-- Создаём временную таблицу для хранения невставленных записей
CREATE TEMP TABLE failed_inserts AS
WITH input_data (id, name, email) AS (
    VALUES
        (1, 'Иван', 'ivan@example.com'),
        (2, 'Петр', 'petr@example.com'),
        (3, 'Сидор', 'sidor@example.com'),
        (1, 'Иван Дубль', 'ivan.duplicate@example.com') -- Дубликат по id
),
insert_attempt AS (
    INSERT INTO users (id, name, email)
    SELECT id, name, email FROM input_data
    ON CONFLICT (id) DO NOTHING
    RETURNING id, name, email
)
SELECT id, name, email
FROM input_data
WHERE id NOT IN (SELECT id FROM insert_attempt);

-- Вывод невставленных записей
SELECT * FROM failed_inserts;
```

---

### **1.2. Вставка с обновлением дубликатов и выводом невставленных записей**

**Задача:** Вставить данные, обновляя дубликаты, и вывести записи, которые не были вставлены из-за других конфликтов.

```sql
-- Создаём временную таблицу для невставленных записей
CREATE TEMP TABLE failed_inserts AS
WITH input_data (id, name, email) AS (
    VALUES
        (1, 'Иван', 'ivan@example.com'),
        (2, 'Петр', 'petr@example.com'),
        (3, 'Сидор', 'sidor@example.com'),
        (1, 'Иван Обновлённый', 'ivan.updated@example.com') -- Дубликат по id
),
insert_attempt AS (
    INSERT INTO users (id, name, email)
    SELECT id, name, email FROM input_data
    ON CONFLICT (id) DO UPDATE
        SET name = EXCLUDED.name,
            email = EXCLUDED.email
    RETURNING id
)
SELECT id, name, email
FROM input_data
WHERE id NOT IN (SELECT id FROM insert_attempt);

-- Вывод невставленных записей
SELECT * FROM failed_inserts;
```

---

## **2. Использование `EXCEPTION` для обработки ошибок и вывода невставленных записей**

### **2.1. Вставка с обработкой исключений и выводом невставленных записей**

**Задача:** Вставить данные и вывести те записи, которые вызвали ошибки.

```sql
DO $$
DECLARE
    rec RECORD;
    failed_records RECORD;
BEGIN
    -- Создаём временную таблицу для невставленных записей
    CREATE TEMP TABLE failed_inserts (id INT, name TEXT, email TEXT);

    FOR rec IN
        SELECT * FROM (
            VALUES
                (1, 'Иван', 'ivan@example.com'),
                (2, 'Петр', 'petr@example.com'),
                (3, 'Сидор', 'sidor@example.com'),
                (1, 'Иван Дубль', 'ivan.duplicate@example.com') -- Дубликат по id
        ) AS t(id, name, email)
    LOOP
        BEGIN
            INSERT INTO users (id, name, email)
            VALUES (rec.id, rec.name, rec.email);
        EXCEPTION WHEN unique_violation THEN
            -- Записываем невставленные данные во временную таблицу
            INSERT INTO failed_inserts (id, name, email)
            VALUES (rec.id, rec.name, rec.email);
        END;
    END LOOP;

    -- Вывод невставленных записей
    RAISE NOTICE 'Невставленные записи: %', (SELECT array_to_json(array_agg(row_to_json(failed_inserts))) FROM failed_inserts);
END $$;
```

---

## **3. Использование `NOT EXISTS` для проверки перед вставкой**

### **3.1. Вставка с предварительной проверкой и выводом невставленных записей**

**Задача:** Вставить данные только если они ещё не существуют, и вывести невставленные записи.

```sql
-- Создаём временную таблицу для невставленных записей
WITH input_data (id, name, email) AS (
    VALUES
        (1, 'Иван', 'ivan@example.com'),
        (2, 'Петр', 'petr@example.com'),
        (3, 'Сидор', 'sidor@example.com'),
        (1, 'Иван Дубль', 'ivan.duplicate@example.com') -- Дубликат по id
),
insert_attempt AS (
    INSERT INTO users (id, name, email)
    SELECT id, name, email
    FROM input_data
    WHERE NOT EXISTS (
        SELECT 1 FROM users WHERE users.id = input_data.id
    )
    RETURNING id
)
SELECT id, name, email
FROM input_data
WHERE id NOT IN (SELECT id FROM insert_attempt);
```

---

## **4. Использование функций для вставки и вывода невставленных записей**

### **4.1. Создание функции для вставки с выводом невставленных записей**

**Задача:** Создать функцию, которая вставляет данные и возвращает невставленные записи.

```sql
CREATE OR REPLACE FUNCTION insert_users_with_failed_output(
    user_data INT[],
    name_data TEXT[],
    email_data TEXT[]
) RETURNS TABLE (id INT, name TEXT, email TEXT) AS $$
DECLARE
    i INT;
BEGIN
    -- Создаём временную таблицу для невставленных записей
    CREATE TEMP TABLE failed_inserts (id INT, name TEXT, email TEXT);

    FOR i IN 1..array_length(user_data, 1) LOOP
        BEGIN
            INSERT INTO users (id, name, email)
            VALUES (user_data[i], name_data[i], email_data[i]);
        EXCEPTION WHEN unique_violation THEN
            -- Записываем невставленные данные во временную таблицу
            INSERT INTO failed_inserts (id, name, email)
            VALUES (user_data[i], name_data[i], email_data[i]);
        END;
    END LOOP;

    RETURN QUERY SELECT * FROM failed_inserts;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова функции
SELECT * FROM insert_users_with_failed_output(
    ARRAY[1, 2, 3, 1],
    ARRAY['Иван', 'Петр', 'Сидор', 'Иван Дубль'],
    ARRAY['ivan@example.com', 'petr@example.com', 'sidor@example.com', 'ivan.duplicate@example.com']
);
```

---

## **Вывод**
- **`ON CONFLICT`** позволяет управлять конфликтами при вставке и выводить невставленные записи.
- **`EXCEPTION`** в PL/pgSQL позволяет обрабатывать ошибки и сохранять невставленные данные.
- **`NOT EXISTS`** позволяет проверять данные перед вставкой и выводить невставленные записи.
- **Функции** в PostgreSQL позволяют инкапсулировать логику вставки и вывода невставленных записей.
---
Вот примеры для **`UPDATE`** и **`DELETE`** с выводом записей, которые не были изменены или удалены, с использованием различных подходов в PostgreSQL.

---

## **UPDATE с выводом не обновлённых записей**

### **1. Обновление с выводом записей, которые не были изменены из-за условий**

**Задача:** Обновить записи, но вывести те, которые не были изменены, так как не соответствовали условию.

```sql
-- Создаём временную таблицу для хранения не обновлённых записей
WITH input_data (id, new_email) AS (
    VALUES
        (1, 'new_ivan@example.com'),
        (2, 'new_petr@example.com'),
        (3, 'new_sidor@example.com'),
        (4, 'new_user@example.com') -- Пользователя с id=4 нет в таблице
),
update_attempt AS (
    UPDATE users
    SET email = input_data.new_email
    FROM input_data
    WHERE users.id = input_data.id
    RETURNING users.id
)
SELECT input_data.id, input_data.new_email
FROM input_data
WHERE input_data.id NOT IN (SELECT id FROM update_attempt);
```

---

### **2. Обновление с проверкой на изменение данных и выводом не обновлённых записей**

**Задача:** Обновить записи, но вывести те, которые не были изменены, так как новые значения совпадают со старыми.

```sql
-- Создаём временную таблицу для не обновлённых записей
CREATE TEMP TABLE failed_updates AS
WITH input_data (id, new_email) AS (
    VALUES
        (1, 'ivan@example.com'), -- Текущее значение совпадает с новым
        (2, 'new_petr@example.com'),
        (3, 'new_sidor@example.com')
),
update_attempt AS (
    UPDATE users
    SET email = input_data.new_email
    FROM input_data
    WHERE users.id = input_data.id
    AND users.email <> input_data.new_email -- Проверяем, что значение изменилось
    RETURNING users.id
)
SELECT input_data.id, input_data.new_email
FROM input_data
WHERE input_data.id NOT IN (SELECT id FROM update_attempt);

-- Вывод не обновлённых записей
SELECT * FROM failed_updates;
```

---

### **3. Использование `EXCEPTION` для обработки ошибок и вывода не обновлённых записей**

**Задача:** Обновить записи и вывести те, которые вызвали ошибки.

```sql
DO $$
DECLARE
    rec RECORD;
BEGIN
    -- Создаём временную таблицу для не обновлённых записей
    CREATE TEMP TABLE failed_updates (id INT, new_email TEXT);

    FOR rec IN
        SELECT * FROM (
            VALUES
                (1, 'new_ivan@example.com'),
                (2, 'new_petr@example.com'),
                (3, 'new_sidor@example.com'),
                (999, 'new_nonexistent@example.com') -- Пользователя с id=999 нет
        ) AS t(id, new_email)
    LOOP
        BEGIN
            UPDATE users
            SET email = rec.new_email
            WHERE id = rec.id;

            -- Проверяем, было ли обновление
            IF NOT FOUND THEN
                INSERT INTO failed_updates (id, new_email)
                VALUES (rec.id, rec.new_email);
            END IF;
        EXCEPTION WHEN OTHERS THEN
            -- Записываем не обновлённые данные во временную таблицу
            INSERT INTO failed_updates (id, new_email)
            VALUES (rec.id, rec.new_email);
        END;
    END LOOP;

    -- Вывод не обновлённых записей
    RAISE NOTICE 'Не обновлённые записи: %', (SELECT array_to_json(array_agg(row_to_json(failed_updates))) FROM failed_updates);
END $$;
```

---

## **DELETE с выводом не удалённых записей**

### **1. Удаление с выводом записей, которые не были удалены из-за условий**

**Задача:** Удалить записи, но вывести те, которые не были удалены, так как не соответствовали условию.

```sql
-- Создаём временную таблицу для хранения не удалённых записей
WITH input_data (id) AS (
    VALUES
        (1),
        (2),
        (3),
        (4) -- Пользователя с id=4 нет в таблице
),
delete_attempt AS (
    DELETE FROM users
    WHERE id IN (SELECT id FROM input_data)
    RETURNING id
)
SELECT input_data.id
FROM input_data
WHERE input_data.id NOT IN (SELECT id FROM delete_attempt);
```

---

### **2. Удаление с проверкой на наличие зависимых записей и выводом не удалённых записей**

**Задача:** Удалить записи, но вывести те, которые не были удалены из-за наличия зависимых записей.

```sql
-- Создаём временную таблицу для не удалённых записей
CREATE TEMP TABLE failed_deletes AS
WITH input_data (id) AS (
    VALUES
        (1),
        (2),
        (3)
),
delete_attempt AS (
    DELETE FROM users u
    WHERE u.id IN (SELECT id FROM input_data)
    AND NOT EXISTS (
        SELECT 1 FROM orders o
        WHERE o.user_id = u.id
    )
    RETURNING u.id
)
SELECT input_data.id
FROM input_data
WHERE input_data.id NOT IN (SELECT id FROM delete_attempt);

-- Вывод не удалённых записей
SELECT * FROM failed_deletes;
```

---

### **3. Использование `EXCEPTION` для обработки ошибок и вывода не удалённых записей**

**Задача:** Удалить записи и вывести те, которые вызвали ошибки.

```sql
DO $$
DECLARE
    rec RECORD;
BEGIN
    -- Создаём временную таблицу для не удалённых записей
    CREATE TEMP TABLE failed_deletes (id INT);

    FOR rec IN
        SELECT * FROM (
            VALUES
                (1),
                (2),
                (3),
                (999) -- Пользователя с id=999 нет
        ) AS t(id)
    LOOP
        BEGIN
            DELETE FROM users
            WHERE id = rec.id;

            -- Проверяем, было ли удаление
            IF NOT FOUND THEN
                INSERT INTO failed_deletes (id)
                VALUES (rec.id);
            END IF;
        EXCEPTION WHEN OTHERS THEN
            -- Записываем не удалённые данные во временную таблицу
            INSERT INTO failed_deletes (id)
            VALUES (rec.id);
        END;
    END LOOP;

    -- Вывод не удалённых записей
    RAISE NOTICE 'Не удалённые записи: %', (SELECT array_to_json(array_agg(id)) FROM failed_deletes);
END $$;
```

---

### **4. Удаление с использованием функции для вывода не удалённых записей**

**Задача:** Создать функцию, которая удаляет данные и возвращает не удалённые записи.

```sql
CREATE OR REPLACE FUNCTION delete_users_with_failed_output(
    user_ids INT[]
) RETURNS TABLE (id INT) AS $$
DECLARE
    i INT;
BEGIN
    -- Создаём временную таблицу для не удалённых записей
    CREATE TEMP TABLE failed_deletes (id INT);

    FOR i IN 1..array_length(user_ids, 1) LOOP
        BEGIN
            DELETE FROM users
            WHERE id = user_ids[i];

            -- Проверяем, было ли удаление
            IF NOT FOUND THEN
                INSERT INTO failed_deletes (id)
                VALUES (user_ids[i]);
            END IF;
        EXCEPTION WHEN OTHERS THEN
            -- Записываем не удалённые данные во временную таблицу
            INSERT INTO failed_deletes (id)
            VALUES (user_ids[i]);
        END;
    END LOOP;

    RETURN QUERY SELECT * FROM failed_deletes;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова функции
SELECT * FROM delete_users_with_failed_output(ARRAY[1, 2, 3, 999]);
```

---

## **Вывод**
- Для **`UPDATE`** и **`DELETE`** можно использовать **`RETURNING`** и **`NOT IN`** для вывода не изменённых записей.
- **`EXCEPTION`** в PL/pgSQL позволяет обрабатывать ошибки и сохранять не изменённые данные.
- **Функции** в PostgreSQL позволяют инкапсулировать логику обновления и удаления с выводом не изменённых записей.