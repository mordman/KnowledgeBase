# CodeStyle Short

### **1. Именование**
- **Классы, интерфейсы, структуры, перечисления (enum):** PascalCase
  ```csharp
  public class UserAccount { }
  public interface ILogger { }
  public enum StatusType { Active, Inactive }
  ```

- **Методы, свойства, события:** PascalCase
  ```csharp
  public void CalculateTotal() { }
  public string FirstName { get; set; }
  public event EventHandler OnSave;
  ```

- **Локальные переменные, параметры методов:** camelCase
  ```csharp
  int totalCount = 0;
  public void PrintMessage(string message) { }
  ```

- **Константы:** PascalCase (иногда с префиксом)
  ```csharp
  public const int MaxRetryCount = 3;
  ```

- **Поля (fields):** camelCase с префиксом `_` (если приватные)
  ```csharp
  private int _userId;
  ```

---

### **2. Форматирование**
- **Отступы:** Используйте 4 пробела (не табуляцию).
- **Фигурные скобки:** Всегда на новой строке для классов, методов, циклов и условий.
  ```csharp
  if (condition)
  {
      // код
  }
  ```
- **Пробелы:**
  - После ключевых слов (`if`, `while`, `for`).
  - После запятых в списках параметров.
  ```csharp
  if (x > 0 && y < 10)
  {
      DoSomething(x, y);
  }
  ```

---

### **3. Организация кода**
- **Порядок элементов в классе:**
  1. Поля (fields)
  2. Конструкторы
  3. Свойства
  4. Методы
  5. Вложенные классы/интерфейсы

- **Модификаторы доступа:** Всегда указывайте (`private`, `public`, `protected` и т.д.), даже если это избыточно.

---

### **4. Комментарии**
- Избегайте избыточных комментариев. Код должен быть самодокументируемым.
- Используйте XML-комментарии для публичных API:
  ```csharp
  /// <summary>
  /// Вычисляет сумму двух чисел.
  /// </summary>
  /// <param name="a">Первое число.</param>
  /// <param name="b">Второе число.</param>
  /// <returns>Сумма чисел.</returns>
  public int Add(int a, int b) => a + b;
  ```

---

### **5. Использование `var`**
- Используйте `var` только когда тип переменной очевиден из правой части выражения:
  ```csharp
  var user = new User(); // Хорошо
  var count = GetCount(); // Плохо, если тип GetCount() неочевиден
  ```

---

### **6. Асинхронный код**
- Методы, возвращающие `Task`, должны иметь суффикс `Async`:
  ```csharp
  public async Task<int> LoadDataAsync()
  ```

---

### **7. Обработка исключений**
- Не игнорируйте исключения. Логируйте или обрабатывайте их.
- Используйте специфические типы исключений:
  ```csharp
  try
  {
      // код
  }
  catch (FileNotFoundException ex)
  {
      // обработка
  }
  ```

---

### **8. Использование `using`**
- Для освобождения ресурсов используйте `using`:
  ```csharp
  using (var file = new StreamReader("file.txt"))
  {
      // работа с файлом
  }
  ```

---

### **9. Null-значения**
- Используйте `null`-проверки или оператор `?.` для избежания `NullReferenceException`:
  ```csharp
  string name = user?.Name ?? "Unknown";
  ```

---

### **10. LINQ**
- Используйте LINQ для работы с коллекциями, но избегайте сложных запросов в одной строке.

---

### **Инструменты для проверки стиля**
- **EditorConfig:** Настройте правила стиля для вашей команды.
- **Roslyn Analyzers:** Используйте встроенные или сторонние анализаторы (например, StyleCop).

---

# CodeStyle Detail

## 1. Соглашения по именованию

### **Пространства имен (Namespaces)**
```csharp
// ПРАВИЛЬНО - Company.Product.Feature
namespace CompanyName.ProjectName.Domain.Users
namespace CompanyName.ProjectName.Application.Commands
namespace CompanyName.ProjectName.Infrastructure.Persistence

// НЕПРАВИЛЬНО
namespace companyName.projectName
namespace CompanyName_ProjectName
namespace Domain
```

