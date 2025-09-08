## **1. Основы LINQ**

### **Вопрос 1: Что такое LINQ? Как он работает под капотом?**
**Ответ:**
**LINQ (Language Integrated Query)** — это набор технологий для **интеграции запросов** в язык C#. Включает:
- **LINQ to Objects** (запросы к коллекциям в памяти).
- **LINQ to SQL/Entities** (запросы к базам данных).
- **LINQ to XML** (работа с XML).

**Как работает LINQ to Objects:**
1. **Синтаксис запросов** (query syntax) преобразуется компилятором в **методы расширения** (method syntax).
   ```csharp
   // Query syntax
   var query = from x in numbers where x > 5 select x;

   // Преобразуется в:
   var query = numbers.Where(x => x > 5).Select(x => x);
   ```
2. **Отложенное выполнение (Deferred Execution)**:
   - Запрос **не выполняется** до момента итерации (например, в `foreach` или вызова `ToList()`).
   - Пример:
     ```csharp
     var query = numbers.Where(x => x > 5); // Запрос ещё не выполнен!
     foreach (var num in query) { ... }      // Здесь выполняется
     ```
3. **Цепочка итераторов**:
   - Каждый оператор LINQ (`Where`, `Select`) возвращает **новый итератор**, который обёртывает предыдущий.
   - При итерации вызывается `MoveNext()` для каждого итератора в цепочке.

**Дополнительные вопросы:**
- *Чем отличается `IEnumerable<T>` от `IQueryable<T>`?*
  **Ответ:**
  - `IEnumerable<T>` — **клиентская оценка** (выполняется в памяти, например, для `List<T>`).
  - `IQueryable<T>` — **серверная оценка** (преобразуется в SQL или другой язык запросов, например, для Entity Framework).
- *Как компилятор преобразует query syntax в method syntax?*
  **Ответ:** Компилятор анализирует синтаксическое дерево и заменяет операторы (`from`, `where`, `select`) на вызовы методов (`Where`, `Select`).

---

### **Вопрос 2: Что такое отложенное выполнение (Deferred Execution) в LINQ? Приведите примеры.**
**Ответ:**
**Отложенное выполнение** означает, что запрос **не выполняется** до момента, пока не потребуются его результаты.
Это позволяет:
- **Оптимизировать** выполнение (например, не грузить все данные сразу).
- **Динамически модифицировать** запрос перед выполнением.

**Примеры:**
1. **Фильтрация с `Where`**:
   ```csharp
   var numbers = new List<int> { 1, 2, 3, 4, 5 };
   var query = numbers.Where(x => x > 2); // Запрос ещё не выполнен!
   numbers.Add(6); // Коллекция изменилась!
   foreach (var num in query) Console.WriteLine(num); // Выведет 3, 4, 5, 6
   ```
   - Запрос выполняется **в момент итерации**, поэтому учитывает добавленный элемент.

2. **Цепочка операторов**:
   ```csharp
   var query = numbers
       .Where(x => x > 2)
       .Select(x => x * 2); // Ничего не выполнено!
   ```
   - Все операторы (`Where`, `Select`) **отложены** до вызова `ToList()` или `foreach`.

3. **Опасность отложенного выполнения**:
   ```csharp
   var query = GetNumbers().Where(x => x > 2);
   var list = query.ToList(); // Выполняется здесь
   GetNumbers().Add(7); // Не повлияет на list!
   ```
   - После вызова `ToList()` запрос **материализуется**, и дальнейшие изменения исходной коллекции не учитываются.

**Дополнительные вопросы:**
- *Как принудительно выполнить запрос?*
  **Ответ:** Использовать методы **немедленного выполнения** (`ToList()`, `ToArray()`, `Count()`, `First()`).
- *Почему отложенное выполнение может привести к ошибкам?*
  **Ответ:** Если исходная коллекция изменится **после создания запроса**, но **до его выполнения**, результаты могут быть неожиданными.

---

### **Вопрос 3: Какие операторы LINQ выполняются немедленно (Eager Evaluation)?**
**Ответ:**
Немедленное выполнение означает, что запрос **выполняется сразу** при вызове метода.
**Список операторов с немедленным выполнением:**

| **Категория**          | **Операторы**                                                                 |
|------------------------|-------------------------------------------------------------------------------|
| **Агрегация**          | `Count()`, `LongCount()`, `Min()`, `Max()`, `Average()`, `Sum()`              |
| **Преобразование**     | `ToList()`, `ToArray()`, `ToDictionary()`, `ToLookup()`, `ToHashSet()`        |
| **Элементы**           | `First()`, `FirstOrDefault()`, `Last()`, `LastOrDefault()`, `Single()`, `ElementAt()` |
| **Проверка условий**   | `Any()`, `All()`, `Contains()`                                                |
| **Объединение**        | `Concat()`, `Zip()` (в некоторых случаях)                                   |

