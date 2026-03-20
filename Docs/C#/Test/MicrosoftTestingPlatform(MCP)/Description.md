# Microsoft.Testing.Platform - Описание и сценарии использования



## Оглавление
  - [Что такое Microsoft.Testing.Platform?](#что-такое-microsofttestingplatform)
  - [Ключевые особенности](#ключевые-особенности)
  - [Установка и настройка](#установка-и-настройка)
    - [Создание тестового проекта](#создание-тестового-проекта)
- [Создание проекта](#создание-проекта)
- [Добавление пакетов](#добавление-пакетов)
  - [Базовые сценарии использования](#базовые-сценарии-использования)
    - [1. Простой Unit Test](#1-простой-unit-test)
    - [2. Интеграционные тесты](#2-интеграционные-тесты)
  - [Продвинутые сценарии](#продвинутые-сценарии)
    - [3. Параметризованные тесты](#3-параметризованные-тесты)
    - [4. Тесты с моками и зависимостями](#4-тесты-с-моками-и-зависимостями)
    - [5. Performance тестирование](#5-performance-тестирование)
  - [Конфигурация платформы](#конфигурация-платформы)
    - [appsettings.json](#appsettingsjson)
    - [Program.cs с конфигурацией](#programcs-с-конфигурацией)
  - [Сценарии использования в реальных проектах](#сценарии-использования-в-реальных-проектах)
    - [6. Микросервисная архитектура](#6-микросервисная-архитектура)
    - [7. Тестирование с контейнерами Docker](#7-тестирование-с-контейнерами-docker)
    - [8. Расширение платформы через кастомные плагины](#8-расширение-платформы-через-кастомные-плагины)
  - [Интеграция с CI/CD](#интеграция-с-cicd)
    - [GitHub Actions](#github-actions)
  - [Преимущества Microsoft.Testing.Platform](#преимущества-microsofttestingplatform)
  - [Миграция с существующих фреймворков](#миграция-с-существующих-фреймворков)

  - [Что такое Microsoft.Testing.Platform?](#что-такое-microsofttestingplatform)
  - [Ключевые особенности](#ключевые-особенности)
  - [Установка и настройка](#установка-и-настройка)
    - [Создание тестового проекта](#создание-тестового-проекта)
  - [Базовые сценарии использования](#базовые-сценарии-использования)
    - [1. Простой Unit Test](#1-простой-unit-test)
    - [2. Интеграционные тесты](#2-интеграционные-тесты)
  - [Продвинутые сценарии](#продвинутые-сценарии)
    - [3. Параметризованные тесты](#3-параметризованные-тесты)
    - [4. Тесты с моками и зависимостями](#4-тесты-с-моками-и-зависимостями)
    - [5. Performance тестирование](#5-performance-тестирование)
  - [Конфигурация платформы](#конфигурация-платформы)
    - [appsettings.json](#appsettingsjson)
    - [Program.cs с конфигурацией](#programcs-с-конфигурацией)
  - [Сценарии использования в реальных проектах](#сценарии-использования-в-реальных-проектах)
    - [6. Микросервисная архитектура](#6-микросервисная-архитектура)
    - [7. Тестирование с контейнерами Docker](#7-тестирование-с-контейнерами-docker)
    - [8. Расширение платформы через кастомные плагины](#8-расширение-платформы-через-кастомные-плагины)
  - [Интеграция с CI/CD](#интеграция-с-cicd)
    - [GitHub Actions](#github-actions)
  - [Преимущества Microsoft.Testing.Platform](#преимущества-microsofttestingplatform)
  - [Миграция с существующих фреймворков](#миграция-с-существующих-фреймворков)
## Что такое Microsoft.Testing.Platform?

**Microsoft.Testing.Platform** - это новая кроссплатформенная платформа для тестирования от Microsoft, предназначенная для замены старых тестовых фреймворков (MSTest, NUnit, xUnit). Это единая, расширяемая платформа для всех типов тестирования в .NET экосистеме.

## Ключевые особенности

- **Унифицированная архитектура** для всех тестовых фреймворков
- **Высокая производительность** и масштабируемость
- **Расширяемость** через плагины
- **Кросс-платформенность** (Windows, Linux, macOS)
- **Поддержка современных сценариев** (unit, integration, e2e)
- **Интеграция с CI/CD** системами
- **Богатая аналитика** и отчетность

## Установка и настройка

### Создание тестового проекта

```xml
<!-- Project.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <OutputType>Exe</OutputType>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Testing.Platform" Version="1.0.0" />
    <PackageReference Include="MSTest" Version="3.2.0" />
  </ItemGroup>

</Project>
```

```bash
# Создание проекта
dotnet new console -n MyTestProject
cd MyTestProject

# Добавление пакетов
dotnet add package Microsoft.Testing.Platform
dotnet add package MSTest
```

## Базовые сценарии использования

### 1. Простой Unit Test

```csharp
using Microsoft.Testing.Platform;
using Microsoft.VisualStudio.TestTools.UnitTesting;

[TestClass]
public class CalculatorTests
{
    [TestMethod]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        var calculator = new Calculator();
        
        // Act
        var result = calculator.Add(3, 5);
        
        // Assert
        Assert.AreEqual(8, result);
    }
    
    [TestMethod]
    public void Divide_ByZero_ThrowsException()
    {
        // Arrange
        var calculator = new Calculator();
        
        // Act & Assert
        Assert.ThrowsException<DivideByZeroException>(
            () => calculator.Divide(10, 0)
        );
    }
}

// Тестируемый класс
public class Calculator
{
    public int Add(int a, int b) => a + b;
    public int Divide(int a, int b) => a / b;
}
```

### 2. Интеграционные тесты

```csharp
[TestClass]
public class DatabaseIntegrationTests
{
    private static string _connectionString;

    [ClassInitialize]
    public static void ClassInitialize(TestContext context)
    {
        _connectionString = "Server=localhost;Database=TestDB;Trusted_Connection=true;";
        InitializeTestDatabase();
    }

    [TestMethod]
    public async Task CreateUser_ValidData_UserCreated()
    {
        // Arrange
        var userService = new UserService(_connectionString);
        var user = new User { Name = "Test User", Email = "test@example.com" };
        
        // Act
        var userId = await userService.CreateUserAsync(user);
        
        // Assert
        Assert.IsTrue(userId > 0);
        
        var createdUser = await userService.GetUserAsync(userId);
        Assert.AreEqual(user.Name, createdUser.Name);
    }
    
    [TestMethod]
    public async Task GetUser_NonExistentId_ReturnsNull()
    {
        // Arrange
        var userService = new UserService(_connectionString);
        
        // Act
        var user = await userService.GetUserAsync(-1);
        
        // Assert
        Assert.IsNull(user);
    }
}
```

## Продвинутые сценарии

### 3. Параметризованные тесты

```csharp
[TestClass]
public class ParameterizedTests
{
    [TestMethod]
    [DataRow(1, 1, 2)]
    [DataRow(2, 3, 5)]
    [DataRow(-1, 1, 0)]
    [DataRow(0, 0, 0)]
    public void Add_VariousNumbers_ReturnsCorrectSum(int a, int b, int expected)
    {
        // Arrange
        var calculator = new Calculator();
        
        // Act
        var result = calculator.Add(a, b);
        
        // Assert
        Assert.AreEqual(expected, result);
    }
    
    [DynamicData(nameof(GetTestData), DynamicDataSourceType.Method)]
    [TestMethod]
    public void Multiply_VariousNumbers_ReturnsCorrectProduct(int a, int b, int expected)
    {
        // Arrange
        var calculator = new Calculator();
        
        // Act
        var result = calculator.Multiply(a, b);
        
        // Assert
        Assert.AreEqual(expected, result);
    }
    
    public static IEnumerable<object[]> GetTestData()
    {
        yield return new object[] { 2, 3, 6 };
        yield return new object[] { 4, 5, 20 };
        yield return new object[] { -2, 3, -6 };
        yield return new object[] { 0, 100, 0 };
    }
}
```

### 4. Тесты с моками и зависимостями

```csharp
[TestClass]
public class ServiceTestsWithMocks
{
    [TestMethod]
    public void ProcessOrder_ValidOrder_ProcessesSuccessfully()
    {
        // Arrange
        var mockPaymentService = new Mock<IPaymentService>();
        var mockInventoryService = new Mock<IInventoryService>();
        var mockNotificationService = new Mock<INotificationService>();
        
        var orderService = new OrderService(
            mockPaymentService.Object,
            mockInventoryService.Object,
            mockNotificationService.Object
        );
        
        var order = new Order { Id = 1, TotalAmount = 100.0m };
        
        mockPaymentService.Setup(x => x.ProcessPayment(order.TotalAmount))
                         .Returns(true);
        mockInventoryService.Setup(x => x.ReserveItems(order))
                          .Returns(true);
        
        // Act
        var result = orderService.ProcessOrder(order);
        
        // Assert
        Assert.IsTrue(result.IsSuccess);
        mockNotificationService.Verify(x => x.SendOrderConfirmation(order), Times.Once);
    }
}
```

### 5. Performance тестирование

```csharp
[TestClass]
public class PerformanceTests
{
    [TestMethod]
    [Timeout(1000)] // Тест должен завершиться за 1 секунду
    public void ProcessLargeData_PerformanceTest()
    {
        // Arrange
        var processor = new DataProcessor();
        var largeData = GenerateLargeData(10000);
        
        // Act
        var stopwatch = Stopwatch.StartNew();
        var result = processor.Process(largeData);
        stopwatch.Stop();
        
        // Assert
        Assert.IsNotNull(result);
        Assert.IsTrue(stopwatch.ElapsedMilliseconds < 500, 
            $"Processing took {stopwatch.ElapsedMilliseconds}ms, expected < 500ms");
    }
    
    [TestMethod]
    public void MemoryUsage_Test()
    {
        // Arrange
        var memoryService = new MemoryIntensiveService();
        
        // Act
        var initialMemory = GC.GetTotalMemory(true);
        memoryService.ProcessLargeDataset();
        var finalMemory = GC.GetTotalMemory(true);
        var memoryUsed = finalMemory - initialMemory;
        
        // Assert
        Assert.IsTrue(memoryUsed < 100 * 1024 * 1024, 
            $"Memory usage {memoryUsed} bytes exceeds 100MB limit");
    }
}
```

## Конфигурация платформы

### appsettings.json

```json
{
  "TestingPlatform": {
    "Logging": {
      "Level": "Information",
      "File": {
        "Path": "test-results/logs.txt"
      }
    },
    "Reporting": {
      "Formats": ["json", "html", "trx"],
      "OutputPath": "test-results/"
    },
    "Parallelization": {
      "MaxParallelThreads": 4,
      "ParallelizeAssemblies": true,
      "ParallelizeTestCollections": true
    },
    "Filters": {
      "Categories": ["Unit", "Integration"],
      "Priority": "High"
    }
  }
}
```

### Program.cs с конфигурацией

```csharp
using Microsoft.Testing.Platform;
using Microsoft.Testing.Platform.Builder;

var testApplicationBuilder = await TestApplication.CreateBuilderAsync(args);

// Конфигурация платформы
testApplicationBuilder
    .AddMSTest()
    .ConfigureLogging(loggingBuilder =>
    {
        loggingBuilder.AddConsole();
        loggingBuilder.AddFile("test-log.txt");
    })
    .ConfigureReporting(reportingBuilder =>
    {
        reportingBuilder.AddJsonReport();
        reportingBuilder.AddHtmlReport();
    })
    .ConfigureCapabilities(capabilitiesBuilder =>
    {
        capabilitiesBuilder.AddTestExecution();
        capabilitiesBuilder.AddTestSession();
    });

// Сборка и запуск
var testApp = await testApplicationBuilder.BuildAsync();
return await testApp.RunAsync();
```

## Сценарии использования в реальных проектах

### 6. Микросервисная архитектура

```csharp
[TestClass]
public class MicroserviceTests
{
    private TestServer _apiServer;
    private HttpClient _client;

    [TestInitialize]
    public void Initialize()
    {
        _apiServer = new TestServer(WebHost.CreateDefaultBuilder()
            .UseStartup<TestStartup>());
        _client = _apiServer.CreateClient();
    }

    [TestMethod]
    public async Task UsersApi_GetUser_ReturnsUser()
    {
        // Act
        var response = await _client.GetAsync("/api/users/1");
        
        // Assert
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        var user = JsonSerializer.Deserialize<User>(content);
        
        Assert.IsNotNull(user);
        Assert.AreEqual(1, user.Id);
    }

    [TestCleanup]
    public void Cleanup()
    {
        _client?.Dispose();
        _apiServer?.Dispose();
    }
}
```

### 7. Тестирование с контейнерами Docker

```csharp
[TestClass]
public class DockerIntegrationTests
{
    private Container _databaseContainer;

    [TestInitialize]
    public async Task Initialize()
    {
        // Запуск тестовой БД в Docker
        _databaseContainer = new ContainerBuilder()
            .WithImage("postgres:13")
            .WithEnvironment("POSTGRES_PASSWORD=test", "POSTGRES_DB=testdb")
            .WithPortBinding(5432, true)
            .Build();

        await _databaseContainer.StartAsync();
        await InitializeTestData();
    }

    [TestMethod]
    public async Task DatabaseConnection_Works()
    {
        // Arrange
        var connectionString = "Host=localhost;Port=5432;Database=testdb;Username=postgres;Password=test";
        
        // Act & Assert
        await using var connection = new NpgsqlConnection(connectionString);
        await connection.OpenAsync();
        
        Assert.AreEqual(ConnectionState.Open, connection.State);
    }

    [TestCleanup]
    public async Task Cleanup()
    {
        if (_databaseContainer != null)
        {
            await _databaseContainer.StopAsync();
            await _databaseContainer.RemoveAsync();
        }
    }
}
```

### 8. Расширение платформы через кастомные плагины

```csharp
// Кастомный репортер
public class CustomHtmlReporter : IDataConsumer
{
    public string Uid => nameof(CustomHtmlReporter);
    public string Version => "1.0.0";
    public string DisplayName => "Custom HTML Reporter";
    public string Description => "Generates custom HTML test reports";

    public Task<bool> IsEnabledAsync() => Task.FromResult(true);

    public async Task ConsumeAsync(IDataProducer dataProducer, IData value)
    {
        if (value is TestNodeUpdateMessage testUpdate)
        {
            await GenerateHtmlReport(testUpdate);
        }
    }
    
    private async Task GenerateHtmlReport(TestNodeUpdateMessage testUpdate)
    {
        var htmlContent = $@"
            <html>
                <head><title>Test Report</title></head>
                <body>
                    <h1>Test Results</h1>
                    <p>Test: {testUpdate.TestNode.DisplayName}</p>
                    <p>Status: {testUpdate.Result?.Outcome}</p>
                </body>
            </html>";
            
        await File.WriteAllTextAsync("custom-report.html", htmlContent);
    }
}

// Регистрация плагина
testApplicationBuilder.AddDataConsumer<CustomHtmlReporter>();
```

## Интеграция с CI/CD

### GitHub Actions

```yaml
name: .NET Testing Platform

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: 8.0.x
        
    - name: Restore dependencies
      run: dotnet restore
      
    - name: Run tests
      run: dotnet test --logger "html;logfilename=test-results.html"
      
    - name: Upload test results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: |
          **/test-results*.html
          **/TestResults*.xml
```

## Преимущества Microsoft.Testing.Platform

1. **Унификация** - единая платформа для всех типов тестов
2. **Производительность** - оптимизирована для больших тестовых наборов
3. **Расширяемость** - богатая экосистема плагинов
4. **Современность** - поддержка последних версий .NET
5. **Кросс-платформенность** - полная поддержка Linux, macOS, Windows
6. **Интеграция** - глубокая интеграция с Visual Studio и CI/CD

## Миграция с существующих фреймворков

```csharp
// Старый MSTest
[TestClass]
public class OldTests
{
    [TestMethod]
    public void OldTest() { }
}

// Новый Microsoft.Testing.Platform - совместим со старыми атрибутами!
[TestClass] 
public class NewTests
{
    [TestMethod]
    public void NewTest() { }
}
```