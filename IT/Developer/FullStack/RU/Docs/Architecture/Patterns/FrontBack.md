# Шаблоны проектирования FrontEnd и BackEnd

## FrontEnd шаблоны проектирования

### 1. **Компонентный подход (Component Pattern)**
**Описание:** Разбиение UI на независимые, переиспользуемые компоненты с собственной логикой и состоянием.

**Применение:** React, Vue, Angular компоненты. Идеально для создания модульных интерфейсов.

```javascript
// React компонент
const Button = ({ onClick, children, variant = 'primary' }) => {
  return (
    <button 
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### 2. **HOC (Higher-Order Component)**
**Описание:** Функция, принимающая компонент и возвращающая новый компонент с дополнительной функциональностью.

**Применение:** Аутентификация, логирование, обработка ошибок, инжекция пропсов.

```javascript
// React HOC для аутентификации
const withAuth = (WrappedComponent) => {
  return (props) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    
    useEffect(() => {
      checkAuth().then(setIsAuthenticated);
    }, []);
    
    if (!isAuthenticated) return <LoginPage />;
    return <WrappedComponent {...props} />;
  };
};
```

### 3. **Render Props**
**Описание:** Компонент, который принимает функцию как пропс и использует её для рендера содержимого.

**Применение:** Разделение логики и представления, переиспользуемая логика данных.

```javascript
const DataFetcher = ({ url, children }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  return children({ data, loading });
};
```

### 4. **Custom Hooks**
**Описание:** Кастомные хуки для переиспользования логики состояния между компонентами.

**Применение:** Управление формами, подписки на события, работа с API.

```javascript
// Кастомный хук для управления состоянием формы
const useForm = (initialValues) => {
  const [values, setValues] = useState(initialValues);
  
  const handleChange = (event) => {
    const { name, value } = event.target;
    setValues(prev => ({ ...prev, [name]: value }));
  };
  
  return { values, handleChange };
};
```

### 5. **Flux/Redux Pattern**
**Описание:** Предсказуемый контейнер состояния для JavaScript приложений.

**Применение:** Управление глобальным состоянием приложения, сложные state-машины.

```javascript
// Redux store configuration
const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);
```

### 6. **Provider Pattern**
**Описание:** Передача данных через дерево компонентов без явной передачи пропсов.

**Применение:** Темы, локализация, аутентификация, глобальные настройки.

```javascript
// Context Provider
const ThemeContext = createContext();

const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

### 7. **Compound Components**
**Описание:** Группа компонентов, которые работают вместе как единое целое.

**Применение:** Сложные UI компоненты (табы, аккордеоны, выпадающие списки).

```javascript
const Select = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div className="select">
      {Children.map(children, child => 
        cloneElement(child, { isOpen, setIsOpen })
      )}
    </div>
  );
};

Select.Option = ({ children }) => <div>{children}</div>;
```

### 8. **Container/Presentational Pattern**
**Описание:** Разделение компонентов на "умные" (логика) и "глупые" (представление).

**Применение:** Разделение ответственности, улучшение тестируемости.

```javascript
// Presentational компонент (только UI)
const UserList = ({ users, loading }) => {
  if (loading) return <Spinner />;
  return users.map(user => <UserCard key={user.id} user={user} />);
};

// Container компонент (логика)
const UserListContainer = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  
  return <UserList users={users} loading={loading} />;
};
```

---

## BackEnd шаблоны проектирования

### 1. **MVC (Model-View-Controller)**
**Описание:** Архитектурный шаблон разделения приложения на три компонента: Модель, Представление, Контроллер.

**Применение:** Веб-приложения, RESTful API, enterprise приложения.

```csharp
// ASP.NET Core Controller
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    
    [HttpGet]
    public async Task<IActionResult> GetUsers()
    {
        var users = await _userService.GetAllUsersAsync();
        return Ok(users);
    }
}
```