**Примеры:**
```csharp
var numbers = new List<int> { 1, 2, 3 };
var count = numbers.Where(x => x > 1).Count(); // Выполняется немедленно
var list = numbers.Where(x => x > 1).ToList(); // Также немедленно
```

**Дополнительные вопросы:**
- *Почему `Count()` выполняется немедленно, а `Where()` — нет?*
  **Ответ:** `Count()` должен **посчитать все элементы**, поэтому он вынужден выполнить запрос. `Where()` просто возвращает новый итератор.
- *Как написать кастомный оператор с немедленным выполнением?*
  **Ответ:** Вернуть материаллизованный результат (например, `List<T>` или массив).

---

## **2. Внутренние механизмы LINQ**

### **Вопрос 4: Как работает цепочка вызовов LINQ? Что такое "итераторы" (yield)?**
**Ответ:**
Каждый оператор LINQ (`Where`, `Select`, `OrderBy`) возвращает **новый итератор**, который обёртывает предыдущий.
При итерации (например, в `foreach`) вызывается цепочка `MoveNext()` для каждого итератора.

**Пример цепочки:**
```csharp
var query = numbers
    .Where(x => x > 2)   // Итератор 1: WhereIterator
    .Select(x => x * 2)   // Итератор 2: SelectIterator (обёртывает WhereIterator)
    .OrderBy(x => x);     // Итератор 3: OrderByIterator (обёртывает SelectIterator)
```
**Как это работает:**
1. При вызове `foreach` у `query` вызывается `GetEnumerator()`.
2. `OrderByIterator` вызывает `MoveNext()` у `SelectIterator`.
3. `SelectIterator` вызывает `MoveNext()` у `WhereIterator`.
4. `WhereIterator` перебирает исходную коллекцию и фильтрует элементы.

**Реализация на основе `yield`:**
Методы LINQ (например, `Where`) используют **конечные автоматы** (state machines), сгенерированные компилятором для `yield return`.
Пример упрощённой реализации `Where`:
```csharp
public static IEnumerable<T> Where<T>(this IEnumerable<T> source, Func<T, bool> predicate)
{
    foreach (var item in source)
        if (predicate(item))
            yield return item; // Компилятор генерирует класс-итератор
}
```

**Дополнительные вопросы:**
- *Что такое "конечный автомат" (state machine) в контексте `yield`?*
  **Ответ:** Компилятор преобразует метод с `yield` в класс, реализующий `IEnumerator<T>`, с полем `_state` для отслеживания текущей позиции.
- *Почему цепочка итераторов может быть неэффективной?*
  **Ответ:** Каждый итератор добавляет накладные расходы на вызов `MoveNext()`. Для больших коллекций это может замедлить выполнение.

---

### **Вопрос 5: Как LINQ оптимизирует запросы? Приведите примеры оптимизаций.**
**Ответ:**
LINQ применяет несколько оптимизаций для улучшения производительности:

1. **Слияние операторов (Fusion)**:
   - Некоторые операторы (например, `Where` + `Select`) могут быть **объединены** в один итератор.
   - Пример:
     ```csharp
     var query = numbers.Where(x => x > 2).Select(x => x * 2);
     ```
     - Вместо двух отдельных итераторов (`WhereIterator` + `SelectIterator`), компилятор может сгенерировать **один итератор**, который фильтрует и проецирует за один проход.

2. **Отложенное выполнение**:
   - Запросы выполняются только при необходимости, что экономит ресурсы.

3. **Кэширование делегатов**:
   - Делегаты (например, в `Where`) могут быть **кэшированы** для повторного использования.

4. **Оптимизации для массивов**:
   - Для массивов некоторые операторы (например, `Where`) используют **специализированные реализации** с меньшими накладными расходами.

5. **Использование `Span<T>` в .NET Core 3.0+**:
   - Некоторые операторы (например, `ToArray()`) могут работать напрямую с `Span<T>` для ускорения копирования данных.

**Пример оптимизации слияния:**
```csharp
// До оптимизации:
var query = numbers.Where(x => x > 2).Select(x => x * 2);
// После оптимизации (псевдокод):
foreach (var num in numbers)
    if (num > 2)
        yield return num * 2; // Один проход!
```

**Дополнительные вопросы:**
- *Как проверить, что LINQ применил оптимизацию слияния?*
  **Ответ:** Использовать **декомпилятор** (например, ILSpy) и посмотреть, сколько итераторов сгенерировано.
- *Почему слияние не всегда возможно?*
  **Ответ:** Если операторы имеют **побочные эффекты** или зависят от порядка (например, `OrderBy`), слияние может быть невозможно.

---

### **Вопрос 6: Как работает `GroupBy` в LINQ? Какая у него сложность?**
**Ответ:**
**`GroupBy`** группирует элементы по ключу, возвращая `IEnumerable<IGrouping<TKey, TElement>>`.
**Внутренняя реализация**:
1. Создаётся **словарь** (`Dictionary<TKey, List<TElement>>`), где:
   - **Ключ** — значение, по которому группируем.
   - **Значение** — список элементов группы.
