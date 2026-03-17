**Цель:**  
Object Pool — это порождающий паттерн проектирования, который **управляет набором инициализированных объектов (пулом)**, готовых к повторному использованию. Он позволяет избежать затрат на частое создание и уничтожение «тяжёлых» объектов (например, соединений с БД, потоков, игровых сущностей), повышая производительность и снижая нагрузку на сборщик мусора.

---

**Пример (C#):**

```csharp
// Интерфейс для объектов, поддерживающих возврат в пул
public interface IPoolable
{
    void Reset();
}

// Пример "тяжёлого" объекта
public class ExpensiveConnection : IPoolable
{
    public string Id { get; } = Guid.NewGuid().ToString();

    public void Connect() => Console.WriteLine($"[{Id}] Connected");
    public void Disconnect() => Console.WriteLine($"[{Id}] Disconnected");

    public void Reset()
    {
        // Сброс состояния перед возвратом в пул
        Console.WriteLine($"[{Id}] Reset for reuse");
    }
}

// Простой потокобезопасный пул
public class ObjectPool<T> where T : class, IPoolable, new()
{
    private readonly Stack<T> _available = new();
    private readonly object _lock = new();

    public T Get()
    {
        lock (_lock)
        {
            if (_available.Count > 0)
            {
                var obj = _available.Pop();
                Console.WriteLine($"Reused existing instance: {obj.Id}");
                return obj;
            }
        }

        var newObj = new T();
        Console.WriteLine($"Created new instance: {newObj.Id}");
        return newObj;
    }

    public void Return(T obj)
    {
        obj.Reset(); // Обязательный сброс состояния!
        lock (_lock)
        {
            _available.Push(obj);
            Console.WriteLine($"Returned to pool: {obj.Id}");
        }
    }
}

// Использование
var pool = new ObjectPool<ExpensiveConnection>();

var conn1 = pool.Get();
conn1.Connect();
pool.Return(conn1);

var conn2 = pool.Get(); // Получит тот же экземпляр
conn2.Connect();
```

> 💡 В .NET также существует встроенная поддержка через `Microsoft.Extensions.ObjectPool` (часть DI-фреймворка).

---

**Антипаттерн:**  
- **Создание нового объекта при каждом запросе**, даже если он дорогой и может быть переиспользован.
- **Возврат "грязного" объекта в пул без сброса состояния** → утечки данных между пользователями (например, остаточные данные предыдущего запроса).
- **Отсутствие ограничения размера пула** → неограниченное потребление памяти.

---

**Схема (Mermaid):**

```mermaid
classDiagram
    class ObjectPool~T~ {
        -_available: Stack~T~
        -_lock: object
        +Get(): T
        +Return(obj: T)
    }

    class IPoolable {
        <<interface>>
        +Reset()
    }

    class ExpensiveConnection {
        +Id: string
        +Connect()
        +Disconnect()
        +Reset()
    }

    ObjectPool~T~ ..> IPoolable : requires T : IPoolable
    ExpensiveConnection ..|> IPoolable
```

```
    note right of ObjectPool~T~::Get
        Возвращает существующий объект
        из пула или создаёт новый,
        если пул пуст.
    end note

    note right of ObjectPool~T~::Return
        Обязательно вызывает Reset(),
        затем возвращает объект в пул.
    end note

    note left of ExpensiveConnection
        Должен быть "очищаемым"
        через Reset(), чтобы
        избежать утечек состояния.
    end note
```