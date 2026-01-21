**Цель:**  
Multiton — это порождающий паттерн проектирования, который **гарантирует наличие ограниченного набора экземпляров класса**, каждый из которых ассоциирован с уникальным ключом. Это обобщение Singleton'а: вместо одного глобального экземпляра — несколько, управляемых централизованно.

Typical use cases: кэширование по ключу, менеджеры ресурсов (например, по имени БД), пулы объектов с именованными экземплярами.

---

**Пример (C#):**

```csharp
public class Multiton
{
    private static readonly Dictionary<string, Multiton> _instances = new();
    private static readonly object _lock = new();

    private Multiton() { }

    public static Multiton GetInstance(string key)
    {
        if (!_instances.ContainsKey(key))
        {
            lock (_lock)
            {
                // Проверка внутри блокировки (double-checked locking)
                if (!_instances.ContainsKey(key))
                {
                    _instances[key] = new Multiton();
                }
            }
        }
        return _instances[key];
    }

    // Пример метода для демонстрации
    public void DoSomething(string context) =>
        Console.WriteLine($"Multiton instance '{context}' is working.");
}

// Использование
var db1 = Multiton.GetInstance("DatabaseA");
var db2 = Multiton.GetInstance("DatabaseB");
var db1Again = Multiton.GetInstance("DatabaseA");

Console.WriteLine(ReferenceEquals(db1, db1Again)); // True
Console.WriteLine(ReferenceEquals(db1, db2));      // False
```

> 💡 В реальных сценариях `Multiton` часто параметризуется типом (`Multiton<TKey, TValue>`) или используется с фабриками. Однако будьте осторожны: глобальное состояние усложняет тестирование.

---

**Антипаттерн:**  
- **Ручное управление множеством синглтонов** через статические поля (`public static DbManager DbA; public static DbManager DbB; ...`), что не масштабируется.
- **Использование обычного Dictionary без потокобезопасности** в многопоточной среде → гонки данных, дублирование экземпляров.
- **Злоупотребление глобальным состоянием**: Multiton скрывает зависимости и нарушает принцип инверсии зависимостей (DIP).

---

**Схема (Mermaid):**

```mermaid
classDiagram
    class Multiton {
        <<singleton-like>>
        -{static} _instances: Dictionary~string, Multiton~
        -{static} _lock: object
        -Multiton()
        +{static} GetInstance(key: string): Multiton
        +DoSomething(context: string)
    }

    Multiton ..> Multiton : returns cached instance by key
```

```
    note right of Multiton::GetInstance
        Возвращает существующий экземпляр
        по ключу или создаёт новый.
        Гарантирует только один экземпляр
        на каждый уникальный ключ.
    end note

    note right of Multiton::_instances
        Хранит все экземпляры.
        Ключ — строка (или обобщённый тип).
    end note
```