2. Для каждого элемента исходной коллекции:
   - Вычисляется ключ (`keySelector`).
   - Элемент добавляется в список для этого ключа.
3. Возвращается **обёртка** над словарём, реализующая `IGrouping<TKey, TElement>`.

**Сложность**:
- **`O(n)`** для построения групп (один проход по коллекции).
- **`O(1)`** для доступа к группе по ключу (если ключ известен).
- **Память**: `O(n)` (хранит все элементы + словарь).

**Пример:**
```csharp
var groups = people.GroupBy(p => p.Age);
// Структура в памяти:
// {
//   20: [Alice, Bob],
//   25: [Charlie],
//   30: [Dave]
// }
```

**Дополнительные вопросы:**
- *Чем `GroupBy` отличается от `ToLookup`?*
  **Ответ:**
  - `GroupBy` возвращает **отложенный** `IEnumerable<IGrouping<TKey, TElement>>` (группы создаются при итерации).
  - `ToLookup` возвращает **немедленно выполненный** `ILookup<TKey, TElement>` (группы создаются сразу).
- *Как реализовать кастомный `GroupBy`?*
  **Ответ:**
  ```csharp
  public static IEnumerable<IGrouping<TKey, TElement>> GroupBy<TSource, TKey, TElement>(
      this IEnumerable<TSource> source,
      Func<TSource, TKey> keySelector,
      Func<TSource, TElement> elementSelector)
  {
      var dict = new Dictionary<TKey, List<TElement>>();
      foreach (var item in source)
      {
          var key = keySelector(item);
          if (!dict.TryGetValue(key, out var list))
              dict[key] = list = new List<TElement>();
          list.Add(elementSelector(item));
      }
      return dict.Select(g => new Grouping<TKey, TElement>(g.Key, g.Value));
  }

  private class Grouping<TKey, TElement> : IGrouping<TKey, TElement>
  {
      public TKey Key { get; }
      private readonly IEnumerable<TElement> _elements;
      public Grouping(TKey key, IEnumerable<TElement> elements) =>
          (Key, _elements) = (key, elements);
      public IEnumerator<TElement> GetEnumerator() => _elements.GetEnumerator();
      IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
  }
  ```

---

## **3. Производительность и оптимизации**

### **Вопрос 7: Почему `Count()` может быть медленным? Как ускорить подсчёт элементов?**
**Ответ:**
**`Count()`** может быть медленным, потому что:
1. Для `IEnumerable<T>` он **перебирает все элементы** (`O(n)`):
   ```csharp
   var count = someEnumerable.Count(); // Перебор всех элементов!
   ```
2. Для коллекций с `Count` (например, `List<T>`, `Array`) он **вызывает свойство `Count`** (`O(1)`):
   ```csharp
   var list = new List<int> { 1, 2, 3 };
   var count = list.Count(); // Быстро (использует list.Count)
   ```

**Как ускорить:**
- Если источник — `ICollection<T>` (например, `List<T>`), используйте **свойство `Count`**:
  ```csharp
  var count = list.Count; // O(1)
  ```
- Для LINQ-запросов **сохраняйте результат** в коллекцию:
  ```csharp
  var query = numbers.Where(x => x > 2);
  var list = query.ToList(); // Материализуем запрос
  var count = list.Count;    // O(1)
  ```
- Используйте `Any()` для проверки наличия элементов (не подсчитывает все):
  ```csharp
  if (query.Any()) { ... } // Останавливается на первом элементе
  ```

**Дополнительные вопросы:**
- *Почему `LongCount()` существует, если есть `Count()`?*
  **Ответ:** `LongCount()` возвращает `long` (для коллекций с > 2 млрд элементов), а `Count()` — `int`.
- *Как работает `Count()` для `IQueryable<T>`?*
  **Ответ:** Преобразуется в SQL `COUNT(*)` (выполняется на сервере БД).

---

### **Вопрос 8: Как работает `Select` в LINQ? Какая у него сложность?**
**Ответ:**
**`Select`** проецирует каждый элемент исходной коллекции в новый вид.
**Внутренняя реализация**:
- Возвращает **итератор**, который:
  1. Перебирает исходную коллекцию.
  2. Применяет `selector` к каждому элементу.
  3. Возвращает результат (отложенно).

**Сложность**:
- **`O(n)`** (один проход по коллекции).
- **Память**: `O(1)` (не хранит результаты, если не материаллизован).

**Пример:**
```csharp
var query = numbers.Select(x => x * 2);
// Эквивалентно:
foreach (var num in numbers)
    yield return num * 2;
```