### **Классы и интерфейсы**
```csharp
// Классы - PascalCase, существительные
public class UserService
public class OrderRepository
public class EmailNotificationHandler

// Интерфейсы - PascalCase с префиксом I
public interface IUserService
public interface IRepository<T>
public interface INotificationHandler

// Абстрактные классы - PascalCase с префиксом Base/Abstract
public abstract class BaseEntity
public abstract class AbstractRepository
```

### **Методы и функции**
```csharp
// PascalCase, глаголы или глагольные фразы
public class UserService
{
    public User GetUserById(int id)
    public void CreateUser(User user)
    public bool ValidateUserCredentials(string email, string password)
    public Task<User> GetUserByIdAsync(int id)
    public IEnumerable<User> FindActiveUsers()
}
```

### **Переменные и параметры**
```csharp
// camelCase для локальных переменных и параметров
public void ProcessOrder(Order order, bool sendNotification)
{
    var orderTotal = CalculateTotal(order);
    var customerEmail = order.Customer.Email;
    var isPriority = order.Priority > 5;
    
    // Для коллекций - множественное число
    var activeUsers = new List<User>();
    var userDictionary = new Dictionary<int, User>();
}

// Поля класса - camelCase с префиксом _
public class UserService
{
    private readonly IUserRepository _userRepository;
    private readonly ILogger _logger;
    private int _requestCount;
}
```

### **Константы и статические поля**
```csharp
public class Configuration
{
    // Константы - PascalCase
    public const int MaxRetryCount = 3;
    public const string DefaultConnectionString = "Server=localhost;Database=app;";
    
    // Static readonly - PascalCase
    public static readonly TimeSpan DefaultTimeout = TimeSpan.FromSeconds(30);
    public static readonly string[] SupportedLanguages = { "en", "ru", "es" };
}
```

### **Enums**
```csharp
// PascalCase для enum и его значений
public enum UserStatus
{
    Active,
    Inactive,
    Suspended,
    PendingVerification
}

public enum OrderPriority
{
    Low,
    Normal,
    High,
    Critical
}

// Использование
var status = UserStatus.Active;
```

## 2. Структура кода и форматирование

### **Расположение членов класса**
```csharp
public class UserService : IUserService
{
    // 1. Константы и поля
    private const int MaxLoginAttempts = 5;
    private readonly IUserRepository _userRepository;
    private readonly ILogger _logger;
    
    // 2. Конструкторы
    public UserService(IUserRepository userRepository, ILogger<UserService> logger)
    {
        _userRepository = userRepository;
        _logger = logger;
    }
    
    // 3. Свойства
    public int ActiveUsersCount { get; private set; }
    
    // 4. Методы (сначала публичные, затем приватные)
    public User GetUser(int id)
    {
        ValidateUserId(id);
        return _userRepository.GetById(id);
    }
    
    public async Task<User> GetUserAsync(int id)
    {
        ValidateUserId(id);
        return await _userRepository.GetByIdAsync(id);
    }
    
    private void ValidateUserId(int id)
    {
        if (id <= 0)
            throw new ArgumentException("User ID must be positive", nameof(id));
    }
    
    // 5. События
    public event EventHandler<UserEventArgs> UserCreated;
}
```

### **Форматирование и отступы**
```csharp
// Отступы - 4 пробела
public class Example
{
    private void Method()
    {
        if (condition)
        {
            // Код с отступом 4 пробела
            var result = SomeMethodCall(
                parameter1,
                parameter2,
                parameter3);
        }
    }
}

// Перенос длинных строк
var result = await _userService.GetUsersAsync(
    page: 1, 
    pageSize: 20, 
    filter: new UserFilter 
    { 
        Active = true, 
        Role = UserRole.Admin 
    });

// Выравнивание параметров
public void CreateUser(
    string firstName,
    string lastName,
    string email,
    string phoneNumber,
    UserRole role = UserRole.User)
{
    // Реализация
}
```

### **Фигурные скобки**
```csharp
// K&R стиль - открывающая скобка на той же строке
public class UserService
{
    public User GetUser(int id)
    {
        if (id <= 0)
        {
            throw new ArgumentException("Invalid ID");
        }
        
        return _userRepository.GetById(id);
    }
    
    // Для однострочных блоков скобки обязательны
    public bool IsUserActive(User user)
    {
        if (user == null) 
            return false;
            
        return user.Status == UserStatus.Active;
    }
}
```

