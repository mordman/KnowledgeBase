# Webhook — описание, применение и примеры на C#

## Что такое Webhook?

**Webhook** (веб-хук) — это механизм, при котором одно приложение автоматически отправляет HTTP-запрос (обычно POST) другому приложению при наступлении определённого события. Это реализация паттерна **"push"-уведомлений** — в отличие от polling, где клиент постоянно опрашивает сервер, здесь сервер сам уведомляет клиента.

Проще говоря: **webhook — это "обратный API-вызов"**. Вместо того чтобы спрашивать "есть что-то новое?", вы говорите "если что-то произойдёт — стукни мне сюда".

## Как это работает

```
1. Клиент регистрирует URL (endpoint) на сервере-источнике
2. Происходит событие (новый заказ, коммит в Git, платёж)
3. Сервер отправляет HTTP POST на зарегистрированный URL с payload
4. Клиент принимает запрос, обрабатывает и отвечает 2xx
```

## Где и для чего используется

| Область | Пример |
|---------|--------|
| **Платёжные системы** | Stripe, ЮKassa, PayPal — уведомления об успешной оплате |
| **CI/CD** | GitHub, GitLab — триггер сборки при push или pull request |
| **Мессенджеры** | Telegram Bot API, Slack, Discord — приём сообщений от пользователей |
| **CRM/ERP** | Bitrix24, amoCRM — уведомления о новых сделках |
| **Мониторинг** | Grafana, Prometheus Alertmanager — алерты |
| **SaaS-интеграции** | Zapier, IFTTT — связка сервисов |
| **Email-сервисы** | SendGrid, Mailgun — статусы доставки писем |

## Преимущества и недостатки

**Плюсы:**
- Мгновенные уведомления (real-time)
- Меньше нагрузки, чем polling
- Простота (обычный HTTP)

**Минусы:**
- Нужен публичный endpoint
- Требуется защита (подпись, секрет)
- Нет гарантии доставки — нужны retry-механизмы

## Примеры на C#

### 1. Приём webhook (ASP.NET Core Minimal API)

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Секрет, известный только нам и отправителю
const string WebhookSecret = "super-secret-key";

app.MapPost("/webhooks/payment", async (HttpContext context) =>
{
    // Читаем тело запроса
    using var reader = new StreamReader(context.Request.Body);
    var body = await reader.ReadToEndAsync();

    // Проверяем подпись (HMAC-SHA256)
    var signature = context.Request.Headers["X-Signature"].ToString();
    if (!VerifySignature(body, signature, WebhookSecret))
    {
        return Results.Unauthorized();
    }

    // Парсим payload
    var payload = JsonSerializer.Deserialize<PaymentEvent>(body);
    if (payload is null)
        return Results.BadRequest("Invalid payload");

    // Обрабатываем событие
    Console.WriteLine($"Получен платёж: {payload.PaymentId}, сумма: {payload.Amount}");

    // Возвращаем 200, чтобы отправитель не повторял запрос
    return Results.Ok(new { received = true });
});

app.Run();

static bool VerifySignature(string body, string signature, string secret)
{
    using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
    var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(body));
    var computed = Convert.ToHexString(hash).ToLowerInvariant();
    return CryptographicOperations.FixedTimeEquals(
        Encoding.UTF8.GetBytes(computed),
        Encoding.UTF8.GetBytes(signature));
}

record PaymentEvent(string PaymentId, decimal Amount, string Status);
```

### 2. Приём webhook в контроллере

```csharp
[ApiController]
[Route("webhooks")]
public class WebhookController : ControllerBase
{
    private readonly ILogger<WebhookController> _logger;

    public WebhookController(ILogger<WebhookController> logger) => _logger = logger;

    [HttpPost("github")]
    public async Task<IActionResult> GitHubWebhook(
        [FromBody] GitHubPushEvent payload,
        [FromHeader(Name = "X-GitHub-Event")] string eventType)
    {
        _logger.LogInformation("Событие {Event}: {Count} коммитов в {Repo}",
            eventType, payload.Commits.Length, payload.Repository.FullName);

        // Тут можно запустить сборку
        return Ok();
    }
}

public class GitHubPushEvent
{
    public string Ref { get; set; } = "";
    public Commit[] Commits { get; set; } = Array.Empty<Commit>();
    public Repository Repository { get; set; } = new();
}

public class Commit { public string Id { get; set; } = ""; public string Message { get; set; } = ""; }
public class Repository { public string FullName { get; set; } = ""; }
```

### 3. Отправка webhook другому сервису

```csharp
public class WebhookSender
{
    private readonly HttpClient _http;

    public WebhookSender(HttpClient http) => _http = http;

