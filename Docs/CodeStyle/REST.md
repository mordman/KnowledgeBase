# CodeStyle для REST API



## Оглавление
- [1. Общие принципы REST](#1-общие-принципы-rest)
  - [**RESTful Constraints**](#restful-constraints)
- [2. Соглашения по именованию](#2-соглашения-по-именованию)
  - [**Ресурсы и endpoints**](#ресурсы-и-endpoints)
  - [**Иерархические ресурсы**](#иерархические-ресурсы)
  - [**Коллекции и операции**](#коллекции-и-операции)
- [3. HTTP методы и их семантика](#3-http-методы-и-их-семантика)
  - [**CRUD операции**](#crud-операции)
  - [**Не-CRUD операции**](#не-crud-операции)
- [4. Коды состояния HTTP](#4-коды-состояния-http)
  - [**Успешные ответы (2xx)**](#успешные-ответы-2xx)
  - [**Ошибки клиента (4xx)**](#ошибки-клиента-4xx)
  - [**Ошибки сервера (5xx)**](#ошибки-сервера-5xx)
- [5. Форматы данных](#5-форматы-данных)
  - [**Request/Response форматы**](#requestresponse-форматы)
  - [**Обработка ошибок**](#обработка-ошибок)
- [6. Версионирование API](#6-версионирование-api)
  - [**Стратегии версионирования**](#стратегии-версионирования)
  - [**Миграция между версиями**](#миграция-между-версиями)
- [7. Безопасность и аутентификация](#7-безопасность-и-аутентификация)
  - [**Авторизация**](#авторизация)
  - [**Rate Limiting**](#rate-limiting)
- [8. Пагинация, фильтрация, сортировка](#8-пагинация-фильтрация-сортировка)
  - [**Стандартные параметры**](#стандартные-параметры)
- [9. Документирование API](#9-документирование-api)
  - [**Swagger/OpenAPI конфигурация**](#swaggeropenapi-конфигурация)
- [10. Best Practices](#10-best-practices)
  - [**Кодстайл C# для REST API**](#кодстайл-c-для-rest-api)
  - [**Глобальные настройки**](#глобальные-настройки)
- [Ключевые правила CodeStyle для REST:](#ключевые-правила-codestyle-для-rest)

  - [**RESTful Constraints**](#restful-constraints)
  - [**Ресурсы и endpoints**](#ресурсы-и-endpoints)
  - [**Иерархические ресурсы**](#иерархические-ресурсы)
  - [**Коллекции и операции**](#коллекции-и-операции)
  - [**CRUD операции**](#crud-операции)
  - [**Не-CRUD операции**](#не-crud-операции)
  - [**Успешные ответы (2xx)**](#успешные-ответы-2xx)
  - [**Ошибки клиента (4xx)**](#ошибки-клиента-4xx)
  - [**Ошибки сервера (5xx)**](#ошибки-сервера-5xx)
  - [**Request/Response форматы**](#requestresponse-форматы)
  - [**Обработка ошибок**](#обработка-ошибок)
  - [**Стратегии версионирования**](#стратегии-версионирования)
  - [**Миграция между версиями**](#миграция-между-версиями)
  - [**Авторизация**](#авторизация)
  - [**Rate Limiting**](#rate-limiting)
  - [**Стандартные параметры**](#стандартные-параметры)
  - [**Swagger/OpenAPI конфигурация**](#swaggeropenapi-конфигурация)
  - [**Кодстайл C# для REST API**](#кодстайл-c-для-rest-api)
  - [**Глобальные настройки**](#глобальные-настройки)
## 1. Общие принципы REST

### **RESTful Constraints**
- **Client-Server** - разделение ответственности
- **Stateless** - отсутствие состояния на сервере
- **Cacheable** - поддержка кэширования
- **Uniform Interface** - единообразный интерфейс
- **Layered System** - многоуровневая архитектура
- **Code on Demand** (опционально) - исполняемый код на клиенте

## 2. Соглашения по именованию

### **Ресурсы и endpoints**
```csharp
// ПРАВИЛЬНО - существительные во множественном числе
GET /api/users
GET /api/users/123
POST /api/users
PUT /api/users/123
DELETE /api/users/123

// НЕПРАВИЛЬНО
GET /api/getUser/123
POST /api/createUser
GET /api/user/list
```

### **Иерархические ресурсы**
```csharp
// Вложенные ресурсы
GET /api/users/123/orders          // Заказы пользователя 123
GET /api/users/123/orders/456      // Конкретный заказ пользователя
POST /api/users/123/orders         // Создать заказ для пользователя

// Альтернатива - фильтрация
GET /api/orders?userId=123         // Заказы пользователя 123
```

### **Коллекции и операции**
```csharp
// Поиск и фильтрация
GET /api/users?active=true
GET /api/users?role=admin&department=IT
GET /api/users?name=john&page=1&pageSize=20

// Сортировка
GET /api/users?sort=name,asc&sort=createdAt,desc

// Поля
GET /api/users?fields=id,name,email
```

## 3. HTTP методы и их семантика

### **CRUD операции**
```csharp
// CREATE
POST /api/users
// Body: { "name": "John", "email": "john@example.com" }
// Response: 201 Created + Location header

// READ
GET /api/users                    // Коллекция
GET /api/users/123                // Один ресурс
// Response: 200 OK

// UPDATE
PUT /api/users/123               // Полное обновление
// Body: { "id": 123, "name": "John", "email": "new@email.com" }
// Response: 200 OK или 204 No Content

PATCH /api/users/123             // Частичное обновление
// Body: { "email": "new@email.com" }
// Response: 200 OK

// DELETE
DELETE /api/users/123
// Response: 204 No Content
```

### **Не-CRUD операции**
```csharp
// Действия над ресурсами
POST /api/users/123/activate      // Активация пользователя
POST /api/users/123/deactivate    // Деактивация
POST /api/orders/456/cancel       // Отмена заказа
POST /api/products/789/publish    // Публикация товара

// Bulk операции
POST /api/users/bulk-delete
// Body: { "ids": [123, 456, 789] }

// Search операции
POST /api/users/search
// Body: { "filters": { "role": "admin", "active": true } }
```

## 4. Коды состояния HTTP

### **Успешные ответы (2xx)**
```csharp
// 200 OK - стандартный успешный ответ
return Ok(users);
return Ok(new { message = "Success" });

// 201 Created - ресурс создан
[HttpPost]
public IActionResult CreateUser([FromBody] User user)
{
    var createdUser = _userService.Create(user);
    return CreatedAtAction(
        nameof(GetUser), 
        new { id = createdUser.Id }, 
        createdUser
    );
}

// 202 Accepted - запрос принят, обработка асинхронно
[HttpPost("import")]
public IActionResult ImportUsers([FromBody] List<User> users)
{
    var jobId = _backgroundService.StartImport(users);
    return Accepted(new { jobId = jobId });
}

// 204 No Content - успешно, но без тела ответа
[HttpDelete("{id}")]
public IActionResult DeleteUser(int id)
{
    _userService.Delete(id);
    return NoContent();
}
```

### **Ошибки клиента (4xx)**
```csharp
// 400 Bad Request - невалидный запрос
if (!ModelState.IsValid)
    return BadRequest(ModelState);

if (user == null)
    return BadRequest("User data is required");

// 401 Unauthorized - не аутентифицирован
if (!User.Identity.IsAuthenticated)
    return Unauthorized();

// 403 Forbidden - нет прав
if (!User.HasPermission("delete_users"))
    return Forbid();

// 404 Not Found - ресурс не найден
var user = _userService.GetById(id);
if (user == null)
    return NotFound($"User with id {id} not found");

// 409 Conflict - конфликт (дублирование, нарушение constraints)
try 
{
    _userService.Create(user);
}
catch (DuplicateUserException ex)
{
    return Conflict(new { error = ex.Message });
}

// 422 Unprocessable Entity - семантические ошибки
if (!_validationService.IsValid(user))
    return UnprocessableEntity(_validationService.GetErrors());
```

### **Ошибки сервера (5xx)**
```csharp
// 500 Internal Server Error - общая серверная ошибка
try 
{
    // операция
}
catch (Exception ex)
{
    _logger.LogError(ex, "Error processing request");
    return StatusCode(500, "Internal server error");
}

// 503 Service Unavailable - сервис временно недоступен
if (!_externalService.IsAvailable())
    return StatusCode(503, "Service temporarily unavailable");
```

## 5. Форматы данных

### **Request/Response форматы**
```csharp
// Content-Type заголовки
Content-Type: application/json
Accept: application/json
Accept: application/xml

// Стандартный JSON response
{
    "data": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com",
        "createdAt": "2023-01-15T10:30:00Z"
    },
    "meta": {
        "version": "1.0",
        "timestamp": "2023-01-15T10:31:00Z"
    }
}

// Коллекция с пагинацией
{
    "data": [
        { "id": 1, "name": "User 1" },
        { "id": 2, "name": "User 2" }
    ],
    "pagination": {
        "page": 1,
        "pageSize": 20,
        "totalCount": 150,
        "totalPages": 8
    },
    "links": {
        "self": "/api/users?page=1",
        "next": "/api/users?page=2",
        "prev": null
    }
}
```

### **Обработка ошибок**
```csharp
// Стандартный формат ошибки
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "email",
                "message": "Email is required"
            },
            {
                "field": "password", 
                "message": "Password must be at least 8 characters"
            }
        ],
        "timestamp": "2023-01-15T10:31:00Z",
        "traceId": "abc-123-def-456"
    }
}

// Глобальный обработчик ошибок в ASP.NET Core
public class ErrorHandlingMiddleware
{
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (NotFoundException ex)
        {
            context.Response.StatusCode = 404;
            await context.Response.WriteAsJsonAsync(new {
                error = new { message = ex.Message }
            });
        }
        catch (ValidationException ex)
        {
            context.Response.StatusCode = 400;
            await context.Response.WriteAsJsonAsync(new {
                error = new { 
                    message = "Validation failed",
                    details = ex.Errors
                }
            });
        }
        catch (Exception ex)
        {
            context.Response.StatusCode = 500;
            await context.Response.WriteAsJsonAsync(new {
                error = new { message = "Internal server error" }
            });
        }
    }
}
```

## 6. Версионирование API

### **Стратегии версионирования**
```csharp
// 1. URL версионирование
[ApiController]
[Route("api/v1/[controller]")]
public class UsersController : ControllerBase { }

// 2. Query string версионирование
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase 
{
    [HttpGet]
    public IActionResult GetUsers([FromQuery] string apiVersion = "1.0") { }
}

// 3. Header версионирование
[ApiVersion("1.0")]
[Route("api/[controller]")]
public class UsersController : ControllerBase { }

// Запрос: GET /api/users
// Headers: Api-Version: 1.0
```

### **Миграция между версиями**
```csharp
// V1 - старая версия
[ApiVersion("1.0")]
[Route("api/v1/[controller]")]
public class UsersV1Controller : ControllerBase
{
    [HttpGet]
    public IActionResult GetUsers() 
    {
        return Ok(new { users = _userService.GetAll() });
    }
}

// V2 - новая версия с пагинацией
[ApiVersion("2.0")]
[Route("api/v2/[controller]")]
public class UsersV2Controller : ControllerBase
{
    [HttpGet]
    public IActionResult GetUsers([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
    {
        var result = _userService.GetPaginated(page, pageSize);
        return Ok(new {
            data = result.Items,
            pagination = result.Pagination
        });
    }
}
```

## 7. Безопасность и аутентификация

### **Авторизация**
```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize] // Глобальная авторизация
public class UsersController : ControllerBase
{
    [HttpGet]
    [AllowAnonymous] // Разрешить анонимный доступ
    public IActionResult GetPublicUsers() { }
    
    [HttpGet("profile")]
    [Authorize(Roles = "User,Admin")] // Ролевая авторизация
    public IActionResult GetProfile() { }
    
    [HttpPost]
    [Authorize(Policy = "CanCreateUsers")] // Policy-based авторизация
    public IActionResult CreateUser([FromBody] User user) { }
    
    [HttpDelete("{id}")]
    [Authorize(Policy = "CanDeleteUsers")]
    public IActionResult DeleteUser(int id) 
    {
        // Проверка владения ресурсом
        var user = _userService.GetById(id);
        if (user.CreatedBy != User.Identity.Name)
            return Forbid();
            
        _userService.Delete(id);
        return NoContent();
    }
}
```

### **Rate Limiting**
```csharp
// Ограничение запросов
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    [HttpPost("login")]
    [LimitRequests(MaxRequests = 5, TimeWindow = 60)] // 5 запросов в минуту
    public IActionResult Login([FromBody] LoginRequest request) { }
    
    [HttpPost("register")]
    [LimitRequests(MaxRequests = 3, TimeWindow = 3600)] // 3 запроса в час
    public IActionResult Register([FromBody] RegisterRequest request) { }
}
```

## 8. Пагинация, фильтрация, сортировка

### **Стандартные параметры**
```csharp
[HttpGet]
public async Task<IActionResult> GetUsers(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 20,
    [FromQuery] string sortBy = "name",
    [FromQuery] string sortOrder = "asc",
    [FromQuery] string search = null,
    [FromQuery] string role = null,
    [FromQuery] bool? active = null)
{
    var filter = new UserFilter
    {
        Page = page,
        PageSize = pageSize,
        SortBy = sortBy,
        SortOrder = sortOrder,
        Search = search,
        Role = role,
        Active = active
    };
    
    var result = await _userService.GetFilteredAsync(filter);
    
    return Ok(new {
        data = result.Items,
        pagination = new {
            page = result.Page,
            pageSize = result.PageSize,
            totalCount = result.TotalCount,
            totalPages = result.TotalPages
        },
        links = new {
            self = Url.Action("GetUsers", new { page, pageSize }),
            next = result.HasNext ? Url.Action("GetUsers", new { page = page + 1, pageSize }) : null,
            prev = result.HasPrevious ? Url.Action("GetUsers", new { page = page - 1, pageSize }) : null
        }
    });
}
```

## 9. Документирование API

### **Swagger/OpenAPI конфигурация**
```csharp
// Настройка Swagger
services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo 
    { 
        Title = "User API", 
        Version = "v1",
        Description = "API for managing users",
        Contact = new OpenApiContact { Name = "Support", Email = "support@example.com" }
    });
    
    // JWT аутентификация в Swagger
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });
});

// Атрибуты для документации
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class UsersController : ControllerBase
{
    /// <summary>
    /// Get user by ID
    /// </summary>
    /// <param name="id">User identifier</param>
    /// <returns>User details</returns>
    /// <response code="200">Returns the user</response>
    /// <response code="404">User not found</response>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(UserDto), 200)]
    [ProducesResponseType(typeof(ErrorResponse), 404)]
    public async Task<IActionResult> GetUser(int id)
    {
        // implementation
    }
}
```

## 10. Best Practices

### **Кодстайл C# для REST API**
```csharp
// Правильные названия методов
public class UsersController : ControllerBase
{
    // GET /api/users
    [HttpGet]
    public IActionResult GetUsers() { }
    
    // GET /api/users/123
    [HttpGet("{id}")]
    public IActionResult GetUser(int id) { }
    
    // POST /api/users
    [HttpPost]
    public IActionResult CreateUser([FromBody] User user) { }
    
    // PUT /api/users/123
    [HttpPut("{id}")]
    public IActionResult UpdateUser(int id, [FromBody] User user) { }
    
    // DELETE /api/users/123
    [HttpDelete("{id}")]
    public IActionResult DeleteUser(int id) { }
    
    // POST /api/users/123/activate
    [HttpPost("{id}/activate")]
    public IActionResult ActivateUser(int id) { }
}

// DTO классы для request/response
public class CreateUserRequest
{
    [Required]
    [EmailAddress]
    public string Email { get; set; }
    
    [Required]
    [StringLength(100, MinimumLength = 6)]
    public string Password { get; set; }
    
    [Required]
    public string Name { get; set; }
}

public class UserResponse
{
    public int Id { get; set; }
    public string Email { get; set; }
    public string Name { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}

// Service layer
public interface IUserService
{
    Task<UserResponse> CreateUserAsync(CreateUserRequest request);
    Task<UserResponse> GetUserAsync(int id);
    Task<PagedResult<UserResponse>> GetUsersAsync(UserFilter filter);
    Task<UserResponse> UpdateUserAsync(int id, UpdateUserRequest request);
    Task DeleteUserAsync(int id);
}
```

### **Глобальные настройки**
```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers()
        .ConfigureApiBehaviorOptions(options =>
        {
            // Отключение автоматической валидации модели
            options.SuppressModelStateInvalidFilter = true;
        })
        .AddJsonOptions(options =>
        {
            // Форматирование JSON
            options.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
            options.JsonSerializerOptions.WriteIndented = Environment.IsDevelopment();
        });
    
    // Глобальная фильтрация
    services.AddMvc(options =>
    {
        options.Filters.Add<ValidationFilter>();
        options.Filters.Add<ExceptionFilter>();
        options.Filters.Add<LoggingFilter>();
    });
}
```

## Ключевые правила CodeStyle для REST:

1. **Используйте существительные** для ресурсов
2. **Придерживайтесь семантики HTTP** методов
3. **Используйте правильные коды состояния**
4. **Версионируйте API** с самого начала
5. **Стандартизируйте форматы** ответов и ошибок
6. **Документируйте** endpoints
7. **Реализуйте пагинацию** для коллекций
8. **Обрабатывайте ошибки** единообразно
9. **Используйте DTO** для request/response
10. **Следуйте принципам безопасности**