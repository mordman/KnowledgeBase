# **DDL (Data Definition Language)**

**DDL (Data Definition Language)** — это набор команд для **определения и управления структурой базы данных**. В PostgreSQL DDL используется для создания, изменения и удаления объектов базы данных, таких как таблицы, индексы, представления, функции, триггеры и другие.

---

## **1. Основные команды DDL**

### **1.1. Создание объектов (`CREATE`)**
Команда `CREATE` используется для создания новых объектов в базе данных.

---

#### **1.1.1. Создание базы данных**
```sql
CREATE DATABASE database_name
[WITH
    OWNER = user_name
    ENCODING = 'encoding'
    LC_COLLATE = 'locale'
    LC_CTYPE = 'locale'
    TABLESPACE = tablespace_name
    CONNECTION LIMIT = max_concurrent_connection];
```

**Пример:**
```sql
CREATE DATABASE my_database
WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = 100;
```

---

#### **1.1.2. Создание схемы**
Схемы используются для организации объектов базы данных.

```sql
CREATE SCHEMA schema_name [AUTHORIZATION user_name];
```

**Пример:**
```sql
CREATE SCHEMA hr AUTHORIZATION postgres;
```

---

#### **1.1.3. Создание таблицы**
```sql
CREATE TABLE table_name (
    column1 data_type [constraints],
    column2 data_type [constraints],
    ...
    [table_constraints]
);
```

**Пример:**
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2) CHECK (salary > 0),
    department_id INTEGER REFERENCES departments(department_id)
);
```

---

#### **1.1.4. Создание индекса**
```sql
CREATE [UNIQUE] INDEX index_name
ON table_name (column1, column2, ...)
[USING method]
[TABLESPACE tablespace_name];
```

**Пример:**
```sql
CREATE INDEX idx_employees_last_name ON employees(last_name);
CREATE UNIQUE INDEX idx_employees_email ON employees(email);
```

---

#### **1.1.5. Создание представления (View)**
```sql
CREATE [OR REPLACE] VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
[WHERE condition];
```

**Пример:**
```sql
CREATE VIEW high_salary_employees AS
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 100000;
```

---

#### **1.1.6. Создание последовательности (Sequence)**
```sql
CREATE SEQUENCE sequence_name
[INCREMENT BY increment]
[MINVALUE minvalue | NO MINVALUE]
[MAXVALUE maxvalue | NO MAXVALUE]
[START WITH start]
[CACHE cache]
[CYCLE | NO CYCLE];
```

**Пример:**
```sql
CREATE SEQUENCE employee_id_seq
INCREMENT BY 1
MINVALUE 1
START WITH 1
CACHE 20;
```

---

#### **1.1.7. Создание функции**
```sql
CREATE [OR REPLACE] FUNCTION function_name (parameter1 type1, parameter2 type2, ...)
RETURNS return_type AS $$
DECLARE
    -- переменные
BEGIN
    -- тело функции
END;
$$ LANGUAGE plpgsql;
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION calculate_bonus(salary DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    RETURN salary * 0.1;
END;
$$ LANGUAGE plpgsql;
```

---

#### **1.1.8. Создание триггера**
```sql
CREATE TRIGGER trigger_name
[BEFORE | AFTER | INSTEAD OF] [INSERT | UPDATE | DELETE | TRUNCATE]
ON table_name
[FOR EACH ROW | FOR EACH STATEMENT]
EXECUTE FUNCTION trigger_function();
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION log_employee_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employee_audit (employee_id, old_salary, new_salary, change_date)
    VALUES (OLD.employee_id, OLD.salary, NEW.salary, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_employee_update
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION log_employee_change();
```

---

### **1.2. Изменение объектов (`ALTER`)**
Команда `ALTER` используется для изменения существующих объектов.

---

#### **1.2.1. Изменение таблицы**
```sql
ALTER TABLE table_name
[ADD COLUMN column_name data_type [constraints]]
[DROP COLUMN column_name]
[ALTER COLUMN column_name [SET DATA TYPE data_type] [SET DEFAULT value] [DROP DEFAULT]]
[RENAME COLUMN old_column_name TO new_column_name]
[RENAME TO new_table_name]
[ADD CONSTRAINT constraint_name constraint_definition]
[DROP CONSTRAINT constraint_name];
```

**Примеры:**
```sql
-- Добавление нового столбца
ALTER TABLE employees ADD COLUMN phone_number VARCHAR(20);

-- Удаление столбца
ALTER TABLE employees DROP COLUMN phone_number;

-- Изменение типа данных столбца
ALTER TABLE employees ALTER COLUMN salary TYPE NUMERIC(12, 2);

-- Переименование столбца
ALTER TABLE employees RENAME COLUMN first_name TO given_name;

-- Переименование таблицы
ALTER TABLE employees RENAME TO staff;

-- Добавление ограничения
ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary > 0);

-- Удаление ограничения
ALTER TABLE employees DROP CONSTRAINT chk_salary;
```

---

#### **1.2.2. Изменение индекса**
```sql
ALTER INDEX index_name RENAME TO new_index_name;
```

**Пример:**
```sql
ALTER INDEX idx_employees_last_name RENAME TO idx_staff_last_name;
```

---

#### **1.2.3. Изменение представления**
```sql
CREATE OR REPLACE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
[WHERE condition];
```

---

#### **1.2.4. Изменение последовательности**
```sql
ALTER SEQUENCE sequence_name
[INCREMENT BY increment]
[MINVALUE minvalue | NO MINVALUE]
[MAXVALUE maxvalue | NO MAXVALUE]
[START WITH start]
[RESTART [WITH start]]
[CACHE cache | NO CACHE]
[CYCLE | NO CYCLE];
```

**Пример:**
```sql
ALTER SEQUENCE employee_id_seq INCREMENT BY 2;
```

---

### **1.3. Удаление объектов (`DROP`)**
Команда `DROP` используется для удаления объектов из базы данных.

---

#### **1.3.1. Удаление базы данных**
```sql
DROP DATABASE [IF EXISTS] database_name;
```

**Пример:**
```sql
DROP DATABASE IF EXISTS my_database;
```

---

#### **1.3.2. Удаление схемы**
```sql
DROP SCHEMA [IF EXISTS] schema_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP SCHEMA IF EXISTS hr CASCADE;
```

---

#### **1.3.3. Удаление таблицы**
```sql
DROP TABLE [IF EXISTS] table_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP TABLE IF EXISTS employees CASCADE;
```

---

#### **1.3.4. Удаление индекса**
```sql
DROP INDEX [IF EXISTS] index_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP INDEX IF EXISTS idx_employees_last_name;
```

---

#### **1.3.5. Удаление представления**
```sql
DROP VIEW [IF EXISTS] view_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP VIEW IF EXISTS high_salary_employees;
```

---

#### **1.3.6. Удаление последовательности**
```sql
DROP SEQUENCE [IF EXISTS] sequence_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP SEQUENCE IF EXISTS employee_id_seq;
```

---

#### **1.3.7. Удаление функции**
```sql
DROP FUNCTION [IF EXISTS] function_name (parameter1 type1, parameter2 type2, ...) [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP FUNCTION IF EXISTS calculate_bonus(DECIMAL);
```

---

#### **1.3.8. Удаление триггера**
```sql
DROP TRIGGER [IF EXISTS] trigger_name ON table_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP TRIGGER IF EXISTS trg_employee_update ON employees;
```

---

### **1.4. Переименование объектов (`RENAME`)**
Команда `RENAME` используется для переименования объектов.

---

#### **1.4.1. Переименование таблицы**
```sql
ALTER TABLE table_name RENAME TO new_table_name;
```

**Пример:**
```sql
ALTER TABLE employees RENAME TO staff;
```

---

#### **1.4.2. Переименование столбца**
```sql
ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name;
```

**Пример:**
```sql
ALTER TABLE staff RENAME COLUMN first_name TO given_name;
```

---

#### **1.4.3. Переименование индекса**
```sql
ALTER INDEX index_name RENAME TO new_index_name;
```

**Пример:**
```sql
ALTER INDEX idx_employees_last_name RENAME TO idx_staff_last_name;
```

---

### **1.5. Удаление данных (`TRUNCATE`)**
Команда `TRUNCATE` используется для быстрого удаления всех данных из таблицы.

```sql
TRUNCATE [TABLE] table_name [RESTART IDENTITY | CONTINUE IDENTITY] [CASCADE | RESTRICT];
```

**Пример:**
```sql
TRUNCATE TABLE employees RESTART IDENTITY;
```

---

## **2. Ограничения (Constraints)**

Ограничения используются для обеспечения целостности данных.

---

### **2.1. Типы ограничений**



| Ограничение          | Описание                                                                                     | Пример                                                                                     |
|----------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **PRIMARY KEY**      | Уникальный идентификатор строки.                                                            | `CREATE TABLE employees (employee_id SERIAL PRIMARY KEY, ...);`                            |
| **FOREIGN KEY**      | Обеспечивает ссылочную целостность между таблицами.                                         | `CREATE TABLE employees (..., department_id INTEGER REFERENCES departments(department_id));` |
| **UNIQUE**           | Гарантирует уникальность значений в столбце или группе столбцов.                            | `CREATE TABLE employees (..., email VARCHAR(100) UNIQUE);`                                  |
| **CHECK**            | Ограничивает значения в столбце на основе условия.                                           | `CREATE TABLE employees (..., salary DECIMAL(10, 2) CHECK (salary > 0));`                     |
| **NOT NULL**         | Запрещает значения `NULL` в столбце.                                                        | `CREATE TABLE employees (..., first_name VARCHAR(50) NOT NULL);`                            |
| **EXCLUDE**          | Исключает пересекающиеся значения (например, для временных интервалов).                     | `CREATE TABLE events (..., EXCLUDE USING gist (tsrange FROM start_time TO end_time WITH &&));` |

---

### **2.2. Добавление ограничений**
```sql
ALTER TABLE table_name
ADD CONSTRAINT constraint_name constraint_type (column_name);
```

**Пример:**
```sql
ALTER TABLE employees
ADD CONSTRAINT fk_department
FOREIGN KEY (department_id) REFERENCES departments(department_id);
```

---

### **2.3. Удаление ограничений**
```sql
ALTER TABLE table_name
DROP CONSTRAINT constraint_name;
```

**Пример:**
```sql
ALTER TABLE employees
DROP CONSTRAINT fk_department;
```

---

## **3. Работа с табличными пространствами (Tablespaces)**

Табличные пространства позволяют управлять физическим размещением данных.

---

### **3.1. Создание табличного пространства**
```sql
CREATE TABLESPACE tablespace_name
[OWNER user_name]
LOCATION '/path/to/directory';
```

**Пример:**
```sql
CREATE TABLESPACE my_tablespace
OWNER postgres
LOCATION '/var/lib/postgresql/data/my_tablespace';
```

---

### **3.2. Изменение табличного пространства**
```sql
ALTER TABLESPACE tablespace_name
[RENAME TO new_tablespace_name]
[OWNER TO new_owner];
```

**Пример:**
```sql
ALTER TABLESPACE my_tablespace RENAME TO new_tablespace;
```

---

### **3.3. Удаление табличного пространства**
```sql
DROP TABLESPACE [IF EXISTS] tablespace_name;
```

**Пример:**
```sql
DROP TABLESPACE IF EXISTS new_tablespace;
```

---

### **3.4. Использование табличного пространства**
```sql
CREATE TABLE table_name (
    ...
) TABLESPACE tablespace_name;

CREATE INDEX index_name ON table_name (column_name)
TABLESPACE tablespace_name;
```

**Пример:**
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
) TABLESPACE new_tablespace;
```

---

## **4. Работа с доменами (Domains)**

Домены позволяют создавать пользовательские типы данных с ограничениями.

---

### **4.1. Создание домена**
```sql
CREATE DOMAIN domain_name [AS] data_type
[DEFAULT default_value]
[constraints];
```

**Пример:**
```sql
CREATE DOMAIN positive_numeric AS NUMERIC
CHECK (VALUE > 0);
```

---

### **4.2. Использование домена**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price positive_numeric
);
```

---

### **4.3. Изменение домена**
```sql
ALTER DOMAIN domain_name
[ADD CONSTRAINT constraint_name constraint_definition]
[DROP CONSTRAINT constraint_name];
```

**Пример:**
```sql
ALTER DOMAIN positive_numeric
ADD CONSTRAINT positive_check CHECK (VALUE > 0);
```

---

### **4.4. Удаление домена**
```sql
DROP DOMAIN [IF EXISTS] domain_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP DOMAIN IF EXISTS positive_numeric;
```

---

## **5. Работа с типами данных**

PostgreSQL поддерживает множество встроенных типов данных, а также позволяет создавать пользовательские типы.

---

### **5.1. Создание пользовательского типа**
```sql
CREATE TYPE type_name AS (
    attribute1 data_type,
    attribute2 data_type,
    ...
);
```

**Пример:**
```sql
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    postal_code VARCHAR(20)
);
```

---

### **5.2. Использование пользовательского типа**
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_address address
);
```

