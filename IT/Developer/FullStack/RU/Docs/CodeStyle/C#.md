### **1. Именование**
- **Классы, интерфейсы, структуры, перечисления (enum):** PascalCase
  ```csharp
  public class UserAccount { }
  public interface ILogger { }
  public enum StatusType { Active, Inactive }
  ```

- **Методы, свойства, события:** PascalCase
  ```csharp
  public void CalculateTotal() { }
  public string FirstName { get; set; }
  public event EventHandler OnSave;
  ```

- **Локальные переменные, параметры методов:** camelCase
  ```csharp
  int totalCount = 0;
  public void PrintMessage(string message) { }
  ```

- **Константы:** PascalCase (иногда с префиксом)
  ```csharp
  public const int MaxRetryCount = 3;
  ```

- **Поля (fields):** camelCase с префиксом `_` (если приватные)
  ```csharp
  private int _userId;
  ```

---

### **2. Форматирование**
- **Отступы:** Используйте 4 пробела (не табуляцию).
- **Фигурные скобки:** Всегда на новой строке для классов, методов, циклов и условий.
  ```csharp
  if (condition)
  {
      // код
  }
  ```
- **Пробелы:**
  - После ключевых слов (`if`, `while`, `for`).
  - После запятых в списках параметров.
  ```csharp
  if (x > 0 && y < 10)
  {
      DoSomething(x, y);
  }
  ```

---

### **3. Организация кода**
- **Порядок элементов в классе:**
  1. Поля (fields)
  2. Конструкторы
  3. Свойства
  4. Методы
  5. Вложенные классы/интерфейсы

- **Модификаторы доступа:** Всегда указывайте (`private`, `public`, `protected` и т.д.), даже если это избыточно.

---

### **4. Комментарии**
- Избегайте избыточных комментариев. Код должен быть самодокументируемым.
- Используйте XML-комментарии для публичных API:
  ```csharp
  /// <summary>
  /// Вычисляет сумму двух чисел.
  /// </summary>
  /// <param name="a">Первое число.</param>
  /// <param name="b">Второе число.</param>
  /// <returns>Сумма чисел.</returns>
  public int Add(int a, int b) => a + b;
  ```

---

### **5. Использование `var`**
- Используйте `var` только когда тип переменной очевиден из правой части выражения:
  ```csharp
  var user = new User(); // Хорошо
  var count = GetCount(); // Плохо, если тип GetCount() неочевиден
  ```

---

### **6. Асинхронный код**
- Методы, возвращающие `Task`, должны иметь суффикс `Async`:
  ```csharp
  public async Task<int> LoadDataAsync()
  ```

---

### **7. Обработка исключений**
- Не игнорируйте исключения. Логируйте или обрабатывайте их.
- Используйте специфические типы исключений:
  ```csharp
  try
  {
      // код
  }
  catch (FileNotFoundException ex)
  {
      // обработка
  }
  ```

---

### **8. Использование `using`**
- Для освобождения ресурсов используйте `using`:
  ```csharp
  using (var file = new StreamReader("file.txt"))
  {
      // работа с файлом
  }
  ```

---

### **9. Null-значения**
- Используйте `null`-проверки или оператор `?.` для избежания `NullReferenceException`:
  ```csharp
  string name = user?.Name ?? "Unknown";
  ```

---

### **10. LINQ**
- Используйте LINQ для работы с коллекциями, но избегайте сложных запросов в одной строке.

---

### **Инструменты для проверки стиля**
- **EditorConfig:** Настройте правила стиля для вашей команды.
- **Roslyn Analyzers:** Используйте встроенные или сторонние анализаторы (например, StyleCop).

---