**Оптимизации:**
- **Слияние с `Where`**: Компилятор может объединить `Where` + `Select` в один итератор.
- **Для массивов**: Используется специализированная реализация с меньшими накладными расходами.

**Дополнительные вопросы:**
- *Чем `Select` отличается от `SelectMany`?*
  **Ответ:** `SelectMany` **разворачивает** вложенные коллекции:
  ```csharp
  var query = people.SelectMany(p => p.Orders); // Возвращает все заказы всех людей
  ```
- *Как реализовать кастомный `Select`?*
  **Ответ:**
  ```csharp
  public static IEnumerable<TResult> Select<TSource, TResult>(
      this IEnumerable<TSource> source, Func<TSource, TResult> selector)
  {
      foreach (var item in source)
          yield return selector(item);
  }
  ```

---

### **Вопрос 9: Почему `OrderBy` может быть неэффективным? Как оптимизировать сортировку?**
**Ответ:**
**`OrderBy`** использует алгоритм **быстрой сортировки** (или другой `O(n log n)` алгоритм), что может быть неэффективно для:
1. **Больших коллекций** (например, > 1 млн элементов).
2. **Многократных сортировок** одной и той же коллекции.
3. **Сложных ключей сортировки** (например, если `keySelector` дорогой).

**Проблемы производительности:**
- **Память**: `OrderBy` создаёт **новый массив** для сортировки.
- **Время**: `O(n log n)` — дороже, чем `O(n)` для `Where` или `Select`.

**Как оптимизировать:**
1. **Использовать `OrderBy` только при необходимости**:
   ```csharp
   var query = numbers.Where(x => x > 2); // Отложим сортировку
   if (needSorting) query = query.OrderBy(x => x);
   ```
2. **Сортировать один раз и кэшировать**:
   ```csharp
   var sortedList = numbers.OrderBy(x => x).ToList(); // Материализуем
   ```
3. **Использовать `SortedSet<T>` или `SortedDictionary<TKey, TValue>`**, если данные часто сортируются.
4. **Для LINQ to SQL/Entities**: Сортировка выполняется на **сервере БД** (оптимизирована СУБД).

**Дополнительные вопросы:**
- *Чем `OrderBy` отличается от `OrderByDescending`?*
  **Ответ:** `OrderByDescending` сортирует по убыванию.
- *Как работает `ThenBy`?*
  **Ответ:** Добавляет **вторичный ключ сортировки** (аналог SQL `ORDER BY x, y`).

---

### **Вопрос 10: Как работает `Join` в LINQ? Какая у него сложность?**
**Ответ:**
**`Join`** выполняет **внутреннее соединение** (inner join) двух коллекций по ключу.
**Внутренняя реализация**:
1. **Строит хэш-таблицу** для правой коллекции (`inner`):
   ```csharp
   var lookup = inner.ToLookup(innerKeySelector);
   ```
2. Перебирает левую коллекцию (`outer`) и для каждого элемента:
   - Вычисляет ключ (`outerKeySelector`).
   - Ищет совпадения в хэш-таблице.
   - Возвращает пары `(outer, inner)` для совпадающих ключей.

**Сложность**:
- **`O(n + m)`** (где `n` и `m` — размеры коллекций).
- **Память**: `O(m)` (хэш-таблица для правой коллекции).

**Пример:**
```csharp
var query = from person in people
            join pet in pets on person.Id equals pet.OwnerId
            select new { person.Name, pet.Name };
// Эквивалентно:
var query = people.Join(
    pets,
    person => person.Id,
    pet => pet.OwnerId,
    (person, pet) => new { person.Name, pet.Name }
);
```

**Дополнительные вопросы:**
- *Чем `Join` отличается от `GroupJoin`?*
  **Ответ:** `GroupJoin` возвращает **группы совпадений** (аналог SQL `LEFT JOIN ... GROUP BY`).
- *Как реализовать `Left Outer Join` в LINQ?*
  **Ответ:** Использовать `GroupJoin` + `DefaultIfEmpty`:
  ```csharp
  var query = from person in people
              join pet in pets on person.Id equals pet.OwnerId into petGroup
              from pet in petGroup.DefaultIfEmpty()
              select new { person.Name, PetName = pet?.Name ?? "No pet" };
  ```

---

## **4. LINQ to Objects vs. LINQ to SQL/Entities**

### **Вопрос 11: Чем отличается выполнение LINQ to Objects от LINQ to SQL?**
**Ответ:**