---

### **5.3. Изменение пользовательского типа**
```sql
ALTER TYPE type_name
[RENAME TO new_type_name]
[RENAME ATTRIBUTE attribute_name TO new_attribute_name]
[ADD ATTRIBUTE attribute_name data_type]
[DROP ATTRIBUTE [IF EXISTS] attribute_name [CASCADE | RESTRICT]];
```

**Пример:**
```sql
ALTER TYPE address
ADD ATTRIBUTE country VARCHAR(50);
```

---

### **5.4. Удаление пользовательского типа**
```sql
DROP TYPE [IF EXISTS] type_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP TYPE IF EXISTS address;
```

---

## **6. Работа с расширениями (Extensions)**

Расширения позволяют добавлять новые функции и типы данных в PostgreSQL.

---

### **6.1. Создание расширения**
```sql
CREATE EXTENSION [IF NOT EXISTS] extension_name [WITH] [SCHEMA schema_name];
```

**Пример:**
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

### **6.2. Удаление расширения**
```sql
DROP EXTENSION [IF EXISTS] extension_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP EXTENSION IF EXISTS "uuid-ossp";
```

---

## **7. Работа с ролями и правами доступа**

### **7.1. Создание роли**
```sql
CREATE ROLE role_name [WITH option_list];

option_list:
    SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT connlimit
    | [ENCRYPTED | UNENCRYPTED] PASSWORD 'password'
    | VALID UNTIL 'timestamp'
```

**Пример:**
```sql
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password' CONNECTION LIMIT 10;
```

---

### **7.2. Изменение роли**
```sql
ALTER ROLE role_name [WITH option_list];
```

**Пример:**
```sql
ALTER ROLE app_user WITH PASSWORD 'new_secure_password';
```

---

### **7.3. Удаление роли**
```sql
DROP ROLE [IF EXISTS] role_name;
```

**Пример:**
```sql
DROP ROLE IF EXISTS app_user;
```

---

### **7.4. Предоставление прав доступа**
```sql
GRANT privilege [, ...]
ON object_type object_name [, ...]
TO role_name [, ...]
[WITH GRANT OPTION];
```

**Примеры:**
```sql
-- Предоставить права на SELECT для таблицы
GRANT SELECT ON employees TO app_user;

-- Предоставить все права на таблицу
GRANT ALL PRIVILEGES ON employees TO app_user;

-- Предоставить права на схему
GRANT USAGE ON SCHEMA hr TO app_user;

-- Предоставить права на создание объектов в схеме
GRANT CREATE ON SCHEMA hr TO app_user;
```

---

### **7.5. Отзыв прав доступа**
```sql
REVOKE [GRANT OPTION FOR] privilege [, ...]
ON object_type object_name [, ...]
FROM role_name [, ...]
[CASCADE | RESTRICT];
```

**Пример:**
```sql
REVOKE SELECT ON employees FROM app_user;
```

---

## **8. Работа с триггерами**

### **8.1. Создание триггерной функции**
```sql
CREATE OR REPLACE FUNCTION trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    -- Логика триггера
    RETURN NEW; -- или RETURN OLD;
END;
$$ LANGUAGE plpgsql;
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION log_employee_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employee_audit (employee_id, old_salary, new_salary, change_date)
    VALUES (OLD.employee_id, OLD.salary, NEW.salary, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

### **8.2. Создание триггера**
```sql
CREATE TRIGGER trigger_name
[BEFORE | AFTER | INSTEAD OF] [INSERT | UPDATE | DELETE | TRUNCATE]
ON table_name
[FOR EACH ROW | FOR EACH STATEMENT]
EXECUTE FUNCTION trigger_function();
```

**Пример:**
```sql
CREATE TRIGGER trg_employee_update
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION log_employee_change();
```

---

### **8.3. Удаление триггера**
```sql
DROP TRIGGER [IF EXISTS] trigger_name ON table_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP TRIGGER IF EXISTS trg_employee_update ON employees;
```

---

## **9. Работа с материализованными представлениями**

Материализованные представления хранят результаты запроса и обновляются вручную или по расписанию.

---

### **9.1. Создание материализованного представления**
```sql
CREATE MATERIALIZED VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
[WHERE condition]
[WITH [NO] DATA];
```

**Пример:**
```sql
CREATE MATERIALIZED VIEW high_salary_employees_mv AS
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 100000;
```

---

### **9.2. Обновление материализованного представления**
```sql
REFRESH MATERIALIZED VIEW [CONCURRENTLY] view_name;
```

**Пример:**
```sql
REFRESH MATERIALIZED VIEW high_salary_employees_mv;
```

---

### **9.3. Удаление материализованного представления**
```sql
DROP MATERIALIZED VIEW [IF EXISTS] view_name [CASCADE | RESTRICT];
```

**Пример:**
```sql
DROP MATERIALIZED VIEW IF EXISTS high_salary_employees_mv;
```

---

## **10. Работа с событиями (Event Triggers)**

Событийные триггеры позволяют выполнять действия при выполнении определённых DDL-команд.

---

### **10.1. Создание функции для событийного триггера**
```sql
CREATE OR REPLACE FUNCTION event_trigger_function()
RETURNS event_trigger LANGUAGE plpgsql AS $$
BEGIN
    -- Логика триггера
END;
$$;
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION log_ddl_commands()
RETURNS event_trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO ddl_audit (command_tag, object_type, object_identity)
    VALUES (tg_tag, pg_event_trigger_ddl_commands().object_type,
            pg_event_trigger_ddl_commands().object_identity);
END;
$$;
```

---

### **10.2. Создание событийного триггера**
```sql
CREATE EVENT TRIGGER trigger_name
ON ddl_command
EXECUTE FUNCTION event_trigger_function();
```

**Пример:**
```sql
CREATE EVENT TRIGGER trg_log_ddl
ON ddl_command_start
EXECUTE FUNCTION log_ddl_commands();
```

---

### **10.3. Удаление событийного триггера**
```sql
DROP EVENT TRIGGER [IF EXISTS] trigger_name;
```

**Пример:**
```sql
DROP EVENT TRIGGER IF EXISTS trg_log_ddl;
```

---

## **11. Работа с разделами (Partitions)**

Разделы позволяют разбивать большие таблицы на более мелкие части для улучшения производительности.

---

### **11.1. Создание разделённой таблицы**
```sql
CREATE TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
) PARTITION BY RANGE (column_name);
```

**Пример:**
```sql
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (sale_date);
```

---

### **11.2. Создание разделов**
```sql
CREATE TABLE partition_name PARTITION OF table_name
FOR VALUES FROM (start_value) TO (end_value);
```

**Пример:**
```sql
CREATE TABLE sales_2023 PARTITION OF sales
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE sales_2024 PARTITION OF sales
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

---

### **11.3. Добавление раздела**
```sql
CREATE TABLE partition_name PARTITION OF table_name
FOR VALUES FROM (start_value) TO (end_value);
```

---

### **11.4. Удаление раздела**
```sql
DROP TABLE partition_name;
```

**Пример:**
```sql
DROP TABLE sales_2023;
```

---

## **12. Работа с внешними таблицами (Foreign Data Wrappers)**

Внешние таблицы позволяют работать с данными из других источников (например, CSV, другие базы данных).

---

### **12.1. Создание расширения для работы с внешними данными**
```sql
CREATE EXTENSION [IF NOT EXISTS] extension_name;
```

**Пример:**
```sql
CREATE EXTENSION IF NOT EXISTS file_fdw;
```

---

### **12.2. Создание сервера для внешних данных**
```sql
CREATE SERVER server_name FOREIGN DATA WRAPPER wrapper_name;
```

**Пример:**
```sql
CREATE SERVER csv_server FOREIGN DATA WRAPPER file_fdw;
```

---

### **12.3. Создание пользовательского отображения**
```sql
CREATE USER MAPPING FOR user_name
SERVER server_name
OPTIONS (option 'value');
```

**Пример:**
```sql
CREATE USER MAPPING FOR postgres
SERVER csv_server
OPTIONS (user 'postgres');
```

---

### **12.4. Создание внешней таблицы**
```sql
CREATE FOREIGN TABLE foreign_table_name (
    column1 data_type,
    column2 data_type,
    ...
) SERVER server_name
OPTIONS (option 'value');
```

**Пример:**
```sql
CREATE FOREIGN TABLE csv_employees (
    employee_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
) SERVER csv_server
OPTIONS (filename '/path/to/employees.csv', format 'csv', header 'true');
```

---

### **12.5. Запрос к внешней таблице**
```sql
SELECT * FROM csv_employees;
```

---

### **12.6. Удаление внешней таблицы**
```sql
DROP FOREIGN TABLE [IF EXISTS] foreign_table_name;
```

**Пример:**
```sql
DROP FOREIGN TABLE IF EXISTS csv_employees;
```

---

## **13. Работа с полнотекстовым поиском**

PostgreSQL предоставляет мощные инструменты для полнотекстового поиска.

---

### **13.1. Создание столбца для полнотекстового поиска**
```sql
ALTER TABLE table_name ADD COLUMN search_vector TSVECTOR;
```

**Пример:**
```sql
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR;
```

---

### **13.2. Обновление столбца для полнотекстового поиска**
```sql
UPDATE table_name SET search_vector = TO_TSVECTOR('language', column_name);
```

**Пример:**
```sql
UPDATE articles SET search_vector = TO_TSVECTOR('russian', title || ' ' || content);
```

---

### **13.3. Создание триггера для автоматического обновления**
```sql
CREATE TRIGGER trigger_name
BEFORE INSERT OR UPDATE ON table_name
FOR EACH ROW
EXECUTE FUNCTION tsvector_update_trigger(search_vector, 'pg_catalog.russian', title, content);
```

**Пример:**
```sql
CREATE TRIGGER trg_articles_search_vector
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW
EXECUTE FUNCTION tsvector_update_trigger(search_vector, 'pg_catalog.russian', title, content);
```

---

### **13.4. Создание индекса для полнотекстового поиска**
```sql
CREATE INDEX index_name ON table_name USING GIN (search_vector);
```

**Пример:**
```sql
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);
```

---

### **13.5. Поиск с использованием полнотекстового индекса**
```sql
SELECT * FROM table_name
WHERE search_vector @@ TO_TSQUERY('language', 'search_query');
```

