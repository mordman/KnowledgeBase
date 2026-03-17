**xUnit** — это современный, гибкий и расширяемый фреймворк для модульного тестирования в .NET. Он является альтернативой таким фреймворкам, как MSTest и NUnit, и широко используется благодаря своей простоте, поддержке асинхронных тестов и мощным механизмам расширения.

---

## **Основные концепции xUnit**



## Оглавление
- [**Основные концепции xUnit**](#основные-концепции-xunit)
- [**Примеры использования xUnit**](#примеры-использования-xunit)
  - [**1. Простой тест (Fact)**](#1-простой-тест-fact)
  - [**2. Тест с исключением**](#2-тест-с-исключением)
  - [**3. Параметризованный тест (Theory)**](#3-параметризованный-тест-theory)
  - [**4. Использование `MemberData`**](#4-использование-memberdata)
  - [**5. Использование `ClassData`**](#5-использование-classdata)
  - [**6. Асинхронные тесты**](#6-асинхронные-тесты)
  - [**7. Использование фикстур (Fixtures)**](#7-использование-фикстур-fixtures)
  - [**8. Тестирование коллекций**](#8-тестирование-коллекций)
  - [**9. Кастомные утверждения (Custom Asserts)**](#9-кастомные-утверждения-custom-asserts)
  - [**10. Мокирование зависимостей (с Moq)**](#10-мокирование-зависимостей-с-moq)
- [**Заключение**](#заключение)

  - [**1. Простой тест (Fact)**](#1-простой-тест-fact)
  - [**2. Тест с исключением**](#2-тест-с-исключением)
  - [**3. Параметризованный тест (Theory)**](#3-параметризованный-тест-theory)
  - [**4. Использование `MemberData`**](#4-использование-memberdata)
  - [**5. Использование `ClassData`**](#5-использование-classdata)
  - [**6. Асинхронные тесты**](#6-асинхронные-тесты)
  - [**7. Использование фикстур (Fixtures)**](#7-использование-фикстур-fixtures)
  - [**8. Тестирование коллекций**](#8-тестирование-коллекций)
  - [**9. Кастомные утверждения (Custom Asserts)**](#9-кастомные-утверждения-custom-asserts)
  - [**10. Мокирование зависимостей (с Moq)**](#10-мокирование-зависимостей-с-moq)
- **Факты (Facts)**: Методы, которые всегда должны возвращать `true`. Используются для проверки неизменных условий.
- **Теории (Theories)**: Методы, которые принимают параметры и выполняются для разных наборов данных.
- **Asserts**: Методы для проверки условий (например, `Assert.Equal`, `Assert.True`).
- **Fixtures**: Класс, который используется для инициализации и очистки ресурсов, общих для нескольких тестов.
- **Атрибуты**: Например, `[Fact]`, `[Theory]`, `[InlineData]`, `[ClassData]`, `[MemberData]`.

---

## **Примеры использования xUnit**

### **1. Простой тест (Fact)**
Проверка, что метод возвращает ожидаемое значение.

```csharp
public class CalculatorTests
{
    [Fact]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        var calculator = new Calculator();

        // Act
        var result = calculator.Add(2, 3);

        // Assert
        Assert.Equal(5, result);
    }
}

public class Calculator
{
    public int Add(int a, int b) => a + b;
}
```

---

### **2. Тест с исключением**
Проверка, что метод выбрасывает ожидаемое исключение.

```csharp
[Fact]
public void Divide_ByZero_ThrowsDivideByZeroException()
{
    var calculator = new Calculator();
    Assert.Throws<DivideByZeroException>(() => calculator.Divide(10, 0));
}

public class Calculator
{
    public int Divide(int a, int b) => a / b;
}
```

---

### **3. Параметризованный тест (Theory)**
Проверка метода с разными входными данными.

```csharp
[Theory]
[InlineData(2, 3, 5)]
[InlineData(-1, 1, 0)]
[InlineData(0, 0, 0)]
public void Add_MultipleValues_ReturnsSum(int a, int b, int expected)
{
    var calculator = new Calculator();
    var result = calculator.Add(a, b);
    Assert.Equal(expected, result);
}
```

---

### **4. Использование `MemberData`**
Параметры для теста загружаются из свойства или метода.

```csharp
public static IEnumerable<object[]> TestData =>
    new List<object[]>
    {
        new object[] { 2, 3, 5 },
        new object[] { -1, 1, 0 },
        new object[] { 0, 0, 0 }
    };

[Theory]
[MemberData(nameof(TestData))]
public void Add_MemberData_ReturnsSum(int a, int b, int expected)
{
    var calculator = new Calculator();
    var result = calculator.Add(a, b);
    Assert.Equal(expected, result);
}
```

---

### **5. Использование `ClassData`**
Параметры для теста загружаются из отдельного класса.

```csharp
public class CalculatorTestData : IEnumerable<object[]>
{
    public IEnumerator<object[]> GetEnumerator()
    {
        yield return new object[] { 2, 3, 5 };
        yield return new object[] { -1, 1, 0 };
        yield return new object[] { 0, 0, 0 };
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

[Theory]
[ClassData(typeof(CalculatorTestData))]
public void Add_ClassData_ReturnsSum(int a, int b, int expected)
{
    var calculator = new Calculator();
    var result = calculator.Add(a, b);
    Assert.Equal(expected, result);
}
```

---

### **6. Асинхронные тесты**
Тестирование асинхронных методов.

```csharp
public class AsyncCalculator
{
    public async Task<int> AddAsync(int a, int b)
    {
        await Task.Delay(100);
        return a + b;
    }
}

[Fact]
public async Task AddAsync_TwoNumbers_ReturnsSum()
{
    var calculator = new AsyncCalculator();
    var result = await calculator.AddAsync(2, 3);
    Assert.Equal(5, result);
}
```

---

### **7. Использование фикстур (Fixtures)**
Общие ресурсы для нескольких тестов.

```csharp
public class DatabaseFixture : IDisposable
{
    public DatabaseFixture()
    {
        Connection = new SqlConnection("Server=myServer;Database=myDB;...");
        Connection.Open();
    }

    public SqlConnection Connection { get; }

    public void Dispose()
    {
        Connection.Close();
    }
}

public class DatabaseTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public DatabaseTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void Connection_IsOpen()
    {
        Assert.Equal(ConnectionState.Open, _fixture.Connection.State);
    }
}
```

---

### **8. Тестирование коллекций**
Проверка содержимого коллекций.

```csharp
[Fact]
public void GetNames_ReturnsExpectedList()
{
    var service = new NameService();
    var names = service.GetNames();

    Assert.Contains("Alice", names);
    Assert.DoesNotContain("Bob", names);
    Assert.Equal(3, names.Count);
}

public class NameService
{
    public List<string> GetNames() => new List<string> { "Alice", "Charlie", "David" };
}
```

---

### **9. Кастомные утверждения (Custom Asserts)**
Создание собственных методов для проверки условий.

```csharp
public static class CustomAsserts
{
    public static void IsEven(int number)
    {
        Assert.True(number % 2 == 0, $"{number} is not even.");
    }
}

[Fact]
public void Number_IsEven()
{
    CustomAsserts.IsEven(4);
}
```

---

### **10. Мокирование зависимостей (с Moq)**
Использование моков для изоляции тестов.

```csharp
public interface IUserRepository
{
    bool IsUserActive(int userId);
}

public class UserService
{
    private readonly IUserRepository _repository;

    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }

    public bool CanAccess(int userId) => _repository.IsUserActive(userId);
}

[Fact]
public void CanAccess_ReturnsTrue_WhenUserIsActive()
{
    var mockRepository = new Mock<IUserRepository>();
    mockRepository.Setup(repo => repo.IsUserActive(1)).Returns(true);

    var userService = new UserService(mockRepository.Object);
    var result = userService.CanAccess(1);

    Assert.True(result);
}
```

---

## **Заключение**
xUnit — это мощный и гибкий инструмент для модульного тестирования в .NET. Он поддерживает:
- Простые и параметризованные тесты.
- Асинхронные сценарии.
- Работу с фикстурами и моками.
- Расширяемость через кастомные утверждения и данные.