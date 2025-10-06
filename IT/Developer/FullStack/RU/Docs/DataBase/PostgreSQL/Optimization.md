# Часть 1

### 1. **Индексы: Добавление индекса для ускорения поиска**

#### Неоптимизированный запрос
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```
Если на поле `email` нет индекса, PostgreSQL выполнит полное сканирование таблицы (`Seq Scan`), что может быть медленно для больших таблиц.

#### Оптимизированный запрос
```sql
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
```
**Объяснение:**
Создание индекса на поле `email` позволяет PostgreSQL использовать индексное сканирование (`Index Scan`), что значительно ускоряет поиск по этому полю.

---

### 2. **Сортировки: Оптимизация сортировки с помощью индексов**

#### Неоптимизированный запрос
```sql
SELECT * FROM orders ORDER BY created_at DESC;
```
Если на поле `created_at` нет индекса, PostgreSQL выполнит сортировку на лету (`Sort`), что может быть ресурсоёмко.

#### Оптимизированный запрос
```sql
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
SELECT * FROM orders ORDER BY created_at DESC;
```
**Объяснение:**
Создание индекса с указанием порядка сортировки (`DESC`) позволяет PostgreSQL использовать индекс для сортировки, избегая дополнительных затрат на сортировку данных.

---

### 3. **Блокировки: Избегание избыточных блокировок**

#### Неоптимизированный запрос
```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- Долгая обработка данных...
COMMIT;
```
Если транзакция долго удерживает блокировку, это может привести к блокировкам других транзакций.

#### Оптимизированный запрос
```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR NO KEY UPDATE;
-- Быстрая обработка данных...
COMMIT;
```
**Объяснение:**
Использование `FOR NO KEY UPDATE` вместо `FOR UPDATE` позволяет уменьшить уровень блокировки, если не требуется блокировка ключей.

---

### 4. **Порядок полей: Оптимизация порядка полей в индексах**

#### Неоптимизированный запрос
```sql
CREATE INDEX idx_users_name_age ON users(name, age);
SELECT * FROM users WHERE age = 30;
```
Индекс по полям `(name, age)` неэффективен для запросов только по `age`.

#### Оптимизированный запрос
```sql
CREATE INDEX idx_users_age_name ON users(age, name);
SELECT * FROM users WHERE age = 30;
```
**Объяснение:**
Порядок полей в индексе важен. Если часто выполняются запросы по `age`, то это поле должно быть первым в индексе.

---

### 5. **Использование `EXPLAIN PLAN` для анализа запросов**

#### Пример анализа неоптимизированного запроса
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 100 ORDER BY created_at DESC;
```
**Результат:**
```
Sort (cost=1000.00..1001.00 rows=400 width=36) (actual time=10.000..10.001 rows=400 loops=1)
  Sort Key: created_at DESC
  -> Seq Scan on orders (cost=0.00..990.00 rows=400 width=36) (actual time=0.001..5.000 rows=400 loops=1)
        Filter: (user_id = 100)
```
Здесь видно, что выполняется полное сканирование таблицы (`Seq Scan`) и сортировка (`Sort`).

#### Оптимизированный запрос с анализом
```sql
CREATE INDEX idx_orders_user_id_created_at ON orders(user_id, created_at DESC);
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 100 ORDER BY created_at DESC;
```
**Результат:**
```
Index Scan using idx_orders_user_id_created_at on orders (cost=0.15..8.17 rows=1 width=36) (actual time=0.020..0.021 rows=400 loops=1)
  Index Cond: (user_id = 100)
```
Теперь используется индексное сканирование (`Index Scan`), что значительно быстрее.

---

### Итог
- **Индексы** ускоряют поиск и сортировку.
- **Порядок полей** в индексах важен для эффективности.
- **Блокировки** должны использоваться минимально необходимые.
- **`EXPLAIN PLAN`** помогает анализировать и оптимизировать запросы.

# Часть 2

## 1. **Оптимизация JOIN: Замена `SELECT *` на явный список полей**

### Неоптимизированный запрос
```sql
SELECT *
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';
```
Этот запрос извлекает все поля из обеих таблиц, что увеличивает нагрузку на сеть и память.

### Оптимизированный запрос
```sql
SELECT u.id, u.name, o.id AS order_id, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';
```
**Объяснение:**
Явное указание необходимых полей уменьшает объем передаваемых данных и ускоряет выполнение запроса.

---

## 2. **Оптимизация JOIN: Использование индексов для ускорения соединений**

### Неоптимизированный запрос
```sql
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2023-01-01';
```
Если на `users.id` и `orders.user_id` нет индексов, PostgreSQL выполнит `Hash Join` или `Nested Loop`, что может быть медленно для больших таблиц.

### Оптимизированный запрос
```sql
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_users_created_at ON users(created_at);

SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2023-01-01';
```
**Объяснение:**
Индексы на полях соединения (`id`, `user_id`) и фильтрации (`created_at`) ускоряют выполнение запроса.

---

## 3. **Оптимизация LEFT JOIN: Избегание избыточных соединений**

### Неоптимизированный запрос
```sql
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```
Этот запрос выполняет `LEFT JOIN` и подсчитывает заказы для всех пользователей, даже если они не делали заказов.

### Оптимизированный запрос
```sql
SELECT
    u.id,
    u.name,
    COALESCE((
        SELECT COUNT(*)
        FROM orders o
        WHERE o.user_id = u.id
    ), 0) AS order_count
FROM users u;
```
**Объяснение:**
Использование подзапроса вместо `LEFT JOIN` может быть эффективнее, если нужно только посчитать количество заказов.

---

## 4. **Оптимизация сложных JOIN: Использование CTE для улучшения читаемости и производительности**

### Неоптимизированный запрос
```sql
SELECT
    u.name,
    o.amount,
    p.name AS product_name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE u.status = 'active'
AND o.created_at > '2023-01-01';
```
Этот запрос выполняет несколько соединений, что может быть сложно для оптимизатора.

### Оптимизированный запрос
```sql
WITH active_users AS (
    SELECT id, name
    FROM users
    WHERE status = 'active'
),
recent_orders AS (
    SELECT id, user_id, amount
    FROM orders
    WHERE created_at > '2023-01-01'
)
SELECT
    au.name,
    ro.amount,
    p.name AS product_name
FROM active_users au
JOIN recent_orders ro ON au.id = ro.user_id
JOIN order_items oi ON ro.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```
**Объяснение:**
CTE улучшают читаемость и позволяют оптимизатору лучше планировать выполнение запроса.

---

## 5. **Оптимизация JOIN с использованием оконных функций**

### Неоптимизированный запрос
```sql
SELECT
    u.name,
    o.amount,
    (SELECT AVG(amount) FROM orders WHERE user_id = u.id) AS avg_amount
FROM users u
JOIN orders o ON u.id = o.user_id;
```
Этот запрос выполняет подзапрос для каждого пользователя, что неэффективно.

### Оптимизированный запрос
```sql
SELECT
    u.name,
    o.amount,
    AVG(o.amount) OVER (PARTITION BY u.id) AS avg_amount
FROM users u
JOIN orders o ON u.id = o.user_id;
```
**Объяснение:**
Оконные функции позволяют вычислять агрегаты без дополнительных подзапросов.

---

## 6. **Использование `EXPLAIN ANALYZE` для анализа сложных запросов**

### Пример анализа неоптимизированного запроса
```sql
EXPLAIN ANALYZE
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
AND o.created_at > '2023-01-01';
```
**Результат:**
```
Hash Join (cost=100.00..200.00 rows=1000 width=36) (actual time=5.000..10.000 rows=1000 loops=1)
  Hash Cond: (o.user_id = u.id)
  -> Seq Scan on orders o (cost=0.00..150.00 rows=1000 width=20) (actual time=2.000..5.000 rows=1000 loops=1)
        Filter: (created_at > '2023-01-01'::date)
  -> Hash (cost=50.00..50.00 rows=1000 width=16) (actual time=1.000..1.000 rows=1000 loops=1)
        -> Seq Scan on users u (cost=0.00..50.00 rows=1000 width=16) (actual time=0.000..1.000 rows=1000 loops=1)
              Filter: (status = 'active'::text)
```
Здесь видно, что выполняется полное сканирование таблиц (`Seq Scan`) и `Hash Join`.

### Оптимизированный запрос с анализом
```sql
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_user_id ON orders(user_id);

EXPLAIN ANALYZE
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
AND o.created_at > '2023-01-01';
```
**Результат:**
```
Nested Loop (cost=0.42..10.00 rows=1000 width=36) (actual time=0.020..0.100 rows=1000 loops=1)
  -> Index Scan using idx_users_status on users u (cost=0.14..4.14 rows=100 width=16) (actual time=0.010..0.020 rows=100 loops=1)
        Index Cond: (status = 'active'::text)
  -> Index Scan using idx_orders_user_id on orders o (cost=0.28..5.00 rows=10 width=20) (actual time=0.001..0.002 rows=10 loops=100)
        Index Cond: (user_id = u.id)
        Filter: (created_at > '2023-01-01'::date)
```
Теперь используется индексное сканирование (`Index Scan`) и `Nested Loop`, что значительно быстрее.

---