| **Аспект**               | **LINQ to Objects**                              | **LINQ to SQL/Entities**                        |
|--------------------------|--------------------------------------------------|-------------------------------------------------|
| **Источник данных**      | Коллекции в памяти (`List<T>`, `Array`).        | База данных (SQL Server, PostgreSQL).          |
| **Выполнение**           | Клиентское (в процессе .NET).                    | Серверное (на стороне БД).                     |
| **Интерфейс**            | `IEnumerable<T>`.                                | `IQueryable<T>`.                                |
| **Отложенное выполнение**| Да (запрос выполняется при итерации).           | Да (запрос выполняется при материализации).   |
| **Преобразование**       | Методы расширения (`Where`, `Select`).           | Преобразуется в **SQL-запрос**.                |
| **Пример**               | `numbers.Where(x => x > 2)`                     | `dbContext.Users.Where(u => u.Age > 18)`       |
| **Производительность**   | Быстро для небольших коллекций.                 | Медленнее (сетевые задержки, но оптимизировано СУБД). |
| **Ограничения**          | Нет ограничений (всё в памяти).                 | Ограничен возможностями SQL (например, нет `Zip`). |

**Пример различия:**
```csharp
// LINQ to Objects (выполняется в .NET)
var localQuery = new List<int> { 1, 2, 3 }.Where(x => x > 1);

// LINQ to SQL (преобразуется в SQL)
var dbQuery = dbContext.Users.Where(u => u.Age > 18);
// SQL: SELECT * FROM Users WHERE Age > 18
```

**Дополнительные вопросы:**
- *Почему нельзя использовать `Count()` в LINQ to SQL без материализации?*
  **Ответ:** Можно! `Count()` преобразуется в SQL `COUNT(*)` и выполняется на сервере:
  ```csharp
  var count = dbContext.Users.Count(u => u.Age > 18); // SQL: SELECT COUNT(*) FROM Users WHERE Age > 18
  ```
- *Как заставить LINQ to SQL выполнить запрос немедленно?*
  **Ответ:** Использовать `ToList()`, `First()`, `Count()` и др.

---

### **Вопрос 12: Как работает `AsQueryable()`? Когда его использовать?**
**Ответ:**
**`AsQueryable()`** преобразует `IEnumerable<T>` в `IQueryable<T>`, что позволяет:
- **Добавлять условия динамически** (например, в зависимости от пользовательского ввода).
- **Отложить выполнение запроса** до материализации.

**Пример:**
```csharp
IQueryable<User> query = dbContext.Users.AsQueryable();
if (filterByAge)
    query = query.Where(u => u.Age > 18);
var result = query.ToList(); // Запрос выполняется здесь
```

**Когда использовать:**
1. **Динамические запросы**:
   ```csharp
   IQueryable<User> BuildQuery(bool filterByAge)
   {
       var query = dbContext.Users.AsQueryable();
       if (filterByAge)
           query = query.Where(u => u.Age > 18);
       return query;
   }
   ```
2. **Расширение существующих запросов**:
   ```csharp
   var baseQuery = dbContext.Users.Where(u => u.IsActive);
   var extendedQuery = baseQuery.AsQueryable().OrderBy(u => u.Name);
   ```

**Опасности:**
- Если применить `AsQueryable()` к `IEnumerable<T>` (не к `IQueryable<T>`), запрос **выполнится в памяти**, а не на сервере БД!
  ```csharp
  var localList = new List<User> { ... };
  var query = localList.AsQueryable().Where(u => u.Age > 18); // Выполнится в памяти!
  ```

**Дополнительные вопросы:**
- *Чем `AsQueryable()` отличается от `AsEnumerable()`?*
  **Ответ:**
  - `AsQueryable()` преобразует в `IQueryable<T>` (для серверной оценки).
  - `AsEnumerable()` преобразует в `IEnumerable<T>` (для клиентской оценки).
- *Как проверить, что запрос будет выполнен на сервере?*
  **Ответ:** Посмотреть сгенерированный SQL (например, через `ToQueryString()` в EF Core):
  ```csharp
  var sql = query.ToQueryString();
  ```

---

### **Вопрос 13: Почему нельзя использовать `Count()` в LINQ to SQL без вызова `ToList()`?**
**Ответ:**
**Можно!** `Count()` в `IQueryable<T>` **преобразуется в SQL `COUNT`** и выполняется на сервере:
```csharp
var count = dbContext.Users.Count(u => u.Age > 18);
// SQL: SELECT COUNT(*) FROM Users WHERE Age > 18
```
**Когда нужен `ToList()`:**
- Если нужно **материализовать данные** для дальнейшей обработки в памяти:
  ```csharp
  var users = dbContext.Users.Where(u => u.Age > 18).ToList(); // Запрос выполнен
  var localCount = users.Count; // Клиентский подсчёт
  ```

**Ошибка:**
Если вызвать `Count()` **после клиентских операций** (например, `Where` в памяти), это приведёт к полной загрузке данных:
```csharp
var query = dbContext.Users.AsEnumerable().Where(u => u.Age > 18);
var count = query.Count(); // Все пользователи загружаются в память!
```

**Дополнительные вопросы:**
- *Как оптимизировать подсчёт в LINQ to SQL?*
  **Ответ:** Использовать `Count()` **до материализации**:
  ```csharp
  var count = dbContext.Users.Count(u => u.Age > 18); // Оптимально
  ```