**Пример:**
```sql
SELECT * FROM articles
WHERE search_vector @@ TO_TSQUERY('russian', 'PostgreSQL & индексы');
```

---

### **13.6. Поиск с ранжированием**
```sql
SELECT *, TS_RANK(search_vector, TO_TSQUERY('language', 'search_query')) AS rank
FROM table_name
WHERE search_vector @@ TO_TSQUERY('language', 'search_query')
ORDER BY rank DESC;
```

**Пример:**
```sql
SELECT *, TS_RANK(search_vector, TO_TSQUERY('russian', 'PostgreSQL & индексы')) AS rank
FROM articles
WHERE search_vector @@ TO_TSQUERY('russian', 'PostgreSQL & индексы')
ORDER BY rank DESC;
```

---

## **14. Работа с JSON и JSONB**

PostgreSQL поддерживает типы данных `JSON` и `JSONB` для работы с данными в формате JSON.

---

### **14.1. Создание таблицы с JSON/JSONB**
```sql
CREATE TABLE table_name (
    id SERIAL PRIMARY KEY,
    data JSONB
);
```

**Пример:**
```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    profile_data JSONB
);
```

---

### **14.2. Вставка данных в JSON/JSONB**
```sql
INSERT INTO table_name (data) VALUES ('{"key": "value"}');
```

**Пример:**
```sql
INSERT INTO user_profiles (profile_data)
VALUES ('{"name": "Иван", "age": 30, "interests": ["программирование", "чтение"]}');
```

---

### **13.3. Запрос данных из JSON/JSONB**
```sql
SELECT data->>'key' FROM table_name;
SELECT data->'key' FROM table_name;
SELECT data#>>'{nested,key}' FROM table_name;
```

**Примеры:**
```sql
-- Получение значения по ключу
SELECT profile_data->>'name' FROM user_profiles;

-- Получение JSON-объекта по ключу
SELECT profile_data->'interests' FROM user_profiles;

-- Поиск по значению в JSON
SELECT * FROM user_profiles
WHERE profile_data @> '{"interests": ["программирование"]}';
```

---

### **14.4. Обновление данных в JSON/JSONB**
```sql
UPDATE table_name
SET data = jsonb_set(data, '{key}', '"new_value"')
WHERE condition;
```

**Пример:**
```sql
UPDATE user_profiles
SET profile_data = jsonb_set(profile_data, '{age}', '31')
WHERE profile_data->>'name' = 'Иван';
```

---

### **14.5. Создание индекса для JSON/JSONB**
```sql
CREATE INDEX index_name ON table_name USING GIN (data jsonb_path_ops);
```

**Пример:**
```sql
CREATE INDEX idx_user_profiles_interests ON user_profiles USING GIN (profile_data jsonb_path_ops);
```

---

## **15. Работа с временными таблицами**

Временные таблицы существуют только в течение сессии или транзакции.

---

### **15.1. Создание временной таблицы**
```sql
CREATE [GLOBAL | LOCAL] TEMPORARY TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
) [ON COMMIT {PRESERVE ROWS | DELETE ROWS | DROP}];
```

**Пример:**
```sql
CREATE TEMPORARY TABLE temp_employees (
    employee_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
) ON COMMIT DROP;
```

---

### **15.2. Использование временной таблицы**
```sql
INSERT INTO temp_employees VALUES (1, 'Иван', 'Иванов');
SELECT * FROM temp_employees;
```

---

### **15.3. Удаление временной таблицы**
Временные таблицы автоматически удаляются в конце сессии или транзакции (в зависимости от параметров).

---

## **16. Работа с транзакциями**

Транзакции позволяют группировать несколько операций в одну атомарную единицу.

---

### **16.1. Начало транзакции**
```sql
BEGIN;
-- или
START TRANSACTION;
```

---

### **16.2. Фиксация транзакции**
```sql
COMMIT;
```

---

### **16.3. Откат транзакции**
```sql
ROLLBACK;
```

---

### **16.4. Точки сохранения (Savepoints)**
```sql
SAVEPOINT savepoint_name;
-- ...
ROLLBACK TO SAVEPOINT savepoint_name;
```

**Пример:**
```sql
BEGIN;
    INSERT INTO employees (first_name, last_name) VALUES ('Иван', 'Иванов');
    SAVEPOINT before_update;
    UPDATE employees SET first_name = 'Петр' WHERE last_name = 'Иванов';
    -- Откат к точке сохранения
    ROLLBACK TO SAVEPOINT before_update;
COMMIT;
```

---

## **17. Работа с комментариями**

Комментарии помогают документировать объекты базы данных.

---

### **17.1. Добавление комментария к объекту**
```sql
COMMENT ON {TABLE | COLUMN | INDEX | ...} object_name IS 'comment_text';
```

**Примеры:**
```sql
COMMENT ON TABLE employees IS 'Таблица сотрудников компании';
COMMENT ON COLUMN employees.salary IS 'Зарплата сотрудника в рублях';
```

---

### **17.2. Просмотр комментариев**
```sql
SELECT obj_description('schema_name.table_name'::regclass);
-- или
SELECT col_description('schema_name.table_name'::regclass, column_number);
```

**Пример:**
```sql
SELECT obj_description('public.employees'::regclass);
```

---

## **18. Работа с доменными ограничениями**

Доменные ограничения позволяют создавать пользовательские типы данных с проверками.

---

### **18.1. Создание домена с ограничением**
```sql
CREATE DOMAIN domain_name AS data_type
[DEFAULT default_value]
[constraint [constraint_name] CHECK (condition)];
```

**Пример:**
```sql
CREATE DOMAIN positive_integer AS INTEGER
CHECK (VALUE > 0);
```

---

### **18.2. Использование домена**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    quantity positive_integer
);
```

---

## **19. Работа с типами данных**

PostgreSQL поддерживает множество встроенных типов данных.

---

### **19.1. Основные типы данных**



| Категория               | Типы данных                                                                                     |
|-------------------------|------------------------------------------------------------------------------------------------|
| **Числовые**           | `SMALLINT`, `INTEGER`, `BIGINT`, `DECIMAL(p,s)`, `NUMERIC(p,s)`, `REAL`, `DOUBLE PRECISION`, `SERIAL` |
| **Строковые**          | `CHAR(n)`, `VARCHAR(n)`, `TEXT`                                                                |
| **Бинарные**            | `BYTEA`                                                                                         |
| **Дата и время**        | `DATE`, `TIME`, `TIMESTAMP`, `INTERVAL`                                                       |
| **Логический**          | `BOOLEAN`                                                                                       |
| **Геометрические**     | `POINT`, `LINE`, `LSEG`, `BOX`, `PATH`, `POLYGON`, `CIRCLE`                                    |
| **Сетевые адреса**      | `INET`, `CIDR`, `MACADDR`                                                                      |
| **JSON**                | `JSON`, `JSONB`                                                                                |
| **XML**                 | `XML`                                                                                          |
| **Массивы**             | `type[]` (например, `INTEGER[]`, `TEXT[]`)                                                     |
| **UUID**                | `UUID`                                                                                         |
| **Специальные**         | `TSVECTOR`, `TSQUERY` (для полнотекстового поиска)                                            |

---

### **19.2. Примеры использования типов данных**

#### **Числовые типы**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10, 2),
    quantity INTEGER
);
```

#### **Строковые типы**
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    bio TEXT
);
```

#### **Дата и время**
```sql
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(100),
    start_time TIMESTAMP,
    duration INTERVAL
);
```

#### **JSON/JSONB**
```sql
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile_data JSONB
);
```

#### **Массивы**
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_ids INTEGER[],
    quantities INTEGER[]
);
```

---

## **20. Работа с ограничениями целостности**

Ограничения целостности обеспечивают корректность данных.

---

### **20.1. Первичный ключ (Primary Key)**
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    ...
);
```

---

### **20.2. Внешний ключ (Foreign Key)**
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    ...
);
```

---

### **20.3. Уникальное ограничение (Unique)**
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    ...
);
```

---

### **20.4. Проверка (Check)**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10, 2) CHECK (price > 0),
    ...
);
```

---

### **20.5. Ограничение исключения (Exclusion)**
```sql
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INTEGER,
    during TSRange,
    EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
```

---

## **21. Работа с наследованием таблиц**

PostgreSQL поддерживает наследование таблиц.

---

### **21.1. Создание дочерней таблицы**
```sql
CREATE TABLE child_table (
    ...
) INHERITS (parent_table);
```

**Пример:**
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    hire_date DATE
);

CREATE TABLE managers (
    department VARCHAR(50),
    bonus DECIMAL(10, 2)
) INHERITS (employees);
```

---

### **21.2. Запрос данных из иерархии таблиц**
```sql
SELECT * FROM parent_table;
```

---

## **22. Работа с разделами (Partitioning)**

Разделы позволяют разбивать большие таблицы на более мелкие части.

---

### **22.1. Создание разделённой таблицы**
```sql
CREATE TABLE table_name (
    ...
) PARTITION BY {RANGE | LIST | HASH} (column_name);
```

**Пример:**
```sql
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (sale_date);
```

---

### **22.2. Создание разделов**
```sql
CREATE TABLE partition_name PARTITION OF table_name
FOR VALUES FROM (start_value) TO (end_value);
```

**Пример:**
```sql
CREATE TABLE sales_2023 PARTITION OF sales
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE sales_2024 PARTITION OF sales
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

---

### **22.3. Добавление раздела**
```sql
CREATE TABLE partition_name PARTITION OF table_name
FOR VALUES FROM (start_value) TO (end_value);
```

---

### **22.4. Удаление раздела**
```sql
DROP TABLE partition_name;
```

**Пример:**
```sql
DROP TABLE sales_2023;
```

---

## **23. Работа с материализованными представлениями**

Материализованные представления хранят результаты запроса и обновляются вручную или по расписанию.

---

### **23.1. Создание материализованного представления**
```sql
CREATE MATERIALIZED VIEW view_name AS
SELECT ...
[WITH [NO] DATA];
```

**Пример:**
```sql
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', sale_date) AS month,
    SUM(amount) AS total_amount
FROM sales
GROUP BY DATE_TRUNC('month', sale_date);
```

---

### **23.2. Обновление материализованного представления**
```sql
REFRESH MATERIALIZED VIEW [CONCURRENTLY] view_name;
```

**Пример:**
```sql
REFRESH MATERIALIZED VIEW monthly_sales;
```

---

### **23.3. Удаление материализованного представления**
```sql
DROP MATERIALIZED VIEW [IF EXISTS] view_name;
```

**Пример:**
```sql
DROP MATERIALIZED VIEW IF EXISTS monthly_sales;
```

---

## **24. Работа с внешними данными (Foreign Data Wrappers)**

Внешние таблицы позволяют работать с данными из других источников.

---

### **24.1. Создание расширения для работы с внешними данными**
```sql
CREATE EXTENSION [IF NOT EXISTS] extension_name;
```

**Пример:**
```sql
CREATE EXTENSION IF NOT EXISTS file_fdw;
```

---

### **24.2. Создание сервера для внешних данных**
```sql
CREATE SERVER server_name FOREIGN DATA WRAPPER wrapper_name;
```

**Пример:**
```sql
CREATE SERVER csv_server FOREIGN DATA WRAPPER file_fdw;
```

---

### **24.3. Создание пользовательского отображения**
```sql
CREATE USER MAPPING FOR user_name
SERVER server_name
OPTIONS (option 'value');
```

**Пример:**
```sql
CREATE USER MAPPING FOR postgres
SERVER csv_server
OPTIONS (user 'postgres');
```

---

### **24.4. Создание внешней таблицы**
```sql
CREATE FOREIGN TABLE foreign_table_name (
    ...
) SERVER server_name
OPTIONS (option 'value');
```