### Итог
- **Индексы** ускоряют соединения и фильтрацию.
- **CTE** улучшают читаемость и могут оптимизировать выполнение.
- **Оконные функции** позволяют избегать подзапросов.
- **`EXPLAIN ANALYZE`** помогает анализировать и оптимизировать сложные запросы.

# Часть 3

## 1. **FULL JOIN: Объединение данных с учетом всех записей из обеих таблиц**

### Неоптимизированный запрос
```sql
-- Получаем всех пользователей и все заказы, даже если нет соответствий
SELECT u.name, o.amount
FROM users u
FULL JOIN orders o ON u.id = o.user_id;
```
Этот запрос может быть медленным, если таблицы большие и не оптимизированы.

### Оптимизированный запрос
```sql
-- Создаем индексы для ускорения соединения
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Используем FULL JOIN с фильтрацией
SELECT u.name, o.amount
FROM users u
FULL JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active' OR o.created_at > '2023-01-01';
```
**Объяснение:**
Индексы на полях соединения (`id`, `user_id`) ускоряют выполнение `FULL JOIN`. Фильтрация после соединения позволяет уменьшить объем данных.

---

## 2. **CROSS JOIN: Декартово произведение таблиц**

### Неоптимизированный запрос
```sql
-- Получаем все возможные комбинации пользователей и продуктов
SELECT u.name, p.name AS product_name
FROM users u
CROSS JOIN products p;
```
Этот запрос создает декартово произведение, что может быть очень ресурсоемко для больших таблиц.

### Оптимизированный запрос
```sql
-- Ограничиваем количество записей с помощью WHERE
SELECT u.name, p.name AS product_name
FROM users u
CROSS JOIN products p
WHERE u.status = 'active' AND p.is_available = TRUE;
```
**Объяснение:**
Фильтрация с помощью `WHERE` уменьшает количество комбинаций, которые необходимо обработать.

---

## 3. **Оптимизация для больших объемов данных: Использование временных таблиц**

### Неоптимизированный запрос
```sql
-- Сложный запрос с несколькими соединениями и агрегациями
SELECT
    u.name,
    COUNT(o.id) AS order_count,
    SUM(o.amount) AS total_amount
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
WHERE u.status = 'active'
GROUP BY u.id;
```
Этот запрос может быть медленным из-за большого количества соединений и агрегаций.

### Оптимизированный запрос
```sql
-- Создаем временную таблицу для промежуточных результатов
CREATE TEMP TABLE active_users_orders AS
SELECT
    o.user_id,
    COUNT(o.id) AS order_count,
    SUM(o.amount) AS total_amount
FROM orders o
WHERE o.user_id IN (
    SELECT id FROM users WHERE status = 'active'
)
GROUP BY o.user_id;

-- Используем временную таблицу для финального запроса
SELECT
    u.name,
    auo.order_count,
    auo.total_amount
FROM users u
JOIN active_users_orders auo ON u.id = auo.user_id;
```
**Объяснение:**
Временные таблицы позволяют разбить сложный запрос на более простые части, что улучшает производительность.

---

## 4. **Оптимизация с использованием материализованных представлений**

### Неоптимизированный запрос
```sql
-- Часто выполняемый запрос с агрегацией
SELECT
    p.category_id,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.category_id;
```
Этот запрос может быть медленным, если выполняется часто и таблицы большие.

### Оптимизированный запрос
```sql
-- Создаем материализованное представление
CREATE MATERIALIZED VIEW mv_category_quantity AS
SELECT
    p.category_id,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.category_id;

-- Обновляем материализованное представление при необходимости
REFRESH MATERIALIZED VIEW mv_category_quantity;

-- Используем материализованное представление
SELECT * FROM mv_category_quantity;
```
**Объяснение:**
Материализованные представления позволяют сохранить результаты запроса и быстро их получать, избегая повторных вычислений.

---

## 5. **Оптимизация сложных запросов с использованием `EXPLAIN ANALYZE`**

### Пример анализа неоптимизированного запроса
```sql
EXPLAIN ANALYZE
SELECT
    u.name,
    COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id;
```
**Результат:**
```
HashAggregate (cost=100.00..101.00 rows=100 width=20) (actual time=10.000..10.001 rows=100 loops=1)
  Group Key: u.id
  -> Hash Right Join (cost=50.00..95.00 rows=1000 width=20) (actual time=5.000..9.000 rows=1000 loops=1)
        Hash Cond: (o.user_id = u.id)
        -> Seq Scan on orders o (cost=0.00..30.00 rows=2000 width=8) (actual time=0.000..2.000 rows=2000 loops=1)
        -> Hash (cost=40.00..40.00 rows=1000 width=16) (actual time=1.000..1.000 rows=1000 loops=1)
              -> Seq Scan on users u (cost=0.00..40.00 rows=1000 width=16) (actual time=0.000..1.000 rows=1000 loops=1)
                    Filter: (status = 'active'::text)
```
Здесь видно, что выполняется полное сканирование таблиц (`Seq Scan`) и `Hash Right Join`.

### Оптимизированный запрос с анализом
```sql
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_orders_user_id ON orders(user_id);

EXPLAIN ANALYZE
SELECT
    u.name,
    COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id;
```
**Результат:**
```
HashAggregate (cost=10.00..11.00 rows=100 width=20) (actual time=0.100..0.101 rows=100 loops=1)
  Group Key: u.id
  -> Hash Right Join (cost=5.00..9.50 rows=1000 width=20) (actual time=0.050..0.090 rows=1000 loops=1)
        Hash Cond: (o.user_id = u.id)
        -> Index Scan using idx_orders_user_id on orders o (cost=0.28..4.28 rows=100 width=8) (actual time=0.001..0.002 rows=100 loops=1)
        -> Hash (cost=4.00..4.00 rows=100 width=16) (actual time=0.010..0.010 rows=100 loops=1)
              -> Index Scan using idx_users_status on users u (cost=0.14..4.14 rows=100 width=16) (actual time=0.001..0.002 rows=100 loops=1)
                    Index Cond: (status = 'active'::text)
```
Теперь используется индексное сканирование (`Index Scan`) и `Hash Right Join`, что значительно быстрее.

---

### Итог
- **`FULL JOIN`** и **`CROSS JOIN`** требуют индексов и фильтрации для оптимизации.
- **Временные таблицы** и **материализованные представления** помогают оптимизировать сложные запросы.
- **`EXPLAIN ANALYZE`** позволяет анализировать и улучшать производительность запросов.

# Часть 4

## 1. **Работа с JSON: Оптимизация запросов к JSON-полям**

### Неоптимизированный запрос
```sql
-- Получаем пользователей, у которых в JSON-профиле указан город "Москва"
SELECT id, name
FROM users
WHERE profile->>'city' = 'Москва';
```
Если на JSON-поле `profile` нет индекса, PostgreSQL выполнит полное сканирование таблицы (`Seq Scan`), что может быть медленно.

### Оптимизированный запрос
```sql
-- Создаем функциональный индекс для ускорения поиска по JSON-полю
CREATE INDEX idx_users_profile_city ON users ((profile->>'city'));

-- Используем индекс в запросе
SELECT id, name
FROM users
WHERE profile->>'city' = 'Москва';
```
**Объяснение:**
Функциональный индекс на JSON-поле позволяет PostgreSQL использовать индексное сканирование (`Index Scan`), что значительно ускоряет поиск.

---

## 2. **Рекурсивные запросы: Оптимизация с использованием CTE**

### Неоптимизированный запрос
```sql
-- Рекурсивный запрос для получения иерархии категорий (без оптимизации)
WITH RECURSIVE category_hierarchy AS (
    SELECT id, name, parent_id
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN category_hierarchy ch ON c.parent_id = ch.id
)
SELECT * FROM category_hierarchy;
```
Этот запрос может быть медленным, если таблица `categories` большая и не оптимизирована.

### Оптимизированный запрос
```sql
-- Добавляем индекс на поле parent_id для ускорения рекурсивного соединения
CREATE INDEX idx_categories_parent_id ON categories(parent_id);

-- Используем рекурсивный CTE с ограничением глубины рекурсии
WITH RECURSIVE category_hierarchy AS (
    SELECT id, name, parent_id, 1 AS level
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ch.level + 1
    FROM categories c
    JOIN category_hierarchy ch ON c.parent_id = ch.id
    WHERE ch.level < 10  -- Ограничиваем глубину рекурсии
)
SELECT * FROM category_hierarchy;
```
**Объяснение:**
Индекс на `parent_id` ускоряет рекурсивное соединение, а ограничение глубины рекурсии (`level < 10`) предотвращает избыточные вычисления.

---

## 3. **Оптимизация транзакций: Минимизация блокировок**

### Неоптимизированный запрос
```sql
-- Длительная транзакция с блокировкой строк
BEGIN;
    -- Блокируем строку на длительное время
    SELECT * FROM accounts WHERE id = 1 FOR UPDATE;

    -- Выполняем долгие операции...
    -- Например, сложные вычисления или внешние запросы

    -- Обновляем запись
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```
Эта транзакция блокирует строку на длительное время, что может привести к блокировкам других транзакций.

