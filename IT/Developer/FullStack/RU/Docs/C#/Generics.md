### Generics в C#

**Generics** (обобщения) в C# — это механизм, который позволяет создавать классы, интерфейсы, методы и делегаты с **обобщёнными типами**. Это даёт возможность писать код, который работает с разными типами данных, сохраняя **типобезопасность** и избегая приведения типов.

---

## 1. Зачем нужны Generics?

- **Типобезопасность:** Избавляют от необходимости приведения типов (`casting`), что снижает количество ошибок.
- **Повторное использование кода:** Позволяют писать универсальные алгоритмы и структуры данных, которые работают с любыми типами.
- **Производительность:** Избегают боксинга (boxing) и анбоксинга (unboxing) значений, что улучшает производительность.

---

## 2. Примеры использования Generics

### a) Обобщённые коллекции

#### `List<T>`
```csharp
// Список целых чисел
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// Список строк
List<string> names = new List<string> { "Alice", "Bob", "Charlie" };
```

#### `Dictionary<TKey, TValue>`
```csharp
// Словарь: ключ — строка, значение — целое число
Dictionary<string, int> ages = new Dictionary<string, int>
{
    { "Alice", 30 },
    { "Bob", 25 }
};
```

#### `HashSet<T>`
```csharp
// Множество уникальных чисел
HashSet<int> uniqueNumbers = new HashSet<int> { 1, 2, 3, 3, 2 };
// uniqueNumbers будет содержать {1, 2, 3}
```

---

### b) Обобщённые классы

#### Пример: Обобщённый класс `Box<T>`
```csharp
public class Box<T>
{
    public T Content { get; set; }

    public Box(T content)
    {
        Content = content;
    }

    public void Display()
    {
        Console.WriteLine($"Content: {Content}");
    }
}

// Использование:
Box<int> intBox = new Box<int>(123);
intBox.Display(); // Content: 123

Box<string> stringBox = new Box<string>("Hello, Generics!");
stringBox.Display(); // Content: Hello, Generics!
```

---

### c) Обобщённые методы

#### Пример: Метод для обмена значениями
```csharp
public static void Swap<T>(ref T a, ref T b)
{
    T temp = a;
    a = b;
    b = temp;
}

// Использование:
int x = 1, y = 2;
Swap(ref x, ref y);
// Теперь x = 2, y = 1

string s1 = "Hello", s2 = "World";
Swap(ref s1, ref s2);
// Теперь s1 = "World", s2 = "Hello"
```

---

### d) Обобщённые интерфейсы

#### Пример: Интерфейс `IRepository<T>`
```csharp
public interface IRepository<T>
{
    void Add(T item);
    T GetById(int id);
    IEnumerable<T> GetAll();
}

// Реализация для сущности User
public class UserRepository : IRepository<User>
{
    private List<User> _users = new List<User>();

    public void Add(User user) => _users.Add(user);

    public User GetById(int id) => _users.FirstOrDefault(u => u.Id == id);

    public IEnumerable<User> GetAll() => _users;
}
```

---

### e) Ограничения обобщений (Constraints)

Иногда нужно ограничить типы, которые можно использовать с обобщением. Например, требовать, чтобы тип был классом, структурой, имел конструктор без параметров и т.д.

#### Пример: Ограничение `where T : new()`
```csharp
public class Factory<T> where T : new()
{
    public T CreateInstance()
    {
        return new T();
    }
}

// Использование:
Factory<List<int>> listFactory = new Factory<List<int>>();
var newList = listFactory.CreateInstance(); // new List<int>()
```

#### Другие ограничения:
- `where T : class` — тип должен быть ссылочным.
- `where T : struct` — тип должен быть значимым.
- `where T : IComparable` — тип должен реализовывать интерфейс `IComparable`.
- `where T : BaseClass` — тип должен наследоваться от `BaseClass`.

---

## 3. Пример с кастомной коллекцией

#### Обобщённая коллекция `MyList<T>`
```csharp
public class MyList<T>
{
    private T[] _items;
    private int _count;

    public MyList(int capacity = 4)
    {
        _items = new T[capacity];
        _count = 0;
    }

    public void Add(T item)
    {
        if (_count == _items.Length)
        {
            Array.Resize(ref _items, _items.Length * 2);
        }
        _items[_count++] = item;
    }

    public T Get(int index) => _items[index];

    public int Count => _count;
}

// Использование:
MyList<string> myList = new MyList<string>();
myList.Add("Apple");
myList.Add("Banana");
Console.WriteLine(myList.Get(0)); // Apple
```

---

## 4. Итоги

- **Generics** позволяют писать универсальный и типобезопасный код.
- Широко используются в коллекциях (`List<T>`, `Dictionary<TKey, TValue>`), классах, методах и интерфейсах.
- Ограничения (`where T : ...`) помогают контролировать типы, которые можно использовать с обобщениями.