**Пример:**
```sql
CREATE FOREIGN TABLE csv_employees (
    employee_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
) SERVER csv_server
OPTIONS (filename '/path/to/employees.csv', format 'csv', header 'true');
```

---

### **24.5. Запрос к внешней таблице**
```sql
SELECT * FROM csv_employees;
```

---

### **24.6. Удаление внешней таблицы**
```sql
DROP FOREIGN TABLE [IF EXISTS] foreign_table_name;
```

**Пример:**
```sql
DROP FOREIGN TABLE IF EXISTS csv_employees;
```

---

## **25. Работа с событиями (Event Triggers)**

Событийные триггеры позволяют выполнять действия при выполнении DDL-команд.

---

### **25.1. Создание функции для событийного триггера**
```sql
CREATE OR REPLACE FUNCTION event_trigger_function()
RETURNS event_trigger LANGUAGE plpgsql AS $$
BEGIN
    -- Логика триггера
END;
$$;
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION log_ddl_commands()
RETURNS event_trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO ddl_audit (command_tag, object_type, object_identity)
    VALUES (tg_tag, pg_event_trigger_ddl_commands().object_type,
            pg_event_trigger_ddl_commands().object_identity);
END;
$$;
```

---

### **25.2. Создание событийного триггера**
```sql
CREATE EVENT TRIGGER trigger_name
ON ddl_command
EXECUTE FUNCTION event_trigger_function();
```

**Пример:**
```sql
CREATE EVENT TRIGGER trg_log_ddl
ON ddl_command_start
EXECUTE FUNCTION log_ddl_commands();
```

---

### **25.3. Удаление событийного триггера**
```sql
DROP EVENT TRIGGER [IF EXISTS] trigger_name;
```

**Пример:**
```sql
DROP EVENT TRIGGER IF EXISTS trg_log_ddl;
```

---

## **26. Работа с транзакциями и блокировками**

---

### **26.1. Начало транзакции**
```sql
BEGIN;
-- или
START TRANSACTION;
```

---

### **26.2. Фиксация транзакции**
```sql
COMMIT;
```

---

### **26.3. Откат транзакции**
```sql
ROLLBACK;
```

---

### **26.4. Точки сохранения (Savepoints)**
```sql
SAVEPOINT savepoint_name;
-- ...
ROLLBACK TO SAVEPOINT savepoint_name;
```

**Пример:**
```sql
BEGIN;
    INSERT INTO employees (first_name, last_name) VALUES ('Иван', 'Иванов');
    SAVEPOINT before_update;
    UPDATE employees SET first_name = 'Петр' WHERE last_name = 'Иванов';
    -- Откат к точке сохранения
    ROLLBACK TO SAVEPOINT before_update;
COMMIT;
```

---

### **26.5. Уровни изоляции транзакций**
```sql
SET TRANSACTION ISOLATION LEVEL {READ COMMITTED | REPEATABLE READ | SERIALIZABLE};
```

**Пример:**
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- ...
COMMIT;
```

---

### **26.6. Блокировки**
```sql
-- Блокировка строки для обновления
SELECT * FROM table_name WHERE condition FOR UPDATE;

-- Блокировка строки для совместного доступа
SELECT * FROM table_name WHERE condition FOR SHARE;
```

**Пример:**
```sql
BEGIN;
SELECT * FROM accounts WHERE account_id = 1 FOR UPDATE;
-- ...
COMMIT;
```

---

## **27. Работа с комментариями**

Комментарии помогают документировать объекты базы данных.

---

### **27.1. Добавление комментария к объекту**
```sql
COMMENT ON {TABLE | COLUMN | INDEX | ...} object_name IS 'comment_text';
```

**Примеры:**
```sql
COMMENT ON TABLE employees IS 'Таблица сотрудников компании';
COMMENT ON COLUMN employees.salary IS 'Зарплата сотрудника в рублях';
```

---

### **27.2. Просмотр комментариев**
```sql
SELECT obj_description('schema_name.table_name'::regclass);
-- или
SELECT col_description('schema_name.table_name'::regclass, column_number);
```

**Пример:**
```sql
SELECT obj_description('public.employees'::regclass);
```

---

## **28. Работа с последовательностями (Sequences)**

Последовательности используются для генерации уникальных числовых значений.

---

### **28.1. Создание последовательности**
```sql
CREATE SEQUENCE sequence_name
[INCREMENT BY increment]
[MINVALUE minvalue | NO MINVALUE]
[MAXVALUE maxvalue | NO MAXVALUE]
[START WITH start]
[CACHE cache]
[CYCLE | NO CYCLE];
```

**Пример:**
```sql
CREATE SEQUENCE employee_id_seq
INCREMENT BY 1
MINVALUE 1
START WITH 1
CACHE 20;
```

---

### **28.2. Использование последовательности**
```sql
INSERT INTO table_name (id, ...) VALUES (NEXTVAL('sequence_name'), ...);
-- или
INSERT INTO table_name (id, ...) VALUES (DEFAULT, ...);
```

**Пример:**
```sql
INSERT INTO employees (employee_id, first_name, last_name)
VALUES (NEXTVAL('employee_id_seq'), 'Иван', 'Иванов');
```

---

### **28.3. Изменение последовательности**
```sql
ALTER SEQUENCE sequence_name
[INCREMENT BY increment]
[MINVALUE minvalue | NO MINVALUE]
[MAXVALUE maxvalue | NO MAXVALUE]
[START WITH start]
[RESTART [WITH start]]
[CACHE cache | NO CACHE]
[CYCLE | NO CYCLE];
```

**Пример:**
```sql
ALTER SEQUENCE employee_id_seq INCREMENT BY 2;
```

---

### **28.4. Удаление последовательности**
```sql
DROP SEQUENCE [IF EXISTS] sequence_name;
```

**Пример:**
```sql
DROP SEQUENCE IF EXISTS employee_id_seq;
```

---

## **29. Работа с триггерами**

Триггеры позволяют автоматически выполнять действия при изменении данных.

---

### **29.1. Создание триггерной функции**
```sql
CREATE OR REPLACE FUNCTION trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    -- Логика триггера
    RETURN NEW; -- или RETURN OLD;
END;
$$ LANGUAGE plpgsql;
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION log_employee_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO employee_audit (employee_id, old_salary, new_salary, change_date)
    VALUES (OLD.employee_id, OLD.salary, NEW.salary, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

### **29.2. Создание триггера**
```sql
CREATE TRIGGER trigger_name
[BEFORE | AFTER | INSTEAD OF] [INSERT | UPDATE | DELETE | TRUNCATE]
ON table_name
[FOR EACH ROW | FOR EACH STATEMENT]
EXECUTE FUNCTION trigger_function();
```

**Пример:**
```sql
CREATE TRIGGER trg_employee_update
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION log_employee_change();
```

---

### **29.3. Удаление триггера**
```sql
DROP TRIGGER [IF EXISTS] trigger_name ON table_name;
```

**Пример:**
```sql
DROP TRIGGER IF EXISTS trg_employee_update ON employees;
```

---

## **30. Работа с функциями и процедурами**

---

### **30.1. Создание функции**
```sql
CREATE [OR REPLACE] FUNCTION function_name (parameter1 type1, parameter2 type2, ...)
RETURNS return_type AS $$
DECLARE
    -- переменные
BEGIN
    -- тело функции
END;
$$ LANGUAGE plpgsql;
```

**Пример:**
```sql
CREATE OR REPLACE FUNCTION calculate_bonus(salary DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    RETURN salary * 0.1;
END;
$$ LANGUAGE plpgsql;
```

---

### **30.2. Вызов функции**
```sql
SELECT function_name(parameter1, parameter2, ...);
```

**Пример:**
```sql
SELECT calculate_bonus(100000);
```

---

### **30.3. Создание процедуры**
```sql
CREATE [OR REPLACE] PROCEDURE procedure_name (parameter1 type1, parameter2 type2, ...)
LANGUAGE plpgsql AS $$
BEGIN
    -- тело процедуры
END;
$$;
```

**Пример:**
```sql
CREATE OR REPLACE PROCEDURE update_employee_salary(employee_id INTEGER, new_salary DECIMAL)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employees SET salary = new_salary WHERE employee_id = employee_id;
END;
$$;
```

---

### **30.4. Вызов процедуры**
```sql
CALL procedure_name(parameter1, parameter2, ...);
```

**Пример:**
```sql
CALL update_employee_salary(1, 120000);
```

---

### **30.5. Удаление функции или процедуры**
```sql
DROP FUNCTION [IF EXISTS] function_name (parameter1 type1, parameter2 type2, ...);
DROP PROCEDURE [IF EXISTS] procedure_name (parameter1 type1, parameter2 type2, ...);
```

**Пример:**
```sql
DROP FUNCTION IF EXISTS calculate_bonus(DECIMAL);
DROP PROCEDURE IF EXISTS update_employee_salary(INTEGER, DECIMAL);
```

---

## **31. Работа с представлениями (Views)**

Представления позволяют создавать виртуальные таблицы на основе запросов.

---

### **31.1. Создание представления**
```sql
CREATE [OR REPLACE] VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
[WHERE condition];
```

**Пример:**
```sql
CREATE VIEW high_salary_employees AS
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 100000;
```

---

### **31.2. Запрос к представлению**
```sql
SELECT * FROM view_name;
```

**Пример:**
```sql
SELECT * FROM high_salary_employees;
```

---

### **31.3. Удаление представления**
```sql
DROP VIEW [IF EXISTS] view_name;
```

**Пример:**
```sql
DROP VIEW IF EXISTS high_salary_employees;
```

---

## **32. Работа с временными таблицами**

Временные таблицы существуют только в течение сессии или транзакции.

---

### **32.1. Создание временной таблицы**
```sql
CREATE [GLOBAL | LOCAL] TEMPORARY TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
) [ON COMMIT {PRESERVE ROWS | DELETE ROWS | DROP}];
```

**Пример:**
```sql
CREATE TEMPORARY TABLE temp_employees (
    employee_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
) ON COMMIT DROP;
```

---

### **32.2. Использование временной таблицы**
```sql
INSERT INTO temp_employees VALUES (1, 'Иван', 'Иванов');
SELECT * FROM temp_employees;
```

---

## **33. Работа с ролями и правами доступа**

---

### **33.1. Создание роли**
```sql
CREATE ROLE role_name [WITH option_list];
```

**Пример:**
```sql
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password' CONNECTION LIMIT 10;
```

---

### **33.2. Изменение роли**
```sql
ALTER ROLE role_name [WITH option_list];
```

**Пример:**
```sql
ALTER ROLE app_user WITH PASSWORD 'new_secure_password';
```

---

### **33.3. Удаление роли**
```sql
DROP ROLE [IF EXISTS] role_name;
```

**Пример:**
```sql
DROP ROLE IF EXISTS app_user;
```

---

### **33.4. Предоставление прав доступа**
```sql
GRANT privilege [, ...]
ON object_type object_name [, ...]
TO role_name [, ...]
[WITH GRANT OPTION];
```

**Примеры:**
```sql
GRANT SELECT ON employees TO app_user;
GRANT ALL PRIVILEGES ON employees TO app_user;
GRANT USAGE ON SCHEMA hr TO app_user;
GRANT CREATE ON SCHEMA hr TO app_user;
```

---

### **33.5. Отзыв прав доступа**
```sql
REVOKE [GRANT OPTION FOR] privilege [, ...]
ON object_type object_name [, ...]
FROM role_name [, ...]
[CASCADE | RESTRICT];
```

**Пример:**
```sql
REVOKE SELECT ON employees FROM app_user;
```

---

## **34. Работа с табличными пространствами (Tablespaces)**

Табличные пространства позволяют управлять физическим размещением данных.

---

### **34.1. Создание табличного пространства**
```sql
CREATE TABLESPACE tablespace_name
[OWNER user_name]
LOCATION '/path/to/directory';
```

**Пример:**
```sql
CREATE TABLESPACE my_tablespace
OWNER postgres
LOCATION '/var/lib/postgresql/data/my_tablespace';
```

---

### **34.2. Изменение табличного пространства**
```sql
ALTER TABLESPACE tablespace_name
[RENAME TO new_tablespace_name]
[OWNER TO new_owner];
```

**Пример:**
```sql
ALTER TABLESPACE my_tablespace RENAME TO new_tablespace;
```

---

### **34.3. Удаление табличного пространства**
```sql
DROP TABLESPACE [IF EXISTS] tablespace_name;
```

**Пример:**
```sql
DROP TABLESPACE IF EXISTS new_tablespace;
```

---

### **34.4. Использование табличного пространства**
```sql
CREATE TABLE table_name (
    ...
) TABLESPACE tablespace_name;

CREATE INDEX index_name ON table_name (column_name)
TABLESPACE tablespace_name;
```

**Пример:**
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
) TABLESPACE new_tablespace;
```

---

## **35. Работа с доменами (Domains)**

Домены позволяют создавать пользовательские типы данных с ограничениями.

---

### **35.1. Создание домена**
```sql
CREATE DOMAIN domain_name AS data_type
[DEFAULT default_value]
[constraint [constraint_name] CHECK (condition)];
```

**Пример:**
```sql
CREATE DOMAIN positive_numeric AS NUMERIC
CHECK (VALUE > 0);
```

---

### **35.2. Использование домена**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price positive_numeric
);
```