- *Что быстрее: `Count()` или `Any()`?*
  **Ответ:** `Any()` быстрее, если нужно только проверить наличие элементов (останавливается на первом совпадении).

---

## **5. Кастомные операторы LINQ**

### **Вопрос 14: Как написать кастомный оператор LINQ?**
**Ответ:**
Кастомный оператор LINQ — это **метод расширения** для `IEnumerable<T>`.
**Пример: оператор `WhereNotNull`**
```csharp
public static class LinqExtensions
{
    public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> source)
        where T : class
    {
        foreach (var item in source)
            if (item != null)
                yield return item;
    }
}

// Использование:
var numbers = new List<int?> { 1, null, 2, null, 3 };
var nonNullNumbers = numbers.WhereNotNull(); // 1, 2, 3
```

**Как это работает:**
1. Метод принимает `IEnumerable<T?>` и возвращает `IEnumerable<T>`.
2. Использует `yield return` для отложенного выполнения.
3. Может быть использован в цепочках LINQ:
   ```csharp
   var query = numbers.WhereNotNull().Select(x => x * 2);
   ```

**Дополнительные вопросы:**
- *Как написать оператор с немедленным выполнением?*
  **Ответ:** Вернуть материаллизованный результат (например, `List<T>`):
  ```csharp
  public static List<T> ToListWhereNotNull<T>(this IEnumerable<T?> source)
      where T : class
  {
      var result = new List<T>();
      foreach (var item in source)
          if (item != null)
              result.Add(item);
      return result;
  }
  ```
- *Как добавить поддержку `IQueryable<T>` для кастомного оператора?*
  **Ответ:** Написать **провайдер выражений** (expression visitor) для преобразования в SQL. Пример:
  ```csharp
  public static IQueryable<T> WhereNotNull<T>(this IQueryable<T?> source)
      where T : class
  {
      var parameter = Expression.Parameter(typeof(T?), "x");
      var lambda = Expression.Lambda<Func<T?, bool>>(
          Expression.NotEqual(parameter, Expression.Constant(null)),
          parameter
      );
      return source.Where(lambda).Cast<T>();
  }
  ```

---

### **Вопрос 15: Как реализовать кастомный оператор `DistinctBy`?**
**Ответ:**
**`DistinctBy`** возвращает уникальные элементы на основе **ключа селектора** (аналог SQL `DISTINCT ON`).
**Реализация:**
```csharp
public static IEnumerable<TSource> DistinctBy<TSource, TKey>(
    this IEnumerable<TSource> source,
    Func<TSource, TKey> keySelector)
{
    var seenKeys = new HashSet<TKey>();
    foreach (var item in source)
    {
        var key = keySelector(item);
        if (seenKeys.Add(key)) // Возвращает true, если ключ новый
            yield return item;
    }
}

// Использование:
var people = new List<Person>
{
    new Person { Id = 1, Name = "Alice", Age = 20 },
    new Person { Id = 2, Name = "Bob", Age = 20 },
    new Person { Id = 3, Name = "Charlie", Age = 25 }
};
var distinctByAge = people.DistinctBy(p => p.Age);
// Результат: Alice (20), Charlie (25)
```

**Оптимизации:**
- Использовать `HashSet<TKey>` для быстрого поиска дубликатов (`O(1)` на операцию).
- Для `IQueryable<T>` нужно реализовать **провайдер выражений** (преобразовать в SQL `DISTINCT`).

**Дополнительные вопросы:**
- *Как этот оператор будет работать с `IQueryable<T>`?*
  **Ответ:** Нужно написать **expression visitor** для преобразования в SQL:
  ```csharp
  public static IQueryable<TSource> DistinctBy<TSource, TKey>(
      this IQueryable<TSource> source,
      Expression<Func<TSource, TKey>> keySelector)
  {
      // Преобразовать в выражение DISTINCT ON (если поддерживается провайдером)
      // Или эмулировать через GROUP BY + FIRST
      return source.GroupBy(keySelector).Select(g => g.First());
  }
  ```
- *Чем `DistinctBy` отличается от `GroupBy` + `Select`?*
  **Ответ:** `DistinctBy` возвращает **первые уникальные элементы**, а `GroupBy` — **группы всех элементов**.

---

### **Вопрос 16: Как реализовать оператор `Batch` для пакетной обработки?**
**Ответ:**
**`Batch`** разбивает коллекцию на **пакеты фиксированного размера**.
**Реализация:**
```csharp
public static IEnumerable<IEnumerable<T>> Batch<T>(
    this IEnumerable<T> source, int size)
{
    if (size <= 0) throw new ArgumentOutOfRangeException(nameof(size));
    var batch = new List<T>(size);
    foreach (var item in source)
    {
        batch.Add(item);
        if (batch.Count == size)
        {
            yield return batch;
            batch = new List<T>(size);
        }
    }
    if (batch.Count > 0)
        yield return batch;
}

// Использование:
var numbers = Enumerable.Range(1, 10);
var batches = numbers.Batch(3);
// Результат:
// [1, 2, 3], [4, 5, 6], [7, 8, 9], [10]
```

