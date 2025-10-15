**MediatR** — это популярная библиотека для .NET, которая реализует шаблоны **Poser/Handler** и **CQRS** (Command Query Responsibility Segregation). Она упрощает взаимодействие между компонентами приложения, уменьшая связанность кода и улучшая его поддерживаемость.

---

## **Основное назначение MediatR**
1. **Декомпозиция логики:**
   Библиотека позволяет разделить бизнес-логику на небольшие, независимые обработчики (handlers), которые реагируют на команды или запросы.

2. **Реализация CQRS:**
   MediatR помогает разделить операции на **команды** (изменение состояния) и **запросы** (получение данных).

3. **Упрощение взаимодействия между слоями:**
   Вместо прямого вызова методов между слоями (например, из контроллера в сервис), MediatR использует посредника (mediator), который маршрутизирует запросы к соответствующим обработчикам.

---

## **Основные компоненты MediatR**
| Компонент          | Описание                                                                 |
|--------------------|--------------------------------------------------------------------------|
| **IRequest<T>**    | Интерфейс для запросов, которые возвращают результат (например, данные). |
| **IRequest**       | Интерфейс для команд, которые не возвращают результат.                 |
| **IRequestHandler**| Обработчик для запросов или команд.                                      |
| **IMediator**      | Посредник, который маршрутизирует запросы к обработчикам.              |
| **Pipeline**       | Цепочка обработчиков (например, для логирования, валидации).             |

---

## **Сценарии использования MediatR**

### 1. **Обработка команд (Command)**
**Пример:** Создание нового пользователя.
- **Команда:** `CreateUserCommand` (содержит данные пользователя).
- **Обработчик:** `CreateUserCommandHandler` (сохраняет пользователя в базе данных).

```csharp
public class CreateUserCommand : IRequest<int>
{
    public string Name { get; set; }
    public string Email { get; set; }
}

public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, int>
{
    private readonly IUserRepository _repository;

    public CreateUserCommandHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<int> Handle(CreateUserCommand request, CancellationToken cancellationToken)
    {
        var user = new User { Name = request.Name, Email = request.Email };
        await _repository.AddAsync(user);
        return user.Id;
    }
}
```

---

### 2. **Обработка запросов (Query)**
**Пример:** Получение списка пользователей.
- **Запрос:** `GetUsersQuery`.
- **Обработчик:** `GetUsersQueryHandler` (возвращает список пользователей).

```csharp
public class GetUsersQuery : IRequest<List<UserDto>> { }

public class GetUsersQueryHandler : IRequestHandler<GetUsersQuery, List<UserDto>>
{
    private readonly IUserRepository _repository;

    public GetUsersQueryHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<List<UserDto>> Handle(GetUsersQuery request, CancellationToken cancellationToken)
    {
        var users = await _repository.GetAllAsync();
        return users.Select(u => new UserDto { Id = u.Id, Name = u.Name }).ToList();
    }
}
```

---

### 3. **Использование в ASP.NET Core**
MediatR часто интегрируется с **ASP.NET Core** для обработки HTTP-запросов.
**Пример:** Использование MediatR в контроллере.

```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IMediator _mediator;

    public UsersController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpPost]
    public async Task<IActionResult> CreateUser(CreateUserCommand command)
    {
        var userId = await _mediator.Send(command);
        return Ok(userId);
    }

    [HttpGet]
    public async Task<IActionResult> GetUsers()
    {
        var users = await _mediator.Send(new GetUsersQuery());
        return Ok(users);
    }
}
```

---

### 4. **Пайплайны (Pipeline)**
MediatR поддерживает **промежуточные обработчики** (pipeline behaviors) для выполнения дополнительных действий перед или после основного обработчика.
**Пример:** Логирование или валидация запросов.

```csharp
public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken cancellationToken)
    {
        _logger.LogInformation($"Handling {typeof(TRequest).Name}");
        var response = await next();
        _logger.LogInformation($"Handled {typeof(TRequest).Name}");
        return response;
    }
}
```

---

## **Преимущества MediatR**
- **Разделение ответственности:** Логика приложения разбивается на небольшие, независимые обработчики.
- **Упрощение тестирования:** Каждый обработчик можно тестировать отдельно.
- **Гибкость:** Легко добавлять новые обработчики или изменять существующие без изменения клиентского кода.
- **Поддержка CQRS:** Удобно реализовывать разделение команд и запросов.

---

## **Когда использовать MediatR?**
- В сложных приложениях с большим количеством бизнес-логики.
- При необходимости реализовать **CQRS** или **Event Sourcing**.
- Для уменьшения связанности между слоями приложения (например, между контроллерами и сервисами).

---