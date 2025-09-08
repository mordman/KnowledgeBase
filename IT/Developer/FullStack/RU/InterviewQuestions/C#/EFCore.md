# Base

### **1. Что такое Entity Framework Core?**
**Ответ:**
Entity Framework Core (EF Core) — это ORM-фреймворк для работы с базами данных в .NET. Он поддерживает LINQ, миграции, отслеживание изменений и работу с разными СУБД.

**Пример:**
```csharp
// Пример простого запроса
var users = dbContext.Users.Where(u => u.Age > 18).ToList();
```

---

### **2. В чём разница между EF Core и EF6?**
**Ответ:**
EF Core — кроссплатформенный, модульный, оптимизирован для облачных приложений. EF6 работает только на Windows и имеет больше функций (например, EDMX).

---

### **3. Что такое DbContext и зачем он нужен?**
**Ответ:**
`DbContext` — основной класс для работы с базой данных. Управляет подключением, отслеживанием изменений и транзакциями.

**Пример:**
```csharp
public class AppDbContext : DbContext
{
    public DbSet<User> Users { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer("Server=...;Database=TestDb;Trusted_Connection=True;");
    }
}
```

---

### **4. Как работает отслеживание изменений (Change Tracking) в EF Core?**
**Ответ:**
EF Core отслеживает изменения сущностей, загруженных через `DbContext`. При вызове `SaveChanges()` генерируются SQL-запросы для обновления данных.

**Пример:**
```csharp
var user = dbContext.Users.First(u => u.Id == 1);
user.Name = "New Name";
dbContext.SaveChanges(); // Обновляет запись в базе
```

---

### **5. Что такое миграции (Migrations) и как они работают?**
**Ответ:**
Миграции позволяют управлять изменениями схемы базы данных через код.

**Пример:**
```bash
# Команды в Package Manager Console
Add-Migration InitialCreate
Update-Database
```

---

### **6. Какие подходы к загрузке данных поддерживает EF Core?**
**Ответ:**
- **Жадная загрузка:** `Include()`/`ThenInclude()`.
- **Ленивая загрузка:** через прокси-классы.
- **Явная загрузка:** `Load()`.

**Пример (жадная загрузка):**
```csharp
var users = dbContext.Users.Include(u => u.Orders).ToList();
```

---

### **7. Как оптимизировать производительность запросов в EF Core?**
**Ответ:**
- Использовать `AsNoTracking()` для запросов только на чтение.
- Проецировать данные с помощью `Select()`.

**Пример:**
```csharp
var userNames = dbContext.Users
    .Where(u => u.Age > 18)
    .Select(u => u.Name)
    .AsNoTracking()
    .ToList();
```

---

### **8. Что такое Shadow Properties?**
**Ответ:**
Shadow Properties — свойства сущностей, не объявленные в классе, но существующие в модели.

**Пример:**
```csharp
modelBuilder.Entity<User>().Property<DateTime>("CreatedDate");
```

---

### **9. Как реализовать транзакции в EF Core?**
**Ответ:**
Транзакции управляются через `DbContext.Database`.

**Пример:**
```csharp
using var transaction = dbContext.Database.BeginTransaction();
try
{
    dbContext.Users.Add(new User { Name = "Alice" });
    dbContext.SaveChanges();
    transaction.Commit();
}
catch
{
    transaction.Rollback();
}
```

---

### **10. Что такое Value Objects и как их использовать?**
**Ответ:**
Value Objects — неизменяемые объекты, представляющие значение (например, `Address`).

**Пример:**
```csharp
modelBuilder.Entity<User>().OwnsOne(u => u.Address);
```

---

### **11. Как работать с JSON-полями в EF Core?**
**Ответ:**
Использовать конвертеры для сериализации объектов в JSON.

**Пример:**
```csharp
modelBuilder.Entity<User>()
    .Property(u => u.Settings)
    .HasConversion(
        v => JsonSerializer.Serialize(v, null),
        v => JsonSerializer.Deserialize<Dictionary<string, string>>(v, null));
```

---

### **12. Что такое Global Query Filters?**
**Ответ:**
Global Query Filters — условия, автоматически применяемые ко всем запросам.

**Пример:**
```csharp
modelBuilder.Entity<User>().HasQueryFilter(u => !u.IsDeleted);
```

---

### **13. Как реализовать многопоточность с EF Core?**
**Ответ:**
`DbContext` не потокобезопасен. Для многопоточности создавать новый экземпляр `DbContext` на поток.