### 2. **Repository Pattern**
**Описание:** Абстракция доступа к данным, инкапсулирующая всю логику работы с хранилищем.

**Применение:** Изоляция слоя данных, упрощение тестирования, смена БД.

```csharp
public interface IUserRepository
{
    Task<User> GetByIdAsync(int id);
    Task<IEnumerable<User>> GetAllAsync();
    Task AddAsync(User user);
}

public class UserRepository : IUserRepository
{
    public async Task<User> GetByIdAsync(int id)
    {
        return await _context.Users.FindAsync(id);
    }
}
```

### 3. **Unit of Work Pattern**
**Описание:** Поддержание целостности транзакций при работе с несколькими репозиториями.

**Применение:** Сложные бизнес-транзакции, обеспечение согласованности данных.

```csharp
public interface IUnitOfWork : IDisposable
{
    IUserRepository Users { get; }
    IOrderRepository Orders { get; }
    Task<int> CommitAsync();
}
```

### 4. **Service Layer Pattern**
**Описание:** Слой, инкапсулирующий бизнес-логику и координирующий работу репозиториев.

**Применение:** Сложная бизнес-логика, оркестрация операций, валидация.

```csharp
public class UserService : IUserService
{
    public async Task<UserDto> CreateUserAsync(CreateUserDto dto)
    {
        // Бизнес-логика создания пользователя
        var user = _mapper.Map<User>(dto);
        await _userRepository.AddAsync(user);
        return _mapper.Map<UserDto>(user);
    }
}
```

### 5. **CQRS (Command Query Responsibility Segregation)**
**Описание:** Разделение операций на команды (изменение) и запросы (чтение).

**Применение:** Высоконагруженные системы, сложные модели данных, микросервисы.

```csharp
// Command - изменение данных
public class CreateUserCommand : IRequest<int>
{
    public string Name { get; set; }
    public string Email { get; set; }
}

// Query - чтение данных
public class GetUserQuery : IRequest<UserDto>
{
    public int Id { get; set; }
}
```

### 6. **Mediator Pattern**
**Описание:** Объект, который инкапсулирует способ взаимодействия множества объектов.

**Применение:** Уменьшение связности, централизация сложной коммуникации.

```csharp
// Использование MediatR
public class UsersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    [HttpPost]
    public async Task<ActionResult<int>> CreateUser(CreateUserCommand command)
    {
        var userId = await _mediator.Send(command);
        return Ok(userId);
    }
}
```

### 7. **Factory Pattern**
**Описание:** Создание объектов без указания точного класса создаваемого объекта.

**Применение:** Создание семейств связанных объектов, сложная инициализация.

```csharp
public static class NotificationServiceFactory
{
    public static INotificationService Create(string type)
    {
        return type.ToLower() switch
        {
            "email" => new EmailNotificationService(),
            "sms" => new SmsNotificationService(),
            _ => throw new ArgumentException($"Unknown type: {type}")
        };
    }
}
```

### 8. **Strategy Pattern**
**Описание:** Определение семейства алгоритмов, инкапсуляция каждого из них и обеспечение их взаимозаменяемости.

**Применение:** Различные варианты оплаты, способы доставки, алгоритмы расчета.

```csharp
public interface IPaymentStrategy
{
    Task<bool> ProcessPaymentAsync(decimal amount);
}

public class PaymentProcessor
{
    private IPaymentStrategy _strategy;
    
    public void SetStrategy(IPaymentStrategy strategy)
    {
        _strategy = strategy;
    }
    
    public async Task<bool> ProcessAsync(decimal amount)
    {
        return await _strategy.ProcessPaymentAsync(amount);
    }
}
```

### 9. **Observer Pattern**
**Описание:** Определение зависимости "один-ко-многим" между объектами.

**Применение:** Event-driven архитектура, уведомления, системы подписок.