### Оптимизированный запрос
```sql
-- Разбиваем транзакцию на более короткие этапы
BEGIN;
    -- Быстро блокируем и обновляем строку
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- Выполняем долгие операции вне транзакции
-- Например, логирование или отправка уведомлений
```
**Объяснение:**
Минимизация времени блокировки строки (`FOR UPDATE`) и быстрое выполнение критических операций уменьшает вероятность блокировок.

---

## 4. **Оптимизация транзакций: Использование `SAVEPOINT`**

### Неоптимизированный запрос
```sql
-- Длинная транзакция с риском отката всех изменений
BEGIN;
    -- Выполняем несколько операций
    INSERT INTO orders (user_id, amount) VALUES (1, 100);
    UPDATE users SET balance = balance - 100 WHERE id = 1;

    -- Если здесь произойдет ошибка, все изменения будут отменены
    -- Например, внешний запрос или сложная логика
COMMIT;
```

### Оптимизированный запрос
```sql
-- Используем SAVEPOINT для частичного отката
BEGIN;
    -- Первая операция
    INSERT INTO orders (user_id, amount) VALUES (1, 100);

    -- Создаем точку сохранения
    SAVEPOINT after_insert;

    -- Вторая операция
    UPDATE users SET balance = balance - 100 WHERE id = 1;

    -- Если ошибка, откатываем только часть изменений
    -- ROLLBACK TO after_insert;
COMMIT;
```
**Объяснение:**
`SAVEPOINT` позволяет откатывать только часть транзакции, не теряя все изменения.

---

## 5. **Использование `EXPLAIN ANALYZE` для анализа рекурсивных запросов**

### Пример анализа неоптимизированного рекурсивного запроса
```sql
EXPLAIN ANALYZE
WITH RECURSIVE category_hierarchy AS (
    SELECT id, name, parent_id
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN category_hierarchy ch ON c.parent_id = ch.id
)
SELECT * FROM category_hierarchy;
```
**Результат:**
```
CTE Scan on category_hierarchy (cost=100.00..1000.00 rows=1000 width=36) (actual time=10.000..50.000 rows=1000 loops=1)
  CTE category_hierarchy
    -> Recursive Union (cost=0.00..100.00 rows=1000 width=36) (actual time=0.000..10.000 rows=1000 loops=1)
          -> Seq Scan on categories (cost=0.00..10.00 rows=10 width=36) (actual time=0.001..0.002 rows=10 loops=1)
                Filter: (parent_id IS NULL)
          -> Hash Join (cost=1.00..10.00 rows=100 width=36) (actual time=0.001..0.100 rows=100 loops=10)
                Hash Cond: (c.parent_id = ch.id)
                -> Seq Scan on categories c (cost=0.00..10.00 rows=1000 width=36) (actual time=0.001..0.010 rows=1000 loops=10)
                -> WorkTable Scan on category_hierarchy ch (cost=0.00..0.00 rows=10 width=36) (actual time=0.000..0.000 rows=10 loops=10)
```
Здесь видно, что выполняется полное сканирование таблицы (`Seq Scan`) и рекурсивное соединение (`Hash Join`).

### Оптимизированный запрос с анализом
```sql
CREATE INDEX idx_categories_parent_id ON categories(parent_id);

EXPLAIN ANALYZE
WITH RECURSIVE category_hierarchy AS (
    SELECT id, name, parent_id
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN category_hierarchy ch ON c.parent_id = ch.id
)
SELECT * FROM category_hierarchy;
```
**Результат:**
```
CTE Scan on category_hierarchy (cost=10.00..100.00 rows=1000 width=36) (actual time=0.100..1.000 rows=1000 loops=1)
  CTE category_hierarchy
    -> Recursive Union (cost=0.00..10.00 rows=1000 width=36) (actual time=0.000..0.100 rows=1000 loops=1)
          -> Index Scan using idx_categories_parent_id on categories (cost=0.14..1.14 rows=10 width=36) (actual time=0.001..0.002 rows=10 loops=1)
                Index Cond: (parent_id IS NULL)
          -> Hash Join (cost=0.14..1.14 rows=100 width=36) (actual time=0.001..0.010 rows=100 loops=10)
                Hash Cond: (c.parent_id = ch.id)
                -> Index Scan using idx_categories_parent_id on categories c (cost=0.14..1.14 rows=100 width=36) (actual time=0.001..0.002 rows=100 loops=10)
                -> WorkTable Scan on category_hierarchy ch (cost=0.00..0.00 rows=10 width=36) (actual time=0.000..0.000 rows=10 loops=10)
```
Теперь используется индексное сканирование (`Index Scan`), что значительно ускоряет выполнение рекурсивного запроса.

---

### Итог
- **JSON**: Используйте функциональные индексы для ускорения поиска по JSON-полям.
- **Рекурсивные запросы**: Оптимизируйте с помощью индексов и ограничивайте глубину рекурсии.
- **Транзакции**: Минимизируйте время блокировок и используйте `SAVEPOINT` для частичного отката.
- **`EXPLAIN ANALYZE`**: Всегда анализируйте план выполнения для оптимизации сложных запросов.

# Часть 5

## 1. **Работа с массивами: Оптимизация запросов к массивам**

### Неоптимизированный запрос
```sql
-- Получаем пользователей, у которых в массиве тегов есть "premium"
SELECT id, name
FROM users
WHERE 'premium' = ANY(tags);
```
Если на поле `tags` нет индекса, PostgreSQL выполнит полное сканирование таблицы (`Seq Scan`), что может быть медленно для больших таблиц.

### Оптимизированный запрос
```sql
-- Создаем индекс для ускорения поиска по массиву
CREATE INDEX idx_users_tags ON users USING GIN(tags);

-- Используем индекс в запросе
SELECT id, name
FROM users
WHERE 'premium' = ANY(tags);
```
**Объяснение:**
Индекс типа `GIN` на массиве позволяет PostgreSQL использовать индексное сканирование (`Index Scan`), что значительно ускоряет поиск по элементам массива.

---

## 2. **Оптимизация триггеров: Уменьшение накладных расходов**

### Неоптимизированный триггер
```sql
-- Триггер, который выполняет сложную логику при каждом обновлении записи
CREATE OR REPLACE FUNCTION update_user_balance()
RETURNS TRIGGER AS $$
BEGIN
    -- Сложная логика, например, обновление связанных таблиц
    UPDATE statistics SET total_orders = total_orders + 1 WHERE user_id = NEW.id;
    -- Дополнительные операции...
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_user_balance
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_user_balance();
```
Этот триггер выполняет сложные операции при каждом обновлении строки, что может замедлять работу, особенно при массовых обновлениях.

### Оптимизированный триггер
```sql
-- Используем отложенные триггеры (DEFERRABLE) или выполняем логику в отдельной транзакции
CREATE OR REPLACE FUNCTION update_user_balance()
RETURNS TRIGGER AS $$
BEGIN
    -- Откладываем сложную логику на потом или выполняем её асинхронно
    -- Например, используем очередь задач (pg_notify, RabbitMQ) или отложенный триггер
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Пример отложенного тригера
CREATE TRIGGER trg_update_user_balance
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_user_balance();
```
**Объяснение:**
Отложенные триггеры или асинхронная обработка позволяют уменьшить нагрузку на базу данных при массовых операциях.

---

## 3. **Использование `UNLOGGED` таблиц для временных данных**

### Неоптимизированный подход
```sql
-- Используем обычную таблицу для временных данных
CREATE TABLE temp_data (
    id SERIAL PRIMARY KEY,
    value TEXT
);

-- Вставляем и удаляем данные часто
INSERT INTO temp_data (value) SELECT 'data' FROM generate_series(1, 10000);
DELETE FROM temp_data WHERE id < 5000;
```
Обычные таблицы ведут журнал транзакций (`WAL`), что может замедлять операции вставки и удаления, если данные временные и не требуют восстановления.

### Оптимизированный подход
```sql
-- Используем UNLOGGED таблицу для временных данных
CREATE UNLOGGED TABLE temp_data (
    id SERIAL PRIMARY KEY,
    value TEXT
);

-- Вставляем и удаляем данные часто
INSERT INTO temp_data (value) SELECT 'data' FROM generate_series(1, 10000);
DELETE FROM temp_data WHERE id < 5000;
```
**Объяснение:**
`UNLOGGED` таблицы не ведут журнал транзакций (`WAL`), что значительно ускоряет операции вставки, обновления и удаления для временных данных. Однако такие таблицы не восстанавливаются после сбоя сервера.

---

## 4. **Оптимизация триггеров: Использование `STATEMENT`-триггеров вместо `ROW`-триггеров**

### Неоптимизированный триггер
```sql
-- Триггер на уровне строк (ROW)
CREATE OR REPLACE FUNCTION log_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_logs (user_id, action, changed_at)
    VALUES (NEW.id, 'UPDATE', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_user_changes
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_changes();
```
Этот триггер выполняется для каждой изменённой строки, что может быть неэффективно при массовых обновлениях.

### Оптимизированный триггер
```sql
-- Триггер на уровне оператора (STATEMENT)
CREATE OR REPLACE FUNCTION log_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Логируем одно событие на весь оператор UPDATE
    INSERT INTO user_logs (action, changed_at)
    VALUES ('BULK_UPDATE', NOW());
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_user_changes
AFTER UPDATE ON users
FOR EACH STATEMENT
EXECUTE FUNCTION log_user_changes();
```
**Объяснение:**
`STATEMENT`-триггеры выполняются один раз на весь оператор, а не для каждой строки, что значительно уменьшает накладные расходы при массовых операциях.