**Оптимизации:**
- Использовать `List<T>` с предварительным выделением памяти (`new List<T>(size)`).
- Для больших коллекций можно использовать `Span<T>` (в .NET Core 3.0+).

**Дополнительные вопросы:**
- *Как реализовать `Batch` для `IQueryable<T>`?*
  **Ответ:** Невозможно эффективно, так как SQL не поддерживает пакетную обработку. Нужно материализовать данные:
  ```csharp
  var batches = dbContext.Users.ToList().Batch(100);
  ```
- *Как обработать последний пакет, если он меньше заданного размера?*
  **Ответ:** В реализации выше последний пакет возвращается даже если он неполный.

---

## **6. Производительность и оптимизации**

### **Вопрос 17: Почему `First()` быстрее `FirstOrDefault()`?**
**Ответ:**
- **`First()`** бросает исключение `InvalidOperationException`, если элементов нет.
  - **Не проверяет наличие элементов** перед доступом к первому.
- **`FirstOrDefault()`** всегда возвращает `default(T)`, если элементов нет.
  - **Проверяет наличие элементов**, что добавляет накладные расходы.

**Пример:**
```csharp
var emptyList = new List<int>();
var first = emptyList.First(); // Бросит исключение
var firstOrDefault = emptyList.FirstOrDefault(); // Вернёт 0
```

**Когда использовать что:**
- **`First()`** — если **гарантировано**, что коллекция не пустая (или нужно исключение).
- **`FirstOrDefault()`** — если пустая коллекция — **нормальный случай**.

**Дополнительные вопросы:**
- *Чем `Single()` отличается от `First()`?*
  **Ответ:** `Single()` проверяет, что в коллекции **ровно один элемент** (бросает исключение, если 0 или >1 элементов).
- *Как ускорить проверку на пустоту коллекции?*
  **Ответ:** Использовать `Any()`:
  ```csharp
  if (!collection.Any()) { ... } // Быстрее, чем collection.Count() == 0
  ```

---

### **Вопрос 18: Как ускорить LINQ-запросы для больших коллекций?**
**Ответ:**
1. **Избегать `IEnumerable<T>` в горячих путях**:
   - Преобразовывать в массивы или списки (`ToArray()`, `ToList()`).
   ```csharp
   var list = collection.Where(x => x > 2).ToList(); // Материализуем
   ```
2. **Использовать `Span<T>` или `Memory<T>`** (в .NET Core 3.0+):
   ```csharp
   var span = CollectionsMarshal.AsSpan(list); // Быстрый доступ к данным
   ```
3. **Заменять LINQ на ручные циклы**:
   ```csharp
   // Медленно:
   var sum = numbers.Where(x => x > 2).Sum();

   // Быстро:
   int sum = 0;
   foreach (var num in numbers)
       if (num > 2) sum += num;
   ```
4. **Кэшировать результаты запросов**:
   ```csharp
   var cachedQuery = query.ToList(); // Выполняем один раз
   ```
5. **Использовать `Array.ForEach` вместо LINQ**:
   ```csharp
   Array.ForEach(array, x => Console.WriteLine(x)); // Быстрее, чем array.ToList().ForEach
   ```
6. **Оптимизировать `OrderBy`**:
   - Сортировать **один раз** и кэшировать результат.
   - Использовать `SortedSet<T>` или `SortedDictionary<TKey, TValue>` для часто сортируемых данных.

**Дополнительные вопросы:**
- *Почему `ForEach` в LINQ не является частью стандартной библиотеки?*
  **Ответ:** Потому что он **не возвращает `IEnumerable<T>`** (нарушает принцип функциональности LINQ) и может иметь побочные эффекты.
- *Как измерить производительность LINQ-запроса?*
  **Ответ:** Использовать `BenchmarkDotNet`:
  ```csharp
  [MemoryDiagnoser]
  public class LinqBenchmark
  {
      private List<int> _numbers = Enumerable.Range(1, 1000).ToList();

      [Benchmark]
      public int LinqWhereSum() => _numbers.Where(x => x > 500).Sum();

      [Benchmark]
      public int ManualWhereSum()
      {
          int sum = 0;
          foreach (var num in _numbers)
              if (num > 500) sum += num;
          return sum;
      }
  }
  ```

---

### **Вопрос 19: Почему `ToList()` может быть опасным в LINQ to SQL?**
**Ответ:**
**`ToList()`** в `IQueryable<T>`:
1. **Выполняет запрос на сервере** (преобразуется в SQL).
2. **Загружает все данные в память**:
   ```csharp
   var users = dbContext.Users.ToList(); // Все пользователи загружены в List<User>!
   ```
   - Если в таблице **миллионы записей**, это приведёт к **высокому потреблению памяти**.