## 3. Модификаторы доступа

### **Явное указание модификаторов**
```csharp
// ПРАВИЛЬНО
public class User
{
    private int _id;
    public string Name { get; private set; }
    protected DateTime CreatedAt { get; set; }
    internal string InternalCode { get; set; }
    
    public User(string name)
    {
        Name = name;
        CreatedAt = DateTime.UtcNow;
    }
}

// НЕПРАВИЛЬНО - неявный private
class User  // Должен быть public/internal
{
    int _id;  // Должен быть private
    string Name { get; set; }  // Должен быть public
}
```

### **Порядок модификаторов**
```csharp
public class Example
{
    // Правильный порядок: access -> static -> readonly/const -> async
    public static readonly int DefaultValue = 10;
    private const string ConnectionString = "...";
    protected static async Task ProcessAsync() { }
    
    // Для методов: access -> static/virtual/abstract/override -> async
    public virtual async Task<string> GetDataAsync() { }
    protected override void OnInitialized() { }
    private static void HelperMethod() { }
}
```

## 4. Работа с исключениями

### **Обработка исключений**
```csharp
public class UserService
{
    public User GetUser(int id)
    {
        try
        {
            ValidateUserId(id);
            return _userRepository.GetById(id);
        }
        catch (ArgumentException ex)
        {
            // Специфичная обработка известных исключений
            _logger.LogWarning(ex, "Invalid user ID: {UserId}", id);
            throw;
        }
        catch (RepositoryException ex) when (ex.IsTransient)
        {
            // Условный catch
            _logger.LogWarning(ex, "Transient error getting user {UserId}", id);
            throw new ServiceUnavailableException("Service temporarily unavailable", ex);
        }
        catch (Exception ex)
        {
            // Общая обработка
            _logger.LogError(ex, "Unexpected error getting user {UserId}", id);
            throw new UserServiceException("Error retrieving user", ex);
        }
    }
    
    private void ValidateUserId(int id)
    {
        if (id <= 0)
            throw new ArgumentException("User ID must be positive", nameof(id));
    }
}
```

### **Создание пользовательских исключений**
```csharp
public class UserServiceException : Exception
{
    public string UserId { get; }
    public string Operation { get; }
    
    public UserServiceException(string message) : base(message) { }
    
    public UserServiceException(string message, Exception innerException) 
        : base(message, innerException) { }
        
    public UserServiceException(string message, string userId, string operation) 
        : base(message) 
    {
        UserId = userId;
        Operation = operation;
    }
}
```

## 5. Работа с коллекциями и LINQ

### **Инициализация коллекций**
```csharp
// ПРАВИЛЬНО
var users = new List<User>();
var userDictionary = new Dictionary<int, User>();
var activeUsers = new HashSet<string>();

// Инициализация с элементами
var roles = new List<string> { "Admin", "User", "Moderator" };
var settings = new Dictionary<string, string>
{
    ["Theme"] = "Dark",
    ["Language"] = "en",
    ["PageSize"] = "20"
};

// НЕПРАВИЛЬНО
ArrayList users = new ArrayList();  // Не типобезопасно
List<User> users = new List<User>();  // Избыточное указание типа
```

### **LINQ стиль**
```csharp
public class UserService
{
    public IEnumerable<User> GetActiveAdminUsers()
    {
        // Method syntax для сложных запросов
        return _userRepository.GetAll()
            .Where(user => user.IsActive && user.Role == UserRole.Admin)
            .OrderBy(user => user.LastName)
            .ThenBy(user => user.FirstName)
            .Select(user => new UserDto
            {
                Id = user.Id,
                FullName = $"{user.FirstName} {user.LastName}",
                Email = user.Email
            });
    }
    
    public User GetUserByEmail(string email)
    {
        // Query syntax для join'ов
        var query = from user in _userRepository.GetAll()
                    where user.Email == email && user.IsActive
                    select user;
                    
        return query.FirstOrDefault();
    }
}
```

## 6. Асинхронное программирование