---

## 5. **Использование `EXPLAIN ANALYZE` для анализа триггеров**

### Пример анализа неоптимизированного триггера
```sql
EXPLAIN ANALYZE
UPDATE users SET balance = balance + 100 WHERE id < 1000;
```
**Результат:**
```
Update on users (cost=0.00..100.00 rows=1000 width=36) (actual time=10.000..50.000 rows=0 loops=1)
  -> Seq Scan on users (cost=0.00..100.00 rows=1000 width=36) (actual time=0.000..10.000 rows=1000 loops=1)
        Filter: (id < 1000)
  Triggers:
    trg_update_user_balance: time=40.000 calls=1000
```
Здесь видно, что триггер `trg_update_user_balance` выполняется 1000 раз, что занимает значительное время.

### Оптимизированный триггер с анализом
```sql
-- Переписываем триггер на STATEMENT-уровень
CREATE OR REPLACE FUNCTION update_user_balance()
RETURNS TRIGGER AS $$
BEGIN
    -- Обновляем статистику одним запросом
    UPDATE statistics
    SET total_orders = total_orders + (SELECT COUNT(*) FROM NEW_TABLE WHERE id < 1000)
    WHERE user_id IN (SELECT id FROM NEW_TABLE WHERE id < 1000);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_user_balance
AFTER UPDATE ON users
FOR EACH STATEMENT
EXECUTE FUNCTION update_user_balance();

EXPLAIN ANALYZE
UPDATE users SET balance = balance + 100 WHERE id < 1000;
```
**Результат:**
```
Update on users (cost=0.00..100.00 rows=1000 width=36) (actual time=0.100..1.000 rows=0 loops=1)
  -> Seq Scan on users (cost=0.00..100.00 rows=1000 width=36) (actual time=0.000..0.100 rows=1000 loops=1)
        Filter: (id < 1000)
  Triggers:
    trg_update_user_balance: time=0.500 calls=1
```
Теперь триггер выполняется один раз, что значительно ускоряет операцию.

---

### Итог
- **Массивы**: Используйте индексы `GIN` для ускорения поиска по массивам.
- **Триггеры**: Предпочитайте `STATEMENT`-триггеры для массовых операций и минимизируйте накладные расходы.
- **`UNLOGGED` таблицы**: Используйте для временных данных, где не требуется восстановление после сбоя.
- **`EXPLAIN ANALYZE`**: Всегда анализируйте план выполнения для оптимизации триггеров и запросов.

# Часть 6

## 1. **Оптимизация функций на PL/pgSQL**

### Неоптимизированная функция
```sql
CREATE OR REPLACE FUNCTION calculate_user_stats(user_id INT)
RETURNS TABLE(order_count BIGINT, total_amount NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT COUNT(*) FROM orders WHERE user_id = calculate_user_stats.user_id),
        (SELECT COALESCE(SUM(amount), 0) FROM orders WHERE user_id = calculate_user_stats.user_id);
END;
$$ LANGUAGE plpgsql;
```
Эта функция выполняет два подзапроса для каждой строки, что неэффективно.

### Оптимизированная функция
```sql
CREATE OR REPLACE FUNCTION calculate_user_stats(user_id INT)
RETURNS TABLE(order_count BIGINT, total_amount NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*) AS order_count,
        COALESCE(SUM(amount), 0) AS total_amount
    FROM orders
    WHERE user_id = calculate_user_stats.user_id
    GROUP BY user_id;
END;
$$ LANGUAGE plpgsql;
```
**Объяснение:**
Один запрос с агрегацией вместо двух подзапросов значительно ускоряет выполнение функции.

---

## 2. **Оптимизация с использованием `PARTITIONED` таблиц**

### Неоптимизированная таблица
```sql
-- Обычная таблица для хранения заказов
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount NUMERIC NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- Вставка данных
INSERT INTO orders (user_id, amount, created_at)
SELECT 1, 100 * random(), NOW() - (random() * (30 * 24 * 3600 || ' second'))::INTERVAL
FROM generate_series(1, 1000000);
```
Для больших объёмов данных запросы к такой таблице могут быть медленными из-за отсутствия разбиения.

### Оптимизированная таблица
```sql
-- Создаем разбитую таблицу по месяцам
CREATE TABLE orders (
    id BIGSERIAL,
    user_id INT NOT NULL,
    amount NUMERIC NOT NULL,
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- Создаем разделы для каждого месяца
CREATE TABLE orders_2023_01 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

CREATE TABLE orders_2023_02 PARTITION OF orders
    FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');

-- Вставка данных
INSERT INTO orders (user_id, amount, created_at)
SELECT 1, 100 * random(), NOW() - (random() * (30 * 24 * 3600 || ' second'))::INTERVAL
FROM generate_series(1, 1000000);
```
**Объяснение:**
Разбиение таблицы по диапазонам дат (`PARTITION BY RANGE`) позволяет PostgreSQL быстро находить нужные данные, особенно при фильтрации по `created_at`.

---

## 3. **Работа с `HSTORE`: Оптимизация запросов**

### Неоптимизированный запрос
```sql
-- Получаем пользователей, у которых в HSTORE-профиле указан город "Москва"
CREATE EXTENSION IF NOT EXISTS hstore;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    profile HSTORE
);

INSERT INTO users (name, profile)
VALUES ('Иван', 'city => "Москва", age => "30"');

-- Запрос без индекса
SELECT id, name
FROM users
WHERE profile -> 'city' = 'Москва';
```
Без индекса PostgreSQL выполнит полное сканирование таблицы.

### Оптимизированный запрос
```sql
-- Создаем индекс для ускорения поиска по HSTORE
CREATE INDEX idx_users_profile_city ON users ((profile -> 'city'));

-- Используем индекс в запросе
SELECT id, name
FROM users
WHERE profile -> 'city' = 'Москва';
```
**Объяснение:**
Функциональный индекс на `HSTORE` позволяет PostgreSQL использовать индексное сканирование для быстрого поиска.

---

## 4. **Работа с `JSONB`: Оптимизация запросов**

### Неоптимизированный запрос
```sql
-- Получаем пользователей, у которых в JSONB-профиле указан город "Москва"
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    profile JSONB
);

INSERT INTO users (name, profile)
VALUES ('Иван', '{"city": "Москва", "age": 30}');

-- Запрос без индекса
SELECT id, name
FROM users
WHERE profile @> '{"city": "Москва"}';
```
Без индекса PostgreSQL выполнит полное сканирование таблицы.

### Оптимизированный запрос
```sql
-- Создаем индекс для ускорения поиска по JSONB
CREATE INDEX idx_users_profile_city ON users ((profile -> 'city'));

-- Используем индекс в запросе
SELECT id, name
FROM users
WHERE profile ->> 'city' = 'Москва';
```
**Объяснение:**
Индекс на поле `JSONB` позволяет PostgreSQL быстро находить нужные записи.

---

## 5. **Использование `EXPLAIN ANALYZE` для анализа функций и запросов**

### Пример анализа неоптимизированной функции
```sql
EXPLAIN ANALYZE
SELECT * FROM calculate_user_stats(1);
```
**Результат:**
```
Function Scan on calculate_user_stats (cost=0.25..10.25 rows=1000 width=32) (actual time=10.000..50.000 rows=1 loops=1)
  InitPlan 1 (returns $0)
    -> Aggregate (cost=10.00..10.01 rows=1 width=8) (actual time=10.000..10.001 rows=1 loops=1)
          -> Seq Scan on orders (cost=0.00..10.00 rows=100 width=8) (actual time=0.000..10.000 rows=100 loops=1)
                Filter: (user_id = 1)
  InitPlan 2 (returns $1)
    -> Aggregate (cost=10.00..10.01 rows=1 width=32) (actual time=10.000..10.001 rows=1 loops=1)
          -> Seq Scan on orders (cost=0.00..10.00 rows=100 width=32) (actual time=0.000..10.000 rows=100 loops=1)
                Filter: (user_id = 1)
```
Здесь видно, что функция выполняет два полных сканирования таблицы `orders`.

### Оптимизированная функция с анализом
```sql
EXPLAIN ANALYZE
SELECT * FROM calculate_user_stats(1);
```
**Результат:**
```
Function Scan on calculate_user_stats (cost=0.25..5.25 rows=1000 width=32) (actual time=0.100..1.000 rows=1 loops=1)
  InitPlan 1 (returns $0)
    -> Aggregate (cost=5.00..5.01 rows=1 width=16) (actual time=0.100..0.101 rows=1 loops=1)
          -> Index Scan using idx_orders_user_id on orders (cost=0.14..5.14 rows=100 width=8) (actual time=0.001..0.010 rows=100 loops=1)
                Index Cond: (user_id = 1)
```
Теперь используется индексное сканирование (`Index Scan`), что значительно ускоряет выполнение функции.

---

