# Принципы ООП (Объектно-Ориентированного Программирования)



## Оглавление
- [Основные принципы ООП](#основные-принципы-ооп)
  - [1. **Инкапсуляция (Encapsulation)**](#1-инкапсуляция-encapsulation)
  - [2. **Наследование (Inheritance)**](#2-наследование-inheritance)
  - [3. **Полиморфизм (Polymorphism)**](#3-полиморфизм-polymorphism)
  - [4. **Абстракция (Abstraction)**](#4-абстракция-abstraction)
- [Принципы SOLID](#принципы-solid)
  - [1. **S - Single Responsibility Principle (Принцип единственной ответственности)**](#1-s-single-responsibility-principle-принцип-единственной-ответственности)
  - [2. **O - Open/Closed Principle (Принцип открытости/закрытости)**](#2-o-openclosed-principle-принцип-открытостизакрытости)
  - [3. **L - Liskov Substitution Principle (Принцип подстановки Лисков)**](#3-l-liskov-substitution-principle-принцип-подстановки-лисков)
  - [4. **I - Interface Segregation Principle (Принцип разделения интерфейсов)**](#4-i-interface-segregation-principle-принцип-разделения-интерфейсов)
  - [5. **D - Dependency Inversion Principle (Принцип инверсии зависимостей)**](#5-d-dependency-inversion-principle-принцип-инверсии-зависимостей)
- [Дополнительные принципы ООП](#дополнительные-принципы-ооп)
  - [1. **Композиция против наследования**](#1-композиция-против-наследования)
  - [2. **Принцип DRY (Don't Repeat Yourself)**](#2-принцип-dry-dont-repeat-yourself)
- [Практическое применение принципов ООП](#практическое-применение-принципов-ооп)
  - [Пример хорошо спроектированного класса:](#пример-хорошо-спроектированного-класса)
- [Ключевые выводы:](#ключевые-выводы)

  - [1. **Инкапсуляция (Encapsulation)**](#1-инкапсуляция-encapsulation)
  - [2. **Наследование (Inheritance)**](#2-наследование-inheritance)
  - [3. **Полиморфизм (Polymorphism)**](#3-полиморфизм-polymorphism)
  - [4. **Абстракция (Abstraction)**](#4-абстракция-abstraction)
  - [1. **S - Single Responsibility Principle (Принцип единственной ответственности)**](#1-s-single-responsibility-principle-принцип-единственной-ответственности)
  - [2. **O - Open/Closed Principle (Принцип открытости/закрытости)**](#2-o-openclosed-principle-принцип-открытостизакрытости)
  - [3. **L - Liskov Substitution Principle (Принцип подстановки Лисков)**](#3-l-liskov-substitution-principle-принцип-подстановки-лисков)
  - [4. **I - Interface Segregation Principle (Принцип разделения интерфейсов)**](#4-i-interface-segregation-principle-принцип-разделения-интерфейсов)
  - [5. **D - Dependency Inversion Principle (Принцип инверсии зависимостей)**](#5-d-dependency-inversion-principle-принцип-инверсии-зависимостей)
  - [1. **Композиция против наследования**](#1-композиция-против-наследования)
  - [2. **Принцип DRY (Don't Repeat Yourself)**](#2-принцип-dry-dont-repeat-yourself)
  - [Пример хорошо спроектированного класса:](#пример-хорошо-спроектированного-класса)
## Основные принципы ООП

### 1. **Инкапсуляция (Encapsulation)**
**Определение:** Сокрытие внутренней реализации объекта и предоставление контролируемого доступа к данным через публичные методы.

**Суть:** 
- Объединение данных и методов в одном классе
- Сокрытие внутреннего состояния
- Контролируемый доступ через методы (getters/setters)

**Пример:**
```csharp
public class BankAccount
{
    // Private поля - внутреннее состояние
    private decimal _balance;
    private string _accountNumber;
    
    // Конструктор
    public BankAccount(string accountNumber, decimal initialBalance)
    {
        _accountNumber = accountNumber;
        _balance = initialBalance;
    }
    
    // Public методы - контролируемый доступ
    public decimal GetBalance()
    {
        return _balance;
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0)
            _balance += amount;
    }
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= _balance)
        {
            _balance -= amount;
            return true;
        }
        return false;
    }
    
    // Private метод - внутренняя логика
    private void LogTransaction(string transactionType, decimal amount)
    {
        Console.WriteLine($"{transactionType}: {amount}, Balance: {_balance}");
    }
}
```

**Преимущества:**
- Защита данных от некорректного изменения
- Гибкость изменения внутренней реализации
- Упрощение использования класса

### 2. **Наследование (Inheritance)**
**Определение:** Создание нового класса на основе существующего с наследованием его свойств и методов.

**Суть:**
- Повторное использование кода
- Создание иерархии классов
- Расширение функциональности

**Пример:**
```csharp
// Базовый класс
public class Vehicle
{
    public string Make { get; set; }
    public string Model { get; set; }
    public int Year { get; set; }
    
    public virtual void Start()
    {
        Console.WriteLine("Vehicle started");
    }
    
    public void Stop()
    {
        Console.WriteLine("Vehicle stopped");
    }
}

// Производный класс
public class Car : Vehicle
{
    public int NumberOfDoors { get; set; }
    
    // Переопределение метода
    public override void Start()
    {
        Console.WriteLine("Car engine started");
        base.Start(); // Вызов метода базового класса
    }
    
    // Новый метод
    public void OpenTrunk()
    {
        Console.WriteLine("Trunk opened");
    }
}

// Еще один производный класс
public class Motorcycle : Vehicle
{
    public bool HasSideCar { get; set; }
    
    public override void Start()
    {
        Console.WriteLine("Motorcycle engine started");
    }
    
    public void Wheelie()
    {
        Console.WriteLine("Doing a wheelie!");
    }
}
```

**Преимущества:**
- Повторное использование кода
- Логическая организация классов
- Полиморфизм

### 3. **Полиморфизм (Polymorphism)**
**Определение:** Возможность объектов с одинаковой спецификацией иметь различную реализацию.

**Типы полиморфизма:**
- **Параметрический (истинный)** - через переопределение методов
- **Ad-hoc** - через перегрузку методов

**Пример:**
```csharp
public class Shape
{
    public virtual void Draw()
    {
        Console.WriteLine("Drawing a shape");
    }
    
    public virtual double CalculateArea()
    {
        return 0;
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    public override void Draw()
    {
        Console.WriteLine("Drawing a circle");
    }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }
    
    public override void Draw()
    {
        Console.WriteLine("Drawing a rectangle");
    }
    
    public override double CalculateArea()
    {
        return Width * Height;
    }
    
    // Перегрузка метода (ad-hoc полиморфизм)
    public void Resize(double scale)
    {
        Width *= scale;
        Height *= scale;
    }
    
    public void Resize(double newWidth, double newHeight)
    {
        Width = newWidth;
        Height = newHeight;
    }
}

// Использование полиморфизма
public class GraphicsEditor
{
    public void DrawShapes(List<Shape> shapes)
    {
        foreach (var shape in shapes)
        {
            shape.Draw(); // Вызывается соответствующая реализация
            Console.WriteLine($"Area: {shape.CalculateArea()}");
        }
    }
}
```

**Преимущества:**
- Гибкость кода
- Упрощение обработки разнотипных объектов
- Расширяемость

### 4. **Абстракция (Abstraction)**
**Определение:** Сокрытие сложной реализации и предоставление только существенных характеристик объекта.

**Суть:**
- Определение контракта через интерфейсы/абстрактные классы
- Сокрытие деталей реализации
- Фокусировка на взаимодействии

**Пример:**
```csharp
// Абстрактный класс
public abstract class DatabaseConnection
{
    // Абстрактный метод - должен быть реализован в производных классах
    public abstract void Connect();
    public abstract void Disconnect();
    public abstract void ExecuteQuery(string query);
    
    // Конкретный метод - общая реализация
    public void Log(string message)
    {
        Console.WriteLine($"[DB LOG] {DateTime.Now}: {message}");
    }
}

// Интерфейс
public interface IRepository<T>
{
    void Add(T entity);
    void Update(T entity);
    void Delete(int id);
    T GetById(int id);
    IEnumerable<T> GetAll();
}

// Реализация абстрактного класса
public class SqlConnection : DatabaseConnection
{
    public override void Connect()
    {
        Console.WriteLine("Connecting to SQL Server...");
        // Реальная логика подключения
    }
    
    public override void Disconnect()
    {
        Console.WriteLine("Disconnecting from SQL Server...");
    }
    
    public override void ExecuteQuery(string query)
    {
        Console.WriteLine($"Executing SQL query: {query}");
    }
}

// Реализация интерфейса
public class UserRepository : IRepository<User>
{
    public void Add(User entity)
    {
        // Реализация добавления пользователя
    }
    
    public User GetById(int id)
    {
        // Реализация получения пользователя
        return new User();
    }
    
    // остальные методы...
}
```

**Преимущества:**
- Снижение сложности
- Гибкость реализации
- Легкость поддержки

---

## Принципы SOLID

### 1. **S - Single Responsibility Principle (Принцип единственной ответственности)**
**Определение:** Класс должен иметь только одну причину для изменения.

**Пример:**
```csharp
// НЕПРАВИЛЬНО - класс делает слишком много
public class UserManager
{
    public void CreateUser(User user) { /* ... */ }
    public void SendEmail(User user, string message) { /* ... */ }
    public void LogError(string error) { /* ... */ }
    public void SaveToDatabase(User user) { /* ... */ }
}

// ПРАВИЛЬНО - разделение ответственности
public class UserService
{
    public void CreateUser(User user) { /* ... */ }
}

public class EmailService
{
    public void SendEmail(User user, string message) { /* ... */ }
}

public class Logger
{
    public void LogError(string error) { /* ... */ }
}

public class UserRepository
{
    public void Save(User user) { /* ... */ }
}
```

### 2. **O - Open/Closed Principle (Принцип открытости/закрытости)**
**Определение:** Классы должны быть открыты для расширения, но закрыты для модификации.

**Пример:**
```csharp
// НЕПРАВИЛЬНО - при добавлении новой фигуры нужно менять класс
public class AreaCalculator
{
    public double CalculateArea(object shape)
    {
        if (shape is Rectangle rectangle)
            return rectangle.Width * rectangle.Height;
        else if (shape is Circle circle)
            return Math.PI * circle.Radius * circle.Radius;
        // Добавлять новые if для новых фигур
        throw new ArgumentException("Unknown shape");
    }
}

// ПРАВИЛЬНО - используем абстракцию
public abstract class Shape
{
    public abstract double CalculateArea();
}

public class AreaCalculator
{
    public double CalculateArea(Shape shape)
    {
        return shape.CalculateArea(); // Закрыт для модификации
    }
}

// Новые фигуры можно добавлять без изменения AreaCalculator
public class Triangle : Shape
{
    public override double CalculateArea()
    {
        // Реализация для треугольника
        return 0;
    }
}
```

### 3. **L - Liskov Substitution Principle (Принцип подстановки Лисков)**
**Определение:** Объекты должны быть заменяемыми экземплярами их базовых типов без изменения корректности программы.

**Пример:**
```csharp
// НАРУШЕНИЕ LSP
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
        set { base.Width = value; base.Height = value; }
    }
    
    public override int Height
    {
        set { base.Height = value; base.Width = value; }
    }
}

// Проблема: код, ожидающий Rectangle, сломается с Square
void TestRectangle(Rectangle rect)
{
    rect.Width = 5;
    rect.Height = 4;
    Console.WriteLine(rect.Area); // Ожидает 20, но для Square получит 16
}

// РЕШЕНИЕ - общий интерфейс
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

### 4. **I - Interface Segregation Principle (Принцип разделения интерфейсов)**
**Определение:** Много специализированных интерфейсов лучше, чем один универсальный.

**Пример:**
```csharp
// НЕПРАВИЛЬНО - один жирный интерфейс
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
    void Code();
    void Design();
}

public class Programmer : IWorker
{
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
    public void Code() { /* ... */ }
    public void Design() { /* ... */ } // Программист не должен проектировать!
}

// ПРАВИЛЬНО - разделенные интерфейсы
public interface IWorker
{
    void Work();
}

public interface IEater
{
    void Eat();
}

public interface ISleeper
{
    void Sleep();
}

public interface ICoder
{
    void Code();
}

public interface IDesigner
{
    void Design();
}

public class Programmer : IWorker, IEater, ISleeper, ICoder
{
    // Реализуем только нужные методы
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
    public void Code() { /* ... */ }
}
```

### 5. **D - Dependency Inversion Principle (Принцип инверсии зависимостей)**
**Определение:** Зависимости должны строиться на абстракциях, а не на конкретных реализациях.

**Пример:**
```csharp
// НЕПРАВИЛЬНО - зависимость от конкретной реализации
public class EmailService
{
    public void SendEmail(string message) { /* ... */ }
}

public class Notification
{
    private EmailService _emailService; // Жесткая зависимость
    
    public Notification()
    {
        _emailService = new EmailService();
    }
    
    public void SendNotification(string message)
    {
        _emailService.SendEmail(message);
    }
}

// ПРАВИЛЬНО - зависимость от абстракции
public interface IMessageService
{
    void SendMessage(string message);
}

public class EmailService : IMessageService
{
    public void SendMessage(string message) { /* ... */ }
}

public class SmsService : IMessageService
{
    public void SendMessage(string message) { /* ... */ }
}

public class Notification
{
    private readonly IMessageService _messageService; // Зависимость от интерфейса
    
    // Внедрение зависимости через конструктор
    public Notification(IMessageService messageService)
    {
        _messageService = messageService;
    }
    
    public void SendNotification(string message)
    {
        _messageService.SendMessage(message);
    }
}
```

---

## Дополнительные принципы ООП

### 1. **Композиция против наследования**
**Определение:** Предпочтение композиции объектов над наследованием классов.

**Пример:**
```csharp
// Наследование (может быть проблематичным)
public class Duck
{
    public virtual void Quack() { /* ... */ }
    public virtual void Fly() { /* ... */ }
}

public class RubberDuck : Duck
{
    public override void Fly()
    {
        // Резиновая утка не может летать - нарушение LSP!
        throw new NotImplementedException();
    }
}

// Композиция (более гибко)
public interface IFlyBehavior
{
    void Fly();
}

public interface IQuackBehavior
{
    void Quack();
}

public class Duck
{
    private IFlyBehavior _flyBehavior;
    private IQuackBehavior _quackBehavior;
    
    public Duck(IFlyBehavior flyBehavior, IQuackBehavior quackBehavior)
    {
        _flyBehavior = flyBehavior;
        _quackBehavior = quackBehavior;
    }
    
    public void PerformFly() => _flyBehavior.Fly();
    public void PerformQuack() => _quackBehavior.Quack();
}

public class FlyWithWings : IFlyBehavior
{
    public void Fly() => Console.WriteLine("Flying with wings");
}

public class NoFly : IFlyBehavior
{
    public void Fly() => Console.WriteLine("Can't fly");
}

public class NormalQuack : IQuackBehavior
{
    public void Quack() => Console.WriteLine("Quack!");
}

// Использование
var mallardDuck = new Duck(new FlyWithWings(), new NormalQuack());
var rubberDuck = new Duck(new NoFly(), new NormalQuack());
```

### 2. **Принцип DRY (Don't Repeat Yourself)**
**Определение:** Избегание повторения кода.

**Пример:**
```csharp
// Дублирование кода
public class UserValidator
{
    public bool ValidateEmail(string email)
    {
        if (string.IsNullOrEmpty(email))
            return false;
        if (!email.Contains("@"))
            return false;
        return true;
    }
    
    public bool ValidateUsername(string username)
    {
        if (string.IsNullOrEmpty(username))
            return false;
        if (!username.Contains("@")) // Дублирование проверки
            return false;
        return true;
    }
}

// Устранение дублирования
public class StringValidator
{
    public static bool IsNotNullOrEmpty(string value)
    {
        return !string.IsNullOrEmpty(value);
    }
    
    public static bool ContainsCharacter(string value, char character)
    {
        return value?.Contains(character) ?? false;
    }
}

public class UserValidator
{
    public bool ValidateEmail(string email)
    {
        return StringValidator.IsNotNullOrEmpty(email) && 
               StringValidator.ContainsCharacter(email, '@');
    }
    
    public bool ValidateUsername(string username)
    {
        return StringValidator.IsNotNullOrEmpty(username);
    }
}
```

## Практическое применение принципов ООП

### Пример хорошо спроектированного класса:
```csharp
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IPaymentProcessor _paymentProcessor;
    private readonly INotificationService _notificationService;
    
    // Инверсия зависимостей
    public OrderService(
        IOrderRepository orderRepository,
        IPaymentProcessor paymentProcessor,
        INotificationService notificationService)
    {
        _orderRepository = orderRepository;
        _paymentProcessor = paymentProcessor;
        _notificationService = notificationService;
    }
    
    // Единственная ответственность - обработка заказов
    public async Task<OrderResult> ProcessOrderAsync(Order order)
    {
        try
        {
            // Валидация
            if (!order.IsValid())
                return OrderResult.Failure("Invalid order");
            
            // Обработка платежа
            var paymentResult = await _paymentProcessor.ProcessPaymentAsync(order);
            if (!paymentResult.Success)
                return OrderResult.Failure("Payment failed");
            
            // Сохранение заказа
            await _orderRepository.SaveAsync(order);
            
            // Уведомление
            await _notificationService.SendOrderConfirmationAsync(order);
            
            return OrderResult.Success(order.Id);
        }
        catch (Exception ex)
        {
            // Логирование ошибки
            await _notificationService.SendErrorNotificationAsync(ex);
            return OrderResult.Failure("Order processing failed");
        }
    }
}
```

## Ключевые выводы:

1. **Инкапсуляция** - защита данных и контролируемый доступ
2. **Наследование** - повторное использование и расширяемость  
3. **Полиморфизм** - гибкость и единообразная работа с объектами
4. **Абстракция** - сокрытие сложности
5. **SOLID** - принципы проектирования устойчивых систем
6. **Композиция** - более гибкая альтернатива наследованию
7. **DRY** - поддержание чистоты кода