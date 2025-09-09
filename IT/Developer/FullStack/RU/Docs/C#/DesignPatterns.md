## 1. Порождающие шаблоны (Creational Patterns)

### 1. Singleton (Одиночка)
**Цель:** Гарантирует, что класс имеет только один экземпляр и предоставляет глобальную точку доступа к нему.
**Пример:**
```csharp
public sealed class Singleton
{
    private static Singleton _instance;
    private static readonly object _lock = new object();

    private Singleton() { }

    public static Singleton Instance
    {
        get
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = new Singleton();
                }
                return _instance;
            }
        }
    }
}
```
**Антипаттерн:** Может стать антипаттерном, если используется для глобального состояния, что усложняет тестирование и нарушает принцип единственной ответственности.

---

### 2. Factory Method (Фабричный метод)
**Цель:** Определяет интерфейс для создания объектов, но позволяет подклассам изменять тип создаваемых объектов.
**Пример:**
```csharp
public interface IProduct { void Operation(); }

public class ConcreteProductA : IProduct
{
    public void Operation() => Console.WriteLine("Product A");
}

public class Creator
{
    public IProduct FactoryMethod() => new ConcreteProductA();
}
```
**Антипаттерн:** Избыточное использование фабричных методов может привести к усложнению кода.

---

### 3. Abstract Factory (Абстрактная фабрика)
**Цель:** Предоставляет интерфейс для создания семейств взаимосвязанных объектов.
**Пример:**
```csharp
public interface IGUIFactory
{
    IButton CreateButton();
    ICheckbox CreateCheckbox();
}

public class WinFactory : IGUIFactory
{
    public IButton CreateButton() => new WinButton();
    public ICheckbox CreateCheckbox() => new WinCheckbox();
}
```
**Антипаттерн:** Может стать слишком сложным, если семейств продуктов слишком много.

---

### 4. Builder (Строитель)
**Цель:** Разделяет конструкцию сложного объекта от его представления.
**Пример:**
```csharp
public class Car
{
    public string Model { get; set; }
    public string Engine { get; set; }
}

public class CarBuilder
{
    private Car _car = new Car();

    public CarBuilder SetModel(string model) { _car.Model = model; return this; }
    public CarBuilder SetEngine(string engine) { _car.Engine = engine; return this; }
    public Car Build() => _car;
}
```
**Антипаттерн:** Может привести к избыточному количеству классов, если объект простой.

---

### 5. Prototype (Прототип)
**Цель:** Позволяет копировать объекты, не вдаваясь в подробности их реализации.
**Пример:**
```csharp
public class Prototype : ICloneable
{
    public string Data { get; set; }

    public object Clone() => MemberwiseClone();
}
```
**Антипаттерн:** Глубокое копирование может быть ресурсоёмким.

---

### 6. Object Pool (Пул объектов)
**Цель:** Управляет набором инициализированных и готовых к использованию объектов.
**Пример:**
```csharp
public class ObjectPool<T> where T : new()
{
    private Queue<T> _pool = new Queue<T>();

    public T GetObject()
    {
        if (_pool.Count > 0)
            return _pool.Dequeue();
        return new T();
    }

    public void ReleaseObject(T obj) => _pool.Enqueue(obj);
}
```
**Антипаттерн:** Может привести к утечкам памяти, если объекты не возвращаются в пул.

---

### 7. Lazy Initialization (Ленивая инициализация)
**Цель:** Откладывает создание объекта до момента его первого использования.
**Пример:**
```csharp
public class LazyInitializer
{
    private Lazy<ExpensiveObject> _expensiveObject = new Lazy<ExpensiveObject>(() => new ExpensiveObject());

    public ExpensiveObject GetObject() => _expensiveObject.Value;
}
```
**Антипаттерн:** Может вызвать проблемы с многопоточностью, если не синхронизировано.

---

### 8. Dependency Injection (Внедрение зависимостей)
**Цель:** Передаёт зависимости объекту извне, а не создаёт их внутри.
**Пример:**
```csharp
public class Client
{
    private IService _service;

    public Client(IService service) => _service = service;
}
```
**Антипаттерн:** Избыточное использование DI может усложнить архитектуру.

---

### 9. Multiton
**Цель:** Управляет картой ключей и экземпляров, обеспечивая контроль над созданием объектов.
**Пример:**
```csharp
public class Multiton
{
    private static Dictionary<string, Multiton> _instances = new Dictionary<string, Multiton>();

    private Multiton() { }

    public static Multiton GetInstance(string key)
    {
        if (!_instances.ContainsKey(key))
            _instances[key] = new Multiton();
        return _instances[key];
    }
}
```
**Антипаттерн:** Может привести к утечкам памяти, если ключи не удаляются.