### Итог
- **Функции на PL/pgSQL**: Избегайте подзапросов, используйте агрегацию.
- **`PARTITIONED` таблицы**: Разбивайте большие таблицы по диапазонам или спискам для ускорения запросов.
- **`HSTORE` и `JSONB`**: Используйте функциональные индексы для ускорения поиска.
- **`EXPLAIN ANALYZE`**: Всегда анализируйте план выполнения для оптимизации функций и запросов.

# Часть 7

## 1. **Оптимизация CTE (Common Table Expressions)**

### Неоптимизированный CTE
```sql
-- Используем CTE для вычисления статистики по пользователям
WITH user_orders AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_amount
    FROM orders
    GROUP BY user_id
)
SELECT
    u.id,
    u.name,
    uo.order_count,
    uo.total_amount
FROM users u
LEFT JOIN user_orders uo ON u.id = uo.user_id;
```
Этот запрос может быть неэффективным, если CTE не оптимизировано и выполняется как отдельный подзапрос.

### Оптимизированный CTE
```sql
-- Используем CTE с явным указанием индексов и фильтрацией
WITH user_orders AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(amount) AS total_amount
    FROM orders
    WHERE created_at > '2023-01-01'  -- Фильтрация по дате
    GROUP BY user_id
)
SELECT
    u.id,
    u.name,
    uo.order_count,
    uo.total_amount
FROM users u
LEFT JOIN user_orders uo ON u.id = uo.user_id
WHERE u.status = 'active';  -- Фильтрация активных пользователей
```
**Объяснение:**
Добавление фильтров (`WHERE`) внутри CTE и в основном запросе позволяет уменьшить объем обрабатываемых данных и ускорить выполнение.

---

## 2. **Использование BRIN-индексов для больших таблиц**

### Неоптимизированная таблица
```sql
-- Таблица с временными метками, без индексов
CREATE TABLE sensor_data (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    value NUMERIC NOT NULL,
    recorded_at TIMESTAMP NOT NULL
);

-- Вставка большого количества данных
INSERT INTO sensor_data (sensor_id, value, recorded_at)
SELECT
    1 + (random() * 10)::INT,
    random() * 100,
    NOW() - (random() * (365 * 24 * 3600 || ' second'))::INTERVAL
FROM generate_series(1, 10000000);
```
Для больших таблиц с временными метками обычные B-tree индексы могут занимать много места и быть менее эффективными.

### Оптимизированная таблица с BRIN-индексом
```sql
-- Создаем BRIN-индекс для временных меток
CREATE INDEX idx_sensor_data_recorded_at ON sensor_data USING BRIN(recorded_at);

-- Запрос с использованием BRIN-индекса
SELECT sensor_id, AVG(value)
FROM sensor_data
WHERE recorded_at BETWEEN '2023-01-01' AND '2023-01-31'
GROUP BY sensor_id;
```
**Объяснение:**
`BRIN`-индексы (Block Range Indexes) эффективны для больших таблиц с естественным упорядочиванием данных (например, временные метки). Они занимают меньше места и быстрее строятся, чем B-tree индексы.

---

## 3. **Оптимизация LATERAL JOIN**

### Неоптимизированный LATERAL JOIN
```sql
-- Используем LATERAL JOIN для получения последнего заказа каждого пользователя
SELECT
    u.id,
    u.name,
    last_order.amount
FROM users u,
LATERAL (
    SELECT amount
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) AS last_order;
```
Этот запрос может быть медленным, если нет индексов на полях `user_id` и `created_at`.

### Оптимизированный LATERAL JOIN
```sql
-- Добавляем индексы для ускорения LATERAL JOIN
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Используем LATERAL JOIN с индексами
SELECT
    u.id,
    u.name,
    last_order.amount
FROM users u,
LATERAL (
    SELECT amount
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) AS last_order;
```
**Объяснение:**
Индексы на полях `user_id` и `created_at` позволяют PostgreSQL быстро находить последние заказы для каждого пользователя.

---

## 4. **Использование `EXPLAIN ANALYZE` для анализа LATERAL JOIN**

### Пример анализа неоптимизированного LATERAL JOIN
```sql
EXPLAIN ANALYZE
SELECT
    u.id,
    u.name,
    last_order.amount
FROM users u,
LATERAL (
    SELECT amount
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) AS last_order;
```
**Результат:**
```
Nested Loop (cost=0.00..1000.00 rows=1000 width=36) (actual time=10.000..50.000 rows=1000 loops=1)
  -> Seq Scan on users u (cost=0.00..10.00 rows=1000 width=16) (actual time=0.000..1.000 rows=1000 loops=1)
  -> Limit (cost=0.00..10.00 rows=1 width=20) (actual time=0.010..0.050 rows=1 loops=1000)
        -> Sort (cost=0.00..10.00 rows=100 width=20) (actual time=0.010..0.050 rows=1 loops=1000)
              Sort Key: o.created_at DESC
              -> Seq Scan on orders o (cost=0.00..10.00 rows=100 width=20) (actual time=0.001..0.010 rows=100 loops=1000)
                    Filter: (user_id = u.id)
```
Здесь видно, что для каждого пользователя выполняется полное сканирование таблицы `orders` (`Seq Scan`) и сортировка (`Sort`).

### Оптимизированный LATERAL JOIN с анализом
```sql
EXPLAIN ANALYZE
SELECT
    u.id,
    u.name,
    last_order.amount
FROM users u,
LATERAL (
    SELECT amount
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) AS last_order;
```
**Результат:**
```
Nested Loop (cost=0.14..10.00 rows=1000 width=36) (actual time=0.100..1.000 rows=1000 loops=1)
  -> Seq Scan on users u (cost=0.00..10.00 rows=1000 width=16) (actual time=0.000..1.000 rows=1000 loops=1)
  -> Limit (cost=0.14..1.14 rows=1 width=20) (actual time=0.001..0.002 rows=1 loops=1000)
        -> Index Scan Backward using idx_orders_user_id_created_at on orders o (cost=0.14..1.14 rows=1 width=20) (actual time=0.001..0.002 rows=1 loops=1000)
              Index Cond: (user_id = u.id)
```
Теперь используется индексное сканирование (`Index Scan Backward`), что значительно ускоряет выполнение запроса.

---

### Итог
- **CTE**: Добавляйте фильтры и используйте индексы для ускорения.
- **BRIN-индексы**: Эффективны для больших таблиц с естественным упорядочиванием (например, временные метки).
- **LATERAL JOIN**: Используйте индексы для ускорения подзапросов.
- **`EXPLAIN ANALYZE`**: Всегда анализируйте план выполнения для оптимизации сложных запросов.

# Часть 8

## 1. **Оптимизация оконных функций (WINDOW FUNCTIONS)**

### Неоптимизированный запрос с оконными функциями
```sql
-- Получаем пользователей с их рангом по сумме заказов
SELECT
    u.id,
    u.name,
    SUM(o.amount) AS total_amount,
    RANK() OVER (ORDER BY SUM(o.amount) DESC) AS user_rank
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```
Этот запрос может быть медленным, так как оконная функция применяется к результату агрегации, что требует сортировки большого объема данных.

### Оптимизированный запрос
```sql
-- Добавляем индекс на поле amount для ускорения агрегации
CREATE INDEX idx_orders_amount ON orders(amount);

-- Используем CTE для предварительной агрегации
WITH user_totals AS (
    SELECT
        u.id,
        u.name,
        SUM(o.amount) AS total_amount
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
)
SELECT
    id,
    name,
    total_amount,
    RANK() OVER (ORDER BY total_amount DESC) AS user_rank
FROM user_totals;
```
**Объяснение:**
Предварительная агрегация в CTE и индекс на поле `amount` позволяют ускорить выполнение оконной функции.

---

## 2. **Оптимизация материализованных представлений (MATERIALIZED VIEWS)**

### Неоптимизированный подход
```sql
-- Часто выполняемый сложный запрос
SELECT
    p.category_id,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.category_id;
```
Этот запрос может быть медленным, если выполняется часто и таблицы большие.

### Оптимизированный подход с материализованным представлением
```sql
-- Создаем материализованное представление
CREATE MATERIALIZED VIEW mv_category_quantity AS
SELECT
    p.category_id,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.category_id;

-- Обновляем материализованное представление при необходимости
REFRESH MATERIALIZED VIEW mv_category_quantity;

-- Используем материализованное представление
SELECT * FROM mv_category_quantity;
```
**Объяснение:**
Материализованные представления позволяют сохранить результаты сложных запросов и быстро их получать, избегая повторных вычислений.

---

## 3. **Оптимизация полнотекстового поиска (FULL TEXT SEARCH)**

### Неоптимизированный запрос
```sql
-- Получаем статьи, содержащие слово "PostgreSQL"
SELECT id, title, content
FROM articles
WHERE content LIKE '%PostgreSQL%';
```
Этот запрос выполняет полное сканирование таблицы и использует `LIKE`, что неэффективно для полнотекстового поиска.

### Оптимизированный запрос с полнотекстовым поиском
```sql
-- Добавляем столбец для полнотекстового поиска
ALTER TABLE articles ADD COLUMN content_tsvector TSVECTOR;
UPDATE articles SET content_tsvector = to_tsvector('russian', content);

-- Создаем индекс для полнотекстового поиска
CREATE INDEX idx_articles_content_tsvector ON articles USING GIN(content_tsvector);

-- Используем полнотекстовый поиск
SELECT id, title, content
FROM articles
WHERE content_tsvector @@ to_tsquery('russian', 'PostgreSQL');
```
**Объяснение:**
Использование `TSVECTOR` и `GIN`-индекса позволяет PostgreSQL эффективно выполнять полнотекстовый поиск.