---

### **35.3. Изменение домена**
```sql
ALTER DOMAIN domain_name
[ADD CONSTRAINT constraint_name constraint_definition]
[DROP CONSTRAINT constraint_name];
```

**Пример:**
```sql
ALTER DOMAIN positive_numeric
ADD CONSTRAINT positive_check CHECK (VALUE > 0);
```

---

### **35.4. Удаление домена**
```sql
DROP DOMAIN [IF EXISTS] domain_name;
```

**Пример:**
```sql
DROP DOMAIN IF EXISTS positive_numeric;
```

---

## **36. Работа с пользовательскими типами данных**

PostgreSQL позволяет создавать пользовательские типы данных.

---

### **36.1. Создание пользовательского типа**
```sql
CREATE TYPE type_name AS (
    attribute1 data_type,
    attribute2 data_type,
    ...
);
```

**Пример:**
```sql
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    postal_code VARCHAR(20)
);
```

---

### **36.2. Использование пользовательского типа**
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_address address
);
```

---

### **36.3. Изменение пользовательского типа**
```sql
ALTER TYPE type_name
[RENAME TO new_type_name]
[RENAME ATTRIBUTE attribute_name TO new_attribute_name]
[ADD ATTRIBUTE attribute_name data_type]
[DROP ATTRIBUTE [IF EXISTS] attribute_name [CASCADE | RESTRICT]];
```

**Пример:**
```sql
ALTER TYPE address
ADD ATTRIBUTE country VARCHAR(50);
```

---

### **36.4. Удаление пользовательского типа**
```sql
DROP TYPE [IF EXISTS] type_name;
```

**Пример:**
```sql
DROP TYPE IF EXISTS address;
```

---

## **37. Работа с расширениями (Extensions)**

Расширения позволяют добавлять новые функции и типы данных в PostgreSQL.

---

### **37.1. Создание расширения**
```sql
CREATE EXTENSION [IF NOT EXISTS] extension_name [WITH] [SCHEMA schema_name];
```

**Пример:**
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

### **37.2. Удаление расширения**
```sql
DROP EXTENSION [IF EXISTS] extension_name;
```

**Пример:**
```sql
DROP EXTENSION IF EXISTS "uuid-ossp";
```

---

## **38. Работа с JSON и JSONB**

PostgreSQL поддерживает типы данных `JSON` и `JSONB` для работы с данными в формате JSON.

---

### **38.1. Создание таблицы с JSON/JSONB**
```sql
CREATE TABLE table_name (
    id SERIAL PRIMARY KEY,
    data JSONB
);
```

**Пример:**
```sql
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    profile_data JSONB
);
```

---

### **38.2. Вставка данных в JSON/JSONB**
```sql
INSERT INTO table_name (data) VALUES ('{"key": "value"}');
```

**Пример:**
```sql
INSERT INTO user_profiles (profile_data)
VALUES ('{"name": "Иван", "age": 30, "interests": ["программирование", "чтение"]}');
```

---

### **38.3. Запрос данных из JSON/JSONB**
```sql
SELECT data->>'key' FROM table_name;
SELECT data->'key' FROM table_name;
SELECT data#>>'{nested,key}' FROM table_name;
```

**Примеры:**
```sql
-- Получение значения по ключу
SELECT profile_data->>'name' FROM user_profiles;

-- Получение JSON-объекта по ключу
SELECT profile_data->'interests' FROM user_profiles;

-- Поиск по значению в JSON
SELECT * FROM user_profiles
WHERE profile_data @> '{"interests": ["программирование"]}';
```

---

### **38.4. Обновление данных в JSON/JSONB**
```sql
UPDATE table_name
SET data = jsonb_set(data, '{key}', '"new_value"')
WHERE condition;
```

**Пример:**
```sql
UPDATE user_profiles
SET profile_data = jsonb_set(profile_data, '{age}', '31')
WHERE profile_data->>'name' = 'Иван';
```

---

### **38.5. Создание индекса для JSON/JSONB**
```sql
CREATE INDEX index_name ON table_name USING GIN (data jsonb_path_ops);
```

**Пример:**
```sql
CREATE INDEX idx_user_profiles_interests ON user_profiles USING GIN (profile_data jsonb_path_ops);
```

---

## **39. Работа с массивами**

PostgreSQL поддерживает массивы для хранения списков значений.

---

### **39.1. Создание таблицы с массивами**
```sql
CREATE TABLE table_name (
    id SERIAL PRIMARY KEY,
    array_column data_type[]
);
```

**Пример:**
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_ids INTEGER[],
    quantities INTEGER[]
);
```

---

### **39.2. Вставка данных в массив**
```sql
INSERT INTO table_name (array_column) VALUES (ARRAY[value1, value2, ...]);
```

**Пример:**
```sql
INSERT INTO orders (product_ids, quantities)
VALUES (ARRAY[1, 2, 3], ARRAY[2, 1, 3]);
```

---

### **39.3. Запрос данных из массива**
```sql
SELECT array_column[1] FROM table_name;
SELECT unnest(array_column) FROM table_name;
```

**Примеры:**
```sql
-- Получение первого элемента массива
SELECT product_ids[1] FROM orders;

-- Разворачивание массива в строки
SELECT unnest(product_ids) FROM orders;
```

---

### **39.4. Обновление данных в массиве**
```sql
UPDATE table_name
SET array_column[1] = new_value
WHERE condition;
```

**Пример:**
```sql
UPDATE orders
SET quantities[1] = 5
WHERE order_id = 1;
```

---

### **39.5. Создание индекса для массива**
```sql
CREATE INDEX index_name ON table_name USING GIN (array_column);
```

**Пример:**
```sql
CREATE INDEX idx_orders_product_ids ON orders USING GIN (product_ids);
```

---

## **40. Работа с геометрическими типами данных**

PostgreSQL поддерживает геометрические типы данных для работы с пространственными данными.

---

### **40.1. Установка расширения PostGIS**
```sql
CREATE EXTENSION postgis;
```

---

### **40.2. Создание таблицы с геометрическими данными**
```sql
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(Point, 4326)
);
```

---

### **40.3. Вставка геометрических данных**
```sql
INSERT INTO locations (name, geom)
VALUES ('Москва', ST_GeomFromText('POINT(37.6176 55.7558)', 4326));
```

---

### **40.4. Запрос геометрических данных**
```sql
SELECT ST_AsText(geom) FROM locations;
SELECT ST_Distance(geom1, geom2) FROM locations;
```

**Пример:**
```sql
-- Поиск объектов в радиусе 10 км от Москвы
SELECT name FROM locations
WHERE ST_DWithin(
    geom,
    ST_GeomFromText('POINT(37.6176 55.7558)', 4326),
    10000
);
```

---

### **40.5. Создание пространственного индекса**
```sql
CREATE INDEX index_name ON table_name USING GIST (geom);
```

**Пример:**
```sql
CREATE INDEX idx_locations_geom ON locations USING GIST (geom);
```

---

## **41. Работа с временными зонами**

PostgreSQL поддерживает работу с временными зонами.

---

### **41.1. Установка временной зоны**
```sql
SET TIME ZONE 'timezone';
```

**Пример:**
```sql
SET TIME ZONE 'Europe/Moscow';
```

---

### **41.2. Работа с временными метками**
```sql
SELECT NOW(); -- Текущая временная метка
SELECT NOW() AT TIME ZONE 'UTC'; -- Преобразование в UTC
```

**Пример:**
```sql
SELECT
    NOW() AS local_time,
    NOW() AT TIME ZONE 'UTC' AS utc_time;
```

---

## **42. Работа с транзакциями и блокировками**

---

### **42.1. Начало транзакции**
```sql
BEGIN;
-- или
START TRANSACTION;
```

---

### **42.2. Фиксация транзакции**
```sql
COMMIT;
```

---

### **42.3. Откат транзакции**
```sql
ROLLBACK;
```

---

### **42.4. Точки сохранения (Savepoints)**
```sql
SAVEPOINT savepoint_name;
-- ...
ROLLBACK TO SAVEPOINT savepoint_name;
```

**Пример:**
```sql
BEGIN;
    INSERT INTO employees (first_name, last_name) VALUES ('Иван', 'Иванов');
    SAVEPOINT before_update;
    UPDATE employees SET first_name = 'Петр' WHERE last_name = 'Иванов';
    -- Откат к точке сохранения
    ROLLBACK TO SAVEPOINT before_update;
COMMIT;
```

---

### **42.5. Уровни изоляции транзакций**
```sql
SET TRANSACTION ISOLATION LEVEL {READ COMMITTED | REPEATABLE READ | SERIALIZABLE};
```

**Пример:**
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- ...
COMMIT;
```

---

### **42.6. Блокировки**
```sql
-- Блокировка строки для обновления
SELECT * FROM table_name WHERE condition FOR UPDATE;

