Разбор **EXPLAIN PLAN** — ключевой навык для оптимизации запросов. Этот инструмент показывает, **как PostgreSQL выполняет запрос**, и помогает найти узкие места. Давай разберём, как читать планы, на что обращать внимание и как улучшать производительность.

---

## **1. Как получить план выполнения запроса**
### **1.1. Базовый `EXPLAIN`**
Показывает **логический план выполнения** (без реального выполнения запроса):
```sql
EXPLAIN
SELECT * FROM customers WHERE last_name = 'Иванов';
```

### **1.2. `EXPLAIN ANALYZE`**
Показывает **реальное время выполнения** и статистику (выполняет запрос):
```sql
EXPLAIN ANALYZE
SELECT * FROM customers WHERE last_name = 'Иванов';
```

### **1.3. Форматы вывода**
- **Текстовый** (по умолчанию):
  ```sql
  EXPLAIN SELECT * FROM customers WHERE last_name = 'Иванов';
  ```
- **JSON** (удобно для анализа):
  ```sql
  EXPLAIN (FORMAT JSON) SELECT * FROM customers WHERE last_name = 'Иванов';
  ```
- **XML/YAML** (реже используется).

---

## **2. Структура плана выполнения**
План читается **снизу вверх** (или справа налево в графических инструментах, например, **pgAdmin** или **PEV**). Каждый узел плана — это **операция**, которую выполняет PostgreSQL.

### **2.1. Пример плана**
```sql
EXPLAIN ANALYZE
SELECT * FROM customers WHERE last_name = 'Иванов';
```
```
QUERY PLAN
--------------------------------------------------------------------------------------------------------
Seq Scan on customers  (cost=0.00..18.10 rows=1 width=72) (actual time=0.014..0.237 rows=1 loops=1)
  Filter: (last_name = 'Иванов'::text)
  Rows Removed by Filter: 9999
Planning Time: 0.078 ms
Execution Time: 0.251 ms
```

### **2.2. Основные элементы плана**
| Элемент               | Описание                                                                                     |
|------------------------|----------------------------------------------------------------------------------------------|
| **Seq Scan**           | Полное сканирование таблицы (`TABLE ACCESS FULL` в Oracle). Медленная операция.               |
| **Index Scan**         | Сканирование по индексу. Быстрое, если индекс подходит.                                      |
| **Bitmap Heap Scan**   | Используется для объединения результатов нескольких индексов.                                |
| **Nested Loop**        | Вложенный цикл для соединения таблиц (`JOIN`). Медлен, если таблицы большие.                  |
| **Hash Join**          | Хэш-соединение. Быстро для больших таблиц, если хэш-таблица помещается в память.               |
| **Merge Join**         | Соединение слиянием. Быстро, если данные отсортированы.                                      |
| **Sort**               | Сортировка результатов. Медленная операция для больших наборов данных.                       |
| **Aggregate**          | Агрегация (например, `GROUP BY`, `COUNT`, `SUM`).                                            |
| **Filter**             | Фильтрация строк по условию (`WHERE`).                                                       |
| **Rows Removed by Filter** | Количество строк, отфильтрованных условием.                                                 |
| **cost**               | Оценка затрат (в условных единицах). `cost=0.00..18.10` — начальная и конечная стоимость.       |
| **rows**               | Оценка количества возвращаемых строк.                                                       |
| **width**              | Средний размер строки в байтах.                                                              |
| **actual time**        | Реальное время выполнения (в миллисекундах).                                                |
| **loops**              | Количество повторений операции (например, для вложенных циклов).                              |
| **Planning Time**       | Время планирования запроса.                                                                 |
| **Execution Time**      | Общее время выполнения запроса.                                                             |

---

## **3. На что обратить внимание в плане**
### **3.1. Типы сканирования (Scans)**
| Тип сканирования       | Описание                                                                                     | Что делать, если медленно                     |
|------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------|
| **Seq Scan**            | Полное сканирование таблицы. Медленное для больших таблиц.                                   | Добавить индекс или оптимизировать запрос.     |
| **Index Scan**          | Сканирование по индексу. Быстрое, если индекс подходит.                                      | Проверить, почему не используется индекс.     |
| **Bitmap Heap Scan**    | Используется для объединения нескольких индексов. Может быть медленным, если много строк.     | Оптимизировать условия или индексы.           |

