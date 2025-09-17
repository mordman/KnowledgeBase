### **Базовые классы исключений**
1. **`System.Exception`**
   - Базовый класс для всех исключений.
   - Не рекомендуется выбрасывать напрямую, лучше использовать более конкретные типы.

2. **`System.SystemException`**
   - Базовый класс для исключений, генерируемых CLR (Common Language Runtime).
   - Примеры: `NullReferenceException`, `ArgumentException`, `InvalidOperationException`.

3. **`System.ApplicationException`** (устарело, не рекомендуется использовать)
   - Раньше использовался для пользовательских исключений, но теперь Microsoft рекомендует наследовать напрямую от `Exception`.

---

### **Основные встроенные исключения**
- **`ArgumentException`** – неверный аргумент метода.
- **`ArgumentNullException`** – аргумент равен `null`.
- **`ArgumentOutOfRangeException`** – аргумент вне допустимого диапазона.
- **`InvalidOperationException`** – метод вызван в неподходящем состоянии объекта.
- **`NullReferenceException`** – попытка обращения к члену `null`-объекта.
- **`IndexOutOfRangeException`** – индекс массива или коллекции вне диапазона.
- **`KeyNotFoundException`** – ключ не найден в коллекции (например, в `Dictionary`).
- **`NotImplementedException`** – метод не реализован.
- **`NotSupportedException`** – метод не поддерживается.
- **`OverflowException`** – арифметическое переполнение.
- **`DivideByZeroException`** – деление на ноль.
- **`FormatException`** – ошибка формата (например, при парсинге строки).
- **`IOException`** – ошибка ввода-вывода.
- **`FileNotFoundException`** – файл не найден.

---

### **Пользовательские исключения**
Вы можете создавать свои собственные исключения, наследуя их от `Exception` или более конкретного класса:
```csharp
public class MyCustomException : Exception
{
    public MyCustomException(string message) : base(message) { }
}
```

---

### **Пример использования `throw`**
```csharp
if (value == null)
{
    throw new ArgumentNullException(nameof(value), "Значение не может быть null.");
}
```

---

### **Важно**
- Всегда используйте наиболее конкретный тип исключения.
- Избегайте выбрасывания `System.Exception` напрямую.
- Документируйте исключения, которые может выбрасывать ваш метод (с помощью `<exception>` в XML-комментариях).
--- 
В C# **очередность обработки исключений** определяется блоком `try-catch-finally` (или `try-catch` без `finally`). Вот как это работает:

---

### 1. **Порядок выполнения кода**
- Сначала выполняется код внутри блока `try`.
- Если исключение **не возникает**, выполняется блок `finally` (если он есть), а затем код после `try-catch-finally`.
- Если исключение **возникает**, выполнение сразу переходит к блоку `catch`.

---

### 2. **Порядок обработки исключений в `catch`**
- Блоки `catch` проверяются **сверху вниз**.
- Используется **первый подходящий** `catch` (тот, который может обработать тип исключения).
- Если подходящий `catch` не найден, исключение "всплывает" выше по стеку вызовов.

**Пример:**
```csharp
try
{
    // Код, который может выбросить исключение
    int.Parse(null); // Выбросит ArgumentNullException
}
catch (NullReferenceException ex)
{
    // Не сработает, так как исключение другого типа
    Console.WriteLine("NullReferenceException");
}
catch (ArgumentNullException ex)
{
    // Сработает, так как тип совпадает
    Console.WriteLine("ArgumentNullException");
}
catch (Exception ex)
{
    // Сработает, если ни один из предыдущих catch не подошёл
    Console.WriteLine("Общее исключение");
}
finally
{
    // Выполнится в любом случае
    Console.WriteLine("Блок finally");
}
```

---

### 3. **Важные правила**
- **Порядок `catch` важен!** Более конкретные исключения должны идти **раньше** общих. Например:
  ```csharp
  catch (FileNotFoundException ex) { ... } // Конкретное
  catch (IOException ex) { ... }           // Общее
  catch (Exception ex) { ... }              // Самое общее
  ```
  Если поменять местами, компилятор выдаст ошибку.