    public async Task SendAsync<T>(string url, T payload, string secret)
    {
        var json = JsonSerializer.Serialize(payload);

        // Подписываем тело запроса
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
        var signature = Convert.ToHexString(
            hmac.ComputeHash(Encoding.UTF8.GetBytes(json))).ToLowerInvariant();

        var request = new HttpRequestMessage(HttpMethod.Post, url)
        {
            Content = new StringContent(json, Encoding.UTF8, "application/json")
        };
        request.Headers.Add("X-Signature", signature);
        request.Headers.Add("X-Webhook-Id", Guid.NewGuid().ToString());

        // Retry-политика
        for (int attempt = 1; attempt <= 3; attempt++)
        {
            try
            {
                var response = await _http.SendAsync(request);
                if (response.IsSuccessStatusCode) return;
            }
            catch (HttpRequestException) when (attempt < 3)
            {
                await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, attempt)));
            }
        }

        throw new Exception("Не удалось доставить webhook после 3 попыток");
    }
}
```

### 4. Регистрация в DI и использование

```csharp
// Program.cs
builder.Services.AddHttpClient<WebhookSender>();
builder.Services.AddHostedService<OrderEventPublisher>();

// Пример сервиса, который шлёт webhook при создании заказа
public class OrderEventPublisher : BackgroundService
{
    private readonly WebhookSender _sender;
    private readonly IConfiguration _config;

    public OrderEventPublisher(WebhookSender sender, IConfiguration config)
    {
        _sender = sender;
        _config = config;
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        // ... логика получения событий (например, из очереди)
        await _sender.SendAsync(
            _config["Webhook:Url"]!,
            new { orderId = 42, status = "created" },
            _config["Webhook:Secret"]!
        );
    }
}
```

## Best practices

1. **Всегда проверяйте подпись** (HMAC) — иначе злоумышленник подделает запрос.
2. **Используйте HTTPS** — payload может содержать чувствительные данные.
3. **Возвращайте 2xx быстро** — обработку выносите в очередь (RabbitMQ, Kafka, Channel).
4. **Идемпотентность** — webhook может прийти повторно, храните ID события.
5. **Retry с backoff** — если получатель недоступен, отправитель обычно повторяет.
6. **Логируйте всё** — для отладки и аудита.
7. **Таймауты** — не держите соединение долго (обычно 5–30 секунд).

## Итог

Webhook — это простой, но мощный способ организации событийно-ориентированного взаимодействия между сервисами. В C# он реализуется через ASP.NET Core (приём) и `HttpClient` (отправка), а безопасность обеспечивается проверкой HMAC-подписи и идемпотентной обработкой.

---

Аналоги webhook, такие как дуплексный WCF или gRPC, по сути решают ту же задачу — доставку события от сервера клиенту, но используют принципиально иной подход. Если webhook — это «одноразовый выстрел» по HTTP-адресу, то WCF Duplex и gRPC — это постоянные соединения.

Вот ключевые различия и примеры.

### Что общего и в чём разница

| Характеристика | Webhook | Дуплексный WCF | gRPC (стриминг) |
| :--- | :--- | :--- | :--- |
| **Модель связи** | Push (сервер → клиент) | Дуплекс (две стороны) | Дуплекс (две стороны) |
| **Соединение** | Новое на каждое событие | Постоянное (сессия) | Постоянное (HTTP/2) |
| **Транспорт** | HTTP(S) | TCP, HTTP, Named Pipes | HTTP/2 |
| **Контракт** | Неявный (payload JSON) | Явный (ServiceContract) | Явный (Protobuf .proto) |
| **Основное применение** | Уведомления из SaaS | Legacy .NET-системы | Микросервисы, высоконагруженные системы |

---

### Дуплексный WCF

Это классический механизм .NET Framework для организации обратных вызовов. Служба получает от клиента **канал обратного вызова** и может вызывать методы на стороне клиента так же, как клиент вызывает методы службы.

**Когда использовать:** В существующих .NET Framework приложениях, где нужна тесная интеграция и постоянное соединение (например, внутренние корпоративные системы).

**Как работает:**
1.  Определяется **контракт службы** с указанием `CallbackContract` — интерфейса, который будет реализовывать клиент.
2.  Клиент при подключении передаёт реализацию этого интерфейса в `InstanceContext`.
3.  Служба получает ссылку на канал через `OperationContext.Current.GetCallbackChannel<T>()` и вызывает методы.

**Пример (контракты):**

```csharp
// Контракт, который вызывает клиент (запросы к серверу)
[ServiceContract(CallbackContract = typeof(IClientCallback))]
public interface IServerService
{
    [OperationContract(IsOneWay = true)]
    void RegisterClient();
}

