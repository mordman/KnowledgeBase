# NBomber - Описание и сценарии использования



## Оглавление
  - [Что такое NBomber?](#что-такое-nbomber)
  - [Ключевые особенности](#ключевые-особенности)
  - [Установка](#установка)
- [Установка как .NET Global Tool](#установка-как-net-global-tool)
- [Создание проекта](#создание-проекта)
  - [Базовые сценарии использования](#базовые-сценарии-использования)
    - [1. Тестирование HTTP API](#1-тестирование-http-api)
    - [2. Тестирование базы данных (Oracle)](#2-тестирование-базы-данных-oracle)
    - [3. Тестирование gRPC сервисов](#3-тестирование-grpc-сервисов)
  - [Продвинутые сценарии](#продвинутые-сценарии)
    - [4. Сложное нагрузочное тестирование](#4-сложное-нагрузочное-тестирование)
    - [5. Тестирование с кастомными метриками](#5-тестирование-с-кастомными-метриками)
  - [Сценарии использования в реальных проектах](#сценарии-использования-в-реальных-проектах)
    - [1. **Е-commerce платформа**](#1-е-commerce-платформа)
    - [2. **Финансовые транзакции**](#2-финансовые-транзакции)
    - [3. **IoT платформа**](#3-iot-платформа)
    - [4. **API Gateway**](#4-api-gateway)
  - [Анализ результатов](#анализ-результатов)
  - [Преимущества перед JMeter](#преимущества-перед-jmeter)
  - [Рекомендации по использованию](#рекомендации-по-использованию)

  - [Что такое NBomber?](#что-такое-nbomber)
  - [Ключевые особенности](#ключевые-особенности)
  - [Установка](#установка)
  - [Базовые сценарии использования](#базовые-сценарии-использования)
    - [1. Тестирование HTTP API](#1-тестирование-http-api)
    - [2. Тестирование базы данных (Oracle)](#2-тестирование-базы-данных-oracle)
    - [3. Тестирование gRPC сервисов](#3-тестирование-grpc-сервисов)
  - [Продвинутые сценарии](#продвинутые-сценарии)
    - [4. Сложное нагрузочное тестирование](#4-сложное-нагрузочное-тестирование)
    - [5. Тестирование с кастомными метриками](#5-тестирование-с-кастомными-метриками)
  - [Сценарии использования в реальных проектах](#сценарии-использования-в-реальных-проектах)
    - [1. **Е-commerce платформа**](#1-е-commerce-платформа)
    - [2. **Финансовые транзакции**](#2-финансовые-транзакции)
    - [3. **IoT платформа**](#3-iot-платформа)
    - [4. **API Gateway**](#4-api-gateway)
  - [Анализ результатов](#анализ-результатов)
  - [Преимущества перед JMeter](#преимущества-перед-jmeter)
  - [Рекомендации по использованию](#рекомендации-по-использованию)
## Что такое NBomber?

**NBomber** - это современный фреймворк для нагрузочного тестирования, написанный на C#. Это аналог Apache JMeter, но с акцентом на производительность и удобство использования.

## Ключевые особенности

- **Высокая производительность** - может генерировать тысячи запросов в секунду
- **Текстовые сценарии** на C# или F#
- **Поддержка различных протоколов**: HTTP, WebSockets, gRPC, SQL
- **Аналитика в реальном времени**
- **Графическая панель управления** (NBomber Dashboard)
- **Кросс-платформенность** (Windows, Linux, macOS)

## Установка

```bash
# Установка как .NET Global Tool
dotnet tool install -g NBomber

# Создание проекта
dotnet new console -n MyLoadTest
cd MyLoadTest
dotnet add package NBomber
```

## Базовые сценарии использования

### 1. Тестирование HTTP API

```csharp
using NBomber.CSharp;
using NBomber.Plugins.Http.CSharp;

public class HttpLoadTest
{
    public void Run()
    {
        var httpFactory = HttpClientFactory.Create();

        var step = Step.Create("get_users",
            clientFactory: httpFactory,
            execute: async context =>
            {
                var response = await context.Client.GetAsync("https://api.example.com/users");
                return response.IsSuccessStatusCode 
                    ? Response.Ok(statusCode: (int)response.StatusCode)
                    : Response.Fail(statusCode: (int)response.StatusCode);
            });

        var scenario = ScenarioBuilder
            .CreateScenario("http_test", step)
            .WithWarmUpDuration(TimeSpan.FromSeconds(10))
            .WithLoadSimulations(
                Simulation.InjectPerSec(rate: 100, during: TimeSpan.FromMinutes(5))
            );

        NBomberRunner
            .RegisterScenarios(scenario)
            .Run();
    }
}
```

### 2. Тестирование базы данных (Oracle)

```csharp
using NBomber.CSharp;
using Oracle.ManagedDataAccess.Client;

public class OracleLoadTest
{
    public void Run()
    {
        var connectionString = "User Id=user;Password=pass;Data Source=localhost:1521/XE";

        var step = Step.Create("oracle_query",
            execute: async context =>
            {
                using var connection = new OracleConnection(connectionString);
                await connection.OpenAsync();
                
                using var cmd = new OracleCommand(
                    "SELECT * FROM users WHERE status = :status", 
                    connection
                );
                cmd.Parameters.Add("status", "active");
                
                using var reader = await cmd.ExecuteReaderAsync();
                var count = 0;
                while (await reader.ReadAsync())
                    count++;
                
                return count > 0 
                    ? Response.Ok(sizeBytes: 1024) 
                    : Response.Fail();
            });

        var scenario = ScenarioBuilder
            .CreateScenario("oracle_test", step)
            .WithLoadSimulations(
                Simulation.InjectPerSec(rate: 50, during: TimeSpan.FromMinutes(3))
            );

        NBomberRunner
            .RegisterScenarios(scenario)
            .Run();
    }
}
```

### 3. Тестирование gRPC сервисов

```csharp
using NBomber.CSharp;
using Grpc.Net.Client;
using GrpcService;

public class GrpcLoadTest
{
    public void Run()
    {
        var channel = GrpcChannel.ForAddress("https://localhost:5001");
        var client = new Greeter.GreeterClient(channel);

        var step = Step.Create("grpc_call",
            execute: async context =>
            {
                try
                {
                    var response = await client.SayHelloAsync(
                        new HelloRequest { Name = "LoadTest" }
                    );
                    return Response.Ok();
                }
                catch
                {
                    return Response.Fail();
                }
            });

        var scenario = ScenarioBuilder
            .CreateScenario("grpc_test", step)
            .WithLoadSimulations(
                Simulation.RampingInject(
                    rate: 50, 
                    during: TimeSpan.FromSeconds(30),
                    to: 200
                )
            );

        NBomberRunner
            .RegisterScenarios(scenario)
            .Run();
    }
}
```

## Продвинутые сценарии

### 4. Сложное нагрузочное тестирование

```csharp
public class ComplexLoadTest
{
    public void Run()
    {
        // Многоэтапный сценарий
        var loginStep = Step.Create("login", ...);
        var getDataStep = Step.Create("get_data", ...);
        var updateStep = Step.Create("update_data", ...);

        var scenario = ScenarioBuilder
            .CreateScenario("complex_workflow", 
                loginStep, getDataStep, updateStep)
            .WithLoadSimulations(
                // Постепенное увеличение нагрузки
                Simulation.RampingInject(
                    rate: 10, 
                    during: TimeSpan.FromMinutes(2),
                    to: 100
                ),
                // Постоянная нагрузка
                Simulation.InjectPerSec(
                    rate: 100, 
                    during: TimeSpan.FromMinutes(10)
                ),
                // Спайк-тест
                Simulation.InjectPerSec(
                    rate: 500, 
                    during: TimeSpan.FromSeconds(30)
                )
            );

        NBomberRunner
            .RegisterScenarios(scenario)
            .WithReportFolder("load_test_reports")
            .WithReportFormats(ReportFormat.Html, ReportFormat.Txt)
            .Run();
    }
}
```

### 5. Тестирование с кастомными метриками

```csharp
public class CustomMetricsTest
{
    public void Run()
    {
        var step = Step.Create("api_call",
            execute: async context =>
            {
                var stopwatch = Stopwatch.StartNew();
                
                // Вызов API
                var response = await httpClient.GetAsync("...");
                
                stopwatch.Stop();
                
                // Кастомные метрики
                context.Logger.Information($"Response time: {stopwatch.ElapsedMilliseconds}ms");
                
                return Response.Ok(
                    sizeBytes: 1024,
                    latencyMs: stopwatch.ElapsedMilliseconds
                );
            });
    }
}
```

## Сценарии использования в реальных проектах

### 1. **Е-commerce платформа**
```csharp
// Тестирование пиковой нагрузки во время распродаж
Simulation.RampingInject(rate: 50, during: TimeSpan.FromMinutes(5), to: 1000),
Simulation.KeepConstant(copies: 1000, during: TimeSpan.FromMinutes(30))
```

### 2. **Финансовые транзакции**
```csharp
// Тестирование обработки транзакций с гарантированной доставкой
Simulation.InjectPerSec(rate: 200, during: TimeSpan.FromHours(1))
```

### 3. **IoT платформа**
```csharp
// Тестирование множества одновременных подключений
Simulation.InjectPerSec(rate: 5000, during: TimeSpan.FromMinutes(10))
```

### 4. **API Gateway**
```csharp
// Тестирование маршрутизации и балансировки нагрузки
var scenarios = new[]
{
    CreateScenario("auth_api"),
    CreateScenario("payment_api"), 
    CreateScenario("user_api")
};
```

## Анализ результатов

NBomber предоставляет детальные отчеты:
- **RPS (Requests Per Second)**
- **Latency** (мин/макс/средняя)
- **Data transfer** 
- **Error rate**
- **Percentiles** (P50, P75, P95, P99)

## Преимущества перед JMeter

1. **Производительность** - выше пропускная способность
2. **Гибкость** - полная мощность C# для сложной логики
3. **CI/CD интеграция** - легко интегрируется в пайплайны
4. **Меньшее потребление памяти**
5. **Современный UI** (через Dashboard)

## Рекомендации по использованию

1. **Начинайте с простых тестов** и постепенно усложняйте
2. **Используйте реалистичные данные** и сценарии
3. **Мониторьте ресурсы** тестового стенда
4. **Проводите тесты регулярно** для выявления регрессий
5. **Интегрируйте в CI/CD** для автоматического тестирования