---

## 4. **Использование `EXPLAIN ANALYZE` для анализа оконных функций**

### Пример анализа неоптимизированного запроса
```sql
EXPLAIN ANALYZE
SELECT
    u.id,
    u.name,
    SUM(o.amount) AS total_amount,
    RANK() OVER (ORDER BY SUM(o.amount) DESC) AS user_rank
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```
**Результат:**
```
WindowAgg (cost=1000.00..1010.00 rows=1000 width=36) (actual time=50.000..60.000 rows=1000 loops=1)
  -> Sort (cost=1000.00..1005.00 rows=1000 width=36) (actual time=40.000..50.000 rows=1000 loops=1)
        Sort Key: (sum(o.amount)) DESC
        -> HashAggregate (cost=500.00..750.00 rows=1000 width=36) (actual time=30.000..40.000 rows=1000 loops=1)
              Group Key: u.id
              -> Hash Right Join (cost=10.00..400.00 rows=10000 width=36) (actual time=1.000..20.000 rows=10000 loops=1)
                    Hash Cond: (o.user_id = u.id)
                    -> Seq Scan on orders o (cost=0.00..300.00 rows=10000 width=16) (actual time=0.000..10.000 rows=10000 loops=1)
                    -> Hash (cost=5.00..5.00 rows=1000 width=20) (actual time=0.500..0.500 rows=1000 loops=1)
                          -> Seq Scan on users u (cost=0.00..5.00 rows=1000 width=20) (actual time=0.000..0.500 rows=1000 loops=1)
```
Здесь видно, что выполняется полное сканирование таблиц (`Seq Scan`), сортировка (`Sort`) и агрегация (`HashAggregate`).

### Оптимизированный запрос с анализом
```sql
EXPLAIN ANALYZE
WITH user_totals AS (
    SELECT
        u.id,
        u.name,
        SUM(o.amount) AS total_amount
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
)
SELECT
    id,
    name,
    total_amount,
    RANK() OVER (ORDER BY total_amount DESC) AS user_rank
FROM user_totals;
```
**Результат:**
```
WindowAgg (cost=100.00..110.00 rows=1000 width=36) (actual time=1.000..2.000 rows=1000 loops=1)
  -> Sort (cost=100.00..105.00 rows=1000 width=36) (actual time=0.500..1.000 rows=1000 loops=1)
        Sort Key: user_totals.total_amount DESC
        -> HashAggregate (cost=50.00..75.00 rows=1000 width=36) (actual time=0.300..0.500 rows=1000 loops=1)
              Group Key: u.id
              -> Hash Right Join (cost=10.00..40.00 rows=10000 width=36) (actual time=0.100..0.300 rows=10000 loops=1)
                    Hash Cond: (o.user_id = u.id)
                    -> Index Scan using idx_orders_user_id on orders o (cost=0.28..30.00 rows=10000 width=16) (actual time=0.001..0.100 rows=10000 loops=1)
                    -> Hash (cost=5.00..5.00 rows=1000 width=20) (actual time=0.050..0.050 rows=1000 loops=1)
                          -> Seq Scan on users u (cost=0.00..5.00 rows=1000 width=20) (actual time=0.000..0.050 rows=1000 loops=1)
```
Теперь используется индексное сканирование (`Index Scan`), что значительно ускоряет выполнение запроса.

---

### Итог
- **Оконные функции**: Используйте CTE для предварительной агрегации и индексы для ускорения.
- **Материализованные представления**: Сохраняйте результаты сложных запросов для быстрого доступа.
- **Полнотекстовый поиск**: Используйте `TSVECTOR` и `GIN`-индексы для эффективного поиска.
- **`EXPLAIN ANALYZE`**: Всегда анализируйте план выполнения для оптимизации сложных запросов.

# Часть 9

## 1. **Оптимизация `VACUUM` и `ANALYZE`**

### Проблема с неоптимальным использованием `VACUUM`
```sql
-- Ручное выполнение VACUUM без параметров
VACUUM;
```
Эта команда выполняет `VACUUM` для всех таблиц в базе данных без учета их состояния, что может занять много времени и ресурсов.

### Оптимизированное использование `VACUUM`
```sql
-- Выполняем VACUUM только для таблиц, где это необходимо
-- Сначала проверяем статистику по таблицам
SELECT
    schemaname,
    relname,
    n_dead_tup,
    last_vacuum,
    last_autovacuum
FROM pg_stat_all_tables
WHERE n_dead_tup > 1000;  -- Таблицы с большим количеством "мертвых" строк

-- Выполняем VACUUM только для проблемных таблиц
VACUUM (VERBOSE, ANALYZE) table_name;

-- Настройка autovacuum для критичных таблиц
ALTER TABLE large_table SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05,
    autovacuum_vacuum_threshold = 1000
);
```
**Объяснение:**
- Используйте `VACUUM (VERBOSE, ANALYZE)` для конкретных таблиц, где это необходимо.
- Настройте параметры `autovacuum` для таблиц с высокой нагрузкой.
- Мониторьте состояние таблиц с помощью `pg_stat_all_tables`.

---

## 2. **Использование `pg_stat_statements` для анализа запросов**

### Установка и базовая настройка
```sql
-- Устанавливаем расширение
CREATE EXTENSION pg_stat_statements;

-- Проверяем текущие настройки
SHOW shared_preload_libraries;  -- Должно содержать pg_stat_statements
SHOW pg_stat_statements.track;  -- Должно быть 'all'
```
Если расширение не подключено, добавьте в `postgresql.conf`:
```ini
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
```
и перезапустите PostgreSQL.

### Анализ и оптимизация запросов
```sql
-- Получаем список самых долгих запросов
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    rows,
    shared_blks_hit,
    shared_blks_read
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Пример оптимизации найденного медленного запроса
-- Допустим, найден запрос:
-- SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC;

-- Оптимизируем его:
CREATE INDEX idx_users_status_created_at ON users(status, created_at DESC);
```
**Объяснение:**
- `pg_stat_statements` позволяет находить медленные запросы.
- Анализируйте `mean_exec_time`, `shared_blks_read` и создавайте индексы для оптимизации.

---

## 3. **Автоматическое разбиение таблиц с `pg_partman`**

### Установка и настройка `pg_partman`
```sql
-- Устанавливаем расширение
CREATE EXTENSION pg_partman;

-- Проверяем версию
SELECT extversion FROM pg_extension WHERE extname = 'pg_partman';
```

### Создание и управление разбитыми таблицами

#### Пример: Разбиение по времени
```sql
-- Создаем родительскую таблицу
CREATE TABLE sales (
    id BIGSERIAL,
    sale_date TIMESTAMP NOT NULL,
    amount NUMERIC,
    PRIMARY KEY (id, sale_date)
);

-- Преобразуем таблицу в разбитую по месяцам
SELECT partman.create_parent(
    p_parent_table => 'public.sales',
    p_control => 'sale_date',
    p_type => 'native',
    p_interval => 'monthly',
    p_premake => 4
);

-- Добавляем начальные разделы
SELECT partman.create_time_partitions(
    p_parent_table => 'public.sales',
    p_control => 'sale_date',
    p_type => 'native',
    p_interval => 'monthly',
    p_start_partition => '2023-01-01',
    p_end_partition => '2023-12-01'
);
```
**Объяснение:**
- `pg_partman` автоматически создает и управляет разделами.
- `p_premake` задает количество заранее созданных разделов.
- `p_interval` определяет интервал разбиения (например, `monthly`).

#### Пример: Добавление данных и автоматическое управление
```sql
-- Вставляем данные
INSERT INTO sales (sale_date, amount)
SELECT
    NOW() - (random() * (365 * 24 * 3600 || ' second'))::INTERVAL,
    random() * 1000
FROM generate_series(1, 100000);

-- Проверяем состояние разделов
SELECT * FROM partman.partition_list('public.sales');

-- Запускаем автоматическое управление разделами
CALL partman.run_maintenance();
```
**Объяснение:**
- `partman.run_maintenance()` автоматически создает новые разделы и удаляет старые.
- Используйте `partman.partition_list()` для мониторинга разделов.

---

## 4. **Использование `EXPLAIN ANALYZE` для проверки эффективности разбиения**

### Пример анализа запроса к разбитой таблице
```sql
EXPLAIN ANALYZE
SELECT SUM(amount)
FROM sales
WHERE sale_date BETWEEN '2023-06-01' AND '2023-06-30';
```
**Результат без разбиения:**
```
Aggregate (cost=1000.00..1001.00 rows=1 width=8) (actual time=50.000..50.001 rows=1 loops=1)
  -> Seq Scan on sales (cost=0.00..1000.00 rows=10000 width=8) (actual time=0.000..40.000 rows=10000 loops=1)
        Filter: ((sale_date >= '2023-06-01'::timestamp) AND (sale_date <= '2023-06-30'::timestamp))
```
**Результат с разбиением:**
```
Aggregate (cost=10.00..11.00 rows=1 width=8) (actual time=0.100..0.101 rows=1 loops=1)
  -> Append (cost=0.00..10.00 rows=1000 width=8) (actual time=0.000..0.050 rows=1000 loops=1)
        -> Seq Scan on sales_2023_06 (cost=0.00..10.00 rows=1000 width=8) (actual time=0.000..0.050 rows=1000 loops=1)
              Filter: ((sale_date >= '2023-06-01'::timestamp) AND (sale_date <= '2023-06-30'::timestamp))
```
**Объяснение:**
Разбиение позволяет PostgreSQL сканировать только нужный раздел (`sales_2023_06`), а не всю таблицу.

