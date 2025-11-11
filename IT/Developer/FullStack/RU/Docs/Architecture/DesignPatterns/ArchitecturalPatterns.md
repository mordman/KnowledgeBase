### 1. Монолитная архитектура (Monolithic Architecture)
- **Описание**: Все компоненты приложения (интерфейс, бизнес-логика, доступ к данным) объединены в один модуль.
- **Плюсы**: Простота разработки, развертывания и тестирования.
- **Минусы**: Сложность масштабирования, высокая связанность компонентов.


```mermaid
graph TD
    subgraph Application
        UI[User Interface]
        BL[Business Logic]
        DA[Data Access]
    end
    UI --> BL
    BL --> DA
    DA --> Database[(Database)]
```

---

### 2. Микросервисная архитектура (Microservices Architecture)
- **Описание**: Приложение разбито на небольшие независимые сервисы, каждый из которых отвечает за свою функциональность.
- **Плюсы**: Гибкость, масштабируемость, независимое развертывание.
- **Минусы**: Сложность управления, необходимость оркестрации и мониторинга.


```mermaid
graph LR
    Client[Client] -->|HTTP/REST| UserService[User Service]
    Client -->|HTTP/REST| OrderService[Order Service]
    Client -->|HTTP/REST| PaymentService[Payment Service]
    UserService --> UserDB[(User DB)]
    OrderService --> OrderDB[(Order DB)]
    PaymentService --> PaymentDB[(Payment DB)]
```

---

### 3. Многослойная архитектура (Layered Architecture)
- **Описание**: Приложение делится на слои (например, презентационный, бизнес-логика, доступ к данным).
- **Плюсы**: Четкое разделение ответственности, простота поддержки.
- **Минусы**: Может быть избыточной для простых приложений.


```mermaid
graph TD
    PL[Presentation Layer] --> BLL[Business Logic Layer]
    BLL --> DAL[Data Access Layer]
    DAL --> Database[(Database)]
```

---

### 4. Архитектура на основе событий (Event-Driven Architecture)
- **Описание**: Компоненты взаимодействуют через события (например, с использованием брокеров сообщений).
- **Плюсы**: Асинхронность, гибкость, масштабируемость.
- **Минусы**: Сложность отладки и управления потоками данных.


```mermaid
graph LR
    ServiceA[Service A] -->|Event| Broker[Event Broker]
    ServiceB[Service B] -->|Event| Broker
    Broker -->|Event| ServiceC[Service C]
    Broker -->|Event| ServiceD[Service D]
```

---

### 5. Сервис-ориентированная архитектура (SOA)
- **Описание**: Приложение состоит из сервисов, которые взаимодействуют через стандартные протоколы (например, SOAP, REST) и часто используют Enterprise Service Bus (ESB).
- **Плюсы**: Повторное использование сервисов, интеграция с другими системами.
- **Минусы**: Высокая сложность, необходимость управления контрактами сервисов.


```mermaid
graph LR
    Client[Client] --> ESB[Enterprise Service Bus]
    ESB --> UserService[User Service]
    ESB --> OrderService[Order Service]
    ESB --> InventoryService[Inventory Service]
```

---

### 6. Архитектура "Клиент-Сервер" (Client-Server Architecture)
- **Описание**: Клиент отправляет запросы к серверу, который обрабатывает их и возвращает результат.
- **Плюсы**: Централизованное управление, простота обновления серверной части.
- **Минусы**: Зависимость от сервера, возможные проблемы с масштабируемостью.


```mermaid
graph LR
    DesktopClient[Desktop Client] --> Server[Server]
    MobileClient[Mobile Client] --> Server
    Server --> Database[(Database)]
```

---

### 7. Архитектура "Пиринговая сеть" (Peer-to-Peer Architecture)
- **Описание**: Все узлы равноправны и могут взаимодействовать напрямую.
- **Плюсы**: Отсутствие единой точки отказа, масштабируемость.
- **Минусы**: Сложность управления, проблемы с безопасностью.


```mermaid
graph LR
    Node1[Node 1] <---> Node2[Node 2]
    Node2 <---> Node3[Node 3]
    Node3 <---> Node1
```

---

### 8. Чистая архитектура (Clean Architecture)
- **Описание**: Приложение делится на концентрические слои с четким разделением ответственности и зависимостей. Приложение делится на концентрические слои: Entities, Use Cases, Interface Adapters, Frameworks & Drivers.
- **Плюсы**: Гибкость, тестируемость, независимость от фреймворков.
- **Минусы**: Сложность реализации, избыточность для небольших проектов.


```mermaid
graph LR
    subgraph Core
        Entities[Entities]
        UseCases[Use Cases]
    end
    subgraph Adapters
        UIAdapter[UI Adapter]
        DBAdapter[DB Adapter]
    end
    UseCases --> UIAdapter
    UseCases --> DBAdapter
    UIAdapter --> Frameworks[Frameworks & Drivers]
    DBAdapter --> Frameworks
```

---

### 9. Архитектура "Шина сервисов" (Service Bus Architecture)
- **Описание**: Сервисы взаимодействуют через центральную шину, которая управляет маршрутизацией сообщений.
- **Плюсы**: Гибкость, масштабируемость, слабая связанность.
- **Минусы**: Сложность настройки и управления шиной.

```mermaid
graph LR
    ServiceA[Service A] --> Bus[Service Bus]
    ServiceB[Service B] --> Bus
    Bus --> ServiceC[Service C]
    Bus --> ServiceD[Service D]
```

---

### 10. Шестиугольная архитектура (Hexagonal Architecture, Ports and Adapters)
- **Описание**: Приложение изолировано от внешних зависимостей (например, базы данных, UI) с помощью адаптеров.
- **Плюсы**: Гибкость, тестируемость, простота замены внешних компонентов.
- **Минусы**: Сложность реализации для небольших проектов.

```mermaid
graph LR
    subgraph Core
        Application[Application Core]
    end
    UIAdapter[UI Adapter] --> Port1[Port]
    DBAdapter[DB Adapter] --> Port2[Port]
    Port1 --> Application
    Port2 --> Application
```

---