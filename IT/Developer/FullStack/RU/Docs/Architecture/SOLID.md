Разберём каждый принцип **SOLID** подробно с примерами на C#. Эти принципы помогают создавать гибкий, поддерживаемый и расширяемый код.

---

## **1. Single Responsibility Principle (SRP) — Принцип единственной ответственности**
**Определение:**
Класс должен иметь только одну причину для изменения, то есть должен выполнять только одну задачу или отвечать за одну часть функциональности.

**Почему это важно:**
- Упрощает поддержку и тестирование кода.
- Снижает риск внесения ошибок при изменении кода.

**Пример на C#:**
```csharp
// ❌ Нарушение SRP: Класс управляет и пользователями, и логированием
public class UserManager
{
    public void CreateUser(string username)
    {
        // Логика создания пользователя
        Log($"Пользователь {username} создан.");
    }

    private void Log(string message)
    {
        Console.WriteLine(message);
    }
}

// ✅ Соблюдение SRP: Разделение ответственности
public class UserManager
{
    private readonly ILogger _logger;

    public UserManager(ILogger logger)
    {
        _logger = logger;
    }

    public void CreateUser(string username)
    {
        // Логика создания пользователя
        _logger.Log($"Пользователь {username} создан.");
    }
}

public interface ILogger
{
    void Log(string message);
}

public class ConsoleLogger : ILogger
{
    public void Log(string message)
    {
        Console.WriteLine(message);
    }
}
```

---

## **2. Open/Closed Principle (OCP) — Принцип открытости/закрытости**
**Определение:**
Класс должен быть открыт для расширения, но закрыт для модификации. Это означает, что вы можете добавлять новую функциональность, не изменяя существующий код.

**Почему это важно:**
- Позволяет добавлять новые возможности без риска сломать существующий код.
- Упрощает поддержку и масштабирование системы.

**Пример на C#:**
```csharp
// ❌ Нарушение OCP: При добавлении нового типа скидки придётся менять класс Order
public class Order
{
    public double CalculateTotal(double price, string discountType)
    {
        if (discountType == "Standard")
            return price * 0.95;
        else if (discountType == "Premium")
            return price * 0.90;
        // При добавлении нового типа скидки нужно менять этот метод
        throw new NotImplementedException();
    }
}

// ✅ Соблюдение OCP: Использование интерфейсов и наследования
public interface IDiscountStrategy
{
    double ApplyDiscount(double price);
}

public class StandardDiscount : IDiscountStrategy
{
    public double ApplyDiscount(double price) => price * 0.95;
}

public class PremiumDiscount : IDiscountStrategy
{
    public double ApplyDiscount(double price) => price * 0.90;
}

public class Order
{
    private readonly IDiscountStrategy _discountStrategy;

    public Order(IDiscountStrategy discountStrategy)
    {
        _discountStrategy = discountStrategy;
    }

    public double CalculateTotal(double price)
    {
        return _discountStrategy.ApplyDiscount(price);
    }
}
```

---

## **3. Liskov Substitution Principle (LSP) — Принцип подстановки Барбары Лисков**
**Определение:**
Объекты родительского класса должны быть заменяемы объектами дочернего класса без нарушения работы программы.

**Почему это важно:**
- Гарантирует корректное наследование и полиморфизм.
- Избегает неожиданного поведения при использовании подклассов.

**Пример на C#:**
```csharp
// ❌ Нарушение LSP: Квадрат не должен наследоваться от прямоугольника, так как изменение ширины/высоты ведёт себя по-разному
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }

    public int Area => Width * Height;
}

public class Square : Rectangle
{
    public override int Width
    {
        get => base.Width;
        set { base.Width = base.Height = value; }
    }

    public override int Height
    {
        get => base.Height;
        set { base.Width = base.Height = value; }
    }
}

// ✅ Соблюдение LSP: Использование общих интерфейсов
public interface IShape
{
    int Area { get; }
}

public class Rectangle : IShape
{
    public int Width { get; set; }
    public int Height { get; set; }
    public int Area => Width * Height;
}

public class Square : IShape
{
    public int Side { get; set; }
    public int Area => Side * Side;
}
```

---

## **4. Interface Segregation Principle (ISP) — Принцип разделения интерфейсов**
**Определение:**
Клиенты не должны зависеть от интерфейсов, которые они не используют. Разбивайте крупные интерфейсы на более мелкие и специфичные.

**Почему это важно:**
- Избегает "раздутых" интерфейсов, которые вынуждают классы реализовывать ненужные методы.
- Упрощает поддержку и понимание кода.