---

### 10. Simple Factory (Простая фабрика)
**Цель:** Централизует логику создания объектов в одном месте.
**Пример:**
```csharp
public class SimpleFactory
{
    public IProduct CreateProduct(string type)
    {
        return type switch
        {
            "A" => new ProductA(),
            "B" => new ProductB(),
            _ => throw new ArgumentException("Invalid type")
        };
    }
}
```
**Антипаттерн:** Нарушает принцип открытости/закрытости, если требуется часто добавлять новые типы.

---

## 2. Структурные шаблоны (Structural Patterns)

### 1. Adapter (Адаптер)
**Цель:** Позволяет объектам с несовместимыми интерфейсами работать вместе.
**Пример:**
```csharp
public class Adaptee { public void SpecificRequest() => Console.WriteLine("Adaptee"); }

public class Adapter : ITarget
{
    private Adaptee _adaptee = new Adaptee();
    public void Request() => _adaptee.SpecificRequest();
}
```
**Антипаттерн:** Может усложнить код, если адаптеров слишком много.

---

### 2. Decorator (Декоратор)
**Цель:** Динамически добавляет объекту новые обязанности.
**Пример:**
```csharp
public class Decorator : IComponent
{
    private IComponent _component;

    public Decorator(IComponent component) => _component = component;

    public void Operation()
    {
        _component.Operation();
        Console.WriteLine("Decorator operation");
    }
}
```
**Антипаттерн:** Может привести к избыточному количеству мелких классов.

---

### 3. Facade (Фасад)
**Цель:** Предоставляет унифицированный интерфейс к набору интерфейсов подсистемы.
**Пример:**
```csharp
public class Facade
{
    private SubsystemA _a = new SubsystemA();
    private SubsystemB _b = new SubsystemB();

    public void Operation() { _a.OperationA(); _b.OperationB(); }
}
```
**Антипаттерн:** Может скрыть важные детали подсистемы.

---

### 4. Composite (Компоновщик)
**Цель:** Объединяет объекты в древовидные структуры.
**Пример:**
```csharp
public class Composite : IComponent
{
    private List<IComponent> _children = new List<IComponent>();

    public void Add(IComponent component) => _children.Add(component);
    public void Operation() => _children.ForEach(c => c.Operation());
}
```
**Антипаттерн:** Может усложнить управление объектами, если дерево слишком большое.

---

### 5. Proxy (Заместитель)
**Цель:** Предоставляет объект-заместитель для контроля доступа к другому объекту.
**Пример:**
```csharp
public class ProxyImage : IImage
{
    private RealImage _realImage;
    private string _fileName;

    public ProxyImage(string fileName) => _fileName = fileName;

    public void Display()
    {
        if (_realImage == null)
            _realImage = new RealImage(_fileName);
        _realImage.Display();
    }
}
```
**Антипаттерн:** Может добавить ненужную сложность, если объект простой.

---

### 6. Flyweight (Приспособленец)
**Цель:** Использует разделение для эффективной поддержки большого количества мелких объектов.
**Пример:**
```csharp
public class FlyweightFactory
{
    private Dictionary<string, Flyweight> _flyweights = new Dictionary<string, Flyweight>();

    public Flyweight GetFlyweight(string key)
    {
        if (!_flyweights.ContainsKey(key))
            _flyweights[key] = new Flyweight(key);
        return _flyweights[key];
    }
}
```
**Антипаттерн:** Может усложнить код, если объекты часто изменяются.

---

### 7. Bridge (Мост)
**Цель:** Разделяет абстракцию и реализацию, позволяя им изменяться независимо.
**Пример:**
```csharp
public abstract class Abstraction
{
    protected IImplementation _implementation;

    public Abstraction(IImplementation implementation) => _implementation = implementation;

    public abstract void Operation();
}
```
**Антипаттерн:** Может быть избыточным для простых иерархий классов.

---

### 8. Decorator vs. Inheritance
**Цель:** Показывает, когда лучше использовать декоратор вместо наследования.
**Пример:** См. пример для Decorator.
**Антипаттерн:** Наследование может привести к жёсткой связанности.

---

### 9. Module (Модуль)
**Цель:** Группирует связанные классы и функции в один модуль.
**Пример:**
```csharp
public static class Module
{
    public static void FunctionA() => Console.WriteLine("Function A");
    public static void FunctionB() => Console.WriteLine("Function B");
}
```
**Антипаттерн:** Может привести к "божественным объектам", если модуль слишком большой.

