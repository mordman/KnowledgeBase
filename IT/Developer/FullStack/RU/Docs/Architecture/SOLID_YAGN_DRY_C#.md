### **SOLID**

#### 1. Single Responsibility Principle (SRP)
**Описание:** Класс должен иметь только одну причину для изменения — то есть выполнять только одну задачу.

**Пример:**
```csharp
// Плохо: класс User отвечает и за хранение данных, и за их сохранение в БД.
public class User
{
    public string Name { get; set; }
    public void SaveToDatabase() { /* ... */ }
}

// Хорошо: класс User отвечает только за хранение данных.
public class User
{
    public string Name { get; set; }
}

// Класс UserRepository отвечает за сохранение данных в БД.
public class UserRepository
{
    public void Save(User user) { /* ... */ }
}
```

---

#### 2. Open/Closed Principle (OCP)
**Описание:** Класс должен быть открыт для расширения, но закрыт для модификации.

**Пример:**
```csharp
// Плохо: при добавлении нового типа скидки нужно менять класс DiscountCalculator.
public class DiscountCalculator
{
    public decimal CalculateDiscount(string customerType)
    {
        if (customerType == "Regular")
            return 0.1m;
        else if (customerType == "VIP")
            return 0.2m;
        // Нужно добавлять новый if для каждого типа скидки.
        return 0;
    }
}

// Хорошо: используем интерфейс и наследников для добавления новых типов скидок.
public interface IDiscountStrategy
{
    decimal CalculateDiscount();
}

public class RegularDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount() => 0.1m;
}

public class VipDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount() => 0.2m;
}

// Класс DiscountCalculator теперь закрыт для модификации.
public class DiscountCalculator
{
    private readonly IDiscountStrategy _strategy;
    public DiscountCalculator(IDiscountStrategy strategy)
    {
        _strategy = strategy;
    }
    public decimal CalculateDiscount() => _strategy.CalculateDiscount();
}
```

---

#### 3. Liskov Substitution Principle (LSP)
**Описание:** Наследники класса должны быть взаимозаменяемы с базовым классом без нарушения логики программы.

**Пример:**
```csharp
// Плохо: класс Square нарушает LSP, так как не может корректно работать с логикой Rectangle.
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

// Хорошо: Square не наследуется от Rectangle, а реализует общий интерфейс.
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

#### 4. Interface Segregation Principle (ISP)
**Описание:** Клиенты не должны зависеть от интерфейсов, которые они не используют.

**Пример:**
```csharp
// Плохо: один большой интерфейс для всех действий работника.
public interface IWorker
{
    void Eat();
    void Sleep();
    void Work();
}

// Хорошо: интерфейсы разделены по ответственности.
public interface IEater
{
    void Eat();
}

public interface ISleeper
{
    void Sleep();
}

public interface IWorker
{
    void Work();
}

// Теперь класс может реализовывать только нужные интерфейсы.
public class Human : IEater, ISleeper, IWorker { /* ... */ }
public class Robot : IWorker { /* ... */ }
```

---

#### 5. Dependency Inversion Principle (DIP)
**Описание:** Высокоуровневые модули не должны зависеть от низкоуровневых. Оба должны зависеть от абстракций.

**Пример:**
```csharp
// Плохо: класс OrderProcessor напрямую зависит от класса EmailService.
public class EmailService
{
    public void Send(string message) { /* ... */ }
}

public class OrderProcessor
{
    private readonly EmailService _emailService = new EmailService();
    public void ProcessOrder() { _emailService.Send("Order processed!"); }
}

// Хорошо: OrderProcessor зависит от абстракции IMessageService.
public interface IMessageService
{
    void Send(string message);
}

public class EmailService : IMessageService { /* ... */ }
public class SmsService : IMessageService { /* ... */ }

