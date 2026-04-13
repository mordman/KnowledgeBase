## 🔹 Что такое API Gateway?

**API Gateway** (шлюз API) — это серверный компонент, который выступает **единой точкой входа** для клиентских запросов в распределённую архитектуру (чаще всего микросервисную). Вместо того чтобы клиенты напрямую обращались к десяткам внутренних сервисов, они отправляют запросы шлюзу, который анализирует их, применяет политики безопасности и маршрутизирует к нужному бэкенду.

### 🧩 Ключевые функции
| Функция | Описание |
|--------|----------|
| **Маршрутизация** | Перенаправление запросов к нужному сервису по URL, заголовкам, методам |
| **Агрегация** | Сбор данных из нескольких сервисов в один ответ (BFF-паттерн) |
| **Аутентификация/Авторизация** | Валидация JWT, OAuth2, API-ключей, ролевой доступ |
| **Rate Limiting / Throttling** | Ограничение частоты запросов по IP, клиенту, тарифу |
| **Кэширование** | Сохранение ответов на частые `GET`-запросы для снижения нагрузки |
| **Трансформация** | Изменение форматов (XML↔JSON), заголовков, версий API, протоколов |
| **Resilience** | Retry, Circuit Breaker, Fallback (часто через Polly) |
| **Наблюдаемость** | Логирование, метрики, распределённая трассировка |

### 💡 Примеры использования
1. **Маршрутизация**: `POST /api/v2/orders` → шлюз проверяет токен → перенаправляет в `OrderService` (`http://order-svc:8080/orders`).
2. **Агрегация**: `GET /api/user-dashboard` → шлюз параллельно вызывает `UserService`, `OrderService`, `NotificationService`, объединяет JSON и возвращает один объект.
3. **Rate Limiting**: Бесплатный тариф → 100 запросов/мин. При превышении шлюз возвращает `429 Too Many Requests` без нагрузки на бэкенд.
4. **Кэширование**: `GET /api/products?category=electronics` кэшируется на 5 мин. Повторные запросы отдаются из памяти шлюза.

---

## 🛠 Популярные API Gateway для C# / .NET

### 1. **Ocelot**
- **Тип**: Open-source, первый зрелый .NET API Gateway
- **Конфигурация**: Преимущественно JSON (`ocelot.json`), частично через код
- **Возможности**:
  - Динамическая маршрутизация, приоритеты, переписывание путей
  - Service Discovery (Consul, Eureka, Kubernetes)
  - Rate Limiting, QoS (интеграция с Polly)
  - JWT/OIDC аутентификация, кэширование, логирование
- ✅ **Плюсы**: Готовые функции "из коробки", много примеров, легко начать, подходит для средних проектов
- ❌ **Минусы**: Производительность ниже, чем у YARP; конфигурация становится громоздкой; развитие замедлилось
- 📦 **Поддержка**: .NET 6–8 (стабильно работает и на .NET 9)

### 2. **YARP (Yet Another Reverse Proxy)**
- **Тип**: Официальный высокопроизводительный обратный прокси от Microsoft
- **Конфигурация**: JSON + код (полный контроль через ASP.NET Core middleware)
- **Возможности**:
  - Маршрутизация, балансировка нагрузки, health checks
  - Трансформация запросов/заголовков, кастомные фильтры
  - Интеграция с Polly (retry, circuit breaker, timeout)
  - Поддержка HTTP/1.1, HTTP/2, gRPC, WebSockets
- ✅ **Плюсы**: Экстремальная производительность (близка к Nginx), активная поддержка Microsoft, идеален для высоконагруженных сценариев, гибкая кастомизация
- ❌ **Минусы**: Нет встроенного rate limiting / кэширования (реализуется через middleware или библиотеки вроде `AspNetCoreRateLimit`), требует больше кода для продвинутой логики
- 📦 **Поддержка**: .NET 6–9. **Рекомендуется Microsoft для новых проектов**.