---

### Итог
- **`VACUUM` и `ANALYZE`**: Настройте `autovacuum` и выполняйте `VACUUM` выборочно.
- **`pg_stat_statements`**: Используйте для поиска и оптимизации медленных запросов.
- **`pg_partman`**: Автоматизируйте разбиение таблиц по времени или другим критериям.
- **`EXPLAIN ANALYZE`**: Проверяйте эффективность разбиения и оптимизации.

# Часть 10

## 1. **Оптимизация WAL (Write-Ahead Logging)**

### Проблема с неоптимальной настройкой WAL
По умолчанию PostgreSQL использует настройки WAL, которые могут не подходить для высоконагруженных систем. Например, слишком частые `fsync` или большой объем WAL могут замедлять запись.

### Оптимизированные настройки WAL
```ini
# postgresql.conf

# Увеличиваем объем WAL-буфера для уменьшения количества записей на диск
wal_buffers = 16MB  # По умолчанию: 3MB–1/32 от shared_buffers

# Настраиваем частоту сброса WAL на диск
synchronous_commit = off  # Для некритичных операций (улучшает производительность, но рискует потерей данных при сбое)
# synchronous_commit = remote_apply  # Для репликации с подтверждением применения на реплике

# Увеличиваем размер сегмента WAL для уменьшения количества файлов
wal_segment_size = 1GB  # По умолчанию: 16MB–1GB в зависимости от версии

# Настраиваем архивацию WAL для резервного копирования
wal_level = replica  # Минимальный уровень для репликации
archive_mode = on
archive_command = 'test ! -f /wal_archive/%f && cp %p /wal_archive/%f'  # Пример команды архивации
```
**Объяснение:**
- **`wal_buffers`**: Увеличение буфера WAL уменьшает количество операций записи на диск.
- **`synchronous_commit`**: Отключение (`off`) ускоряет запись, но может привести к потере данных при сбое.
- **`wal_segment_size`**: Увеличение размера сегмента WAL уменьшает количество файлов и накладные расходы.
- **Архивация WAL**: Важна для резервного копирования и восстановления (PITR).

---

## 2. **Использование `pg_bouncer` для управления подключениями**

### Проблема без `pg_bouncer`
PostgreSQL создает отдельный процесс для каждого подключения, что может привести к перегрузке системы при большом количестве клиентов.

### Установка и настройка `pg_bouncer`
```ini
# /etc/pgbouncer/pgbouncer.ini

[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = admin_user
stats_users = stats_user

# Настройки пула подключений
pool_mode = transaction  # Режим пула: session, transaction, statement
default_pool_size = 20   # Размер пула по умолчанию
min_pool_size = 5        # Минимальный размер пула
max_client_conn = 100    # Максимальное количество клиентских подключений
server_reset_query = DISCARD ALL  # Сброс состояния подключения
```
**Объяснение параметров:**
- **`pool_mode`**:
  - `session`: Подключение возвращается в пул только после завершения сессии.
  - `transaction`: Подключение возвращается в пул после завершения транзакции.
  - `statement`: Подключение возвращается в пул после выполнения каждого запроса.
- **`default_pool_size`**: Определяет количество подключений к PostgreSQL, которые `pg_bouncer` поддерживает для каждого клиента.
- **`max_client_conn`**: Максимальное количество клиентских подключений.

### Запуск `pg_bouncer`
```bash
sudo systemctl start pgbouncer
sudo systemctl enable pgbouncer
```

### Мониторинг `pg_bouncer`
```sql
-- Подключаемся к pg_bouncer и проверяем статистику
psql -p 6432 -U stats_user pgbouncer
SHOW POOLS;
```
**Объяснение:**
- `pg_bouncer` уменьшает нагрузку на PostgreSQL, управляя пулом подключений.
- Режим `transaction` подходит для большинства веб-приложений.

---

## 3. **Настройка `work_mem` и `maintenance_work_mem`**

### Проблема с неоптимальными настройками памяти
По умолчанию PostgreSQL использует небольшие значения для `work_mem` и `maintenance_work_mem`, что может привести к использованию временных файлов на диске и замедлению выполнения запросов.

### Оптимизированные настройки памяти
```ini
# postgresql.conf

# Память для операций сортировки и хэш-агрегации
work_mem = 64MB  # По умолчанию: 4MB

# Память для операций обслуживания (VACUUM, CREATE INDEX)
maintenance_work_mem = 1GB  # По умолчанию: 64MB

# Память для буфера shared_buffers (25% от общей памяти сервера)
shared_buffers = 8GB  # По умолчанию: 128MB
```
**Объяснение:**
- **`work_mem`**: Используется для сортировки (`ORDER BY`, `DISTINCT`), хэш-соединений (`JOIN`), и оконных функций. Увеличение этого параметра уменьшает использование временных файлов на диске.
- **`maintenance_work_mem`**: Используется для операций `VACUUM`, `CREATE INDEX`, и `ALTER TABLE`. Увеличение ускоряет выполнение этих операций.
- **`shared_buffers`**: Кэш данных в памяти. Рекомендуется устанавливать в 25% от общей памяти сервера.

---

## 4. **Проверка эффективности настроек с `EXPLAIN ANALYZE`**

### Пример анализа запроса с сортировкой
```sql
-- Запрос с сортировкой большого объема данных
EXPLAIN ANALYZE
SELECT * FROM large_table ORDER BY created_at DESC LIMIT 100;
```
**Результат до оптимизации `work_mem`:**
```
Limit (cost=1000.00..1000.10 rows=100 width=36) (actual time=500.000..500.010 rows=100 loops=1)
  -> Sort (cost=1000.00..1010.00 rows=4000 width=36) (actual time=500.000..500.005 rows=100 loops=1)
        Sort Key: created_at DESC
        Sort Method: external merge  Disk: 1024kB
        -> Seq Scan on large_table (cost=0.00..500.00 rows=4000 width=36) (actual time=0.000..100.000 rows=4000 loops=1)
```
Здесь видно, что сортировка использует внешний merge (`external merge`) и временные файлы на диске (`Disk: 1024kB`).

**Результат после оптимизации `work_mem`:**
```
Limit (cost=1000.00..1000.10 rows=100 width=36) (actual time=50.000..50.001 rows=100 loops=1)
  -> Sort (cost=1000.00..1010.00 rows=4000 width=36) (actual time=50.000..50.001 rows=100 loops=1)
        Sort Key: created_at DESC
        Sort Method: quicksort  Memory: 512kB
        -> Seq Scan on large_table (cost=0.00..500.00 rows=4000 width=36) (actual time=0.000..50.000 rows=4000 loops=1)
```
Теперь сортировка выполняется в памяти (`quicksort Memory: 512kB`), что значительно быстрее.

---

### Итог
- **WAL**: Настройте `wal_buffers`, `synchronous_commit`, и `wal_segment_size` для оптимизации записи.
- **`pg_bouncer`**: Используйте для управления подключениями и уменьшения нагрузки на PostgreSQL.
- **`work_mem` и `maintenance_work_mem`**: Увеличьте для ускорения сортировки и операций обслуживания.
- **`EXPLAIN ANALYZE`**: Проверяйте эффективность настроек памяти и запросов.

# Часть 11

## 1. **Оптимизация параметров `checkpoint`**

### Проблема с настройками `checkpoint` по умолчанию
По умолчанию PostgreSQL выполняет контрольные точки (`checkpoint`) каждые 5 минут или при заполнении 16MB WAL-сегментов. Это может привести к избыточным записям на диск и замедлению работы системы, особенно на SSD-накопителях.

### Оптимизированные настройки `checkpoint`
```ini
# postgresql.conf

# Увеличиваем интервал между контрольными точками
checkpoint_timeout = 30min  # По умолчанию: 5min

# Увеличиваем объем WAL между контрольными точками
max_wal_size = 4GB  # По умолчанию: 1GB
min_wal_size = 1GB  # По умолчанию: 80MB

# Настраиваем скорость записи WAL во время контрольной точки
checkpoint_completion_target = 0.9  # По умолчанию: 0.5
```
**Объяснение:**
- **`checkpoint_timeout`**: Увеличение интервала между контрольными точками уменьшает количество записей на диск.
- **`max_wal_size`** и **`min_wal_size`**: Увеличение объема WAL между контрольными точками снижает частоту их выполнения.
- **`checkpoint_completion_target`**: Увеличение этого параметра позволяет равномернее распределять нагрузку на диск во время контрольной точки.

---

## 2. **Использование `pg_prewarm` для предварительной загрузки данных в кэш**

