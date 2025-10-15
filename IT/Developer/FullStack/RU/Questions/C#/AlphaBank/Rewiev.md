## Вопрос
1. Как это работает
2. Как можно улучшить

```c#
public class Plane
{
    private int FlightId;
    private Person Pilot;
    private int _currentNumber = 0;
    private string coordinate;

    public Plane(Person p, int id)
    {
        Pilot = p;
        FlightId = id;
        Passengers = new ConcurrentDictionary<int, Person>();
    }

    public void Register(Person p)
    {
        Passengers[_currentNumber++] = p;
    }

    private static object _sync = new object();

    public async void CheckCoordinate()
    {
        Monitor.Enter(_sync);
        try
        {
            string temp = await Navigator.GetCoordinate();
            if (!coordinate.Equals(temp))
            {
                coordinate = temp;
            }
        }
        catch (Exception e)
        {
            Monitor.Exit(_sync);
        }
    }

    public void ChangePilot(string fn, string ln, string doc)
    {
        Pilot.FirstName = fn;
        Pilot.LastName = ln;
    }

    public async void StartFlight()
    {
        await FlightDb.Start(FlightId, JsonConvert.SerializeObject(Passengers));
        await FlightKafkaQueue.SendStart(FlightId, JsonConvert.SerializeObject(Passengers));
    }

    public ConcurrentDictionary<int, Person> Passengers { get; set; }
}

public class Person
{
    public string DocumentId { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
}
```

Вот разбор кода с точки зрения архитектуры, потокобезопасности, стиля и возможных улучшений — как это сделал бы сеньор на код-ревью.

---

### **1. Общий обзор класса `Plane`**

#### **Поля и свойства**
- **`FlightId`, `Pilot`, `_currentNumber`, `coordinate`**
  - Поля объявлены как `private`, что правильно.
  - `_currentNumber` используется для генерации ключей в `Passengers`. Это потенциально небезопасно в многопоточной среде (см. ниже).
  - `coordinate` не инициализировано, что может привести к `NullReferenceException` при первом вызове `CheckCoordinate`.

- **`Passengers`**
  - Используется `ConcurrentDictionary<int, Person>`, что хорошо для многопоточности.
  - Однако, доступ к `_currentNumber` не синхронизирован, что может привести к дублированию ключей.

---

#### **Конструктор**
```csharp
public Plane(Person p, int id)
{
    Pilot = p;
    FlightId = id;
    Passengers = new ConcurrentDictionary<int, Person>();
}
```
- **Проблема**: Нет проверки на `null` для `p`.
- **Улучшение**: Добавить валидацию:
  ```csharp
  Pilot = p ?? throw new ArgumentNullException(nameof(p));
  ```

---

#### **Метод `Register`**
```csharp
public void Register(Person p)
{
    Passengers[_currentNumber++] = p;
}
```
- **Проблемы**:
  - Нет проверки на `null` для `p`.
  - `_currentNumber` не синхронизирован, что может привести к дублированию ключей в многопоточной среде.
- **Улучшения**:
  - Использовать `Interlocked.Increment` для `_currentNumber`:
    ```csharp
    public void Register(Person p)
    {
        if (p == null)
            throw new ArgumentNullException(nameof(p));
        Passengers.TryAdd(Interlocked.Increment(ref _currentNumber) - 1, p);
    }
    ```

---

#### **Метод `CheckCoordinate`**
```csharp
public async void CheckCoordinate()
{
    Monitor.Enter(_sync);
    try
    {
        string temp = await Navigator.GetCoordinate();
        if (!coordinate.Equals(temp))
        {
            coordinate = temp;
        }
    }
    catch (Exception e)
    {
        Monitor.Exit(_sync);
    }
}
```
- **Проблемы**:
  - `async void` — антипаттерн. Может привести к необработанным исключениям.
  - `Monitor.Exit` не вызывается в `finally`, что может привести к дедлоку.
  - `coordinate` может быть `null` при первом вызове.
  - Нет обработки `NullReferenceException` при вызове `Equals`.
- **Улучшения**:
  - Заменить на `async Task`.
  - Использовать `finally` для `Monitor.Exit`.
  - Инициализировать `coordinate` в конструкторе.
  - Добавить проверку на `null`:
    ```csharp
    public async Task CheckCoordinate()
    {
        Monitor.Enter(_sync);
        try
        {
            string temp = await Navigator.GetCoordinate();
            if (coordinate == null || !coordinate.Equals(temp))
            {
                coordinate = temp;
            }
        }
        finally
        {
            Monitor.Exit(_sync);
        }
    }
    ```

---

#### **Метод `ChangePilot`**
```csharp
public void ChangePilot(string fn, string ln, string doc)
{
    Pilot.FirstName = fn;
    Pilot.LastName = ln;
}
```
- **Проблемы**:
  - Нет проверки на `null` для `Pilot`.
  - Параметр `doc` не используется.