**Пример на C#:**
```csharp
// ❌ Нарушение ISP: Один большой интерфейс для всех устройств
public interface IDevice
{
    void Print();
    void Scan();
    void Fax();
}

public class MultiFunctionPrinter : IDevice
{
    public void Print() { /* ... */ }
    public void Scan() { /* ... */ }
    public void Fax() { /* ... */ }
}

public class OldPrinter : IDevice
{
    public void Print() { /* ... */ }
    public void Scan() => throw new NotImplementedException(); // Принтер не умеет сканировать
    public void Fax() => throw new NotImplementedException();  // Принтер не умеет отправлять факсы
}

// ✅ Соблюдение ISP: Разделение интерфейсов
public interface IPrinter
{
    void Print();
}

public interface IScanner
{
    void Scan();
}

public interface IFax
{
    void Fax();
}

public class MultiFunctionPrinter : IPrinter, IScanner, IFax
{
    public void Print() { /* ... */ }
    public void Scan() { /* ... */ }
    public void Fax() { /* ... */ }
}

public class OldPrinter : IPrinter
{
    public void Print() { /* ... */ }
}
```

---

## **5. Dependency Inversion Principle (DIP) — Принцип инверсии зависимостей**
**Определение:**
Модули высокого уровня не должны зависеть от модулей низкого уровня. Оба должны зависеть от абстракций. Абстракции не должны зависеть от деталей, а детали должны зависеть от абстракций.

**Почему это важно:**
- Уменьшает связанность кода.
- Облегчает тестирование и замену компонентов.

**Пример на C#:**
```csharp
// ❌ Нарушение DIP: Класс OrderProcessor напрямую зависит от класса EmailService
public class EmailService
{
    public void SendEmail(string message) { /* ... */ }
}

public class OrderProcessor
{
    private readonly EmailService _emailService;

    public OrderProcessor()
    {
        _emailService = new EmailService();
    }

    public void ProcessOrder()
    {
        _emailService.SendEmail("Заказ обработан.");
    }
}

// ✅ Соблюдение DIP: Использование интерфейсов и внедрение зависимостей
public interface IMessageService
{
    void Send(string message);
}

public class EmailService : IMessageService
{
    public void Send(string message) { /* ... */ }
}

public class OrderProcessor
{
    private readonly IMessageService _messageService;

    public OrderProcessor(IMessageService messageService)
    {
        _messageService = messageService;
    }

    public void ProcessOrder()
    {
        _messageService.Send("Заказ обработан.");
    }
}
```

---

### **Итоги**
- **SRP:** Один класс — одна ответственность.
- **OCP:** Расширяйте код через наследование и полиморфизм, а не через модификацию.
- **LSP:** Подклассы должны корректно заменять родительские классы.
- **ISP:** Разбивайте интерфейсы на мелкие и специфичные.
- **DIP:** Зависите от абстракций, а не от конкретных реализаций.

---

# Пример рефакторинга
>Упрощённую версию системы управления заказами в интернет-магазине. Исходный код нарушает принципы SOLID, а после рефакторинга будет соответствовать всем пяти принципам.

---

## **Исходный код (с нарушениями SOLID)**

### **Класс `OrderProcessor`**
```csharp
public class OrderProcessor
{
    private readonly string _connectionString;

    public OrderProcessor(string connectionString)
    {
        _connectionString = connectionString;
    }

    public void ProcessOrder(Order order)
    {
        // 1. Валидация заказа
        if (order.Items.Count == 0)
            throw new Exception("Заказ не может быть пустым.");

        if (order.CustomerEmail == null)
            throw new Exception("Email клиента обязателен.");

        // 2. Сохранение заказа в базу данных
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            var command = new SqlCommand(
                "INSERT INTO Orders (CustomerEmail, Total) VALUES (@email, @total)",
                connection);
            command.Parameters.AddWithValue("@email", order.CustomerEmail);
            command.Parameters.AddWithValue("@total", order.Total);
            command.ExecuteNonQuery();
        }

        // 3. Отправка уведомления клиенту
        var smtpClient = new SmtpClient("smtp.example.com");
        var mailMessage = new MailMessage
        {
            From = new MailAddress("noreply@example.com"),
            Subject = "Ваш заказ подтверждён",
            Body = $"Спасибо за заказ на сумму {order.Total}!",
            IsBodyHtml = false
        };
        mailMessage.To.Add(order.CustomerEmail);
        smtpClient.Send(mailMessage);

        // 4. Логирование
        File.AppendAllText("order_log.txt", $"Заказ обработан: {order.CustomerEmail}\n");
    }
}

public class Order
{
    public List<OrderItem> Items { get; set; } = new List<OrderItem>();
    public string CustomerEmail { get; set; }
    public decimal Total { get; set; }
}

public class OrderItem
{
    public string ProductName { get; set; }
    public decimal Price { get; set; }
}
```

---

### **Проблемы в исходном коде:**
1. **SRP:** `OrderProcessor` делает всё — валидацию, сохранение в БД, отправку email и логирование.
2. **OCP:** При добавлении нового способа оплаты или уведомления придётся менять `OrderProcessor`.
3. **LSP:** Нет наследования, но если бы было, код не был бы готов к замене компонентов.
4. **ISP:** Нет явных интерфейсов, но если бы были, они были бы "раздутыми".
5. **DIP:** `OrderProcessor` напрямую зависит от `SqlConnection`, `SmtpClient` и `File`.