-- Блокировка строки для совместного доступа
SELECT * FROM table_name WHERE condition FOR SHARE;
```

**Пример:**
```sql
BEGIN;
SELECT * FROM accounts WHERE account_id = 1 FOR UPDATE;
-- ...
COMMIT;
```

---

## **43. Работа с репликацией**

PostgreSQL поддерживает различные виды репликации для обеспечения отказоустойчивости.

---

### **43.1. Настройка потоковой репликации (Streaming Replication)**

1. **Настройка основного сервера (`postgresql.conf`)**:
   ```ini
   wal_level = replica
   max_wal_senders = 3
   wal_keep_segments = 8
   ```

2. **Настройка аутентификации (`pg_hba.conf`)**:
   ```ini
   host    replication     replica_user     192.168.1.0/24    md5
   ```

3. **Создание пользователя для репликации**:
   ```sql
   CREATE ROLE replica_user WITH REPLICATION LOGIN PASSWORD 'replica_password';
   ```

4. **Настройка резервного сервера (`recovery.conf`)**:
   ```ini
   standby_mode = 'on'
   primary_conninfo = 'host=primary_server port=5432 user=replica_user password=replica_password'
   trigger_file = '/tmp/postgresql.trigger'
   ```

---

### **43.2. Настройка логической репликации (Logical Replication)**

1. **Настройка основного сервера (`postgresql.conf`)**:
   ```ini
   wal_level = logical
   ```

2. **Создание публикации**:
   ```sql
   CREATE PUBLICATION my_publication FOR TABLE table1, table2;
   ```

3. **Настройка резервного сервера**:
   ```sql
   CREATE SUBSCRIPTION my_subscription
   CONNECTION 'host=primary_server port=5432 dbname=db_name user=replica_user password=replica_password'
   PUBLICATION my_publication;
   ```

---

## **44. Работа с резервным копированием и восстановлением**

---

### **44.1. Создание резервной копии с помощью `pg_dump`**
```bash
pg_dump -U username -d dbname -f backup.sql
```

**Пример:**
```bash
pg_dump -U postgres -d my_database -f my_database_backup.sql
```

---

### **44.2. Восстановление из резервной копии с помощью `psql`**
```bash
psql -U username -d dbname -f backup.sql
```

**Пример:**
```bash
psql -U postgres -d my_database -f my_database_backup.sql
```

---

### **44.3. Создание бинарной резервной копии с помощью `pg_basebackup`**
```bash
pg_basebackup -D /path/to/backup -U replica_user -P -v -Ft -z -Xs
```

---

### **44.4. Восстановление из бинарной резервной копии**
1. Остановите PostgreSQL.
2. Скопируйте данные из резервной копии в каталог данных PostgreSQL.
3. Запустите PostgreSQL.

---

## **45. Работа с мониторингом и производительностью**

---

### **45.1. Просмотр активных соединений**
```sql
SELECT * FROM pg_stat_activity;
```

---

### **45.2. Просмотр статистики таблиц**
```sql
SELECT * FROM pg_stat_user_tables;
```

---

### **45.3. Просмотр статистики индексов**
```sql
SELECT * FROM pg_stat_user_indexes;
```

---

### **45.4. Анализ производительности запросов**
```sql
EXPLAIN ANALYZE SELECT * FROM table_name WHERE condition;
```

---

### **45.5. Просмотр блокировок**
```sql
SELECT * FROM pg_locks;
```

---

### **45.6. Просмотр настроек PostgreSQL**
```sql
SHOW parameter_name;
```

**Пример:**
```sql
SHOW shared_buffers;
SHOW work_mem;
```

---

### **45.7. Изменение настроек PostgreSQL**
```sql
ALTER SYSTEM SET parameter_name = value;
```

**Пример:**
```sql
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET work_mem = '16MB';
```

---

## **46. Работа с расширением `pg_partman` для управления разделами**

`pg_partman` — это расширение для автоматического управления разделами.

---

### **46.1. Установка расширения**
```sql
CREATE EXTENSION pg_partman;
```

---

### **46.2. Создание разделённой таблицы**
```sql
CREATE TABLE table_name (
    ...
) PARTITION BY RANGE (column_name);

SELECT create_parent('schema_name.table_name', 'column_name', 'prefix', 'interval');
```

**Пример:**
```sql
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (sale_date);

SELECT create_parent('public.sales', 'sale_date', 'sales_', 'monthly');
```

---

### **46.3. Добавление нового раздела**
```sql
SELECT create_time_partition('interval', 'timestamp');
```

**Пример:**
```sql
SELECT create_time_partition('2023-01-01', '2023-02-01');
```

---

### **46.4. Удаление старого раздела**
```sql
SELECT drop_partition_time('timestamp');
```

**Пример:**
```sql
SELECT drop_partition_time('2022-01-01');
```

---

### **46.5. Настройка автоматического управления разделами**
```sql
SELECT run_maintenance();
```

---

## **47. Работа с расширением `pg_stat_statements` для анализа запросов**

`pg_stat_statements` позволяет собирать статистику по выполняемым запросам.

---

### **47.1. Установка расширения**
```sql
CREATE EXTENSION pg_stat_statements;
```

---

### **47.2. Просмотр статистики запросов**
```sql
SELECT * FROM pg_stat_statements;
```

**Пример:**
```sql
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

---

### **47.3. Сброс статистики**
```sql
SELECT pg_stat_statements_reset();
```

---

## **48. Работа с расширением `pg_repack` для дефрагментации таблиц**

`pg_repack` позволяет дефрагментировать таблицы и индексы без блокировки.

---

### **48.1. Установка расширения**
```bash
sudo apt-get install postgresql-14-repack
```

---

### **48.2. Дефрагментация таблицы**
```bash
pg_repack -d dbname -t table_name
```

**Пример:**
```bash
pg_repack -d my_database -t employees
```

---

### **48.3. Дефрагментация всех таблиц в базе данных**
```bash
pg_repack -d dbname
```

---

## **49. Работа с расширением `pgAudit` для аудита**

`pgAudit` позволяет вести журнал аудита для отслеживания изменений в базе данных.

---

### **49.1. Установка расширения**
```sql
CREATE EXTENSION pgaudit;
```

---

### **49.2. Настройка аудита в `postgresql.conf`**
```ini
pgaudit.log = 'all'
pgaudit.log_catalog = on
```

---

### **49.3. Просмотр журнала аудита**
```sql
SELECT * FROM pgaudit.log;
```

---

## **50. Работа с расширением `PostGIS` для геопространственных данных**

`PostGIS` добавляет поддержку геопространственных данных.

---

### **50.1. Установка расширения**
```sql
CREATE EXTENSION postgis;
```

---

### **50.2. Создание таблицы с геометрическими данными**
```sql
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(Point, 4326)
);
```

---

### **50.3. Вставка геометрических данных**
```sql
INSERT INTO locations (name, geom)
VALUES ('Москва', ST_GeomFromText('POINT(37.6176 55.7558)', 4326));
```

---

### **50.4. Запрос геометрических данных**
```sql
SELECT ST_AsText(geom) FROM locations;
SELECT ST_Distance(geom1, geom2) FROM locations;
```

**Пример:**
```sql
-- Поиск объектов в радиусе 10 км от Москвы
SELECT name FROM locations
WHERE ST_DWithin(
    geom,
    ST_GeomFromText('POINT(37.6176 55.7558)', 4326),
    10000
);
```

---

### **50.5. Создание пространственного индекса**
```sql
CREATE INDEX index_name ON table_name USING GIST (geom);
```

**Пример:**
```sql
CREATE INDEX idx_locations_geom ON locations USING GIST (geom);
```

---

## **51. Работа с расширением `pg_cron` для планирования задач**

`pg_cron` позволяет запускать SQL-запросы по расписанию.

---

### **51.1. Установка расширения**
```sql
CREATE EXTENSION pg_cron;
```

---

### **51.2. Добавление задачи в расписание**
```sql
SELECT cron.schedule('job_name', 'schedule', 'SQL_command');
```

**Пример:**
```sql
SELECT cron.schedule('nightly-vacuum', '0 3 * * *', 'VACUUM ANALYZE');
```

---

### **51.3. Просмотр запланированных задач**
```sql
SELECT * FROM cron.job;
```

---

### **51.4. Удаление задачи из расписания**
```sql
SELECT cron.unschedule(job_name);
```

**Пример:**
```sql
SELECT cron.unschedule('nightly-vacuum');
```

---

## **52. Работа с расширением `uuid-ossp` для генерации UUID**

`uuid-ossp` предоставляет функции для генерации UUID.

---

### **52.1. Установка расширения**
```sql
CREATE EXTENSION "uuid-ossp";
```

---

### **52.2. Генерация UUID**
```sql
SELECT uuid_generate_v4();
```

**Пример:**
```sql
INSERT INTO users (user_id, name)
VALUES (uuid_generate_v4(), 'Иван');
```

---

## **53. Работа с расширением `hstore` для хранения пар "ключ-значение"**

`hstore` позволяет хранить пары "ключ-значение" в одном поле.

---

### **53.1. Установка расширения**
```sql
CREATE EXTENSION hstore;
```

---

### **53.2. Создание таблицы с полем `hstore`**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    attributes HSTORE
);
```

---

### **53.3. Вставка данных в `hstore`**
```sql
INSERT INTO products (attributes)
VALUES ('color => "red", size => "large"');
```

---

### **53.4. Запрос данных из `hstore`**
```sql
SELECT attributes->'color' FROM products;
SELECT * FROM products WHERE attributes->'color' = 'red';
```

---

### **53.5. Обновление данных в `hstore`**
```sql
UPDATE products
SET attributes = attributes || 'weight => "1kg"'
WHERE product_id = 1;
```

---

### **53.6. Создание индекса для `hstore`**
```sql
CREATE INDEX index_name ON table_name USING GIN (hstore_column);
```

**Пример:**
```sql
CREATE INDEX idx_products_attributes ON products USING GIN (attributes);
```

---

## **54. Работа с расширением `citext` для регистронезависимого сравнения строк**

`citext` позволяет сравнивать строки без учёта регистра.

---

### **54.1. Установка расширения**
```sql
CREATE EXTENSION citext;
```

---

### **54.2. Создание таблицы с полем `citext`**
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email CITEXT UNIQUE
);
```

---

### **54.3. Вставка данных в `citext`**
```sql
INSERT INTO users (email) VALUES ('User@example.com');
```

---

### **54.4. Запрос данных из `citext`**
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

---

### **54.5. Создание индекса для `citext`**
```sql
CREATE INDEX index_name ON table_name (citext_column);
```

**Пример:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

---

## **55. Работа с расширением `pg_trgm` для нечёткого поиска**

`pg_trgm` позволяет выполнять нечёткий поиск и сравнение строк на основе триграмм.

---

### **55.1. Установка расширения**
```sql
CREATE EXTENSION pg_trgm;
```

---

### **55.2. Создание индекса для нечёткого поиска**
```sql
CREATE INDEX index_name ON table_name USING GIN (column_name gin_trgm_ops);
```

**Пример:**
```sql
CREATE INDEX idx_products_name_trgm ON products USING GIN (name gin_trgm_ops);
```

---

### **55.3. Поиск похожих строк**
```sql
SELECT * FROM table_name
WHERE column_name % 'search_string';
```

**Пример:**
```sql
SELECT * FROM products
WHERE name % 'ноутбук';
```

---

### **55.4. Оценка схожести строк**
```sql
SELECT similarity(column_name, 'search_string') FROM table_name;
```

**Пример:**
```sql
SELECT name, similarity(name, 'ноутбук') AS similarity
FROM products
ORDER BY similarity DESC;
```

---

## **56. Работа с расширением `tablefunc` для работы с таблицами**

`tablefunc` предоставляет функции для работы с таблицами.

---

### **56.1. Установка расширения**
```sql
CREATE EXTENSION tablefunc;
```

---

### **56.2. Использование функции `crosstab`**
```sql
SELECT * FROM crosstab(
    'SQL_query',
    'SQL_query_for_categories'
) AS ct (row_name type, category1 type, category2 type, ...);
```

**Пример:**
```sql
SELECT * FROM crosstab(
    'SELECT department_id, job_title, COUNT(*)
     FROM employees
     GROUP BY 1, 2
     ORDER BY 1, 2',
    'SELECT DISTINCT job_title FROM employees ORDER BY 1'
) AS ct (department_id INTEGER, "Manager" INTEGER, "Developer" INTEGER, "Analyst" INTEGER);
```

---

## **57. Работа с расширением `pg_buffercache` для анализа кэша**

`pg_buffercache` позволяет анализировать содержимое кэша PostgreSQL.

---

### **57.1. Установка расширения**
```sql
CREATE EXTENSION pg_buffercache;
```

---

### **57.2. Просмотр содержимого кэша**
```sql
SELECT * FROM pg_buffercache;
```