- **Улучшения**:
  - Добавить валидацию:
    ```csharp
    public void ChangePilot(string fn, string ln, string doc)
    {
        if (Pilot == null)
            throw new InvalidOperationException("Pilot is not assigned.");
        Pilot.FirstName = fn ?? throw new ArgumentNullException(nameof(fn));
        Pilot.LastName = ln ?? throw new ArgumentNullException(nameof(ln));
        Pilot.DocumentId = doc ?? throw new ArgumentNullException(nameof(doc));
    }
    ```

---

#### **Метод `StartFlight`**
```csharp
public async void StartFlight()
{
    await FlightDb.Start(FlightId, JsonConvert.SerializeObject(Passengers));
    await FlightKafkaQueue.SendStart(FlightId, JsonConvert.SerializeObject(Passengers));
}
```
- **Проблемы**:
  - `async void` — антипаттерн.
  - Нет обработки ошибок.
- **Улучшения**:
  - Заменить на `async Task`.
  - Добавить логирование/обработку ошибок:
    ```csharp
    public async Task StartFlight()
    {
        try
        {
            await FlightDb.Start(FlightId, JsonConvert.SerializeObject(Passengers));
            await FlightKafkaQueue.SendStart(FlightId, JsonConvert.SerializeObject(Passengers));
        }
        catch (Exception ex)
        {
            // Логирование или проброс исключения
            throw;
        }
    }
    ```

---

### **2. Общий обзор класса `Person`**
- Простой DTO-класс, ничего критического.
- **Улучшение**: Можно сделать свойства инициализируемыми только через конструктор (immutable):
  ```csharp
  public class Person
  {
      public string DocumentId { get; }
      public string FirstName { get; }
      public string LastName { get; }

      public Person(string doc, string fn, string ln)
      {
          DocumentId = doc ?? throw new ArgumentNullException(nameof(doc));
          FirstName = fn ?? throw new ArgumentNullException(nameof(fn));
          LastName = ln ?? throw new ArgumentNullException(nameof(ln));
      }
  }
  ```

---

### **3. Архитектурные улучшения**
- **Разделение ответственности**:
  - Логика работы с координатами, пассажирами и полётом может быть вынесена в отдельные сервисы.
- **Логирование**:
  - Добавить логирование для отслеживания ошибок и важных событий.
- **Тестируемость**:
  - Вынести зависимости (`Navigator`, `FlightDb`, `FlightKafkaQueue`) в интерфейсы и использовать DI.
- **Потокобезопасность**:
  - Заменить `Monitor` на `SemaphoreSlim` или использовать `lock`.
  - Убедиться, что все критические секции защищены.

---

### **4. Пример улучшенного кода**
```csharp
public class Plane
{
    private readonly int _flightId;
    private Person _pilot;
    private int _currentNumber = 0;
    private string _coordinate = string.Empty;
    private static readonly object _sync = new object();

    public ConcurrentDictionary<int, Person> Passengers { get; } = new();

    public Plane(Person pilot, int flightId)
    {
        _pilot = pilot ?? throw new ArgumentNullException(nameof(pilot));
        _flightId = flightId;
    }

    public void Register(Person person)
    {
        if (person == null)
            throw new ArgumentNullException(nameof(person));
        Passengers.TryAdd(Interlocked.Increment(ref _currentNumber) - 1, person);
    }

    public async Task CheckCoordinate()
    {
        Monitor.Enter(_sync);
        try
        {
            string temp = await Navigator.GetCoordinate();
            if (!_coordinate.Equals(temp))
            {
                _coordinate = temp;
            }
        }
        finally
        {
            Monitor.Exit(_sync);
        }
    }

    public void ChangePilot(string firstName, string lastName, string documentId)
    {
        if (_pilot == null)
            throw new InvalidOperationException("Pilot is not assigned.");
        _pilot.FirstName = firstName ?? throw new ArgumentNullException(nameof(firstName));
        _pilot.LastName = lastName ?? throw new ArgumentNullException(nameof(lastName));
        _pilot.DocumentId = documentId ?? throw new ArgumentNullException(nameof(documentId));
    }

    public async Task StartFlight()
    {
        try
        {
            await FlightDb.Start(_flightId, JsonConvert.SerializeObject(Passengers));
            await FlightKafkaQueue.SendStart(_flightId, JsonConvert.SerializeObject(Passengers));
        }
        catch (Exception ex)
        {
            // Логирование
            throw;
        }
    }
}
```

---

### **5. Итоговые рекомендации**
1. **Избегайте `async void`** — всегда используйте `async Task`.
2. **Синхронизация** — используйте `lock` или `SemaphoreSlim` вместо `Monitor`, если нет веских причин.
3. **Валидация** — проверяйте входные параметры на `null`.
4. **Immutable объекты** — где возможно, делайте классы неизменяемыми.
5. **Логирование** — добавляйте логирование для отладки и мониторинга.
6. **DI** — выносите зависимости в интерфейсы и используйте Dependency Injection.