#### **Пример: Seq Scan vs Index Scan**
- **Плохо (Seq Scan)**:
  ```
  Seq Scan on customers  (cost=0.00..18.10 rows=1 width=72) (actual time=0.014..0.237 rows=1 loops=1)
    Filter: (last_name = 'Иванов'::text)
    Rows Removed by Filter: 9999
  ```
  - **Проблема**: Полное сканирование таблицы (`Seq Scan`), хотя есть условие `WHERE`.
  - **Решение**: Добавить индекс на `last_name`.

- **Хорошо (Index Scan)**:
  ```
  Index Scan using idx_customers_last_name on customers  (cost=0.14..8.16 rows=1 width=72) (actual time=0.021..0.022 rows=1 loops=1)
    Index Cond: (last_name = 'Иванов'::text)
  ```
  - **Преимущество**: Используется индекс (`Index Scan`), запрос выполняется быстро.

---

### **3.2. Соединения (Joins)**
| Тип соединения         | Описание                                                                                     | Когда использовать                          |
|------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------|
| **Nested Loop**        | Вложенный цикл. Быстро для маленьких таблиц.                                                 | Для соединения маленьких таблиц.             |
| **Hash Join**          | Хэш-соединение. Быстро для больших таблиц, если хэш-таблица помещается в память.               | Для соединения больших таблиц.               |
| **Merge Join**         | Соединение слиянием. Быстро, если данные отсортированы.                                      | Если данные уже отсортированы по ключу.      |

#### **Пример: Медленный Nested Loop**
```
Nested Loop  (cost=0.28..18.30 rows=1 width=72) (actual time=0.045..0.245 rows=1 loops=1)
  ->  Seq Scan on orders  (cost=0.00..10.20 rows=1 width=72) (actual time=0.014..0.123 rows=1 loops=1)
        Filter: (customer_id = 1)
  ->  Seq Scan on customers  (cost=0.00..8.10 rows=1 width=72) (actual time=0.010..0.110 rows=1 loops=1)
        Filter: (id = 1)
```
- **Проблема**: Полное сканирование обеих таблиц (`Seq Scan`) в `Nested Loop`.
- **Решение**: Добавить индексы на `orders(customer_id)` и `customers(id)`.

---

### **3.3. Сортировка (Sort)**
- **Проблема**: Сортировка больших наборов данных (`Sort`) может быть медленной.
- **Пример**:
  ```
  Sort  (cost=18.30..18.31 rows=1 width=72) (actual time=0.245..0.246 rows=1 loops=1)
    Sort Key: customers.last_name
    Sort Method: quicksort  Memory: 25kB
    ->  Seq Scan on customers  (cost=0.00..18.10 rows=1 width=72) (actual time=0.014..0.230 rows=1 loops=1)
  ```
- **Решение**:
  - Добавить индекс на столбец, по которому сортируете:
    ```sql
    CREATE INDEX idx_customers_last_name ON customers(last_name);
    ```
  - Использовать `ORDER BY` по индексированному столбцу.

---

### **3.4. Агрегация (Aggregate)**
- **Проблема**: Агрегация больших наборов данных (`GROUP BY`, `COUNT`, `SUM`) может быть медленной.
- **Пример**:
  ```
  Aggregate  (cost=18.30..18.31 rows=1 width=8) (actual time=0.245..0.246 rows=1 loops=1)
    ->  Seq Scan on orders  (cost=0.00..18.10 rows=1 width=8) (actual time=0.014..0.230 rows=1 loops=1)
  ```
- **Решение**:
  - Добавить индекс на столбцы, участвующие в `GROUP BY`.
  - Использовать **материализованные представления** для часто используемых агрегатов.

---

### **3.5. Фильтрация (Filter)**
- **Проблема**: Если `Rows Removed by Filter` большое, значит фильтр отсеивает много строк, и сканирование неэффективно.
- **Пример**:
  ```
  Seq Scan on customers  (cost=0.00..18.10 rows=1 width=72) (actual time=0.014..0.237 rows=1 loops=1)
    Filter: (last_name = 'Иванов'::text)
    Rows Removed by Filter: 9999
  ```
- **Решение**: Добавить индекс на столбец `last_name`.

---

## **4. Как улучшить производительность**
### **4.1. Добавить индексы**
- Если в плане есть `Seq Scan` для таблицы с условием `WHERE`, добавьте индекс:
  ```sql
  CREATE INDEX idx_customers_last_name ON customers(last_name);
  ```

### **4.2. Оптимизировать соединения (Joins)**
- Для `Nested Loop` убедитесь, что внутренняя таблица маленькая.
- Для `Hash Join` убедитесь, что хэш-таблица помещается в память (`work_mem`).
- Для `Merge Join` убедитесь, что данные отсортированы по ключу соединения.

