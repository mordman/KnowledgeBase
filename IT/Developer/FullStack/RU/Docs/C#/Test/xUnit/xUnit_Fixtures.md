## **Зачем нужны Fixtures?**

### **1. Совместное использование ресурсов**
Fixtures позволяют **один раз инициализировать ресурсы** (например, подключение к базе данных, HTTP-клиент, файл) и **переиспользовать их во всех тестах класса или сборки**. Это экономит время и память.

**Пример:**
Если у вас 10 тестов, которые работают с базой данных, вы не хотите открывать и закрывать соединение для каждого теста отдельно. Вместо этого вы можете сделать это **один раз** в фикстуре.

---

### **2. Изоляция тестов**
Fixtures помогают **гарантировать, что тесты не влияют друг на друга**. Например, если один тест изменяет состояние базы данных, фикстура может **восстанавливать исходное состояние** перед каждым тестом.

---

### **3. Упрощение кода тестов**
Fixtures позволяют **вынести повторяющуюся логику** (например, настройку окружения, создание тестовых данных) в отдельный класс. Это делает тесты **короче и понятнее**.

---

### **4. Управление жизненным циклом ресурсов**
Fixtures могут **автоматически освобождать ресурсы** после завершения тестов (например, закрывать соединения с базой данных, удалять временные файлы).

---

## **Типы Fixtures в xUnit**

### **1. `IClassFixture<TFixture>`**
- **Область действия:** Один экземпляр фикстуры создаётся **на весь класс** с тестами.
- **Когда использовать:** Когда все тесты в классе нуждаются в одном и том же ресурсе (например, подключении к базе данных).

**Пример:**
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
    public void Test1()
    {
        // Используем _fixture.Connection
    }

    [Fact]
    public void Test2()
    {
        // Используем _fixture.Connection
    }
}
```

---

### **2. `ICollectionFixture<TFixture>`**
- **Область действия:** Один экземпляр фикстуры создаётся **для всех тестов в сборке** (или в группе тестов, помеченных одним и тем же интерфейсом).
- **Когда использовать:** Когда ресурс нужен **нескольким классам с тестами** (например, общий HTTP-клиент для интеграционных тестов).

**Пример:**
```csharp
public class SharedHttpClientFixture : IDisposable
{
    public HttpClient Client { get; } = new HttpClient();

    public void Dispose()
    {
        Client.Dispose();
    }
}

public class ApiTests1 : ICollectionFixture<SharedHttpClientFixture>
{
    private readonly SharedHttpClientFixture _fixture;

    public ApiTests1(SharedHttpClientFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task TestApi1()
    {
        var response = await _fixture.Client.GetAsync("https://api.example.com/data");
        // ...
    }
}

public class ApiTests2 : ICollectionFixture<SharedHttpClientFixture>
{
    private readonly SharedHttpClientFixture _fixture;

    public ApiTests2(SharedHttpClientFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task TestApi2()
    {
        var response = await _fixture.Client.GetAsync("https://api.example.com/other-data");
        // ...
    }
}
```

---

## **Когда использовать Fixtures?**
| Сценарий                                      | Тип Fixture          |
|-----------------------------------------------|----------------------|
| Один ресурс нужен всем тестам в классе.       | `IClassFixture<T>`   |
| Один ресурс нужен нескольким классам тестов.  | `ICollectionFixture<T>` |
| Нужно инициализировать тестовые данные.       | `IClassFixture<T>`   |
| Нужно управлять жизненным циклом ресурса.     | Оба типа             |

---

## **Пример с восстановлением состояния**
Fixtures можно использовать для **восстановления исходного состояния** между тестами. Например, если тесты изменяют данные в базе, фикстура может откатывать изменения после каждого теста.

```csharp
public class DatabaseFixture : IDisposable
{
    public SqlConnection Connection { get; }
    public SqlTransaction Transaction { get; }

    public DatabaseFixture()
    {
        Connection = new SqlConnection("Server=myServer;Database=myDB;...");
        Connection.Open();
        Transaction = Connection.BeginTransaction();
    }

    public void Dispose()
    {
        Transaction.Rollback(); // Откатываем изменения после тестов
        Connection.Close();
    }
}

public class UserRepositoryTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public UserRepositoryTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void AddUser_IncreasesUserCount()
    {
        var repository = new UserRepository(_fixture.Connection, _fixture.Transaction);
        repository.AddUser("Alice");
        // ...
    }
}
```

---

## **Вывод**
Fixtures в xUnit — это **мощный инструмент** для:
✅ Совместного использования ресурсов.
✅ Изоляции тестов.
✅ Упрощения кода.
✅ Управления жизненным циклом ресурсов.