### Установка и использование `pg_prewarm`
```sql
-- Устанавливаем расширение
CREATE EXTENSION pg_prewarm;

-- Предварительно загружаем таблицу в shared_buffers
SELECT pg_prewarm('public.large_table');

-- Предварительно загружаем индекс
SELECT pg_prewarm('public.idx_large_table_id');

-- Автоматическая загрузка после перезапуска PostgreSQL
-- Добавляем в autovacuum настройку (или используем cron)
INSERT INTO pg_prewarm.list (database, schema, relation)
SELECT datname, 'public', tablename
FROM pg_tables
WHERE schemaname = 'public' AND datname = current_database();
```
**Объяснение:**
- **`pg_prewarm`** позволяет загрузить часто используемые таблицы и индексы в `shared_buffers` заранее, что ускоряет выполнение запросов.
- Это особенно полезно после перезапуска PostgreSQL или для "холодных" баз данных.

---

## 3. **Настройка `random_page_cost` и `seq_page_cost`**

### Проблема с настройками стоимости страниц по умолчанию
По умолчанию PostgreSQL считает, что случайное чтение страницы (`random_page_cost`) в 4 раза дороже последовательного (`seq_page_cost`). Это может не соответствовать современным SSD-накопителям, где разница минимальна.

### Оптимизированные настройки стоимости страниц
```ini
# postgresql.conf

# Уменьшаем стоимость случайного чтения для SSD
random_page_cost = 1.1  # По умолчанию: 4.0
seq_page_cost = 1.0     # По умолчанию: 1.0
```
**Объяснение:**
- **`random_page_cost`**: Уменьшение этого параметра позволяет планировщику PostgreSQL чаще использовать индексы на SSD-накопителях.
- **`seq_page_cost`**: Обычно оставляют равным 1.0, так как последовательное чтение всегда быстрее случайного.

---

## 4. **Проверка эффективности настроек с помощью `EXPLAIN ANALYZE`**

### Пример анализа запроса с индексом
```sql
-- Запрос с использованием индекса
EXPLAIN ANALYZE
SELECT * FROM users WHERE id = 1000;
```
**Результат до изменения `random_page_cost` (на HDD):**
```
Index Scan using users_pkey on users (cost=0.15..8.17 rows=1 width=72) (actual time=0.020..0.021 rows=1 loops=1)
  Index Cond: (id = 1000)
```
Здесь планировщик выбирает индексное сканирование, но стоимость случайного чтения высока.

**Результат после изменения `random_page_cost` (на SSD):**
```
Index Scan using users_pkey on users (cost=0.15..1.17 rows=1 width=72) (actual time=0.005..0.006 rows=1 loops=1)
  Index Cond: (id = 1000)
```
Теперь стоимость случайного чтения ниже, и индексное сканирование становится еще более предпочтительным.

---

### Итог
- **`checkpoint`**: Увеличьте интервал и объем WAL между контрольными точками для уменьшения нагрузки на диск.
- **`pg_prewarm`**: Используйте для предварительной загрузки часто используемых таблиц и индексов в кэш.
- **`random_page_cost` и `seq_page_cost`**: Настройте в соответствии с типом накопителя (SSD/HDD).
- **`EXPLAIN ANALYZE`**: Проверяйте, как изменения параметров влияют на планы выполнения запросов.

# Часть 12

## 1. **Оптимизация `effective_cache_size`**

### Проблема с настройкой `effective_cache_size` по умолчанию
По умолчанию `effective_cache_size` установлен в 4GB, но это значение не соответствует реальному объему оперативной памяти на современных серверах. Планировщик PostgreSQL использует это значение для оценки стоимости операций чтения с диска.

### Оптимизированная настройка `effective_cache_size`
```ini
# postgresql.conf

# Устанавливаем значение, близкое к общему объему оперативной памяти сервера,
# но не превышающее его (например, 75% от общей памяти)
effective_cache_size = 24GB  # По умолчанию: 4GB
```
**Объяснение:**
- **`effective_cache_size`** сообщает планировщику PostgreSQL, сколько данных может находиться в кэше операционной системы. Это помогает планировщику выбирать более эффективные планы выполнения запросов, особенно для больших таблиц.
- Рекомендуется устанавливать значение, близкое к общему объему оперативной памяти сервера (например, 50-75% от общей памяти).

---

## 2. **Использование `pg_repack` для дефрагментации таблиц**

### Проблема с фрагментацией таблиц
Со временем таблицы и индексы в PostgreSQL могут фрагментироваться из-за частых операций `UPDATE` и `DELETE`, что приводит к увеличению их физического размера и замедлению запросов.

### Установка и использование `pg_repack`
```bash
# Устанавливаем pg_repack (например, на Ubuntu/Debian)
sudo apt-get install postgresql-15-repack
```

```sql
-- Подключаем расширение в базе данных
CREATE EXTENSION pg_repack;

-- Запускаем дефрагментацию для конкретной таблицы
-- (требует подключения к базе данных с правами суперпользователя)
\c your_database
SELECT pg_repack_repack_table('public.large_table');
```
**Дополнительные опции:**
```sql
-- Дефрагментация таблицы с индексами
SELECT pg_repack_repack_table('public.large_table', 'indexes');

-- Дефрагментация всей базы данных
SELECT pg_repack_repack_database();
```
**Объяснение:**
- **`pg_repack`** позволяет дефрагментировать таблицы и индексы без блокировки таблиц на запись (в отличие от `VACUUM FULL`).
- Это особенно полезно для больших таблиц, где `VACUUM FULL` может занять много времени и заблокировать работу приложения.

---

## 3. **Настройка `max_parallel_workers_per_gather`**

### Проблема с параллельным выполнением запросов
По умолчанию PostgreSQL ограничивает количество параллельных воркеров для операций сбора данных (`Gather`), что может замедлять выполнение сложных запросов на многоядерных системах.

### Оптимизированная настройка параллельных воркеров
```ini
# postgresql.conf

# Устанавливаем максимальное количество параллельных воркеров для одного запроса
max_parallel_workers_per_gather = 8  # По умолчанию: 2

# Общее количество параллельных воркеров в системе
max_worker_processes = 16  # По умолчанию: 8
max_parallel_workers = 16 # По умолчанию: 8

# Включаем параллельное выполнение для конкретных операций
parallel_setup_cost = 1000   # По умолчанию: 1000
parallel_tuple_cost = 0.1    # По умолчанию: 0.1
min_parallel_table_scan_size = 16MB  # По умолчанию: 8MB
min_parallel_index_scan_size = 512KB # По умолчанию: 512KB
```
**Объяснение:**
- **`max_parallel_workers_per_gather`**: Определяет максимальное количество параллельных процессов, которые могут быть использованы для одного запроса. Увеличение этого параметра позволяет ускорить выполнение сложных запросов на многоядерных системах.
- **`max_worker_processes`** и **`max_parallel_workers`**: Определяют общее количество параллельных процессов, доступных в системе.
- **`min_parallel_table_scan_size`** и **`min_parallel_index_scan_size`**: Минимальный размер таблицы или индекса, при котором PostgreSQL будет рассматривать возможность параллельного сканирования.

---

## 4. **Проверка эффективности настроек с помощью `EXPLAIN ANALYZE`**

### Пример анализа параллельного запроса
```sql
-- Запрос с агрегацией по большой таблице
EXPLAIN ANALYZE
SELECT category_id, SUM(amount)
FROM large_table
GROUP BY category_id;
```
**Результат до настройки параллельных воркеров:**
```
HashAggregate (cost=10000.00..10100.00 rows=1000 width=16) (actual time=500.000..500.010 rows=1000 loops=1)
  Group Key: category_id
  -> Seq Scan on large_table (cost=0.00..5000.00 rows=100000 width=16) (actual time=0.000..400.000 rows=100000 loops=1)
```
Запрос выполняется последовательно.

**Результат после настройки параллельных воркеров:**
```
Finalize HashAggregate (cost=10000.00..10100.00 rows=1000 width=16) (actual time=100.000..100.010 rows=1000 loops=1)
  Group Key: category_id
  -> Gather (cost=9999.00..10099.00 rows=1000 width=16) (actual time=90.000..99.000 rows=1000 loops=1)
        Workers Planned: 8
        Workers Launched: 8
        -> Partial HashAggregate (cost=9999.00..9999.10 rows=125 width=16) (actual time=85.000..85.001 rows=125 loops=9)
              Group Key: category_id
              -> Parallel Seq Scan on large_table (cost=0.00..4000.00 rows=12500 width=16) (actual time=0.000..50.000 rows=12500 loops=9)
```
Теперь запрос выполняется параллельно с использованием 8 воркеров, что значительно ускоряет его выполнение.

---

### Итог
- **`effective_cache_size`**: Установите значение, близкое к объему оперативной памяти сервера, чтобы помочь планировщику выбирать более эффективные планы.
- **`pg_repack`**: Используйте для дефрагментации таблиц и индексов без блокировки на запись.
- **`max_parallel_workers_per_gather`**: Увеличьте для ускорения выполнения сложных запросов на многоядерных системах.
- **`EXPLAIN ANALYZE`**: Проверяйте, как изменения параметров влияют на планы выполнения запросов.

Примеры для других сценариев (например, оптимизация `shared_buffers`, использование `pgBadger` для анализа логов, настройка `huge_pages`)