---

### 10. Twin
**Цель:** Позволяет двум объектам обмениваться состоянием.
**Пример:**
```csharp
public class Twin
{
    private Twin _twin;

    public Twin(Twin twin) => _twin = twin;

    public void Sync() { /* Обмен состоянием */ }
}
```
**Антипаттерн:** Может привести к циклическим зависимостям.

---

## 3. Поведенческие шаблоны (Behavioral Patterns)

### 1. Observer (Наблюдатель)
**Цель:** Определяет зависимость "один ко многим" между объектами.
**Пример:**
```csharp
public class Subject
{
    private List<IObserver> _observers = new List<IObserver>();

    public void Attach(IObserver observer) => _observers.Add(observer);
    public void Notify() => _observers.ForEach(o => o.Update());
}
```
**Антипаттерн:** Может привести к утечкам памяти, если наблюдатели не удаляются.

---

### 2. Strategy (Стратегия)
**Цель:** Определяет семейство алгоритмов и делает их взаимозаменяемыми.
**Пример:**
```csharp
public class Context
{
    private IStrategy _strategy;

    public Context(IStrategy strategy) => _strategy = strategy;

    public void Execute() => _strategy.Execute();
}
```
**Антипаттерн:** Может привести к большому количеству мелких классов.

---

### 3. Command (Команда)
**Цель:** Инкапсулирует запрос как объект.
**Пример:**
```csharp
public class LightOnCommand : ICommand
{
    private Light _light;

    public LightOnCommand(Light light) => _light = light;

    public void Execute() => _light.On();
}
```
**Антипаттерн:** Может усложнить код, если команд слишком много.

---

### 4. State (Состояние)
**Цель:** Позволяет объекту изменять своё поведение при изменении внутреннего состояния.
**Пример:**
```csharp
public class Context
{
    private IState _state;

    public Context(IState state) => _state = state;

    public void Request() => _state.Handle(this);
}
```
**Антипаттерн:** Может привести к большому количеству классов состояний.

---

### 5. Chain of Responsibility (Цепочка обязанностей)
**Цель:** Позволяет передавать запросы последовательно по цепочке обработчиков.
**Пример:**
```csharp
public abstract class Handler
{
    private Handler _next;

    public Handler SetNext(Handler handler) => _next = handler;

    public abstract void HandleRequest();
}
```
**Антипаттерн:** Может привести к необработанным запросам, если цепочка неправильно настроена.

---

### 6. Iterator (Итератор)
**Цель:** Предоставляет способ последовательного доступа к элементам коллекции.
**Пример:**
```csharp
public class ConcreteIterator : IIterator<int>
{
    private List<int> _collection;
    private int _position = -1;

    public ConcreteIterator(List<int> collection) => _collection = collection;

    public int Current => _collection[_position];
    public bool MoveNext() => ++_position < _collection.Count;
}
```
**Антипаттерн:** Может быть избыточным для простых коллекций.

---

### 7. Mediator (Посредник)
**Цель:** Уменьшает связанность между классами.
**Пример:**
```csharp
public class Mediator
{
    public void Send(string message, Colleague colleague) => colleague.Receive(message);
}
```
**Антипаттерн:** Может стать "божественным объектом", если слишком много логики сосредоточено в посреднике.

---

### 8. Memento (Хранитель)
**Цель:** Позволяет сохранять и восстанавливать предыдущее состояние объекта.
**Пример:**
```csharp
public class Memento
{
    public string State { get; }

    public Memento(string state) => State = state;
}
```
**Антипаттерн:** Может потребовать много памяти для хранения состояний.

---

### 9. Visitor (Посетитель)
**Цель:** Позволяет добавлять новые операции к классам без их изменения.
**Пример:**
```csharp
public interface IVisitor
{
    void Visit(ElementA element);
    void Visit(ElementB element);
}
```
**Антипаттерн:** Может нарушить инкапсуляцию, если посетитель получает доступ к внутренним данным.

---

### 10. Template Method (Шаблонный метод)
**Цель:** Определяет скелет алгоритма, перекладывая ответственность за некоторые шаги на подклассы.
**Пример:**
```csharp
public abstract class GameAI
{
    public void Run()
    {
        CollectResources();
        BuildStructures();
        Attack();
    }

    protected abstract void CollectResources();
    protected abstract void BuildStructures();
    protected abstract void Attack();
}
```
**Антипаттерн:** Может нарушить принцип подстановки Лисков, если шаги слишком жёстко заданы.

---