---

## **Рефакторинг (соблюдение SOLID)**

### **1. Разделение ответственности (SRP, ISP, DIP)**
Создадим отдельные классы для каждой задачи и определим интерфейсы.

#### **Интерфейсы:**
```csharp
public interface IOrderValidator
{
    void Validate(Order order);
}

public interface IOrderRepository
{
    void Save(Order order);
}

public interface INotificationService
{
    void Notify(Order order);
}

public interface ILogger
{
    void Log(string message);
}
```

---

### **2. Реализация компонентов**

#### **Валидация заказа:**
```csharp
public class OrderValidator : IOrderValidator
{
    public void Validate(Order order)
    {
        if (order.Items.Count == 0)
            throw new Exception("Заказ не может быть пустым.");

        if (string.IsNullOrEmpty(order.CustomerEmail))
            throw new Exception("Email клиента обязателен.");
    }
}
```

#### **Сохранение заказа в БД:**
```csharp
public class SqlOrderRepository : IOrderRepository
{
    private readonly string _connectionString;

    public SqlOrderRepository(string connectionString)
    {
        _connectionString = connectionString;
    }

    public void Save(Order order)
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            var command = new SqlCommand(
                "INSERT INTO Orders (CustomerEmail, Total) VALUES (@email, @total)",
                connection);
            command.Parameters.AddWithValue("@email", order.CustomerEmail);
            command.Parameters.AddWithValue("@total", order.Total);
            command.ExecuteNonQuery();
        }
    }
}
```

#### **Отправка уведомления:**
```csharp
public class EmailNotificationService : INotificationService
{
    public void Notify(Order order)
    {
        var smtpClient = new SmtpClient("smtp.example.com");
        var mailMessage = new MailMessage
        {
            From = new MailAddress("noreply@example.com"),
            Subject = "Ваш заказ подтверждён",
            Body = $"Спасибо за заказ на сумму {order.Total}!",
            IsBodyHtml = false
        };
        mailMessage.To.Add(order.CustomerEmail);
        smtpClient.Send(mailMessage);
    }
}
```

#### **Логирование:**
```csharp
public class FileLogger : ILogger
{
    public void Log(string message)
    {
        File.AppendAllText("order_log.txt", $"{message}\n");
    }
}
```

---

### **3. Новый `OrderProcessor` (OCP, DIP)**
Теперь `OrderProcessor` зависит от абстракций, а не от конкретных реализаций.

```csharp
public class OrderProcessor
{
    private readonly IOrderValidator _validator;
    private readonly IOrderRepository _repository;
    private readonly INotificationService _notificationService;
    private readonly ILogger _logger;

    public OrderProcessor(
        IOrderValidator validator,
        IOrderRepository repository,
        INotificationService notificationService,
        ILogger logger)
    {
        _validator = validator;
        _repository = repository;
        _notificationService = notificationService;
        _logger = logger;
    }

    public void ProcessOrder(Order order)
    {
        _validator.Validate(order);
        _repository.Save(order);
        _notificationService.Notify(order);
        _logger.Log($"Заказ обработан: {order.CustomerEmail}");
    }
}
```

---

### **4. Пример использования (Inversion of Control)**
```csharp
// Настройка зависимостей (например, в ASP.NET Core или через DI-контейнер)
var connectionString = "Server=myServer;Database=myDB;...";
var orderProcessor = new OrderProcessor(
    new OrderValidator(),
    new SqlOrderRepository(connectionString),
    new EmailNotificationService(),
    new FileLogger()
);

// Использование
var order = new Order
{
    CustomerEmail = "client@example.com",
    Items = new List<OrderItem> { new OrderItem { ProductName = "Товар 1", Price = 100 } },
    Total = 100
};

orderProcessor.ProcessOrder(order);
```

---

## **Преимущества рефакторинга:**
1. **SRP:** Каждый класс отвечает только за свою задачу.
2. **OCP:** Можно добавлять новые реализации (например, `SmsNotificationService` или `MongoOrderRepository`), не меняя `OrderProcessor`.
3. **LSP:** Все классы корректно реализуют интерфейсы и могут быть заменены.
4. **ISP:** Интерфейсы мелкие и специфичные.
5. **DIP:** `OrderProcessor` зависит от абстракций, а не от конкретных классов.

---

## **Дополнительные улучшения:**
- **Логирование:** Можно заменить `FileLogger` на `Serilog` или `NLog`.
- **Уведомления:** Легко добавить SMS или Push-уведомления, реализовав `INotificationService`.
- **Тестирование:** Теперь легко написать юнит-тесты для каждого компонента.

---