public class OrderProcessor
{
    private readonly IMessageService _messageService;
    public OrderProcessor(IMessageService messageService)
    {
        _messageService = messageService;
    }
    public void ProcessOrder() { _messageService.Send("Order processed!"); }
}
```

---

### **DRY (Don’t Repeat Yourself)**
**Описание:** Избегайте дублирования кода. Повторяющуюся логику выносите в отдельные методы или классы.

**Пример:**
```csharp
// Плохо: дублирование логики валидации.
public void ValidateUser(User user)
{
    if (string.IsNullOrEmpty(user.Name))
        throw new ArgumentException("Name is required!");
}

public void ValidateProduct(Product product)
{
    if (string.IsNullOrEmpty(product.Name))
        throw new ArgumentException("Name is required!");
}

// Хорошо: общая логика вынесена в отдельный метод.
public void ValidateName(string name)
{
    if (string.IsNullOrEmpty(name))
        throw new ArgumentException("Name is required!");
}

public void ValidateUser(User user) => ValidateName(user.Name);
public void ValidateProduct(Product product) => ValidateName(product.Name);
```

---

### **GRASP**

#### 1. Information Expert
**Описание:** Назначайте ответственность классу, который обладает всей необходимой информацией.

**Пример:**
```csharp
// Класс Order содержит информацию о заказе, поэтому он отвечает за расчет общей суммы.
public class Order
{
    public List<OrderItem> Items { get; set; }
    public decimal TotalAmount => Items.Sum(item => item.Price * item.Quantity);
}
```

---

#### 2. Creator
**Описание:** Класс A должен создавать объекты класса B, если A содержит или агрегирует B.

**Пример:**
```csharp
// Класс Order создает объекты OrderItem, так как содержит их.
public class Order
{
    private List<OrderItem> _items = new List<OrderItem>();
    public void AddItem(Product product, int quantity)
    {
        _items.Add(new OrderItem(product, quantity));
    }
}
```

---

#### 3. Low Coupling
**Описание:** Минимизируйте зависимости между классами.

**Пример:**
```csharp
// Плохо: класс OrderProcessor напрямую зависит от EmailService и Database.
public class OrderProcessor
{
    private EmailService _emailService = new EmailService();
    private Database _database = new Database();
    public void Process() { /* ... */ }
}

// Хорошо: зависимости передаются через интерфейсы.
public class OrderProcessor
{
    private readonly IMessageService _messageService;
    private readonly IDatabase _database;
    public OrderProcessor(IMessageService messageService, IDatabase database)
    {
        _messageService = messageService;
        _database = database;
    }
    public void Process() { /* ... */ }
}
```

---

#### 4. High Cohesion
**Описание:** Класс должен выполнять только тесно связанные задачи.

**Пример:**
```csharp
// Плохо: класс UserManager отвечает и за аутентификацию, и за отправку email.
public class UserManager
{
    public void Authenticate(string login, string password) { /* ... */ }
    public void SendWelcomeEmail(string email) { /* ... */ }
}

// Хорошо: задачи разделены по классам.
public class Authenticator { public void Authenticate(string login, string password) { /* ... */ } }
public class EmailSender { public void SendWelcomeEmail(string email) { /* ... */ } }
```

---

### **KISS (Keep It Simple, Stupid)**
**Описание:** Пишите код максимально просто и понятно.

**Пример:**
```csharp
// Плохо: излишне сложная логика для простой задачи.
public bool IsEven(int number)
{
    return (number % 2 == 0) ? true : false;
}

// Хорошо: просто и понятно.
public bool IsEven(int number)
{
    return number % 2 == 0;
}
```

---

### **YAGNI (You Aren’t Gonna Need It)**
**Описание:** Не реализуйте функциональность, которая "может понадобиться в будущем".

**Пример:**
```csharp
// Плохо: добавление абстрактного класса для "будущих нужд".
public abstract class Animal
{
    public abstract void MakeSound();
    public abstract void Fly(); // Не все животные летают!
}

// Хорошо: реализуем только то, что нужно сейчас.
public class Dog
{
    public void Bark() { /* ... */ }
}
```

---