---

### **14. Что такое Raw SQL и когда его использовать?**
**Ответ:**
Raw SQL позволяет выполнять сырые SQL-запросы.

**Пример:**
```csharp
var users = dbContext.Users.FromSqlRaw("SELECT * FROM Users WHERE Age > {0}", 18).ToList();
```

---

### **15. Как настроить связь "многие ко многим" без сущности-посредника?**
**Ответ:**
В EF Core 5+ связь "многие ко многим" настраивается без явной сущности.

**Пример:**
```csharp
modelBuilder.Entity<User>()
    .HasMany(u => u.Roles)
    .WithMany(r => r.Users);
```

---

### **16. Что такое TPH, TPT, TPC в EF Core?**
**Ответ:**
Стратегии наследования:
- **TPH:** одна таблица для всей иерархии.
- **TPT:** отдельная таблица для каждого типа.
- **TPC:** таблица только для конкретных типов.

**Пример (TPH):**
```csharp
modelBuilder.Entity<User>().ToTable("Users");
modelBuilder.Entity<Admin>().ToTable("Users"); // Та же таблица
```

---

### **17. Как реализовать soft delete?**
**Ответ:**
Добавить поле `IsDeleted` и глобальный фильтр.

**Пример:**
```csharp
modelBuilder.Entity<User>().HasQueryFilter(u => !u.IsDeleted);
// При удалении:
user.IsDeleted = true;
dbContext.SaveChanges();
```

---

### **18. Как работать с составными ключами?**
**Ответ:**
Составные ключи настраиваются через Fluent API.

**Пример:**
```csharp
modelBuilder.Entity<UserRole>()
    .HasKey(ur => new { ur.UserId, ur.RoleId });
```

---

### **19. Что такое Interceptors в EF Core?**
**Ответ:**
Interceptors позволяют перехватывать и модифицировать операции EF Core.

**Пример:**
```csharp
public class MyInterceptor : DbCommandInterceptor
{
    public override InterceptionResult<DbDataReader> ReaderExecuting(
        DbCommand command,
        CommandEventData eventData,
        InterceptionResult<DbDataReader> result)
    {
        Console.WriteLine(command.CommandText);
        return result;
    }
}
// Регистрация:
optionsBuilder.AddInterceptors(new MyInterceptor());
```

---

### **20. Как тестировать код с EF Core?**
**Ответ:**
Использовать **In-Memory Provider** для юнит-тестов.

**Пример:**
```csharp
var options = new DbContextOptionsBuilder<AppDbContext>()
    .UseInMemoryDatabase(databaseName: "TestDb")
    .Options;
using var context = new AppDbContext(options);
// Тесты...
```

---

# Joins

### **1. Как выполнить INNER JOIN в EF Core?**
**Ответ:**
`INNER JOIN` возвращает только те записи, для которых есть совпадения в обеих таблицах. В EF Core это реализуется через LINQ-метод `Join` или навигационные свойства.

**Пример с `Join`:**
```csharp
var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, order) => new { User = user, Order = order }
    )
    .ToList();
```

**Пример с навигационными свойствами:**
```csharp
var query = dbContext.Users
    .SelectMany(
        user => user.Orders,
        (user, order) => new { User = user, Order = order }
    )
    .ToList();
```

---

### **2. Как выполнить LEFT JOIN (или LEFT OUTER JOIN) в EF Core?**
**Ответ:**
`LEFT JOIN` возвращает все записи из левой таблицы и совпадающие записи из правой. В EF Core используется метод `GroupJoin` + `DefaultIfEmpty`.

**Пример:**
```csharp
var query = dbContext.Users
    .GroupJoin(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, orders) => new { User = user, Orders = orders }
    )
    .SelectMany(
        x => x.Orders.DefaultIfEmpty(),
        (x, order) => new { User = x.User, Order = order }
    )
    .ToList();
```

**Упрощённый вариант (с навигационными свойствами):**
```csharp
var query = dbContext.Users
    .Select(user => new
    {
        User = user,
        Order = user.Orders.FirstOrDefault() // или DefaultIfEmpty()
    })
    .ToList();
```

---

### **3. Как выполнить RIGHT JOIN в EF Core?**
**Ответ:**
`RIGHT JOIN` возвращает все записи из правой таблицы и совпадающие из левой. В EF Core это реализуется через `GroupJoin` с перестановкой таблиц.

