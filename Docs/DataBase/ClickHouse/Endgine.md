Вот подробное описание основных **движков таблиц ClickHouse** с примерами конфигураций и сценариями использования:

---

## **1. MergeTree и его семейство**


## Оглавление
- [**1. MergeTree и его семейство**](#1-mergetree-и-его-семейство)
  - [**MergeTree**](#mergetree)
  - [**ReplicatedMergeTree**](#replicatedmergetree)
  - [**SummingMergeTree**](#summingmergetree)
  - [**AggregatingMergeTree**](#aggregatingmergetree)
  - [**CollapsingMergeTree**](#collapsingmergetree)
  - [**VersionedCollapsingMergeTree**](#versionedcollapsingmergetree)
  - [**GraphiteMergeTree**](#graphitemergetree)
- [**2. Log-семейство**](#2-log-семейство)
  - [**TinyLog**](#tinylog)
  - [**StripeLog**](#stripelog)
  - [**Log**](#log)
- [**3. Интеграционные движки**](#3-интеграционные-движки)
  - [**Kafka**](#kafka)
  - [**MySQL**](#mysql)
  - [**JDBC**](#jdbc)
  - [**HDFS**](#hdfs)
  - [**S3**](#s3)
- [**4. Специальные движки**](#4-специальные-движки)
  - [**Distributed**](#distributed)
  - [**MaterializedView**](#materializedview)
  - [**Dictionary**](#dictionary)
  - [**File**](#file)
  - [**URL**](#url)
  - [**EmbeddedRocksDB**](#embeddedrocksdb)
- [**5. Системные движки**](#5-системные-движки)
  - [**System**](#system)
  - [**Memory**](#memory)
- [**Вывод**](#вывод)

  - [**MergeTree**](#mergetree)
  - [**ReplicatedMergeTree**](#replicatedmergetree)
  - [**SummingMergeTree**](#summingmergetree)
  - [**AggregatingMergeTree**](#aggregatingmergetree)
  - [**CollapsingMergeTree**](#collapsingmergetree)
  - [**VersionedCollapsingMergeTree**](#versionedcollapsingmergetree)
  - [**GraphiteMergeTree**](#graphitemergetree)
  - [**TinyLog**](#tinylog)
  - [**StripeLog**](#stripelog)
  - [**Log**](#log)
  - [**Kafka**](#kafka)
  - [**MySQL**](#mysql)
  - [**JDBC**](#jdbc)
  - [**HDFS**](#hdfs)
  - [**S3**](#s3)
  - [**Distributed**](#distributed)
  - [**MaterializedView**](#materializedview)
  - [**Dictionary**](#dictionary)
  - [**File**](#file)
  - [**URL**](#url)
  - [**EmbeddedRocksDB**](#embeddedrocksdb)
  - [**System**](#system)
  - [**Memory**](#memory)
**Тип:** Физическое хранение данных.
**Особенности:**
- Поддержка **индексации**, **сжатия**, **фоновых слияний** и **репликации**.
- Оптимизированы для **аналитических запросов** и работы с большими объёмами данных.

---

### **MergeTree**
**Описание:**
Базовый движок для хранения данных в виде **частей (parts)**, которые периодически сливаются для оптимизации производительности.

**Сценарии использования:**
- Хранение **логических данных** (например, логов веб-серверов).
- Аналитика **временных рядов** (метрики, события).

**Пример конфигурации:**
```sql
CREATE TABLE events (
    event_date Date,
    event_time DateTime,
    user_id UInt64,
    event_type String,
    data String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, event_type, user_id)
SETTINGS index_granularity = 8192;
```
- **`PARTITION BY`** — разбивает данные по месяцам для ускорения запросов.
- **`ORDER BY`** — определяет порядок сортировки для индексации.
- **`index_granularity`** — размер блока индекса (влияет на скорость чтения).

---

### **ReplicatedMergeTree**
**Описание:**
Расширение `MergeTree` с поддержкой **репликации** между серверами. Используется для обеспечения **отказоустойчивости**.

**Сценарии использования:**
- Распределённые системы с **несколькими репликами** (например, кластер ClickHouse в разных дата-центрах).
- Системы, где важна **высокая доступность** данных.

**Пример конфигурации:**
```sql
CREATE TABLE events_replicated (
    event_date Date,
    event_time DateTime,
    user_id UInt64,
    event_type String,
    data String
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/events_replicated', '{replica}')
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, event_type, user_id);
```
- **`/clickhouse/tables/{shard}/events_replicated`** — путь к данным в ZooKeeper.
- **`{replica}`** — идентификатор реплики.

---

### **SummingMergeTree**
**Описание:**
Автоматически **суммирует** значения с одинаковыми ключами при слиянии частей.

**Сценарии использования:**
- **Агрегация метрик** (например, суммирование количества событий за день).
- **Финансовые данные** (например, суммирование транзакций по счетам).

**Пример конфигурации:**
```sql
CREATE TABLE metrics (
    date Date,
    metric_name String,
    value UInt64
) ENGINE = SummingMergeTree()
ORDER BY (date, metric_name);
```
- При слиянии строк с одинаковыми `date` и `metric_name` значения `value` будут суммированы.

---

### **AggregatingMergeTree**
**Описание:**
Хранит **предварительно агрегированные данные** и поддерживает агрегатные функции (например, `sum`, `count`, `avg`).

**Сценарии использования:**
- **Аналитика с предварительной агрегацией** (например, расчёт средних значений по группам).
- **Ускорение запросов** за счёт хранения агрегатов.

**Пример конфигурации:**
```sql
CREATE TABLE aggregated_events (
    event_date Date,
    event_type String,
    user_count SimpleAggregateFunction(count, UInt64),
    total_value SimpleAggregateFunction(sum, UInt64)
) ENGINE = AggregatingMergeTree()
ORDER BY (event_date, event_type);
```
- **`SimpleAggregateFunction`** — специальный тип данных для хранения агрегатов.

---

### **CollapsingMergeTree**
**Описание:**
Удаляет **дубликаты** по заданному правилу (например, по полю `Sign`).

**Сценарии использования:**
- **Обработка потоковых данных** с возможными дублями (например, данные из Kafka).
- **Хранение только актуальных версий** записей.

**Пример конфигурации:**
```sql
CREATE TABLE collapsing_events (
    event_date Date,
    event_id UInt64,
    user_id UInt64,
    data String,
    version Int32,
    sign Int8
) ENGINE = CollapsingMergeTree(sign)
ORDER BY (event_date, event_id);
```
- **`sign`** — поле, определяющее, какая запись актуальна (`1` — актуальная, `-1` — устаревшая).

---

### **VersionedCollapsingMergeTree**
**Описание:**
Улучшенная версия `CollapsingMergeTree` для работы с **версиями данных**.

**Сценарии использования:**
- **Хранение истории изменений** (например, история заказов в интернет-магазине).

**Пример конфигурации:**
```sql
CREATE TABLE versioned_events (
    event_date Date,
    event_id UInt64,
    user_id UInt64,
    data String,
    version UInt64
) ENGINE = VersionedCollapsingMergeTree(version, event_id)
ORDER BY (event_date, event_id);
```
- **`version`** — поле с версией записи.

---

### **GraphiteMergeTree**
**Описание:**
Оптимизирован для хранения **метрик** в формате **Graphite**.

**Сценарии использования:**
- **Мониторинг систем** (например, хранение метрик с Graphite).

**Пример конфигурации:**
```sql
CREATE TABLE graphite_data (
    date Date,
    name String,
    value Float64,
    timestamp DateTime
) ENGINE = GraphiteMergeTree(date, (name), 8192, 'graphite_rollup');
```
- **`graphite_rollup`** — правило агрегации метрик.

---

---

## **2. Log-семейство**
**Тип:** Простое хранение данных без индексации.
**Особенности:**
- **Низкая задержка записи**.
- **Нет поддержки индексов** (медленные запросы на больших объёмах данных).

---

### **TinyLog**
**Описание:**
Минималистичный движок для хранения данных в виде **одного файла**.

**Сценарии использования:**
- **Временные данные** (например, промежуточные результаты ETL).
- **Логи с низкой нагрузкой**.

**Пример конфигурации:**
```sql
CREATE TABLE tiny_log (
    timestamp DateTime,
    message String
) ENGINE = TinyLog();
```

---

### **StripeLog**
**Описание:**
Разбивает данные на **"полосы"** (stripe) для более эффективного хранения.

**Сценарии использования:**
- **Логи с умеренной нагрузкой**.

**Пример конфигурации:**
```sql
CREATE TABLE stripe_log (
    timestamp DateTime,
    message String
) ENGINE = StripeLog();
```

---

### **Log**
**Описание:**
Базовый движок для логов.

**Сценарии использования:**
- **Простое хранение логов** без требований к производительности.

**Пример конфигурации:**
```sql
CREATE TABLE simple_log (
    timestamp DateTime,
    message String
) ENGINE = Log();
```

---

---

## **3. Интеграционные движки**
**Тип:** Работа с внешними системами.

---

### **Kafka**
**Описание:**
Позволяет **читать и записывать данные** в **Apache Kafka**.

**Сценарии использования:**
- **Потоковая обработка данных** (например, логи в реальном времени).
- **Интеграция с системами очередей**.

**Пример конфигурации:**
```sql
CREATE TABLE kafka_events (
    timestamp DateTime,
    message String
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'kafka-broker:9092',
    kafka_topic_list = 'events',
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSONEachRow';
```

---

### **MySQL**
**Описание:**
Предоставляет доступ к данным в **MySQL**.

**Сценарии использования:**
- **Миграция данных** из MySQL в ClickHouse.
- **Объединение данных** из разных источников.

**Пример конфигурации:**
```sql
CREATE TABLE mysql_data (
    id UInt32,
    name String
) ENGINE = MySQL('host:port', 'database', 'table', 'user', 'password');
```

---

### **JDBC**
**Описание:**
Подключение к **любым базам данных** через JDBC-драйвер.

**Сценарии использования:**
- **Интеграция с PostgreSQL, Oracle, MS SQL** и другими СУБД.

**Пример конфигурации:**
```sql
CREATE TABLE jdbc_data (
    id UInt32,
    name String
) ENGINE = JDBC('jdbc:postgresql://host:port/database', 'table', 'user', 'password');
```

---

### **HDFS**
**Описание:**
Работа с данными в **Hadoop Distributed File System**.

**Сценарии использования:**
- **Аналитика больших данных** в экосистеме Hadoop.

**Пример конфигурации:**
```sql
CREATE TABLE hdfs_data (
    id UInt32,
    data String
) ENGINE = HDFS('hdfs://namenode:port/path/to/data', 'format');
```

---

### **S3**
**Описание:**
Работа с данными в **Amazon S3** или совместимых хранилищах.

**Сценарии использования:**
- **Хранение и анализ данных** в облачных хранилищах.

**Пример конфигурации:**
```sql
CREATE TABLE s3_data (
    id UInt32,
    data String
) ENGINE = S3('https://bucket.s3.amazonaws.com/path/to/data', 'access_key', 'secret_key', 'format');
```

---

---

## **4. Специальные движки**

---

### **Distributed**
**Описание:**
Распределяет запросы между **несколькими серверами** в кластере.

**Сценарии использования:**
- **Горизонтальное масштабирование** запросов.
- **Распределённая обработка данных**.

**Пример конфигурации:**
```sql
CREATE TABLE distributed_events (
    event_date Date,
    event_time DateTime,
    user_id UInt64,
    event_type String,
    data String
) ENGINE = Distributed('cluster_name', 'database', 'local_table', rand());
```
- **`cluster_name`** — имя кластера в конфигурации ClickHouse.
- **`local_table`** — таблица на каждом сервере кластера.

---

### **MaterializedView**
**Описание:**
Создаёт **материализованные представления**, которые автоматически обновляются при изменении данных.

**Сценарии использования:**
- **Ускорение запросов** за счёт предварительно вычисленных данных.
- **Агрегация данных** в реальном времени.

**Пример конфигурации:**
```sql
CREATE MATERIALIZED VIEW mv_events_daily
ENGINE = SummingMergeTree()
ORDER BY (event_date, event_type)
AS SELECT
    toDate(event_time) AS event_date,
    event_type,
    count() AS event_count
FROM events
GROUP BY event_date, event_type;
```

---

### **Dictionary**
**Описание:**
Хранит **справочные данные** (словарь) для быстрого доступа.

**Сценарии использования:**
- **Обогащение данных** (например, подстановка названий городов по коду).
- **Кэширование справочников**.

**Пример конфигурации:**
```sql
CREATE DICTIONARY city_dict (
    city_id UInt64,
    city_name String
)
PRIMARY KEY city_id
SOURCE(CLICKHOUSE(TABLE 'cities'))
LIFETIME(3600)
LAYOUT(HASHED());
```

---

### **File**
**Описание:**
Позволяет работать с данными в **файлах** (CSV, JSON, Parquet).

**Сценарии использования:**
- **Импорт/экспорт данных** из файлов.
- **Анализ данных** без загрузки в базу.

**Пример конфигурации:**
```sql
CREATE TABLE file_data (
    id UInt32,
    data String
) ENGINE = File(CSV, '/path/to/data.csv');
```

---

### **URL**
**Описание:**
Считывает данные по **HTTP/HTTPS**.

**Сценарии использования:**
- **Загрузка данных** из внешних API.
- **Анализ данных** в реальном времени.

**Пример конфигурации:**
```sql
CREATE TABLE url_data (
    id UInt32,
    data String
) ENGINE = URL('https://example.com/data.csv', CSV);
```

---

### **EmbeddedRocksDB**
**Описание:**
Встраиваемая **ключ-значение база данных** на основе **RocksDB**.

**Сценарии использования:**
- **Хранение небольших объёмов данных** с высокой скоростью доступа.
- **Кэширование**.

**Пример конфигурации:**
```sql
CREATE TABLE rocksdb_cache (
    key String,
    value String
) ENGINE = EmbeddedRocksDB(PRIMARY KEY key);
```

---

---

## **5. Системные движки**

---

### **System**
**Описание:**
Предоставляет доступ к **системным таблицам** ClickHouse (например, `system.tables`, `system.metrics`).

**Сценарии использования:**
- **Мониторинг** состояния сервера.
- **Анализ производительности** запросов.

**Пример запроса:**
```sql
SELECT * FROM system.tables;
```

---

### **Memory**
**Описание:**
Хранит данные в **оперативной памяти**.

**Сценарии использования:**
- **Временные таблицы** для промежуточных результатов.
- **Тестирование** без сохранения на диск.

**Пример конфигурации:**
```sql
CREATE TABLE temp_data (
    id UInt32,
    data String
) ENGINE = Memory();
```

---

---

## **Вывод**
ClickHouse предоставляет **широкий выбор движков** для различных сценариев:
- **MergeTree** — для аналитики больших данных.
- **Log** — для простого хранения логов.
- **Kafka/MySQL/JDBC** — для интеграции с внешними системами.
- **Distributed** — для распределённых запросов.
- **Dictionary** — для справочников.
- **File/URL** — для работы с файлами и внешними источниками.