### **Async/await паттерны**
```csharp
public class UserService
{
    // Правильные суффиксы Async
    public async Task<User> GetUserAsync(int id)
    {
        // Использование ConfigureAwait(false) в library code
        var user = await _userRepository.GetByIdAsync(id)
            .ConfigureAwait(false);
            
        return user;
    }
    
    // ValueTask для потенциально синхронных операций
    public async ValueTask<bool> UserExistsAsync(int id)
    {
        if (_cache.TryGetValue(id, out _))
            return true;
            
        return await _userRepository.ExistsAsync(id);
    }
    
    // Параллельное выполнение
    public async Task<UserDashboard> GetUserDashboardAsync(int userId)
    {
        var userTask = _userRepository.GetByIdAsync(userId);
        var ordersTask = _orderRepository.GetUserOrdersAsync(userId);
        var notificationsTask = _notificationService.GetUserNotificationsAsync(userId);
        
        await Task.WhenAll(userTask, ordersTask, notificationsTask);
        
        return new UserDashboard
        {
            User = userTask.Result,
            Orders = ordersTask.Result,
            Notifications = notificationsTask.Result
        };
    }
}
```

### **Отмена операций**
```csharp
public class DataService
{
    public async Task<List<User>> GetUsersAsync(
        UserFilter filter, 
        CancellationToken cancellationToken = default)
    {
        // Проверка токена отмены
        cancellationToken.ThrowIfCancellationRequested();
        
        var users = await _repository.GetUsersAsync(filter, cancellationToken);
        
        // Дополнительная проверка в долгих операциях
        foreach (var user in users)
        {
            cancellationToken.ThrowIfCancellationRequested();
            // Обработка пользователя
        }
        
        return users;
    }
}
```

## 7. Комментарии и документация

### **XML документация**
```csharp
/// <summary>
/// Сервис для управления пользователями системы.
/// </summary>
/// <remarks>
/// Этот сервис предоставляет методы для создания, чтения, обновления 
/// и удаления пользователей, а также для управления их ролями.
/// </remarks>
public class UserService : IUserService
{
    /// <summary>
    /// Получает пользователя по указанному идентификатору.
    /// </summary>
    /// <param name="id">Идентификатор пользователя. Должен быть положительным числом.</param>
    /// <returns>Объект <see cref="User"/> если пользователь найден; иначе null.</returns>
    /// <exception cref="ArgumentException">Выбрасывается когда <paramref name="id"/> меньше или равен 0.</exception>
    /// <exception cref="UserNotFoundException">Выбрасывается когда пользователь не найден.</exception>
    /// <example>
    /// <code>
    /// var user = await userService.GetUserAsync(123);
    /// if (user != null) 
    /// {
    ///     Console.WriteLine(user.Name);
    /// }
    /// </code>
    /// </example>
    public async Task<User> GetUserAsync(int id)
    {
        if (id <= 0)
            throw new ArgumentException("User ID must be positive", nameof(id));
            
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            throw new UserNotFoundException($"User with ID {id} not found");
            
        return user;
    }
}
```

### **Комментарии в коде**
```csharp
public class OrderProcessor
{
    public async Task<OrderResult> ProcessOrderAsync(Order order)
    {
        // Валидация входных данных
        if (order == null)
            throw new ArgumentNullException(nameof(order));
            
        if (order.Items.Count == 0)
            return OrderResult.Failure("Order must contain at least one item");
        
        // Проверка доступности товаров на складе
        var availabilityResult = await CheckInventoryAvailabilityAsync(order.Items);
        if (!availabilityResult.IsAvailable)
            return OrderResult.Failure("Some items are out of stock");
        
        /*
         * Сложная логика расчета скидок:
         * - Скидка постоянного клиента
         * - Сезонные акции
         * - Промокоды
         */
        var discount = await CalculateDiscountAsync(order);
        order.ApplyDiscount(discount);
        
        // TODO: Добавить логику применения налогов
        // FIXME: Исправить округление при расчете итоговой суммы
        
        return OrderResult.Success(order);
    }
}
```

## 8. Тестирование

