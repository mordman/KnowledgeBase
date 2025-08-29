### **1. Регистр и форматирование**
- **Ключевые слова:** Пишите в **ВЕРХНЕМ РЕГИСТРЕ** (например, `SELECT`, `FROM`, `WHERE`, `JOIN`).
- **Имена таблиц и столбцов:** Используйте **нижний регистр** или **PascalCase** (в зависимости от соглашений вашей команды).
  ```sql
  SELECT user_id, first_name, last_name
  FROM Users
  WHERE status = 'active';
  ```

- **Отступы:** Используйте отступы для выравнивания логических блоков:
  ```sql
  SELECT
      u.user_id,
      u.first_name,
      u.last_name
  FROM
      Users u
  WHERE
      u.status = 'active'
      AND u.created_at > '2023-01-01';
  ```

---

### **2. Именование**
- **Таблицы:** Используйте существительные в единственном числе (например, `User`, `Order`, `Product`).
- **Столбцы:** Называйте их ясно и кратко (например, `user_id`, `created_at`, `total_price`).
- **Первичные ключи:** Обычно `id` или `<table_name>_id` (например, `user_id`).
- **Внешние ключи:** `<referenced_table>_id` (например, `order_id` в таблице `OrderItems`).

---

### **3. Псевдонимы (Aliases)**
- Используйте короткие и понятные псевдонимы для таблиц:
  ```sql
  SELECT
      u.user_id,
      o.order_date
  FROM
      Users u
  JOIN
      Orders o ON u.user_id = o.user_id;
  ```
- Для столбцов используйте псевдонимы, если имя слишком длинное или неинформативное:
  ```sql
  SELECT
      COUNT(*) AS total_users
  FROM
      Users;
  ```

---

### **4. Условия и операторы**
- Каждое условие в `WHERE` или `JOIN` размещайте на отдельной строке:
  ```sql
  SELECT
      u.user_id,
      u.first_name
  FROM
      Users u
  WHERE
      u.status = 'active'
      AND u.age > 18
      AND u.country = 'Russia';
  ```

- Используйте скобки для группировки условий:
  ```sql
  SELECT
      *
  FROM
      Orders
  WHERE
      (status = 'shipped' OR status = 'delivered')
      AND order_date > '2024-01-01';
  ```

---

### **5. JOIN-ы**
- Размещайте каждый `JOIN` на отдельной строке:
  ```sql
  SELECT
      o.order_id,
      u.first_name,
      p.product_name
  FROM
      Orders o
  JOIN
      Users u ON o.user_id = u.user_id
  JOIN
      Products p ON o.product_id = p.product_id;
  ```

---

### **6. Подзапросы**
- Форматируйте подзапросы с отступами:
  ```sql
  SELECT
      user_id,
      first_name
  FROM
      Users
  WHERE
      user_id IN (
          SELECT
              user_id
          FROM
              Orders
          WHERE
              order_date > '2024-01-01'
      );
  ```

---

### **7. Комментарии**
- Используйте комментарии для объяснения сложных запросов или логики:
  ```sql
  -- Получаем активных пользователей, которые сделали заказ в 2024 году
  SELECT
      u.user_id,
      u.first_name
  FROM
      Users u
  JOIN
      Orders o ON u.user_id = o.user_id
  WHERE
      u.status = 'active'
      AND o.order_date >= '2024-01-01';
  ```

---

### **8. Транзакции**
- Явно указывайте начало и конец транзакций:
  ```sql
  BEGIN TRANSACTION;

  UPDATE
      Accounts
  SET
      balance = balance - 100
  WHERE
      account_id = 123;

  UPDATE
      Accounts
  SET
      balance = balance + 100
  WHERE
      account_id = 456;

  COMMIT;
  ```

---

### **9. Избегайте `SELECT *`**
- Всегда указывайте конкретные столбцы, чтобы избежать лишних данных и улучшить производительность:
  ```sql
  -- Плохо
  SELECT * FROM Users;

  -- Хорошо
  SELECT user_id, first_name, last_name FROM Users;
  ```

---

### **10. Индексация и производительность**
- Указывайте индексы для часто используемых столбцов в `WHERE`, `JOIN` или `ORDER BY`.
- Избегайте сложных подзапросов в `WHERE`, если их можно заменить на `JOIN`.

---

### **Пример полного запроса**
```sql
-- Получаем список активных пользователей с их последними заказами
SELECT
    u.user_id,
    u.first_name,
    u.last_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM
    Users u
JOIN
    Orders o ON u.user_id = o.user_id
WHERE
    u.status = 'active'
    AND o.order_date = (
        SELECT
            MAX(order_date)
        FROM
            Orders o2
        WHERE
            o2.user_id = u.user_id
    )
ORDER BY
    o.order_date DESC;
```