**Пример:**
```csharp
var query = dbContext.Orders
    .GroupJoin(
        dbContext.Users,
        order => order.UserId,
        user => user.Id,
        (order, users) => new { Order = order, Users = users }
    )
    .SelectMany(
        x => x.Users.DefaultIfEmpty(),
        (x, user) => new { Order = x.Order, User = user }
    )
    .ToList();
```

---

### **4. Как выполнить FULL JOIN (или FULL OUTER JOIN) в EF Core?**
**Ответ:**
`FULL JOIN` возвращает все записи из обеих таблиц, с `NULL` для несовпадающих строк. В EF Core это реализуется через объединение `LEFT JOIN` и `RIGHT JOIN`.

**Пример:**
```csharp
var leftJoin = dbContext.Users
    .GroupJoin(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, orders) => new { User = user, Orders = orders }
    )
    .SelectMany(
        x => x.Orders.DefaultIfEmpty(),
        (x, order) => new { x.User, Order }
    );

var rightJoin = dbContext.Orders
    .GroupJoin(
        dbContext.Users,
        order => order.UserId,
        user => user.Id,
        (order, users) => new { Order = order, Users = users }
    )
    .SelectMany(
        x => x.Users.DefaultIfEmpty(),
        (x, user) => new { User = user, x.Order }
    );

var fullJoin = leftJoin.Union(rightJoin).ToList();
```

---

### **5. Как выполнить CROSS JOIN в EF Core?**
**Ответ:**
`CROSS JOIN` возвращает декартово произведение двух таблиц. В EF Core это реализуется через вложенные циклы `SelectMany`.

**Пример:**
```csharp
var query = dbContext.Users
    .SelectMany(
        user => dbContext.Orders,
        (user, order) => new { User = user, Order = order }
    )
    .ToList();
```

---

### **6. Как выполнить соединение с несколькими условиями?**
**Ответ:**
Можно использовать анонимные типы для соединения по нескольким полям.

**Пример:**
```csharp
var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => new { user.Id, user.DepartmentId },
        order => new { Id = order.UserId, DepartmentId = order.DepartmentId },
        (user, order) => new { User = user, Order = order }
    )
    .ToList();
```

---

### **7. Как выполнить соединение с фильтрацией?**
**Ответ:**
Фильтрацию можно применять как до, так и после соединения.

**Пример (фильтрация после соединения):**
```csharp
var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, order) => new { User = user, Order = order }
    )
    .Where(x => x.Order.Amount > 1000)
    .ToList();
```

---

### **8. Как выполнить соединение с агрегацией?**
**Ответ:**
Можно комбинировать соединения с агрегирующими функциями (`GroupBy`, `Sum`, `Count` и др.).

**Пример:**
```csharp
var query = dbContext.Users
    .GroupJoin(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, orders) => new
        {
            User = user,
            TotalAmount = orders.Sum(o => o.Amount)
        }
    )
    .ToList();
```

---
Вот ещё **10 вопросов** по **Entity Framework Core**, включая работу с соединениями, оптимизацию и специфические сценарии, с примерами кода:

---

### **9. Как выполнить соединение с подзапросами (Subquery Join)?**
**Ответ:**
Иногда нужно соединить таблицу с результатом подзапроса. В EF Core это делается через `Join` с предварительно сформированным подзапросом.

**Пример:**
```csharp
var activeUsers = dbContext.Users.Where(u => u.IsActive);
var query = dbContext.Orders
    .Join(
        activeUsers,
        order => order.UserId,
        user => user.Id,
        (order, user) => new { Order = order, User = user }
    )
    .ToList();
```

---

### **10. Как выполнить соединение с группировкой (Group Join)?**
**Ответ:**
`Group Join` позволяет сгруппировать данные из связанной таблицы. Это полезно для создания иерархических структур.

**Пример:**
```csharp
var query = dbContext.Users
    .GroupJoin(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, orders) => new { User = user, Orders = orders.ToList() }
    )
    .ToList();
```

---

### **11. Как выполнить соединение с несколькими таблицами?**
**Ответ:**
Можно соединять более двух таблиц, последовательно применяя `Join`.

**Пример:**
```csharp
var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, order) => new { User = user, Order = order }
    )
    .Join(
        dbContext.Products,
        uo => uo.Order.ProductId,
        product => product.Id,
        (uo, product) => new { uo.User, uo.Order, Product = product }
    )
    .ToList();
```