- **Блок `finally`** выполняется **всегда**, независимо от того, было исключение или нет.

- Если исключение не обработано ни одним `catch`, оно "всплывает" по стеку вызовов, пока не будет обработано или не завершит программу.

---

### 4. **Пример с несколькими `catch` и `finally`**
```csharp
try
{
    int a = 10, b = 0;
    int c = a / b; // Выбросит DivideByZeroException
}
catch (DivideByZeroException ex)
{
    Console.WriteLine("Деление на ноль!");
}
catch (ArithmeticException ex)
{
    Console.WriteLine("Арифметическая ошибка");
}
finally
{
    Console.WriteLine("Это выполнится в любом случае");
}
```

---

### 5. **Что будет, если не обработать исключение?**
Если ни один `catch` не подходит, исключение "всплывает" выше по стеку вызовов. Если его не обработать нигде, программа завершится с ошибкой.

---
Работа с исключениями в **асинхронных методах** (`async/await`) в C# имеет свои особенности. Вот как это работает:

---

### 1. **Исключения в асинхронных методах**
- Если внутри асинхронного метода (`async`) возникает исключение, оно **не выбрасывается сразу** (как в синхронном коде).
- Вместо этого исключение **запоминается** в объекте `Task` (или `Task<T>`), который возвращает метод.
- Исключение будет **выброшено повторно**, когда кто-то попытается получить результат `Task` (например, через `await`, `.Result` или `.Wait()`).

---

### 2. **Обработка исключений с `try-catch`**
- Чтобы поймать исключение из асинхронного метода, используйте `try-catch` **вместе с `await`**:
  ```csharp
  try
  {
      await SomeAsyncMethod(); // Исключение будет выброшено здесь
  }
  catch (Exception ex)
  {
      Console.WriteLine($"Поймано исключение: {ex.Message}");
  }
  ```

- Если не использовать `await`, исключение останется "спрятанным" в `Task` и не будет обработано:
  ```csharp
  var task = SomeAsyncMethod(); // Исключение не выбрасывается здесь
  // Если не использовать await, исключение не будет обработано!
  ```

---

### 3. **Исключения в нескольких асинхронных операциях**
- Если в `Task` возникает несколько исключений (например, в `Task.WhenAll`), они **объединяются** в `AggregateException`.
- При использовании `await` исключения **разворачиваются**: вместо `AggregateException` вы получите первое исключение напрямую.
  ```csharp
  try
  {
      await Task.WhenAll(task1, task2); // Если оба упадут, будет выброшено первое исключение
  }
  catch (Exception ex)
  {
      Console.WriteLine(ex.Message); // Первое исключение
  }
  ```

- Если нужно получить **все исключения**, используйте `.Exception` у `Task`:
  ```csharp
  var task = Task.WhenAll(task1, task2);
  try
  {
      await task;
  }
  catch
  {
      if (task.Exception != null)
      {
          foreach (var ex in task.Exception.InnerExceptions)
          {
              Console.WriteLine(ex.Message); // Все исключения
          }
      }
  }
  ```

---

### 4. **Исключения в `Task.Run`**
- Если исключение возникает в `Task.Run`, оно ведёт себя так же, как и в обычном асинхронном методе:
  ```csharp
  try
  {
      await Task.Run(() => { throw new InvalidOperationException(); });
  }
  catch (InvalidOperationException ex)
  {
      Console.WriteLine("Поймано!");
  }
  ```

---

### 5. **Что будет, если не обработать исключение?**
- Если исключение из `Task` не обработать (например, не использовать `await` и не проверять `.Exception`), оно **не убьёт программу сразу**.
- Однако, если `Task` будет собран сборщиком мусора, исключение **может быть выброшено в финалайзере** и привести к падению программы (в зависимости от версии .NET и конфигурации).

---