### 3. **Azure API Management (APIM)**
- **Тип**: Полностью управляемое облачное решение (PaaS)
- **Конфигурация**: Политики через XML, ARM/Bicep, Azure CLI, Portal
- **Возможности**:
  - Версионирование API, портал разработчика, подписки
  - Мониторинг (Application Insights), аналитика, алерты
  - Трансформация, аутентификация, rate limiting, GraphQL/gRPC поддержка
  - Интеграция с Azure Functions, Logic Apps, Key Vault, Managed Identities
- ✅ **Плюсы**: Enterprise-уровень, SLA, минимум инфраструктуры, встроенная аналитика, поддержка мульти-облака
- ❌ **Минусы**: Платный, вендор-лок, меньше контроля над низкоуровневой логикой
- 📦 **Поддержка**: Работает с любыми бэкендами, включая .NET, Java, Python, Node.js

> 📌 **Не .NET, но часто используются вместе с C#**: `Kong`, `Envoy`, `NGINX`, `Traefik`. Они мощные, но требуют отдельного стека и часто настраиваются через YAML/Lua.

---

## 📊 Сравнительная таблица

| Критерий | Ocelot | YARP | Azure APIM |
|----------|--------|------|------------|
| **Лицензия** | MIT | MIT | Платный (SaaS/PaaS) |
| **Производительность** | Средняя | Высокая (ближе к Nginx) | Высокая (зависит от тарифа) |
| **Готовые функции** | ✅ Rate limit, кэш, Discovery | ❌ (требует middleware) | ✅ Полноценный набор |
| **Кастомизация** | Ограничена конфигом | Полная (C# middleware) | Ограничена политиками XML |
| **Сложность внедрения** | Низкая | Средняя | Низкая (облако) |
| **Лучше для** | Средние проекты, быстрый старт | Высокая нагрузка, кастомная логика | Enterprise, облако, compliance |

---

## 💻 Пример минимальной настройки YARP (.NET 8/9)

**`Program.cs`**
```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();
app.MapReverseProxy();
app.Run();
```

**`appsettings.json`**
```json
{
  "ReverseProxy": {
    "Routes": {
      "orders-route": {
        "ClusterId": "orders-cluster",
        "Match": { "Path": "/api/orders/{**catch-all}" }
      },
      "users-route": {
        "ClusterId": "users-cluster",
        "Match": { "Path": "/api/users/{**catch-all}" }
      }
    },
    "Clusters": {
      "orders-cluster": {
        "Destinations": {
          "orders-dest": { "Address": "http://order-service:8080/" }
        }
      },
      "users-cluster": {
        "Destinations": {
          "users-dest": { "Address": "http://user-service:8080/" }
        }
      }
    }
  }
}
```

Для добавления rate limiting в YARP можно использовать пакет `AspNetCoreRateLimit` или написать кастомный middleware. Для resilience — `Microsoft.Extensions.Http.Resilience` + Polly.

---

## 🎯 Как выбрать?
- 🟢 **Нужен быстрый старт + готовые функции** → `Ocelot`
- 🔵 **Высокая нагрузка + кастомная логика на C#** → `YARP` (рекомендация Microsoft)
- 🟣 **Enterprise, облако, минимум инфраструктуры** → `Azure API Management`
- 🟡 **Кроссплатформенный стек / уже есть инфраструктура** → `Kong`, `Envoy`, `Traefik`

API Gateway — не обязательный компонент для монолита, но **критичен для микросервисов, публичных API и многоканальных приложений**. В .NET-экосистеме `YARP` сегодня является де-факто стандартом для self-hosted решений, а `Ocelot` остаётся выбором для проектов, где важна готовая конфигурация без написания кода.

Вот практические, production-ready примеры для **.NET 8/9**. Я покажу, как реализовать JWT-аутентификацию, Rate Limiting и агрегацию ответов в **YARP** и **Ocelot**, с учётом современных паттернов ASP.NET Core.

---

## 🔐 1. JWT-аутентификация

### 🟦 YARP
YARP не имеет встроенной аутентификации, но отлично интегрируется со стандартным пайплайном ASP.NET Core.

**`Program.cs`**
```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;

var builder = WebApplication.CreateBuilder(args);

// 1. Настраиваем JWT
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = "https://your-identity-server.com";
        options.Audience = "api-gateway";
        options.TokenValidationParameters.ValidateAudience = true;
    });

builder.Services.AddAuthorization();

// 2. Подключаем YARP
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();

// 3. Middleware порядок критичен!
app.UseAuthentication();
app.UseAuthorization();

// Защищённые маршруты
app.MapReverseProxy(config => 
{
    config.RequireAuthorization(); // Требует валидный JWT для всех проксируемых запросов
});

// Если нужны публичные маршруты, мапьте их отдельно или используйте кастомную политику
app.Run();
```

### 🟧 Ocelot
Ocelot настраивает аутентификацию через конфиг + DI.

**`Program.cs`**
```csharp
builder.Services.AddAuthentication()
    .AddJwtBearer("Bearer", options =>
    {
        options.Authority = "https://your-identity-server.com";
        options.Audience = "api-gateway";
    });

builder.Services.AddOcelot();
// ...
await app.UseOcelot();
```

**`ocelot.json`**
```json
{
  "Routes": [
    {
      "DownstreamPathTemplate": "/api/orders/{everything}",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{ "Host": "order-svc", "Port": 8080 }],
      "UpstreamPathTemplate": "/api/orders/{everything}",
      "AuthenticationOptions": {
        "AuthenticationProviderKey": "Bearer",
        "AllowedScopes": ["orders.read"]
      }
    }
  ]
}
```
> 💡 Ocelot автоматически проверит токен и scope **до** отправки запроса в downstream-сервис.

---

## ⏱ 2. Rate Limiting (Ограничение запросов)

С **.NET 7+** в фреймворке появился встроенный `Microsoft.AspNetCore.RateLimiting`. Он работает **и в YARP, и в Ocelot** одинаково, поэтому писать кастомные middleware больше не нужно.

**`Program.cs` (универсально)**
```csharp
using System.Threading.RateLimiting;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRateLimiter(options =>
{
    // Политика: 100 запросов в минуту по IP
    options.AddFixedWindowLimiter("ip-limit", opt =>
    {
        opt.PermitLimit = 100;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.QueueLimit = 50;
        opt.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
    });

    // Политика: 10 запросов в минуту для авторизованных пользователей
    options.AddFixedWindowLimiter("user-limit", opt =>
    {
        opt.PermitLimit = 10;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.QueueLimit = 0;
    });

    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    options.OnRejected = (ctx, ct) =>
    {
        ctx.HttpContext.Response.Headers.RetryAfter = "60";
        return ValueTask.CompletedTask;
    };
});

// ... настройка YARP или Ocelot ...

var app = builder.Build();
app.UseRateLimiter(); // ← Включает middleware

// Применяем к YARP
app.MapReverseProxy().RequireRateLimiting("ip-limit");

// Или к Ocelot (работает глобально до обработки роутов)
app.UseOcelot();
app.Run();
```

> ✅ **Преимущество**: Не зависит от шлюза, легко менять политики, поддерживает метрики (`System.Diagnostics.Metrics`).

---

## 📦 3. Агрегация ответов (BFF-паттерн)

### 🟧 Ocelot (встроенная агрегация)
Ocelot умеет объединять ответы нескольких роутов в один.

**`ocelot.json`**
```json
{
  "Routes": [
    { "UpstreamPathTemplate": "/users/{id}", "Downstream...": "...", "RouteKey": "user-route" },
    { "UpstreamPathTemplate": "/orders?userId={id}", "Downstream...": "...", "RouteKey": "orders-route" }
  ],
  "Aggregates": [
    {
      "ReRouteKeys": [ "user-route", "orders-route" ],
      "UpstreamPathTemplate": "/api/dashboard/{id}",
      "Aggregator": "DashboardAggregator"
    }
  ]
}
```

**`DashboardAggregator.cs`**
```csharp
using Ocelot.Aggregation;

public class DashboardAggregator : IDefinedAggregator
{
    public async Task<DownstreamResponse> Aggregate(List<HttpContext> responses)
    {
        // responses[0] -> User, responses[1] -> Orders
        var userJson = await responses[0].Items.DownstreamResponse().Content.ReadAsStringAsync();
        var ordersJson = await responses[1].Items.DownstreamResponse().Content.ReadAsStringAsync();

        var result = $"{{\"user\":{userJson},\"orders\":{ordersJson}}}";
        
        return new DownstreamResponse(
            new StringContent(result, Encoding.UTF8, "application/json"),
            HttpStatusCode.OK,
            new List<KeyValuePair<string, IEnumerable<string>>>(),
            "OK");
    }
}
```
⚠️ **Нюанс**: Агрегация в Ocelot работает, но сложна в отладке и не поддерживает async-параллельные вызовы "из коробки". Для сложных сценариев Microsoft рекомендует выносить BFF в отдельный сервис.

### 🟦 YARP (рекомендуемый подход: отдельный BFF-эндпоинт)
YARP **не агрегирует** по дизайну (это чистый reverse-proxy). Современный паттерн: рядом с шлюзом поднимается минимальный API, который собирает данные.

**`BffEndpoints.cs`**
```csharp
// В Program.cs
app.MapGet("/api/dashboard/{userId}", async (string userId, IHttpClientFactory http, CancellationToken ct) =>
{
    using var client = http.CreateClient("backend");
    
    // Параллельные запросы к микросервисам
    var userTask = client.GetFromJsonAsync<UserDto>($"/users/{userId}", ct);
    var ordersTask = client.GetFromJsonAsync<List<OrderDto>>($"/orders?userId={userId}", ct);
    
    await Task.WhenAll(userTask, ordersTask);
    
    return Results.Ok(new
    {
        User = userTask.Result,
        Orders = ordersTask.Result
    });
}).RequireAuthorization(); // + Rate Limiting при желании
```

**`Program.cs` (настройка HttpClient)**
```csharp
builder.Services.AddHttpClient("backend", client =>
{
    client.BaseAddress = new Uri("http://internal-network/"); // или Discovery
    client.DefaultRequestVersion = HttpVersion.Version20;
});
```
> ✅ Это гибче, проще тестировать, легко кэшировать, добавлять fallback-логику и Polly.

---

## 🛠 Сводная таблица реализации

| Функция | YARP | Ocelot |
|--------|------|--------|
| **JWT Auth** | ASP.NET Core middleware (`AddAuthentication`) | `AuthenticationOptions` в конфиге + `AddJwtBearer` в DI |
| **Rate Limit** | Встроенный `Microsoft.AspNetCore.RateLimiting` (`.NET 7+`) | Тот же фреймворковый лимитер или `EnableRateLimiting` в конфиге (устаревает) |
| **Агрегация** | ❌ Нет. Рекомендуется отдельный BFF-сервис/эндпоинт | ✅ Встроена через `Aggregates` + `IDefinedAggregator` |
| **Кэш** | Кастомный middleware или `IDistributedCache` | Встроенный `FileCache` / `Redis` через конфиг |
| **Service Discovery** | `Yarp.ReverseProxy.ServiceDiscovery` (Consul, K8s) | Встроенный провайдер Consul, Eureka, Config |

---

## 💡 Архитектурные рекомендации (2025–2026)

1. **Не превращайте Gateway в монолит**. Если логика агрегации, трансформации или сложной авторизации занимает >50 строк кода → выносите в отдельный BFF-сервис.
2. **Используйте YARP как транспорт**, а бизнес-логику (валидация, обогащение данных) оставляйте в ASP.NET Core middleware или отдельных сервисах.
3. **Для Rate Limiting в продакшене** используйте распределённый кэш (Redis) через `IDistributedCache`, чтобы лимиты работали в кластере шлюзов.
4. **Observability**: подключите `OpenTelemetry` на уровне шлюза. Все запросы будут трассироваться до downstream-сервисов без изменения их кода.

## API Gateway Template

Вот расширенный production-шаблон с **Redis-кэшированием** и **BFF-агрегацией**. Архитектура сохраняет YARP как транспорт, добавляет слой агрегации рядом с ним, использует `IDistributedCache` для Redis и `Microsoft.Extensions.Http.Resilience` (Polly) для отказоустойчивости.

---

## 📦 1. Новые NuGet-пакеты
```bash
dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
dotnet add package Microsoft.Extensions.Http.Resilience
```

---

## 📄 2. `appsettings.json`
Добавляем секции для Redis и адресов микросервисов.
```json
{
  "Logging": { "LogLevel": { "Default": "Information", "Microsoft.AspNetCore": "Warning", "Yarp": "Debug" } },
  "AllowedHosts": "*",
  "Jwt": {
    "Authority": "https://your-auth-server.com",
    "Audience": "api-gateway"
  },
  "Redis": {
    "ConnectionString": "redis:6379,password=,ssl=false,abortConnect=false"
  },
  "Backend": {
    "UserService": "http://mock-user-svc:80",
    "OrderService": "http://mock-order-svc:80"
  },
  "ReverseProxy": {
    "Routes": {
      "orders-route": {
        "ClusterId": "orders-cluster",
        "Match": { "Path": "/api/orders/{**catch-all}" },
        "Transforms": [{ "PathRemovePrefix": "/api/orders" }, { "PathPrefix": "/orders" }]
      },
      "users-route": {
        "ClusterId": "users-cluster",
        "Match": { "Path": "/api/users/{**catch-all}" }
      }
    },
    "Clusters": {
      "orders-cluster": { "Destinations": { "d1": { "Address": "http://mock-order-svc:80" } } },
      "users-cluster": { "Destinations": { "d1": { "Address": "http://mock-user-svc:80" } } }
    }
  }
}
```

---

## 🗃️ 3. `Models/Dto.cs`
Простые DTO для агрегации.
```csharp
namespace ApiGateway.Models;

public record UserDto(string Id, string Name, string Email);
public record OrderDto(string OrderId, string Product, decimal Amount);
public record DashboardDto(UserDto User, List<OrderDto> Orders, DateTime GeneratedAt);
```

---

## 🧩 4. `Services/DashboardService.cs`
Отвечает за параллельный запрос к бэкендам, обработку ошибок и кэширование в Redis.
```csharp
using System.Text.Json;
using Microsoft.Extensions.Caching.Distributed;
using ApiGateway.Models;

namespace ApiGateway.Services;

public class DashboardService
{
    private readonly IHttpClientFactory _httpFactory;
    private readonly IDistributedCache _cache;
    private readonly ILogger<DashboardService> _logger;

    public DashboardService(IHttpClientFactory httpFactory, IDistributedCache cache, ILogger<DashboardService> logger)
    {
        _httpFactory = httpFactory;
        _cache = cache;
        _logger = logger;
    }

    public async Task<DashboardDto?> GetDashboardAsync(string userId, CancellationToken ct = default)
    {
        var cacheKey = $"bff:dashboard:{userId}";
        
        // 1. Проверяем кэш
        var cached = await _cache.GetStringAsync(cacheKey, ct);
        if (!string.IsNullOrEmpty(cached))
            return JsonSerializer.Deserialize<DashboardDto>(cached);

        var client = _httpFactory.CreateClient("backend");

        // 2. Параллельные запросы с обработкой сбоев
        Task<UserDto?> userTask = null;
        Task<List<OrderDto>?> ordersTask = null;

        try { userTask = client.GetFromJsonAsync<UserDto>($"/users/{userId}", ct); }
        catch (Exception ex) { _logger.LogWarning(ex, "User service failed for {UserId}", userId); }

        try { ordersTask = client.GetFromJsonAsync<List<OrderDto>>($"/orders?userId={userId}", ct); }
        catch (Exception ex) { _logger.LogWarning(ex, "Order service failed for {UserId}", userId); }

        if (userTask != null) await userTask;
        if (ordersTask != null) await ordersTask;

        var user = userTask?.Result;
        var orders = ordersTask?.Result ?? new();

        if (user is null && !orders.Any())
            return null; // Оба упали или пользователь не найден

        var result = new DashboardDto(user!, orders, DateTime.UtcNow);

        // 3. Сохраняем в Redis на 5 минут
        var options = new DistributedCacheEntryOptions { AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5) };
        await _cache.SetStringAsync(cacheKey, JsonSerializer.Serialize(result), options, ct);

        return result;
    }
}
```

---

## 🌐 5. `Endpoints/BffEndpoints.cs`
Выделяем BFF в отдельный файл для чистоты.
```csharp
using ApiGateway.Services;
using Microsoft.AspNetCore.Mvc;

namespace ApiGateway.Endpoints;

public static class BffEndpoints
{
    public static void MapBffEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/bff")
                       .RequireAuthorization()
                       .RequireRateLimiting("global-ip")
                       .WithTags("BFF");

        group.MapGet("/dashboard/{userId}", async (
            [FromRoute] string userId, 
            DashboardService service, 
            CancellationToken ct) =>
        {
            var dashboard = await service.GetDashboardAsync(userId, ct);
            return dashboard is null ? Results.NotFound() : Results.Ok(dashboard);
        })
        .WithName("GetDashboard")
        .WithOpenApi();
    }
}
```

---

## ⚙️ 6. `Program.cs` (обновлённый)
```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.RateLimiting;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using System.Threading.RateLimiting;
using ApiGateway.Endpoints;
using ApiGateway.Services;

var builder = WebApplication.CreateBuilder(args);

// 🔹 1. OpenTelemetry
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("api-gateway"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation().AddOtlpExporter())
    .WithMetrics(m => m.AddAspNetCoreInstrumentation().AddHttpClientInstrumentation().AddOtlpExporter());

// 🔹 2. Redis Distributed Cache
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration["Redis:ConnectionString"];
    options.InstanceName = "gateway:";
});

// 🔹 3. Rate Limiting
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("global-ip", opt =>
    {
        opt.PermitLimit = 100;
        opt.Window = TimeSpan.FromMinutes(1);
        opt.QueueLimit = 20;
    });
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});

// 🔹 4. Auth
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Jwt:Authority"]!;
        options.Audience = builder.Configuration["Jwt:Audience"]!;
    });
builder.Services.AddAuthorization();

// 🔹 5. HttpClient + Resilience (Polly)
builder.Services.AddHttpClient("backend")
    .ConfigureHttpClient(client => client.Timeout = TimeSpan.FromSeconds(5))
    .AddStandardResilienceHandler(); // Retry, Circuit Breaker, Timeout из коробки

// 🔹 6. BFF Service
builder.Services.AddScoped<DashboardService>();

// 🔹 7. YARP
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

builder.Services.AddHealthChecks();

var app = builder.Build();

// ⚠️ Порядок middleware
app.UseRateLimiter();
app.UseAuthentication();
app.UseAuthorization();

// Публичные
app.MapHealthChecks("/health");
app.MapGet("/", () => "API Gateway + BFF + Redis");

// BFF Endpoints
app.MapBffEndpoints();

// YARP Proxy
app.MapReverseProxy(proxyConfig =>
{
    proxyConfig.RequireAuthorization();
    proxyConfig.RequireRateLimiting("global-ip");
});

app.Run();
```

---

## 🐳 7. `docker-compose.yml` (с Redis)
```yaml
version: '3.8'
services:
  api-gateway:
    build: .
    ports:
      - "5000:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
      - Jwt__Authority=https://mock-auth.local
      - Jwt__Audience=api-gateway
      - Redis__ConnectionString=redis:6379
      - Backend__UserService=http://mock-user-svc:80
      - Backend__OrderService=http://mock-order-svc:80
    depends_on:
      - redis
      - jaeger
      - mock-user-svc
      - mock-order-svc

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes: ["redis-data:/data"]
    command: redis-server --appendonly yes

  mock-user-svc:
    image: kennethreitz/httpbin
    ports: ["5002:80"]

  mock-order-svc:
    image: kennethreitz/httpbin
    ports: ["5003:80"]

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports: ["16686:16686", "4317:4317"]

volumes:
  redis-data:
```

---

## 🧪 8. Тестирование

1. **Запуск:** `docker compose up -d --build`
2. **Проверка кэша (первый запрос):**
   ```bash
   curl -H "Authorization: Bearer <VALID_JWT>" http://localhost:5000/bff/dashboard/user123
   ```
   ⏱ Первый запрос займёт ~200-500мс (обращение к бэкендам). Ответ: `{"user":{...},"orders":[...],"generatedAt":"..."}`
3. **Второй запрос (из Redis):**
   Тот же URL ответит за **<10мс**. Данные берутся из `redis:6379`.
4. **Просмотр кэша:**
   ```bash
   docker exec -it <redis-container> redis-cli KEYS "gateway:*"
   ```
5. **Отказоустойчивость:** Остановите `mock-order-svc`. Запрос к `/bff/dashboard/` вернёт только `user`, логи покают предупреждение, но шлюз не упадёт благодаря `try/catch` + Polly retry.

---

## 📌 Архитектурные нюансы (2025+)

| Компонент | Почему так |
|-----------|------------|
| **BFF рядом с Gateway** | Не смешивайте агрегацию с проксированием. BFF — это отдельный логический слой, но физически может жить в одном процессе для экономии ресурсов на старте. |
| `IDistributedCache` vs `OutputCaching` | `OutputCaching` удобен для простых `GET`, но в BFF часто нужна бизнес-логика (частичные ответы, обогащение, условный кэш). `IDistributedCache` даёт полный контроль. |
| **Resilience Handler** | `.AddStandardResilienceHandler()` включает `RetryStrategyOptions` (3 попытки), `CircuitBreakerStrategyOptions` (разрыв цепи при 50% ошибок) и `TimeoutStrategyOptions`. Не нужно писать Polly вручную. |
| **Redis в кластере** | Встроенный `FixedWindowLimiter` работает в памяти ноды. Для распределённого rate limiting используйте `AspNetCoreRateLimit.Redis` или кастомный `PartitionedRateLimiter<string>` с Redis. |

---

## 🛠 Production-чеклист перед деплоем
- [ ] Замените `kennethreitz/httpbin` на реальные сервисы или Consul/K8s Service Discovery
- [ ] Настройте `Redis__ConnectionString` с паролем и TLS для продакшена
- [ ] Добавьте `IHostedService` для валидации подключения к Redis при старте
- [ ] Настройте `Metrics` на `System.Net.Http` и `StackExchange.Redis` для мониторинга в Grafana
- [ ] Для распределённого rate limiting подключите `Microsoft.AspNetCore.RateLimiting` с кастомным `Partitioner` по IP/User

Если нужно, добавлю:
- 🔹 **Service Discovery** (Consul/K8s) для динамических `Clusters`
- 🔹 **GraphQL BFF** поверх тех же сервисов
- 🔹 **Распределённый Rate Limiter** на Redis с sliding window