// Контракт обратного вызова (сервер стучится к клиенту)
public interface IClientCallback
{
    [OperationContract(IsOneWay = true)]
    void OnEvent(string message);
}
```

**Пример (сервер):**

```csharp
[ServiceBehavior(InstanceContextMode = InstanceContextMode.PerSession)]
public class ServerService : IServerService
{
    public void RegisterClient()
    {
        // Получаем канал для общения с конкретным клиентом
        var callback = OperationContext.Current.GetCallbackChannel<IClientCallback>();
        // Вызываем метод на клиенте (webhook-подобное поведение)
        callback.OnEvent("Событие с сервера!");
    }
}
```

**Нюанс:** Дуплексный WCF требует сессий и специфических привязок (например, `netTcpBinding` или `wsDualHttpBinding`). Это сложный и «тяжёлый» механизм, который часто критикуют за избыточность для простых задач.

---

### gRPC

Современная альтернатива, построенная на HTTP/2 и Protocol Buffers. gRPC поддерживает **двунаправленный стриминг** (bidirectional streaming), что делает его прямым аналогом дуплексного WCF, но кроссплатформенным и производительным.

**Когда использовать:** В микросервисной архитектуре, для высоконагруженных систем или когда нужна строгая типизация контрактов.

**Как работает (Bidirectional Streaming):**
Клиент и сервер открывают один RPC-вызов, в рамках которого **обе стороны могут отправлять и читать поток сообщений** одновременно.

**Пример (определение .proto):**

```protobuf
service EventService {
  // Двунаправленный стриминг: и клиент, и сервер шлют потоки
  rpc Subscribe(stream ClientMessage) returns (stream ServerEvent);
}
```

**Пример (сервер на C#):**

```csharp
public class EventService : EventService.EventServiceBase
{
    public override async Task Subscribe(
        IAsyncStreamReader<ClientMessage> requestStream,
        IServerStreamWriter<ServerEvent> responseStream,
        ServerCallContext context)
    {
        // Читаем от клиента и пишем клиенту в одном цикле
        await foreach (var request in requestStream.ReadAllAsync())
        {
            // Отправляем событие обратно (webhook-подобное поведение)
            await responseStream.WriteAsync(new ServerEvent 
            { 
                Message = $"Ответ на: {request.Text}" 
            });
        }
    }
}
```

**Важное правило gRPC:** При стриминге `StartRead` и `StartWrite` не являются потокобезопасными — нельзя одновременно вызывать две записи или два чтения.

---

**Webhook и SignalR решают разные задачи и не являются взаимозаменяемыми.** Webhook — это механизм уведомлений между сервисами (Server-to-Server), а SignalR — это фреймворк для реального времени в браузере или приложении (Server-to-Client).

Вот ключевые различия:

### 📊 Сравнение

| Характеристика | Webhook | SignalR |
| :--- | :--- | :--- |
| **Направление** | Однонаправленный (событие → получатель)  | Двунаправленный (полный дуплекс)  |
| **Соединение** | Разовое, новое на каждое событие  | Постоянное (WebSocket, SSE, Long Polling)  |
| **Аудитория** | Server-to-Server, B2B, интеграции с SaaS  | Server-to-Client, пользователи в реальном времени  |
| **Контракт** | HTTP POST с JSON payload | RPC-вызовы методов на клиенте |

### 🔔 Когда использовать Webhook

Webhook — это **паттерн уведомлений**, а не фреймворк . Он идеален для интеграции с внешними системами, где вы не контролируете клиента.

**Примеры:**
- **Платежи:** PayPal уведомляет ваш сервер об успешной оплате, отправляя POST на ваш URL .
- **CI/CD:** GitHub отправляет событие при push, чтобы запустить сборку.
- **SaaS:** Dropbox, Slack уведомляют о новых файлах или сообщениях .

**Преимущества:**
- Не требует постоянного соединения .
- Легковесный, работает поверх стандартного HTTP.
- Простая интеграция с внешними сервисами.

**Недостатки:**
- Нет встроенного retry — нужно реализовывать самому.
- Требует публичный endpoint и проверку подписи.

### 📡 Когда использовать SignalR

SignalR — это **абстракция над постоянным соединением**, которая автоматически выбирает лучший транспорт (WebSockets → Server-Sent Events → Long Polling) . Он создан для сценариев, где **пользователь ждет мгновенных обновлений в интерфейсе**.

**Примеры:**
- **Чаты и мессенджеры:** мгновенная доставка сообщений .
- **Дашборды и трейдинг:** обновление котировок и метрик в реальном времени .
- **Совместная работа:** редактирование документов несколькими пользователями .
- **Уведомления в веб-приложении:** «Ваш заказ готов» без перезагрузки страницы.

**Преимущества:**
- Автоматический выбор транспорта (fallback) .
- Встроенные группы для рассылки конкретным пользователям .
- Автоматическое переподключение.

**Недостатки:**
- Требует постоянного соединения (проблемы с корпоративными прокси).
- При горизонтальном масштабировании нужен backplane (Redis, Azure Service Bus) .

### 🔗 Как они работают вместе (комплементарность)

Это не конкуренты, а **взаимодополняющие технологии**. Типичный сценарий:

1.  **Webhook** приходит на ваш сервер от внешнего сервиса (например, оплата от PayPal) .
2.  Ваш сервер обрабатывает событие и через **SignalR** мгновенно уведомляет об этом пользователя в браузере .

**Итог:** Webhook — для связи **между сервисами**, SignalR — для связи **с пользователем** в реальном времени.