### 6. **Пример: полная обработка исключений**
```csharp
async Task ProcessAsync()
{
    try
    {
        await SomeAsyncMethod();
    }
    catch (CustomException ex)
    {
        Console.WriteLine($"Обработано: {ex.Message}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Неожиданное исключение: {ex.Message}");
    }
    finally
    {
        Console.WriteLine("Очистка ресурсов");
    }
}
```

---

### 7. **Важные моменты**
- **Всегда используйте `await`** для обработки исключений из асинхронных методов.
- Если нужно дождаться завершения `Task` без `await`, используйте `try-catch` с `.Wait()` или `.Result`, но это может привести к дедлоку в UI-потоках.
- В `.NET 6+` исключения из `Task` не приводят к падению программы, если их не наблюдать (но это не рекомендуется игнорировать).

---
Вот примеры работы с исключениями в асинхронном коде для `Task.WhenAny`, `ValueTask`, а также с использованием `.Wait()` и `.Result`:

---

## 1. **`Task.WhenAny` и обработка исключений**
`Task.WhenAny` возвращает `Task`, который завершается, когда завершается **любой** из переданных `Task`-ов. Исключения обрабатываются так:

```csharp
async Task ExampleWhenAny()
{
    var task1 = Task.Run(() =>
    {
        Thread.Sleep(1000);
        throw new InvalidOperationException("Ошибка в task1");
    });

    var task2 = Task.Delay(500);

    try
    {
        var completedTask = await Task.WhenAny(task1, task2);
        Console.WriteLine($"Завершился: {completedTask.Id}");

        // Проверяем, не упал ли завершившийся Task
        if (completedTask.IsFaulted)
        {
            Console.WriteLine($"Исключение: {completedTask.Exception?.InnerException?.Message}");
        }
    }
    catch (Exception ex)
    {
        // Сюда попадём, только если await выбросит исключение
        Console.WriteLine($"Поймано: {ex.Message}");
    }
}
```
**Пояснение:**
- `Task.WhenAny` завершится, когда завершится **первый** `Task` (в данном случае `task2`).
- Если завершившийся `Task` упал, его исключение можно получить через `completedTask.Exception`.
- Если использовать `await` для `Task.WhenAny`, исключение не будет выброшено напрямую (только если завершившийся `Task` не был проанализирован).

---

## 2. **`ValueTask` и обработка исключений**
`ValueTask` — это облегчённая версия `Task`, которая может избегать выделения памяти на куче. Исключения обрабатываются аналогично `Task`:

```csharp
async ValueTask<int> DivideAsync(int a, int b)
{
    if (b == 0)
        throw new DivideByZeroException("Деление на ноль!");
    return a / b;
}

async Task ExampleValueTask()
{
    try
    {
        int result = await DivideAsync(10, 0);
        Console.WriteLine(result);
    }
    catch (DivideByZeroException ex)
    {
        Console.WriteLine($"Поймано: {ex.Message}");
    }
}
```
**Пояснение:**
- Исключение из `ValueTask` выбрасывается при `await`, как и в `Task`.
- `ValueTask` не поддерживает множественные исключения (в отличие от `Task.WhenAll`).

---

## 3. **Использование `.Wait()` и `.Result`**
Эти методы **блокируют** текущий поток до завершения `Task` и могут привести к дедлоку в UI-потоках (например, в WPF или ASP.NET). Исключения обрабатываются так:

### Пример с `.Wait()`
```csharp
Task FaultyTask()
{
    return Task.Run(() => throw new InvalidOperationException("Ошибка!"));
}

void ExampleWait()
{
    try
    {
        var task = FaultyTask();
        task.Wait(); // Блокирует поток и выбрасывает AggregateException
    }
    catch (AggregateException ae)
    {
        foreach (var ex in ae.InnerExceptions)
        {
            Console.WriteLine($"Исключение: {ex.Message}");
        }
    }
}
```
**Пояснение:**
- `.Wait()` выбрасывает `AggregateException`, даже если в `Task` было одно исключение.

---