**Пример:**
```sql
SELECT c.relname, count(*) AS buffers
FROM pg_class c
JOIN pg_buffercache b ON b.relfilenode = c.relfilenode
GROUP BY c.relname
ORDER BY buffers DESC;
```

---

## **58. Работа с расширением `pg_prewarm` для предварительной загрузки данных в кэш**

`pg_prewarm` позволяет загружать данные в кэш заранее.

---

### **58.1. Установка расширения**
```sql
CREATE EXTENSION pg_prewarm;
```

---

### **58.2. Предварительная загрузка таблицы в кэш**
```sql
SELECT pg_prewarm('schema_name.table_name');
```

**Пример:**
```sql
SELECT pg_prewarm('public.employees');
```

---

## **59. Работа с расширением `pg_visibility` для анализа видимости строк**

`pg_visibility` позволяет анализировать видимость строк в таблицах.

---

### **59.1. Установка расширения**
```sql
CREATE EXTENSION pg_visibility;
```

---

### **59.2. Просмотр статистики видимости строк**
```sql
SELECT * FROM pg_visibility('schema_name.table_name');
```

**Пример:**
```sql
SELECT * FROM pg_visibility('public.employees');
```

---

## **60. Работа с расширением `pg_freespacemap` для анализа свободного пространства**

`pg_freespacemap` позволяет анализировать свободное пространство в таблицах.

---

### **60.1. Установка расширения**
```sql
CREATE EXTENSION pg_freespacemap;
```

---

### **60.2. Просмотр информации о свободном пространстве**
```sql
SELECT * FROM pg_freespace('schema_name.table_name');
```

**Пример:**
```sql
SELECT * FROM pg_freespace('public.employees');
```

---

## **61. Работа с расширением `pgrowlocks` для анализа блокировок строк**

`pgrowlocks` позволяет анализировать блокировки на уровне строк.

---

### **61.1. Установка расширения**
```sql
CREATE EXTENSION pgrowlocks;
```

---

### **61.2. Просмотр блокировок строк**
```sql
SELECT * FROM pgrowlocks('schema_name.table_name');
```

**Пример:**
```sql
SELECT * FROM pgrowlocks('public.employees');
```

---

## **62. Работа с расширением `pg_stat_kcache` для анализа использования кэша ядра**

`pg_stat_kcache` позволяет анализировать использование кэша ядра.

---

### **62.1. Установка расширения**
```sql
CREATE EXTENSION pg_stat_kcache;
```

---

### **62.2. Просмотр статистики использования кэша**
```sql
SELECT * FROM pg_stat_kcache;
```

---

## **63. Работа с расширением `pg_wait_sampling` для анализа ожиданий**

`pg_wait_sampling` позволяет анализировать, на чем тратится время ожидания в PostgreSQL.

---

### **63.1. Установка расширения**
```sql
CREATE EXTENSION pg_wait_sampling;
```

---

### **63.2. Запуск сбора статистики ожиданий**
```sql
SELECT pg_wait_sampling_start();
```

---

### **63.3. Просмотр статистики ожиданий**
```sql
SELECT * FROM pg_wait_sampling_get_samples();
```

---

### **63.4. Остановка сбора статистики ожиданий**
```sql
SELECT pg_wait_sampling_stop();
```

---

## **64. Работа с расширением `hypopg` для гипотетических индексов**

`hypopg` позволяет создавать гипотетические индексы для оценки их эффективности без реального создания.

---

### **64.1. Установка расширения**
```sql
CREATE EXTENSION hypopg;
```

---

### **64.2. Создание гипотетического индекса**
```sql
SELECT * FROM hypopg_create_index('CREATE INDEX ON table_name (column_name)');
```

**Пример:**
```sql
SELECT * FROM hypopg_create_index('CREATE INDEX ON employees (last_name)');
```

---

### **64.3. Проверка использования гипотетического индекса**
```sql
EXPLAIN SELECT * FROM table_name WHERE condition;
```

---

### **64.4. Удаление гипотетического индекса**
```sql
SELECT * FROM hypopg_drop_index(index_oid);
```

---

## **65. Работа с расширением `pgqualstats` для анализа условий в запросах**

`pgqualstats` собирает статистику по условиям в запросах.

---

### **65.1. Установка расширения**
```sql
CREATE EXTENSION pgqualstats;
```

---

### **65.2. Просмотр статистики условий**
```sql
SELECT * FROM pgqualstats.pg_qualstats;
```

---

## **66. Работа с расширением `pg_track_settings` для отслеживания изменений настроек**

`pg_track_settings` позволяет отслеживать изменения настроек PostgreSQL.

---

### **66.1. Установка расширения**
```sql
CREATE EXTENSION pg_track_settings;
```

---

### **66.2. Просмотр истории изменений настроек**
```sql
SELECT * FROM pg_track_settings_history;
```

---

## **67. Работа с расширением `wal2json` для логической репликации**

`wal2json` позволяет преобразовывать WAL (Write-Ahead Log) в формат JSON для логической репликации.

---

### **67.1. Установка расширения**
```sql
CREATE EXTENSION wal2json;
```

---

### **67.2. Настройка логической репликации с использованием `wal2json`**
```ini
# В postgresql.conf
wal_level = logical
```

---

## **68. Работа с расширением `pg_jieba` для китайской сегментации текста**

`pg_jieba` предоставляет функции для сегментации китайского текста.

---

### **68.1. Установка расширения**
```sql
CREATE EXTENSION pg_jieba;
```

---

### **68.2. Сегментация китайского текста**
```sql
SELECT jieba_segment('中文文本');
```

---

## **69. Работа с расширением `pg_similarity` для сравнения строк**

`pg_similarity` предоставляет функции для сравнения строк на основе различных алгоритмов.

---

### **69.1. Установка расширения**
```sql
CREATE EXTENSION pg_similarity;
```

---

### **69.2. Сравнение строк**
```sql
SELECT similarity('string1', 'string2');
SELECT levenshtein('string1', 'string2');
```

**Пример:**
```sql
SELECT similarity('PostgreSQL', 'Postgres');
```

---

## **70. Работа с расширением `pgTAP` для тестирования**

`pgTAP` позволяет писать тесты для PostgreSQL на языке TAP.

---

### **70.1. Установка расширения**
```sql
CREATE EXTENSION pgtap;
```

---

### **70.2. Написание тестов**
```sql
BEGIN;
SELECT plan(1);
SELECT is(1, 1, '1 equals 1');
SELECT * FROM finish();
ROLLBACK;
```

---

## **71. Работа с расширением `pgMemCache` для кэширования**

`pgMemCache` позволяет кэшировать данные в памяти.

---

### **71.1. Установка расширения**
```sql
CREATE EXTENSION pgmemcache;
```

---

### **71.2. Использование кэша**
```sql
SELECT memcache_set('key', 'value');
SELECT memcache_get('key');
```

**Пример:**
```sql
SELECT memcache_set('user_1', 'Иван');
SELECT memcache_get('user_1');
```

---

## **72. Работа с расширением `pg_bigm` для полнотекстового поиска на японском языке**

`pg_bigm` предоставляет функции для полнотекстового поиска на японском языке.

---

### **72.1. Установка расширения**
```sql
CREATE EXTENSION pg_bigm;
```

---

### **72.2. Создание индекса для японского текста**
```sql
CREATE INDEX index_name ON table_name USING GIN (column_name pg_bigm_ops);
```

---

## **73. Работа с расширением `pg_roaringbitmap` для работы с битовыми картами**

`pg_roaringbitmap` предоставляет функции для работы с битовыми картами.

---

### **73.1. Установка расширения**
```sql
CREATE EXTENSION pg_roaringbitmap;
```

---

### **73.2. Использование битовых карт**
```sql
SELECT bitmap_create(ARRAY[1, 2, 3]);
```

---

## **74. Работа с расширением `pg_partman` для управления разделами**

`pg_partman` автоматизирует управление разделами.

---

### **74.1. Установка расширения**
```sql
CREATE EXTENSION pg_partman;
```

---

### **74.2. Создание разделённой таблицы**
```sql
CREATE TABLE table_name (
    ...
) PARTITION BY RANGE (column_name);

SELECT create_parent('schema_name.table_name', 'column_name', 'prefix', 'interval');
```

**Пример:**
```sql
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (sale_date);

SELECT create_parent('public.sales', 'sale_date', 'sales_', 'monthly');
```

---

### **74.3. Добавление нового раздела**
```sql
SELECT create_time_partition('interval', 'timestamp');
```

**Пример:**
```sql
SELECT create_time_partition('2023-01-01', '2023-02-01');
```

---

### **74.4. Удаление старого раздела**
```sql
SELECT drop_partition_time('timestamp');
```

**Пример:**
```sql
SELECT drop_partition_time('2022-01-01');
```

---

### **74.5. Настройка автоматического управления разделами**
```sql
SELECT run_maintenance();
```

---

## **75. Работа с расширением `timescaledb` для временных рядов**

`TimescaleDB` расширяет PostgreSQL для работы с временными рядами.

---

### **75.1. Установка расширения**
```sql
CREATE EXTENSION timescaledb;
```

---

### **75.2. Создание гипертаблицы**
```sql
SELECT create_hypertable('table_name', 'time_column');
```

**Пример:**
```sql
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id INTEGER,
    value DOUBLE PRECISION
);

SELECT create_hypertable('metrics', 'time');
```

---

### **75.3. Добавление данных в гипертаблицу**
```sql
INSERT INTO metrics (time, device_id, value)
VALUES (NOW(), 1, 42.5);
```

---

### **75.4. Запрос данных из гипертаблицы**
```sql
SELECT * FROM metrics WHERE time > NOW() - INTERVAL '1 day';
```

---

### **75.5. Создание непрерывных агрегатов**
```sql
SELECT create_continuous_aggregate(
    'view_name',
    'time_bucket_interval',
    'table_name',
    'time_column',
    'aggregate_column'
);
```

**Пример:**
```sql
SELECT create_continuous_aggregate(
    'metrics_daily_avg',
    '1 day',
    'metrics',
    'time',
    'AVG(value)'
);
```

---

### **75.6. Обновление непрерывных агрегатов**
```sql
SELECT refresh_continuous_aggregate('view_name', 'start_time', 'end_time');
```

**Пример:**
```sql
SELECT refresh_continuous_aggregate('metrics_daily_avg', NULL, NULL);
```

---

## **76. Работа с расширением `pg_graphql` для GraphQL**

`pg_graphql` позволяет выполнять GraphQL-запросы к PostgreSQL.

---

### **76.1. Установка расширения**
```sql
CREATE EXTENSION pg_graphql;
```

---

### **76.2. Выполнение GraphQL-запросов**
```sql
SELECT graphql('query { users { id name } }');
```

---

## **77. Работа с расширением `pg_net` для работы с сетями**

`pg_net` предоставляет функции для работы с сетями.

---

### **77.1. Установка расширения**
```sql
CREATE EXTENSION pg_net;
```

---

### **77.2. Использование сетевых функций**
```sql
SELECT ip4_in_cidr('192.168.1.1', '192.168.1.0/24');
```

---

## **78. Работа с расширением `pg_qualstats` для анализа условий в запросах**

`pg_qualstats` собирает статистику по условиям в запросах.

---

### **78.1. Установка расширения**
```sql
CREATE EXTENSION pgqualstats;
```

---

### **78.2. Просмотр статистики условий**
```sql
SELECT * FROM pgqualstats.pg_qualstats;
```

---

## **79. Работа с расширением `pg_stat_monitor` для мониторинга запросов**

`pg_stat_monitor` предоставляет расширенные возможности мониторинга запросов.

---

### **79.1. Установка расширения**
```sql
CREATE EXTENSION pg_stat_monitor;
```