**Как избежать:**
- Использовать **постраничную загрузку** (`Skip`/`Take`):
  ```csharp
  var page = dbContext.Users.Skip(100).Take(10).ToList(); // Только 10 записей
  ```
- Фильтровать данные **на сервере**:
  ```csharp
  var filteredUsers = dbContext.Users.Where(u => u.IsActive).ToList();
  ```
- Использовать **потоковую обработку** (`IAsyncEnumerable<T>` в EF Core 3.0+):
  ```csharp
  await foreach (var user in dbContext.Users.AsAsyncEnumerable())
      Console.WriteLine(user.Name);
  ```

**Дополнительные вопросы:**
- *Чем `ToList()` отличается от `AsEnumerable().ToList()`?*
  **Ответ:**
  - `ToList()` выполняет запрос на сервере и загружает данные.
  - `AsEnumerable().ToList()` **сначала загружает все данные**, а затем преобразует в список (хуже для производительности).
- *Как загрузить данные порциями без `ToList()`?*
  **Ответ:** Использовать `IAsyncEnumerable<T>` или `DbContext` с отслеживанием изменений:
  ```csharp
  foreach (var user in dbContext.Users.AsNoTracking())
      ProcessUser(user);
  ```

---

### **Вопрос 20: Как работает `AsParallel()` в PLINQ? Когда его использовать?**
**Ответ:**
**PLINQ (Parallel LINQ)** — расширение LINQ для **параллельной обработки** данных.
**`AsParallel()`** преобразует `IEnumerable<T>` в `ParallelQuery<T>`, который:
1. **Разбивает коллекцию на части** (chunking).
2. **Обрабатывает части на нескольких потоках** (из `ThreadPool`).
3. **Объединяет результаты**.

**Пример:**
```csharp
var numbers = Enumerable.Range(1, 1_000_000);
var evenNumbers = numbers.AsParallel().Where(x => x % 2 == 0).ToList();
```

**Когда использовать:**
| **Сценарий**                     | **Подходит ли PLINQ?** | **Причина**                                  |
|----------------------------------|------------------------|---------------------------------------------|
| Большие коллекции (> 10к элементов) | ✅ Да               | Параллелизм ускоряет обработку.            |
| Малые коллекции (< 1к элементов)  | ❌ Нет               | Накладные расходы на распараллеливание.     |
| Операции с состоянием (например, сумма) | ⚠️ Осторожно      | Нужна синхронизация (например, `lock`).    |
| Запросы к БД (`IQueryable<T>`)   | ❌ Нет               | PLINQ работает только с `IEnumerable<T>`.  |
| Операции с побочными эффектами   | ❌ Нет               | Порядок выполнения не гарантирован.        |

**Оптимизации:**
- **`WithDegreeOfParallelism()`**: Ограничить количество потоков.
  ```csharp
  var query = numbers.AsParallel()
      .WithDegreeOfParallelism(4) // Не более 4 потоков
      .Where(x => x % 2 == 0);
  ```
- **`WithExecutionMode()`**: Контролировать порядок выполнения.
  ```csharp
  var query = numbers.AsParallel()
      .WithExecutionMode(ParallelExecutionMode.ForceParallelism)
      .Where(x => x % 2 == 0);
  ```
- **`AsOrdered()` / `AsUnordered()`**: Сохранять или игнорировать порядок.
  ```csharp
  var orderedQuery = numbers.AsParallel().AsOrdered().Where(x => x % 2 == 0);
  ```

**Дополнительные вопросы:**
- *Почему PLINQ может быть медленнее обычного LINQ?*
  **Ответ:**
  - Накладные расходы на **разбиение данных** и **синхронизацию потоков**.
  - Если операция **быстрая** (например, фильтрация по простому условию), выигрыш от параллелизма минимален.
- *Как отладить PLINQ-запрос?*
  **Ответ:** Использовать `AsSequential()` для отладки:
  ```csharp
  var query = numbers.AsParallel().Where(x => x % 2 == 0).AsSequential();
  // Теперь выполняется в одном потоке
  ```

---

## **Заключение**
Эти вопросы охватывают **все ключевые аспекты LINQ**:
1. **Отложенное vs. немедленное выполнение**.
2. **Внутренние механизмы** (итераторы, `yield`, цепочки вызовов).
3. **Производительность и оптимизации** (кэширование, `Span<T>`, ручные циклы).
4. **LINQ to Objects vs. LINQ to SQL**.
5. **Кастомные операторы** (`DistinctBy`, `Batch`).
6. **Параллельная обработка** (PLINQ).

Если нужны ещё более специфичные вопросы (например, по **выражениям LINQ**, **провайдерам IQueryable**, или **оптимизациям для конкретных СУБД**) — дайте знать!