### 1. **Шаблоны уровня системы (System-level Patterns)**


## Оглавление
  - [1. **Шаблоны уровня системы (System-level Patterns)**](#1-шаблоны-уровня-системы-system-level-patterns)
  - [2. **Шаблоны уровня компонентов (Component-level Patterns)**](#2-шаблоны-уровня-компонентов-component-level-patterns)
  - [3. **Шаблоны уровня данных (Data-level Patterns)**](#3-шаблоны-уровня-данных-data-level-patterns)
  - [4. **Шаблоны взаимодействия (Communication Patterns)**](#4-шаблоны-взаимодействия-communication-patterns)
  - [5. **Шаблоны развертывания (Deployment Patterns)**](#5-шаблоны-развертывания-deployment-patterns)
  - [6. **Шаблоны безопасности (Security Patterns)**](#6-шаблоны-безопасности-security-patterns)
  - [Пример применения](#пример-применения)
- [Details](#details)
- [1. **Многослойная архитектура (Layered Architecture, N-tier)**](#1-многослойная-архитектура-layered-architecture-n-tier)
- [2. **Микросервисы (Microservices)**](#2-микросервисы-microservices)
- [3. **Ориентированная на события (Event-Driven Architecture, EDA)**](#3-ориентированная-на-события-event-driven-architecture-eda)
- [4. **Репозиторий (Repository Pattern)**](#4-репозиторий-repository-pattern)
- [5. **CQRS (Command Query Responsibility Segregation)**](#5-cqrs-command-query-responsibility-segregation)
- [6. **API Gateway**](#6-api-gateway)
- [7. **Безсерверная архитектура (Serverless)**](#7-безсерверная-архитектура-serverless)
  - [Итоговая таблица: Когда какой шаблон использовать](#итоговая-таблица-когда-какой-шаблон-использовать)

  - [1. **Шаблоны уровня системы (System-level Patterns)**](#1-шаблоны-уровня-системы-system-level-patterns)
  - [2. **Шаблоны уровня компонентов (Component-level Patterns)**](#2-шаблоны-уровня-компонентов-component-level-patterns)
  - [3. **Шаблоны уровня данных (Data-level Patterns)**](#3-шаблоны-уровня-данных-data-level-patterns)
  - [4. **Шаблоны взаимодействия (Communication Patterns)**](#4-шаблоны-взаимодействия-communication-patterns)
  - [5. **Шаблоны развертывания (Deployment Patterns)**](#5-шаблоны-развертывания-deployment-patterns)
  - [6. **Шаблоны безопасности (Security Patterns)**](#6-шаблоны-безопасности-security-patterns)
  - [Пример применения](#пример-применения)
  - [Итоговая таблица: Когда какой шаблон использовать](#итоговая-таблица-когда-какой-шаблон-использовать)
Определяют общую структуру приложения.

- **Многослойная архитектура (Layered Architecture, N-tier)**
  Разделение системы на слои (например, представление, бизнес-логика, доступ к данным). Каждый слой взаимодействует только с соседним.

- **Клиент-сервер (Client-Server)**
  Разделение на клиентскую часть (интерфейс) и серверную (обработка данных).

- **Микросервисы (Microservices)**
  Система разбивается на небольшие независимые сервисы, каждый из которых отвечает за свою функциональность.

- **Ориентированная на события (Event-Driven Architecture, EDA)**
  Компоненты взаимодействуют через события (например, через брокеры сообщений).

---

### 2. **Шаблоны уровня компонентов (Component-level Patterns)**
Определяют организацию отдельных частей системы.

- **Модуль (Module Pattern)**
  Группировка связанных функций и данных в отдельные модули.

- **Монолит (Monolithic Architecture)**
  Вся система разрабатывается как единое целое (противоположность микросервисам).

- **Плагин (Plugin Architecture)**
  Возможность динамически подключать/отключать функциональность.

---

### 3. **Шаблоны уровня данных (Data-level Patterns)**
Определяют, как система работает с данными.

- **Репозиторий (Repository Pattern)**
  Абстракция для доступа к данным (например, базам данных), скрывающая детали хранения.

- **Единица работы (Unit of Work Pattern)**
  Управление транзакциями и изменениями данных как единым целым.

- **CQRS (Command Query Responsibility Segregation)**
  Разделение операций чтения и записи данных.

---

### 4. **Шаблоны взаимодействия (Communication Patterns)**
Определяют, как компоненты обмениваются данными.

- **API Gateway**
  Единая точка входа для клиентов к микросервисам.

- **Брокер сообщений (Message Broker)**
  Промежуточный компонент для обмена сообщениями между сервисами (например, RabbitMQ, Kafka).

- **Публикация/подписка (Pub/Sub)**
  Компоненты публикуют события, а другие подписываются на них.

---

### 5. **Шаблоны развертывания (Deployment Patterns)**
Определяют, как система развертывается и масштабируется.

- **Контейнеризация (Containerization)**
  Использование контейнеров (например, Docker) для изоляции и развертывания компонентов.

- **Безсерверная архитектура (Serverless Architecture)**
  Исполнение кода без управления серверами (например, AWS Lambda).

- **Кластер (Cluster)**
  Группа серверов, работающих как единое целое для обеспечения отказоустойчивости и масштабируемости.

---

### 6. **Шаблоны безопасности (Security Patterns)**
Обеспечивают защиту системы.

- **Аутентификация и авторизация (Authentication & Authorization)**
  Механизмы проверки подлинности пользователей и разграничения доступа.

- **Шифрование (Encryption)**
  Защита данных при передаче и хранении.

---

### Пример применения
Если вы разрабатываете веб-приложение, то можете использовать:
- **Многослойную архитектуру** для разделения логики,
- **Микросервисы** для масштабируемости,
- **API Gateway** для управления запросами,
- **Репозиторий** для работы с базой данных.

---

## Details

Разберём архитектурные шаблоны подробно, с примерами и пояснениями, как и где их применять.

---

## 1. **Многослойная архитектура (Layered Architecture, N-tier)**
**Описание:**
Система делится на логические слои, каждый из которых отвечает за свою часть функциональности. Классический пример — три слоя: представление (UI), бизнес-логика (BL), доступ к данным (DAL).

**Пример на C#:**
```csharp
// Слой доступа к данным (DAL)
public class UserRepository
{
    public User GetUserById(int id)
    {
        // Логика работы с базой данных
        return new User { Id = id, Name = "Иван" };
    }
}

// Слой бизнес-логики (BL)
public class UserService
{
    private readonly UserRepository _repository;

    public UserService(UserRepository repository)
    {
        _repository = repository;
    }

    public User GetUser(int id)
    {
        // Дополнительная логика (например, проверка прав)
        return _repository.GetUserById(id);
    }
}

// Слой представления (UI)
public class UserController
{
    private readonly UserService _service;

    public UserController(UserService service)
    {
        _service = service;
    }

    public void ShowUser(int id)
    {
        var user = _service.GetUser(id);
        Console.WriteLine($"Пользователь: {user.Name}");
    }
}
```
**Когда использовать:**
- Для небольших и средних приложений.
- Когда требуется чёткое разделение ответственности.

---

## 2. **Микросервисы (Microservices)**
**Описание:**
Приложение разбивается на небольшие независимые сервисы, каждый из которых выполняет одну функцию (например, сервис авторизации, сервис заказов). Сервисы взаимодействуют через API или события.

**Пример:**
- **Сервис авторизации** (отвечает за регистрацию и вход пользователей).
- **Сервис заказов** (управляет созданием и обработкой заказов).
- **Сервис уведомлений** (отправляет email/SMS).

**Реализация на C#:**
Каждый микросервис — это отдельное приложение (например, на ASP.NET Core), которое можно развернуть независимо.

**Когда использовать:**
- Для крупных систем с высокой нагрузкой.
- Когда команда разработчиков большая и требуется независимое масштабирование частей системы.

---

## 3. **Ориентированная на события (Event-Driven Architecture, EDA)**
**Описание:**
Компоненты системы взаимодействуют через события. Например, после создания заказа отправляется событие `OrderCreated`, на которое реагируют другие сервисы (например, сервис уведомлений).

**Пример на C# с использованием MediatR (библиотека для работы с событиями):**
```csharp
// Событие
public class OrderCreatedEvent : INotification
{
    public int OrderId { get; set; }
}

// Обработчик события
public class OrderCreatedHandler : INotificationHandler<OrderCreatedEvent>
{
    public Task Handle(OrderCreatedEvent notification, CancellationToken cancellationToken)
    {
        Console.WriteLine($"Отправляем уведомление о заказе #{notification.OrderId}");
        return Task.CompletedTask;
    }
}

// Публикация события
public class OrderService
{
    private readonly IMediator _mediator;

    public OrderService(IMediator mediator)
    {
        _mediator = mediator;
    }

    public async Task CreateOrder(int orderId)
    {
        // Логика создания заказа
        await _mediator.Publish(new OrderCreatedEvent { OrderId = orderId });
    }
}
```
**Когда использовать:**
- Когда система должна быть гибкой и легко расширяемой.
- Для интеграции между микросервисами.

---

## 4. **Репозиторий (Repository Pattern)**
**Описание:**
Абстракция для работы с данными. Позволяет скрыть детали хранения (например, базу данных) и предоставляет единый интерфейс для доступа к данным.

**Пример на C#:**
```csharp
public interface IUserRepository
{
    User GetById(int id);
    void Add(User user);
}

public class UserRepository : IUserRepository
{
    private readonly DbContext _context;

    public UserRepository(DbContext context)
    {
        _context = context;
    }

    public User GetById(int id)
    {
        return _context.Users.Find(id);
    }

    public void Add(User user)
    {
        _context.Users.Add(user);
        _context.SaveChanges();
    }
}
```
**Когда использовать:**
- Для работы с базой данных в многослойной архитектуре.
- Когда требуется тестируемость и гибкость кода.

---

## 5. **CQRS (Command Query Responsibility Segregation)**
**Описание:**
Разделение операций чтения (Query) и записи (Command) данных. Позволяет оптимизировать производительность и масштабируемость.

**Пример на C#:**
```csharp
// Команда (запись)
public class CreateUserCommand
{
    public string Name { get; set; }
}

public class CreateUserHandler
{
    private readonly IUserRepository _repository;

    public CreateUserHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    public void Handle(CreateUserCommand command)
    {
        var user = new User { Name = command.Name };
        _repository.Add(user);
    }
}

// Запрос (чтение)
public class GetUserQuery
{
    public int Id { get; set; }
}

public class GetUserHandler
{
    private readonly IUserRepository _repository;

    public GetUserHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    public User Handle(GetUserQuery query)
    {
        return _repository.GetById(query.Id);
    }
}
```
**Когда использовать:**
- Для систем с высокой нагрузкой на чтение или запись.
- Когда требуется гибкость в масштабировании.

---

## 6. **API Gateway**
**Описание:**
Единая точка входа для клиентов к микросервисам. Маршрутизирует запросы, агрегирует данные и обеспечивает безопасность.

**Пример:**
- Клиент отправляет запрос на `/orders`, а API Gateway перенаправляет его на сервис заказов.

**Реализация на C#:**
Можно использовать Ocelot или Yazor для создания API Gateway на ASP.NET Core.

---

## 7. **Безсерверная архитектура (Serverless)**
**Описание:**
Код выполняется в облаке без управления серверами. Например, функции Azure Functions или AWS Lambda.

**Пример на C# (Azure Function):**
```csharp
public static class OrderProcessor
{
    [FunctionName("ProcessOrder")]
    public static async Task<IActionResult> Run(
        [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req,
        ILogger log)
    {
        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        log.LogInformation($"Processing order: {requestBody}");
        return new OkObjectResult("Order processed");
    }
}
```
**Когда использовать:**
- Для обработки событий или коротких задач.
- Когда требуется автоматическое масштабирование.

---

### Итоговая таблица: Когда какой шаблон использовать



| Шаблон                     | Когда использовать                                                                 | Пример реализации на C#                     |
|----------------------------|------------------------------------------------------------------------------------|---------------------------------------------|
| Многослойная архитектура   | Небольшие/средние приложения, чёткое разделение логики.                           | Разделение на DAL, BL, UI.                  |
| Микросервисы               | Крупные системы, независимое масштабирование.                                     | Отдельные ASP.NET Core сервисы.             |
| Event-Driven Architecture  | Гибкость, интеграция между сервисами.                                              | MediatR, RabbitMQ.                          |
| Репозиторий                | Работа с базой данных, тестируемость.                                               | Интерфейсы для доступа к данным.            |
| CQRS                       | Высокая нагрузка на чтение/запись, оптимизация производительности.                 | Разделение команд и запросов.               |
| API Gateway                | Единая точка входа для микросервисов, маршрутизация.                               | Ocelot, Yazor.                              |
| Serverless                 | Обработка событий, автоматическое масштабирование.                                 | Azure Functions, AWS Lambda.                |

---