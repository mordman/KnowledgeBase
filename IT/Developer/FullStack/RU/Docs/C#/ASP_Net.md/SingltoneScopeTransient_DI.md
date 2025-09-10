В .NET (особенно в ASP.NET Core) для регистрации зависимостей в контейнере внедрения зависимостей (DI-контейнере) используются методы `AddSingleton`, `AddScoped` и `AddTransient`. Они определяют **время жизни (lifetime)** сервиса. Далее — подробное описание каждого из них, сценарии использования, ограничения и возможность передачи сервисов друг в друга.

---

## 1. **AddSingleton**
### Описание:
Сервис создаётся **один раз** и используется **всем приложением** до его завершения.
### Сценарии использования:
- **Глобальные настройки** (например, конфигурация приложения).
- **Кэш** (например, `IMemoryCache`).
- **Логгеры** (если они потокобезопасны).
- **Статические данные** (например, список стран, справочники).
### Ограничения:
- **Не потокобезопасные сервисы** могут вызвать проблемы при параллельном доступе.
- **Состояние сервиса** сохраняется на всё время работы приложения (может привести к утечкам памяти, если не очищать кэш или ресурсы).
### Примеры:
1. **Конфигурация приложения:**
   ```csharp
   services.AddSingleton<IConfiguration>(Configuration);
   ```
2. **Кэш в памяти:**
   ```csharp
   services.AddSingleton<IMemoryCache, MemoryCache>();
   ```
3. **Логгер:**
   ```csharp
   services.AddSingleton<ILogger, FileLogger>();
   ```
4. **Список стран:**
   ```csharp
   services.AddSingleton<IReadOnlyList<Country>>(new List<Country> { ... });
   ```
5. **HTTP-клиент с фиксированными настройками:**
   ```csharp
   services.AddSingleton<HttpClient>(new HttpClient { BaseAddress = new Uri("https://api.example.com") });
   ```

---

## 2. **AddScoped**
### Описание:
Сервис создаётся **один раз на запрос** (в контексте HTTP-запроса или другого "scope").
### Сценарии использования:
- **Сервисы, зависящие от контекста запроса** (например, `DbContext` в Entity Framework Core).
- **Логика бизнес-процессов**, которая должна быть изолирована на уровне запроса.
- **Авторизация и аутентификация** (например, `IUserService`).
### Ограничения:
- **Нельзя использовать вне контекста запроса** (например, в фоновых задачах или singleton-сервисах).
- **Утечка ресурсов**, если не освобождать их правильно (например, не вызывать `Dispose` для `DbContext`).
### Примеры:
6. **Контекст базы данных:**
   ```csharp
   services.AddScoped<ApplicationDbContext>();
   ```
7. **Сервис пользователя:**
   ```csharp
   services.AddScoped<IUserService, UserService>();
   ```
8. **Сервис корзины покупок:**
   ```csharp
   services.AddScoped<ShoppingCart>();
   ```
9. **Сервис авторизации:**
   ```csharp
   services.AddScoped<IAuthorizationService, AuthorizationService>();
   ```
10. **Сервис для работы с файлами в контексте запроса:**
    ```csharp
    services.AddScoped<IFileUploadService, FileUploadService>();
    ```

---

## 3. **AddTransient**
### Описание:
Сервис создаётся **каждый раз**, когда он запрашивается.
### Сценарии использования:
- **Лёгкие сервисы без состояния** (например, утилиты, валидаторы).
- **Сервисы, которые не должны сохранять состояние между вызовами**.
- **Тестирование** (легко заменять моки).
### Ограничения:
- **Низкая производительность**, если создание сервиса ресурсоёмкое.
- **Не подходит для сервисов с состоянием** (например, кэш или подключение к БД).
### Примеры:
11. **Сервис отправки email:**
    ```csharp
    services.AddTransient<IEmailService, EmailService>();
    ```
12. **Валидатор данных:**
    ```csharp
    services.AddTransient<IValidator, ProductValidator>();
    ```
13. **Сервис генерации отчётов:**
    ```csharp
    services.AddTransient<IReportGenerator, ReportGenerator>();
    ```
14. **Сервис для работы с API:**
    ```csharp
    services.AddTransient<IApiClient, ApiClient>();
    ```
15. **Сервис для логирования в файл (если не потокобезопасен):**
    ```csharp
    services.AddTransient<ILogger, FileLogger>();
    ```

---

## Можно ли передавать сервисы друг в друга?
### Правила:
1. **Singleton → Scoped/Transient:** **НЕЛЬЗЯ** (приведёт к ошибке, так как singleton создаётся один раз, а scoped/transient — позднее).
   - **Исключение:** Если singleton не зависит от scoped/transient напрямую (например, через фабрику).
2. **Scoped → Singleton:** **МОЖНО** (но singleton будет жить дольше, чем scoped).
3. **Scoped → Transient:** **МОЖНО** (transient создаётся каждый раз).
4. **Transient → Singleton/Scoped:** **МОЖНО** (но transient не должен сохранять состояние).

### Пример ошибки:
```csharp
// Ошибка: Singleton зависит от Scoped
services.AddSingleton<SingletonService>();
services.AddScoped<ScopedService>();
// В конструкторе SingletonService: public SingletonService(ScopedService scoped) { ... }
// Приведёт к исключению: Cannot consume scoped service from singleton.
```

### Пример корректного использования:
```csharp
// OK: Scoped зависит от Transient
services.AddScoped<ScopedService>();
services.AddTransient<TransientService>();
// В конструкторе ScopedService: public ScopedService(TransientService transient) { ... }
```

---

## Итоговая таблица

| Метод          | Время жизни               | Сценарии использования                     | Ограничения                                  |
|----------------|---------------------------|--------------------------------------------|---------------------------------------------|
| **Singleton**  | На всё время приложения   | Конфигурация, кэш, логгеры                | Не потокобезопасность, утечки памяти        |
| **Scoped**     | На запрос                 | DbContext, сервисы пользователя           | Нельзя использовать вне запроса             |
| **Transient**  | На каждый вызов           | Утилиты, валидаторы, лёгкие сервисы       | Низкая производительность при сложном создании |

---