### **4.3. Избегать сортировки (Sort)**
- Используйте индексы для `ORDER BY`.
- Увеличьте `work_mem`, если сортировка происходит в памяти.

### **4.4. Оптимизировать агрегацию (Aggregate)**
- Добавляйте индексы на столбцы в `GROUP BY`.
- Используйте материализованные представления для часто используемых агрегатов.

### **4.5. Настройка параметров PostgreSQL**
- **`shared_buffers`**: Увеличьте для кэширования данных.
- **`work_mem`**: Увеличьте для сортировки и хэш-соединений.
- **`effective_cache_size`**: Укажите реальный объём кэша (ОЗУ).

---

## **5. Примеры оптимизации**
### **5.1. Оптимизация запроса с `Seq Scan`**
**Исходный запрос**:
```sql
EXPLAIN ANALYZE
SELECT * FROM customers WHERE last_name = 'Иванов';
```
```
Seq Scan on customers  (cost=0.00..18.10 rows=1 width=72) (actual time=0.014..0.237 rows=1 loops=1)
  Filter: (last_name = 'Иванов'::text)
  Rows Removed by Filter: 9999
```

**Решение**: Добавить индекс.
```sql
CREATE INDEX idx_customers_last_name ON customers(last_name);
```

**Результат**:
```
Index Scan using idx_customers_last_name on customers  (cost=0.14..8.16 rows=1 width=72) (actual time=0.021..0.022 rows=1 loops=1)
  Index Cond: (last_name = 'Иванов'::text)
```

---

### **5.2. Оптимизация соединения (Join)**
**Исходный запрос**:
```sql
EXPLAIN ANALYZE
SELECT * FROM orders JOIN customers ON orders.customer_id = customers.id
WHERE customers.last_name = 'Иванов';
```
```
Nested Loop  (cost=0.28..18.30 rows=1 width=72) (actual time=0.045..0.245 rows=1 loops=1)
  ->  Seq Scan on customers  (cost=0.00..8.10 rows=1 width=72) (actual time=0.014..0.123 rows=1 loops=1)
        Filter: (last_name = 'Иванов'::text)
  ->  Seq Scan on orders  (cost=0.00..10.20 rows=1 width=72) (actual time=0.010..0.110 rows=1 loops=1)
        Filter: (customer_id = 1)
```

**Решение**: Добавить индексы на `customers(last_name)` и `orders(customer_id)`.
```sql
CREATE INDEX idx_customers_last_name ON customers(last_name);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Результат**:
```
Nested Loop  (cost=0.28..8.30 rows=1 width=72) (actual time=0.021..0.030 rows=1 loops=1)
  ->  Index Scan using idx_customers_last_name on customers  (cost=0.14..4.16 rows=1 width=72) (actual time=0.010..0.011 rows=1 loops=1)
        Index Cond: (last_name = 'Иванов'::text)
  ->  Index Scan using idx_orders_customer_id on orders  (cost=0.14..4.14 rows=1 width=72) (actual time=0.005..0.006 rows=1 loops=1)
        Index Cond: (customer_id = customers.id)
```

---

## **6. Инструменты для анализа планов**
1. **`EXPLAIN ANALYZE`** — основной инструмент для анализа.
2. **pgAdmin** — графический интерфейс для визуализации планов.
3. **PEV (Postgres Explain Visualizer)** — онлайн-инструмент для визуализации: [pev](https://explain.depesz.com/).
4. **Auto Explain** — расширение для логирования планов медленных запросов:
   ```sql
   -- Настройка Auto Explain
   ALTER SYSTEM SET shared_preload_libraries = 'auto_explain';
   ALTER SYSTEM SET auto_explain.log_min_duration = '100ms';  -- Логировать запросы медленнее 100 мс
   ALTER SYSTEM SET auto_explain.log_analyze = on;  -- Включить ANALYZE
   ```

---

## **7. Итоговые рекомендации**
1. **Ищите `Seq Scan`** — если есть условие `WHERE`, добавьте индекс.
2. **Проверяйте соединения (`Joins`)** — убедитесь, что используются индексы.
3. **Избегайте сортировки (`Sort`)** — используйте индексы для `ORDER BY`.
4. **Оптимизируйте агрегацию (`Aggregate`)** — добавьте индексы на `GROUP BY`.
5. **Настройте параметры PostgreSQL** (`work_mem`, `shared_buffers`).
6. **Используйте `EXPLAIN ANALYZE`** для реальных метрик времени.
7. **Логируйте медленные запросы** с помощью `Auto Explain`.

---