### **Структура unit-тестов**
```csharp
// Именование тестов: MethodName_Scenario_ExpectedResult
public class UserServiceTests
{
    private readonly UserService _userService;
    private readonly Mock<IUserRepository> _userRepositoryMock;
    
    public UserServiceTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _userService = new UserService(_userRepositoryMock.Object);
    }
    
    [Fact]
    public async Task GetUserAsync_ValidId_ReturnsUser()
    {
        // Arrange
        var userId = 1;
        var expectedUser = new User { Id = userId, Name = "Test User" };
        _userRepositoryMock
            .Setup(repo => repo.GetByIdAsync(userId))
            .ReturnsAsync(expectedUser);
        
        // Act
        var result = await _userService.GetUserAsync(userId);
        
        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(userId);
        result.Name.Should().Be("Test User");
        _userRepositoryMock.Verify(repo => repo.GetByIdAsync(userId), Times.Once);
    }
    
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void GetUserAsync_InvalidId_ThrowsArgumentException(int invalidId)
    {
        // Act & Assert
        Func<Task> act = async () => await _userService.GetUserAsync(invalidId);
        act.Should().ThrowAsync<ArgumentException>();
    }
}
```

## 9. Конфигурация и настройки

### **Классы конфигурации**
```csharp
public class DatabaseSettings
{
    public const string SectionName = "Database";
    
    public string ConnectionString { get; set; } = string.Empty;
    public int CommandTimeout { get; set; } = 30;
    public bool EnableSensitiveDataLogging { get; set; }
}

public class EmailSettings
{
    public const string SectionName = "Email";
    
    public string SmtpServer { get; set; } = string.Empty;
    public int Port { get; set; } = 587;
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public bool EnableSsl { get; set; } = true;
}

// Использование в Startup
services.Configure<DatabaseSettings>(
    configuration.GetSection(DatabaseSettings.SectionName));
```

## 10. Best Practices и антипаттерны

### **ПРАВИЛЬНО**
```csharp
// Использование readonly и const
public class Calculator
{
    private readonly IMathService _mathService;
    private const double Pi = 3.14159;
    
    public Calculator(IMathService mathService)
    {
        _mathService = mathService;
    }
}

// Использование using для disposable объектов
public async Task<string> ReadFileAsync(string path)
{
    using var reader = new StreamReader(path);
    return await reader.ReadToEndAsync();
}

// Nullable reference types
public class User
{
    public string Name { get; set; } = string.Empty; // Не null
    public string? MiddleName { get; set; }         // Может быть null
}
```

### **НЕПРАВИЛЬНО**
```csharp
// Магические числа
if (status == 3)  // Что такое 3?
{
    // ...
}

// Вместо этого:
public class OrderStatus
{
    public const int Pending = 1;
    public const int Processing = 2;
    public const int Completed = 3;
}

if (status == OrderStatus.Completed)
{
    // ...
}

// Избыточные проверки
if (user != null)
{
    if (user.Name != null)
    {
        if (user.Name.Length > 0)
        {
            // ...
        }
    }
}

// Вместо этого:
if (!string.IsNullOrEmpty(user?.Name))
{
    // ...
}
```

## 11. .editorconfig пример
```ini
# EditorConfig для C#
root = true

[*]
indent_style = space
indent_size = 4
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
end_of_line = crlf

[*.cs]
# Стиль именования
dotnet_naming_rule.private_members_with_underscore.symbols = private_fields
dotnet_naming_rule.private_members_with_underscore.style = prefix_underscore
dotnet_naming_rule.private_members_with_underscore.severity = warning

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.prefix_underscore.capitalization = camel_case
dotnet_naming_style.prefix_underscore.required_prefix = _

# Форматирование
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true
csharp_indent_case_contents = true
csharp_indent_switch_labels = true

# Качество кода
dotnet_diagnostic.CA2007.severity = warning
dotnet_diagnostic.CA2016.severity = warning
```

## Ключевые правила CodeStyle для C#:

1. **Соглашения именования** - PascalCase для типов, camelCase для переменных
2. **Четкая структура** - логическое расположение членов класса  
3. **Явные модификаторы** - всегда указывать уровень доступа
4. **Правильная обработка исключений** - специфичные catch блоки
5. **Асинхронность** - правильное использование async/await
6. **Документация** - XML комментарии для публичных API
7. **Тестируемость** - четкая структура unit-тестов
8. **Чистота кода** - избегание антипаттернов и магических чисел
9. **Безопасность** - использование readonly, using, nullable types
10. **Консистентность** - единый стиль во всем проекте