```csharp
public interface IOrderObserver
{
    Task OnOrderCreatedAsync(Order order);
}

public class OrderService
{
    private readonly List<IOrderObserver> _observers = new();
    
    public async Task CreateOrderAsync(Order order)
    {
        await _repository.AddAsync(order);
        
        // Уведомление наблюдателей
        foreach (var observer in _observers)
        {
            await observer.OnOrderCreatedAsync(order);
        }
    }
}
```

### 10. **Dependency Injection**
**Описание:** Внедрение зависимостей вместо их создания внутри класса.

**Применение:** Управление зависимостями, тестирование, слабая связность.

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddScoped<IUserRepository, UserRepository>();
    services.AddScoped<IUserService, UserService>();
    services.AddTransient<INotificationService, EmailNotificationService>();
}
```

---

## Кросс-платформенные шаблоны

### 1. **Adapter Pattern**
**Описание:** Преобразование интерфейса одного класса в интерфейс, ожидаемый клиентом.

**Применение:** Интеграция с legacy системами, работа с разными API, миграции.

```csharp
public class LegacyApiAdapter : IExternalServiceAdapter
{
    public async Task<UserData> GetUserDataAsync(string userId)
    {
        var legacyUser = await _legacyService.GetUserAsync(userId);
        // Адаптация данных под новую модель
        return new UserData { Name = $"{legacyUser.FirstName} {legacyUser.LastName}" };
    }
}
```

### 2. **Decorator Pattern**
**Описание:** Динамическое добавление новой функциональности объекту.

**Применение:** Логирование, кэширование, аутентификация, мониторинг.

```csharp
public class LoggingServiceDecorator : IUserService
{
    private readonly IUserService _userService;
    private readonly ILogger _logger;
    
    public async Task<UserDto> GetUserAsync(int id)
    {
        _logger.LogInformation("Getting user {UserId}", id);
        var user = await _userService.GetUserAsync(id);
        _logger.LogInformation("User retrieved successfully");
        return user;
    }
}
```

### 3. **Singleton Pattern**
**Описание:** Гарантирует, что класс имеет только один экземпляр и предоставляет глобальную точку доступа.

**Применение:** Логгеры, кэши, конфигурации, подключения к БД.

```csharp
public sealed class DatabaseConnection
{
    private static DatabaseConnection _instance;
    
    private DatabaseConnection() { }
    
    public static DatabaseConnection Instance
    {
        get
        {
            if (_instance == null)
                _instance = new DatabaseConnection();
            return _instance;
        }
    }
}
```

### 4. **Facade Pattern**
**Описание:** Предоставляет унифицированный интерфейс к набору интерфейсов в подсистеме.

**Применение:** Упрощение сложных систем, абстракция над микросервисами.

```csharp
public class OrderFacade
{
    private readonly IOrderService _orderService;
    private readonly IPaymentService _paymentService;
    private readonly INotificationService _notificationService;
    
    public async Task<OrderResult> PlaceOrderAsync(OrderRequest request)
    {
        // Сложная логика оформления заказа скрыта за простым интерфейсом
        var order = await _orderService.CreateAsync(request);
        await _paymentService.ProcessAsync(order);
        await _notificationService.SendConfirmationAsync(order);
        return new OrderResult { Success = true, OrderId = order.Id };
    }
}
```

## Рекомендации по выбору шаблонов

### Для FrontEnd:
- **Компонентный подход** - основа современных SPA
- **Provider Pattern** - для глобального состояния (темы, пользователь)
- **Custom Hooks** - для переиспользуемой логики
- **Container/Presentational** - для разделения ответственности

### Для BackEnd:
- **Repository + Unit of Work** - для работы с данными
- **Service Layer** - для бизнес-логики
- **CQRS** - для высоконагруженных систем
- **Dependency Injection** - для управления зависимостями

### Универсальные:
- **Adapter** - для интеграций
- **Strategy** - для заменяемых алгоритмов
- **Observer** - для event-driven архитектуры
- **Decorator** - для добавления функциональности