---

### **79.2. Просмотр статистики запросов**
```sql
SELECT * FROM pg_stat_monitor;
```

---

## **80. Работа с расширением `pg_walinspect` для анализа WAL**

`pg_walinspect` позволяет анализировать содержимое WAL (Write-Ahead Log).

---

### **80.1. Установка расширения**
```sql
CREATE EXTENSION pg_walinspect;
```

---

### **80.2. Просмотр информации из WAL**
```sql
SELECT * FROM pg_walinspect_lsn_range('lsn_start', 'lsn_end');
```

---

## **81. Работа с расширением `pg_hint_plan` для управления планами выполнения**

`pg_hint_plan` позволяет управлять планами выполнения запросов с помощью hint-ов.

---

### **81.1. Установка расширения**
```sql
CREATE EXTENSION pg_hint_plan;
```

---

### **81.2. Использование hint-ов в запросах**
```sql
SELECT /*+ SeqScan(table_name) */ * FROM table_name;
```

**Пример:**
```sql
SELECT /*+ IndexScan(employees idx_employees_last_name) */ *
FROM employees
WHERE last_name = 'Иванов';
```

---

### **81.3. Настройка hint-ов на уровне базы данных**
```sql
SET pg_hint_plan.enable_hint = on;
SET pg_hint_plan.message_level = log;
```

---

## **82. Работа с расширением `pg_visibility` для анализа видимости строк**

`pg_visibility` позволяет анализировать видимость строк в таблицах.

---

### **82.1. Установка расширения**
```sql
CREATE EXTENSION pg_visibility;
```

---

### **82.2. Просмотр статистики видимости строк**
```sql
SELECT * FROM pg_visibility('schema_name.table_name');
```

**Пример:**
```sql
SELECT * FROM pg_visibility('public.employees');
```

---

## **83. Работа с расширением `pg_freespacemap` для анализа свободного пространства**

`pg_freespacemap` позволяет анализировать свободное пространство в таблицах.

---

### **83.1. Установка расширения**
```sql
CREATE EXTENSION pg_freespacemap;
```

---

### **83.2. Просмотр информации о свободном пространстве**
```sql
SELECT * FROM pg_freespace('schema_name.table_name');
```

**Пример:**
```sql
SELECT * FROM pg_freespace('public.employees');
```

---

## **84. Работа с расширением `pgrowlocks` для анализа блокировок строк**

`pgrowlocks` позволяет анализировать блокировки на уровне строк.

---

### **84.1. Установка расширения**
```sql
CREATE EXTENSION pgrowlocks;
```

---

### **84.2. Просмотр блокировок строк**
```sql
SELECT * FROM pgrowlocks('schema_name.table_name');
```

**Пример:**
```sql
SELECT * FROM pgrowlocks('public.employees');
```

---

## **85. Работа с расширением `pg_stat_kcache` для анализа использования кэша ядра**

`pg_stat_kcache` позволяет анализировать использование кэша ядра.

---

### **85.1. Установка расширения**
```sql
CREATE EXTENSION pg_stat_kcache;
```

---

### **85.2. Просмотр статистики использования кэша**
```sql
SELECT * FROM pg_stat_kcache;
```

---

## **86. Работа с расширением `pg_wait_sampling` для анализа ожиданий**

`pg_wait_sampling` позволяет анализировать, на чем тратится время ожидания в PostgreSQL.

---

### **86.1. Установка расширения**
```sql
CREATE EXTENSION pg_wait_sampling;
```

---

### **86.2. Запуск сбора статистики ожиданий**
```sql
SELECT pg_wait_sampling_start();
```

---

### **86.3. Просмотр статистики ожиданий**
```sql
SELECT * FROM pg_wait_sampling_get_samples();
```

---

### **86.4. Остановка сбора статистики ожиданий**
```sql
SELECT pg_wait_sampling_stop();
```

---

## **87. Работа с расширением `hypopg` для гипотетических индексов**

`hypopg` позволяет создавать гипотетические индексы для оценки их эффективности.

---

### **87.1. Установка расширения**
```sql
CREATE EXTENSION hypopg;
```

---

### **87.2. Создание гипотетического индекса**
```sql
SELECT * FROM hypopg_create_index('CREATE INDEX ON table_name (column_name)');
```

**Пример:**
```sql
SELECT * FROM hypopg_create_index('CREATE INDEX ON employees (last_name)');
```

---

### **87.3. Проверка использования гипотетического индекса**
```sql
EXPLAIN SELECT * FROM table_name WHERE condition;
```

---

### **87.4. Удаление гипотетического индекса**
```sql
SELECT * FROM hypopg_drop_index(index_oid);
```

---

## **88. Работа с расширением `pgqualstats` для анализа условий в запросах**

`pgqualstats` собирает статистику по условиям в запросах.

---

### **88.1. Установка расширения**
```sql
CREATE EXTENSION pgqualstats;
```

---

### **88.2. Просмотр статистики условий**
```sql
SELECT * FROM pgqualstats.pg_qualstats;
```

---

## **89. Работа с расширением `pg_track_settings` для отслеживания изменений настроек**

`pg_track_settings` позволяет отслеживать изменения настроек PostgreSQL.

---

### **89.1. Установка расширения**
```sql
CREATE EXTENSION pg_track_settings;
```

---

### **89.2. Просмотр истории изменений настроек**
```sql
SELECT * FROM pg_track_settings_history;
```

---

## **90. Работа с расширением `wal2json` для логической репликации**

`wal2json` позволяет преобразовывать WAL в формат JSON для логической репликации.

---

### **90.1. Установка расширения**
```sql
CREATE EXTENSION wal2json;
```

---

### **90.2. Настройка логической репликации с использованием `wal2json`**
```ini
# В postgresql.conf
wal_level = logical
```

---

## **91. Работа с расширением `pg_jieba` для китайской сегментации текста**

`pg_jieba` предоставляет функции для сегментации китайского текста.

---

### **91.1. Установка расширения**
```sql
CREATE EXTENSION pg_jieba;
```

---

### **91.2. Сегментация китайского текста**
```sql
SELECT jieba_segment('中文文本');
```

---

## **92. Работа с расширением `pg_similarity` для сравнения строк**

`pg_similarity` предоставляет функции для сравнения строк.

---

### **92.1. Установка расширения**
```sql
CREATE EXTENSION pg_similarity;
```

---

### **92.2. Сравнение строк**
```sql
SELECT similarity('string1', 'string2');
SELECT levenshtein('string1', 'string2');
```

**Пример:**
```sql
SELECT similarity('PostgreSQL', 'Postgres');
```

---

## **93. Работа с расширением `pgTAP` для тестирования**

`pgTAP` позволяет писать тесты для PostgreSQL.

---

### **93.1. Установка расширения**
```sql
CREATE EXTENSION pgtap;
```

---

### **93.2. Написание тестов**
```sql
BEGIN;
SELECT plan(1);
SELECT is(1, 1, '1 equals 1');
SELECT * FROM finish();
ROLLBACK;
```

---

## **94. Работа с расширением `pgMemCache` для кэширования**

`pgMemCache` позволяет кэшировать данные в памяти.

---

### **94.1. Установка расширения**
```sql
CREATE EXTENSION pgmemcache;
```

---

### **94.2. Использование кэша**
```sql
SELECT memcache_set('key', 'value');
SELECT memcache_get('key');
```

**Пример:**
```sql
SELECT memcache_set('user_1', 'Иван');
SELECT memcache_get('user_1');
```

---

## **95. Работа с расширением `pg_bigm` для полнотекстового поиска на японском языке**

`pg_bigm` предоставляет функции для полнотекстового поиска на японском языке.

---

### **95.1. Установка расширения**
```sql
CREATE EXTENSION pg_bigm;
```

---

### **95.2. Создание индекса для японского текста**
```sql
CREATE INDEX index_name ON table_name USING GIN (column_name pg_bigm_ops);
```

---

## **96. Работа с расширением `pg_roaringbitmap` для работы с битовыми картами**

`pg_roaringbitmap` предоставляет функции для работы с битовыми картами.

---

### **96.1. Установка расширения**
```sql
CREATE EXTENSION pg_roaringbitmap;
```

---

### **96.2. Использование битовых карт**
```sql
SELECT bitmap_create(ARRAY[1, 2, 3]);
```

---

## **97. Работа с расширением `pg_partman` для управления разделами**

`pg_partman` автоматизирует управление разделами.

---

### **97.1. Установка расширения**
```sql
CREATE EXTENSION pg_partman;
```

---

### **97.2. Создание разделённой таблицы**
```sql
CREATE TABLE table_name (
    ...
) PARTITION BY RANGE (column_name);

SELECT create_parent('schema_name.table_name', 'column_name', 'prefix', 'interval');
```

**Пример:**
```sql
CREATE TABLE sales (
    sale_id SERIAL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (sale_date);

SELECT create_parent('public.sales', 'sale_date', 'sales_', 'monthly');
```

---

### **97.3. Добавление нового раздела**
```sql
SELECT create_time_partition('interval', 'timestamp');
```

**Пример:**
```sql
SELECT create_time_partition('2023-01-01', '2023-02-01');
```

---

### **97.4. Удаление старого раздела**
```sql
SELECT drop_partition_time('timestamp');
```

**Пример:**
```sql
SELECT drop_partition_time('2022-01-01');
```

---

### **97.5. Настройка автоматического управления разделами**
```sql
SELECT run_maintenance();
```

---

## **98. Работа с расширением `timescaledb` для временных рядов**

`TimescaleDB` расширяет PostgreSQL для работы с временными рядами.

---

### **98.1. Установка расширения**
```sql
CREATE EXTENSION timescaledb;
```

---

### **98.2. Создание гипертаблицы**
```sql
SELECT create_hypertable('table_name', 'time_column');
```

**Пример:**
```sql
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id INTEGER,
    value DOUBLE PRECISION
);

SELECT create_hypertable('metrics', 'time');
```

---

### **98.3. Добавление данных в гипертаблицу**
```sql
INSERT INTO metrics (time, device_id, value)
VALUES (NOW(), 1, 42.5);
```

---

### **98.4. Запрос данных из гипертаблицы**
```sql
SELECT * FROM metrics WHERE time > NOW() - INTERVAL '1 day';
```

---

### **98.5. Создание непрерывных агрегатов**
```sql
SELECT create_continuous_aggregate(
    'view_name',
    'time_bucket_interval',
    'table_name',
    'time_column',
    'aggregate_column'
);
```

**Пример:**
```sql
SELECT create_continuous_aggregate(
    'metrics_daily_avg',
    '1 day',
    'metrics',
    'time',
    'AVG(value)'
);
```

---

### **98.6. Обновление непрерывных агрегатов**
```sql
SELECT refresh_continuous_aggregate('view_name', 'start_time', 'end_time');
```

**Пример:**
```sql
SELECT refresh_continuous_aggregate('metrics_daily_avg', NULL, NULL);
```

---

## **99. Работа с расширением `pg_graphql` для GraphQL**

`pg_graphql` позволяет выполнять GraphQL-запросы к PostgreSQL.

---

### **99.1. Установка расширения**
```sql
CREATE EXTENSION pg_graphql;
```

---

### **99.2. Выполнение GraphQL-запросов**
```sql
SELECT graphql('query { users { id name } }');
```

---

## **100. Работа с расширением `pg_net` для работы с сетями**

`pg_net` предоставляет функции для работы с сетями.

---

### **100.1. Установка расширения**
```sql
CREATE EXTENSION pg_net;
```

---

### **100.2. Использование сетевых функций**
```sql
SELECT ip4_in_cidr('192.168.1.1', '192.168.1.0/24');
```

---