---

### **12. Как выполнить соединение с использованием навигационных свойств и фильтрацией?**
**Ответ:**
Можно использовать навигационные свойства и фильтровать связанные данные.

**Пример:**
```csharp
var query = dbContext.Users
    .Where(user => user.Orders.Any(order => order.Amount > 1000))
    .Select(user => new
    {
        User = user,
        ExpensiveOrders = user.Orders.Where(order => order.Amount > 1000)
    })
    .ToList();
```

---

### **13. Как выполнить соединение с использованием Raw SQL и LINQ?**
**Ответ:**
Можно комбинировать Raw SQL и LINQ для сложных запросов.

**Пример:**
```csharp
var userIds = dbContext.Users
    .FromSqlRaw("SELECT * FROM Users WHERE IsActive = 1")
    .Select(u => u.Id)
    .ToList();

var query = dbContext.Orders
    .Where(order => userIds.Contains(order.UserId))
    .ToList();
```

---

### **14. Как выполнить соединение с использованием временных таблиц?**
**Ответ:**
В EF Core нет прямой поддержки временных таблиц, но можно использовать Raw SQL для их создания и последующего соединения.

**Пример:**
```csharp
dbContext.Database.ExecuteSqlRaw("CREATE TEMPORARY TABLE TempActiveUsers AS SELECT * FROM Users WHERE IsActive = 1");

var query = dbContext.Orders
    .FromSqlRaw("SELECT * FROM Orders INNER JOIN TempActiveUsers ON Orders.UserId = TempActiveUsers.Id")
    .ToList();
```

---

### **15. Как выполнить соединение с использованием анонимных типов и проекции?**
**Ответ:**
Можно использовать анонимные типы для проекции данных после соединения.

**Пример:**
```csharp
var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, order) => new
        {
            UserName = user.Name,
            OrderAmount = order.Amount,
            OrderDate = order.Date
        }
    )
    .ToList();
```

---

### **16. Как выполнить соединение с использованием внешних ключей и фильтрацией?**
**Ответ:**
Можно фильтровать данные по внешним ключам и соединять таблицы.

**Пример:**
```csharp
var query = dbContext.Users
    .Where(user => user.DepartmentId == 1)
    .Join(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, order) => new { User = user, Order = order }
    )
    .ToList();
```

---

### **17. Как выполнить соединение с использованием агрегатных функций?**
**Ответ:**
Можно соединять таблицы и применять агрегатные функции, такие как `Sum`, `Count`, `Average`.

**Пример:**
```csharp
var query = dbContext.Users
    .GroupJoin(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, orders) => new
        {
            User = user,
            TotalOrders = orders.Count(),
            TotalAmount = orders.Sum(o => o.Amount)
        }
    )
    .ToList();
```

---

### **18. Как выполнить соединение с использованием сложных условий?**
**Ответ:**
Можно использовать сложные условия в соединениях, например, с проверкой диапазона дат.

**Пример:**
```csharp
var startDate = new DateTime(2023, 1, 1);
var endDate = new DateTime(2023, 12, 31);

var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => user.Id,
        order => order.UserId,
        (user, order) => new { User = user, Order = order }
    )
    .Where(joined => joined.Order.Date >= startDate && joined.Order.Date <= endDate)
    .ToList();
```

---

### **19. Как выполнить соединение с использованием подзапроса в SELECT?**
**Ответ:**
Можно использовать подзапросы в `Select` для получения дополнительных данных.

**Пример:**
```csharp
var query = dbContext.Users
    .Select(user => new
    {
        User = user,
        LastOrderAmount = dbContext.Orders
            .Where(order => order.UserId == user.Id)
            .OrderByDescending(order => order.Date)
            .Select(order => order.Amount)
            .FirstOrDefault()
    })
    .ToList();
```

---

### **20. Как выполнить соединение с использованием нескольких условий и сортировки?**
**Ответ:**
Можно соединять таблицы по нескольким условиям и применять сортировку.

**Пример:**
```csharp
var query = dbContext.Users
    .Join(
        dbContext.Orders,
        user => new { user.Id, user.DepartmentId },
        order => new { Id = order.UserId, DepartmentId = order.DepartmentId },
        (user, order) => new { User = user, Order = order }
    )
    .OrderBy(joined => joined.Order.Date)
    .ThenByDescending(joined => joined.Order.Amount)
    .ToList();
```

---