### Пример с `.Result`
```csharp
void ExampleResult()
{
    try
    {
        var task = FaultyTask();
        var result = task.Result; // Блокирует поток и выбрасывает AggregateException
    }
    catch (AggregateException ae)
    {
        Console.WriteLine($"Исключение: {ae.InnerException?.Message}");
    }
}
```
**Пояснение:**
- `.Result` аналогично `.Wait()` выбрасывает `AggregateException`.

---

### ⚠️ **Важно!**
- **Не используйте `.Wait()` или `.Result` в UI-потоках** (например, в WPF, WinForms, ASP.NET), так как это может привести к дедлоку.
- Предпочитайте `await` для асинхронного кода.
- Если нужно дождаться `Task` синхронно, используйте `task.GetAwaiter().GetResult()` (выбросит оригинальное исключение, а не `AggregateException`).

---
В блоке `catch` оператор `throw` используется для **повторного выбрасывания исключения** после его обработки (или частичной обработки). Это нужно в следующих случаях:

---

### 1. **Логгирование с повторным выбрасыванием**
Если вы хотите **залоггировать исключение**, но не обрабатывать его полностью, а передать дальше по стеку вызовов:
```csharp
try
{
    // Код, который может выбросить исключение
    int.Parse(null);
}
catch (Exception ex)
{
    Console.WriteLine($"Ошибка: {ex.Message}"); // Логгируем
    throw; // Повторно выбрасываем то же исключение
}
```
- `throw;` (без указания исключения) **сохраняет исходный стек вызовов** (stack trace), что важно для отладки.

---

### 2. **Обёртывание исключения в новое**
Если вы хотите **добавить контекст** к исключению, но сохранить исходную информацию:
```csharp
try
{
    // Код, который может выбросить исключение
    File.ReadAllText("nonexistent.txt");
}
catch (FileNotFoundException ex)
{
    throw new ApplicationException("Не удалось загрузить конфигурацию.", ex);
    // Новое исключение с исходным как InnerException
}
```
- Здесь `ex` становится `InnerException` нового исключения.

---

### 3. **Частичная обработка с повторным выбрасыванием**
Если вы хотите **частично обработать исключение** (например, освободить ресурсы), но не гасить его полностью:
```csharp
try
{
    // Работа с файлом
}
catch (IOException ex)
{
    Console.WriteLine("Ошибка ввода-вывода, очищаем ресурсы...");
    // Освобождаем ресурсы
    throw; // Повторно выбрасываем, чтобы вызывающий код тоже отреагировал
}
```

---

### 4. **Разница между `throw;` и `throw ex;`**
- **`throw;`** — повторно выбрасывает **исходное исключение** с сохранением стека вызовов.
- **`throw ex;`** — выбрасывает **новое исключение** (теряется исходный стек вызовов, что усложняет отладку).
  ```csharp
  catch (Exception ex)
  {
      // ❌ Плохо: теряется стек вызовов
      throw ex;

      // ✅ Хорошо: сохраняется стек вызовов
      throw;
  }
  ```

---

### 5. **Когда не нужно повторно выбрасывать**
- Если исключение **полностью обработано** в `catch` и дальнейшая обработка не требуется.
- Если вы хотите **заменить исключение** на более подходящее (например, преобразовать `SqlException` в `DataAccessException`).

---

### Пример: Полный сценарий
```csharp
try
{
    // Код, который может выбросить исключение
    var data = LoadData();
}
catch (SqlException ex)
{
    Console.WriteLine($"Ошибка БД: {ex.Message}");
    throw; // Повторно выбрасываем, чтобы вызывающий код тоже обработал
}
catch (Exception ex)
{
    Console.WriteLine($"Неожиданная ошибка: {ex.Message}");
    throw new ApplicationException("Критическая ошибка приложения.", ex);
}
```

---

### Вывод
- `throw;` в `catch` используется для **передачи исключения дальше** после логгирования или частичной обработки.
- Всегда предпочитайте `throw;` вместо `throw ex;`, чтобы сохранить стек вызовов.
- Если нужно добавить контекст, используйте конструктор нового исключения с параметром `innerException`.