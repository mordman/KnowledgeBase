### **1. Структура проекта**


## Оглавление
  - [**1. Структура проекта**](#1-структура-проекта)
  - [**2. Установка дополнительных NuGet-пакетов**](#2-установка-дополнительных-nuget-пакетов)
  - [**3. Код**](#3-код)
    - [**AppDbContext.cs** (добавлено логгирование)](#appdbcontextcs-добавлено-логгирование)
    - [**IPatientService.cs** (без изменений)](#ipatientservicecs-без-изменений)
    - [**PatientService.cs** (добавлена обработка ошибок и логгирование)](#patientservicecs-добавлена-обработка-ошибок-и-логгирование)
    - [**Program.cs** (добавлены логгирование и обработка миграций)](#programcs-добавлены-логгирование-и-обработка-миграций)
  - [**4. Создание и применение миграций**](#4-создание-и-применение-миграций)
    - [**Создание миграции**](#создание-миграции)
    - [**Применение миграции**](#применение-миграции)
  - [**5. Логирование**](#5-логирование)
  - [**6. Итог**](#6-итог)
- [**1. Что такое Scoped?**](#1-что-такое-scoped)
- [**2. Почему Scoped для `IPatientService`?**](#2-почему-scoped-для-ipatientservice)
  - [**А. Работа с Entity Framework Core**](#а-работа-с-entity-framework-core)
  - [**Б. Пример проблемы с Singleton**](#б-пример-проблемы-с-singleton)
  - [**В. Пример корректной регистрации**](#в-пример-корректной-регистрации)
- [**3. Почему не Transient?**](#3-почему-не-transient)
- [**4. Как это работает в консольном приложении?**](#4-как-это-работает-в-консольном-приложении)
- [**5. Итог: Почему Scoped?**](#5-итог-почему-scoped)
  - [**Вывод**](#вывод)

  - [**1. Структура проекта**](#1-структура-проекта)
  - [**2. Установка дополнительных NuGet-пакетов**](#2-установка-дополнительных-nuget-пакетов)
  - [**3. Код**](#3-код)
    - [**AppDbContext.cs** (добавлено логгирование)](#appdbcontextcs-добавлено-логгирование)
    - [**IPatientService.cs** (без изменений)](#ipatientservicecs-без-изменений)
    - [**PatientService.cs** (добавлена обработка ошибок и логгирование)](#patientservicecs-добавлена-обработка-ошибок-и-логгирование)
    - [**Program.cs** (добавлены логгирование и обработка миграций)](#programcs-добавлены-логгирование-и-обработка-миграций)
  - [**4. Создание и применение миграций**](#4-создание-и-применение-миграций)
    - [**Создание миграции**](#создание-миграции)
    - [**Применение миграции**](#применение-миграции)
  - [**5. Логирование**](#5-логирование)
  - [**6. Итог**](#6-итог)
  - [**А. Работа с Entity Framework Core**](#а-работа-с-entity-framework-core)
  - [**Б. Пример проблемы с Singleton**](#б-пример-проблемы-с-singleton)
  - [**В. Пример корректной регистрации**](#в-пример-корректной-регистрации)
  - [**Вывод**](#вывод)
```
PatientConsoleApp/
├── Models/
│   └── Patient.cs
├── Services/
│   ├── IPatientService.cs
│   └── PatientService.cs
├── Data/
│   ├── AppDbContext.cs
│   └── PatientRepository.cs
├── Migrations/          # Папка для миграций (создастся автоматически)
└── Program.cs
```

---

### **2. Установка дополнительных NuGet-пакетов**
```bash
dotnet add package Microsoft.Extensions.Logging.Console
dotnet add package Microsoft.EntityFrameworkCore.Tools
```

---

### **3. Код**

#### **AppDbContext.cs** (добавлено логгирование)
```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using PatientConsoleApp.Models;

namespace PatientConsoleApp.Data
{
    public class AppDbContext : DbContext
    {
        private readonly ILogger<AppDbContext> _logger;

        public DbSet<Patient> Patients { get; set; }

        public AppDbContext(
            DbContextOptions<AppDbContext> options,
            ILogger<AppDbContext> logger)
            : base(options)
        {
            _logger = logger;
            _logger.LogInformation("Инициализация контекста БД.");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Patient>().HasData(
                new Patient { Id = 1, FullName = "Иванов Иван Иванович", Age = 35, Diagnosis = "Грипп" },
                new Patient { Id = 2, FullName = "Петрова Мария Сергеевна", Age = 28, Diagnosis = "Ангина" }
            );
            _logger.LogInformation("Применены начальные данные.");
        }
    }
}
```

---

#### **IPatientService.cs** (без изменений)
```csharp
using PatientConsoleApp.Models;

namespace PatientConsoleApp.Services
{
    public interface IPatientService
    {
        Task AddPatientAsync(Patient patient);
        Task<IEnumerable<Patient>> GetAllPatientsAsync();
        Task<Patient?> GetPatientByIdAsync(int id);
    }
}
```

---

#### **PatientService.cs** (добавлена обработка ошибок и логгирование)
```csharp
using Microsoft.Extensions.Logging;
using PatientConsoleApp.Data;
using PatientConsoleApp.Models;

namespace PatientConsoleApp.Services
{
    public class PatientService : IPatientService
    {
        private readonly AppDbContext _context;
        private readonly ILogger<PatientService> _logger;

        public PatientService(
            AppDbContext context,
            ILogger<PatientService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task AddPatientAsync(Patient patient)
        {
            try
            {
                _context.Patients.Add(patient);
                await _context.SaveChangesAsync();
                _logger.LogInformation("Пациент {FullName} добавлен.", patient.FullName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при добавлении пациента {FullName}.", patient.FullName);
                throw;
            }
        }

        public async Task<IEnumerable<Patient>> GetAllPatientsAsync()
        {
            try
            {
                var patients = await Task.FromResult(_context.Patients.ToList());
                _logger.LogInformation("Получен список из {Count} пациентов.", patients.Count);
                return patients;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при получении списка пациентов.");
                throw;
            }
        }

        public async Task<Patient?> GetPatientByIdAsync(int id)
        {
            try
            {
                var patient = await _context.Patients.FindAsync(id);
                if (patient != null)
                    _logger.LogInformation("Найден пациент с ID {Id}: {FullName}.", id, patient.FullName);
                else
                    _logger.LogWarning("Пациент с ID {Id} не найден.", id);
                return patient;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при поиске пациента с ID {Id}.", id);
                throw;
            }
        }
    }
}
```

---

#### **Program.cs** (добавлены логгирование и обработка миграций)
```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using PatientConsoleApp.Data;
using PatientConsoleApp.Models;
using PatientConsoleApp.Services;

// Настройка DI
var services = new ServiceCollection();

// Настройка логгирования в консоль
services.AddLogging(configure => configure.AddConsole());

// Регистрация контекста БД (SQLite)
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=patients.db")
           .EnableSensitiveDataLogging() // Логирование SQL-запросов (только для разработки!)
           .LogTo(Console.WriteLine, LogLevel.Information) // Логирование в консоль
);

// Регистрация сервиса
services.AddScoped<IPatientService, PatientService>();

// Построение провайдера сервисов
var serviceProvider = services.BuildServiceProvider();

// Применение миграций (если нужно)
await ApplyMigrationsAsync(serviceProvider);

// Получение сервиса и логгера
var patientService = serviceProvider.GetRequiredService<IPatientService>();
var logger = serviceProvider.GetRequiredService<ILogger<Program>>();

async Task ApplyMigrationsAsync(IServiceProvider serviceProvider)
{
    using var scope = serviceProvider.CreateScope();
    var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    logger.LogInformation("Применение миграций...");
    await dbContext.Database.MigrateAsync();
    logger.LogInformation("Миграции применены.");
}

// Пример асинхронного использования
async Task RunAppAsync()
{
    try
    {
        // Добавим нового пациента
        var newPatient = new Patient
        {
            FullName = "Сидоров Алексей Петрович",
            Age = 42,
            Diagnosis = "Гипертония"
        };
        await patientService.AddPatientAsync(newPatient);

        // Получим всех пациентов
        var patients = await patientService.GetAllPatientsAsync();
        logger.LogInformation("\nСписок пациентов:");
        foreach (var patient in patients)
        {
            logger.LogInformation($"{patient.Id}: {patient.FullName}, {patient.Age}, {patient.Diagnosis}");
        }

        // Получим пациента по ID
        var patientById = await patientService.GetPatientByIdAsync(1);
        logger.LogInformation($"\nПациент с ID 1: {patientById?.FullName}");
    }
    catch (Exception ex)
    {
        logger.LogCritical(ex, "Произошла критичная ошибка в приложении.");
    }
}

// Запуск асинхронного метода
await RunAppAsync();
```

---

### **4. Создание и применение миграций**

#### **Создание миграции**
```bash
dotnet ef migrations add InitialCreate
```
Эта команда создаст папку `Migrations` с файлами миграции.

#### **Применение миграции**
Миграция применяется автоматически при запуске `dotnet run` (см. метод `ApplyMigrationsAsync` в `Program.cs`).

---

### **5. Логирование**
Теперь все важные события (добавление пациента, ошибки, SQL-запросы) логируются в консоль. Пример вывода:
```
info: PatientConsoleApp.Data.AppDbContext[0]
      Инициализация контекста БД.
info: PatientConsoleApp.Data.AppDbContext[0]
      Применены начальные данные.
info: PatientConsoleApp.Program[0]
      Применение миграций...
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (1ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      SELECT COUNT(*) FROM "sqlite_master" WHERE "type" = 'table' AND "name" = '__EFMigrationsHistory';
info: PatientConsoleApp.Program[0]
      Миграции применены.
info: PatientConsoleApp.Services.PatientService[0]
      Пациент Сидоров Алексей Петрович добавлен.
info: PatientConsoleApp.Services.PatientService[0]
      Получен список из 3 пациентов.
info: PatientConsoleApp.Program[0]
      Список пациентов:
info: PatientConsoleApp.Program[0]
      1: Иванов Иван Иванович, 35, Грипп
info: PatientConsoleApp.Program[0]
      2: Петрова Мария Сергеевна, 28, Ангина
info: PatientConsoleApp.Program[0]
      3: Сидоров Алексей Петрович, 42, Гипертония
info: PatientConsoleApp.Services.PatientService[0]
      Найден пациент с ID 1: Иванов Иван Иванович.
info: PatientConsoleApp.Program[0]
      Пациент с ID 1: Иванов Иван Иванович
```

---

### **6. Итог**
- **Логгирование**: Все важные события и ошибки логируются.
- **Миграции**: Схема БД управляется через EF Core Migrations.
- **Обработка ошибок**: Все асинхронные операции обёрнуты в `try-catch`.
- **DI**: Все зависимости корректно зарегистрированы и внедрены.

---
В контексте **Microsoft.Extensions.DependencyInjection** (и вообще в .NET) **`Scoped`** — это один из трёх основных **жизненных циклов** (lifetimes) зависимостей, наряду с **`Transient`** и **`Singleton`**. Давай разберём, почему в примере с базой данных пациентов я использовал именно **`Scoped`** для регистрации `IPatientService` и почему это важно.

---

## **1. Что такое Scoped?**
**Scoped** означает, что **один экземпляр зависимости создаётся на один "scope"** (обычно — на один HTTP-запрос в веб-приложениях или на одну "операцию" в консольных/десктопных приложениях).
- В **ASP.NET Core** `Scoped` привязан к **HTTP-запросу**: все сервисы, зарегистрированные как `Scoped`, будут одинаковыми в рамках одного запроса, но разными для разных запросов.
- В **консольных приложениях** `Scoped` обычно привязан к **одному "блоку работы"** (например, к одному вызову `using var scope = serviceProvider.CreateScope()`).

---

## **2. Почему Scoped для `IPatientService`?**

### **А. Работа с Entity Framework Core**
- **`AppDbContext`** (контекст EF Core) **всегда регистрируется как `Scoped`** (или `Transient` в редких случаях).
  **Почему?**
  - Контекст EF Core **не потокобезопасен** (не поддерживает многопоточный доступ).
  - Контекст **отслеживает изменения** (change tracking) в рамках одной "операции" (например, одного HTTP-запроса или одной транзакции).
  - Если использовать `Singleton`, контекст будет **разделяться между разными запросами**, что приведёт к **конфликтам, утечкам памяти и ошибкам**.

- **`IPatientService` зависит от `AppDbContext`**, поэтому **должен иметь такой же или более короткий жизненный цикл**.
  - Если зарегистрировать `IPatientService` как `Singleton`, а `AppDbContext` как `Scoped`, то:
    - `IPatientService` (Singleton) **попытается использовать один и тот же `AppDbContext` для разных запросов** → **ошибки многопоточности**.
  - Если зарегистрировать оба как `Scoped`, то:
    - На каждый запрос (или операцию) будет создаваться **новый `AppDbContext` и новый `IPatientService`**, что **безопасно и корректно**.

---

### **Б. Пример проблемы с Singleton**
```csharp
// ❌ Некорректно: Singleton для сервиса, зависящего от Scoped-контекста
services.AddSingleton<IPatientService, PatientService>(); // Ошибка!
services.AddScoped<AppDbContext>();
```
**Что произойдёт?**
- `IPatientService` (Singleton) **создаётся один раз** и **хранит ссылку на `AppDbContext`**.
- При втором запросе `AppDbContext` **уже будет другим** (так как он `Scoped`), но `IPatientService` **попробует использовать старый контекст** → **исключения**.

---

### **В. Пример корректной регистрации**
```csharp
// ✅ Корректно: оба сервиса — Scoped
services.AddScoped<IPatientService, PatientService>();
services.AddScoped<AppDbContext>();
```
**Что происходит?**
- На каждый запрос (или операцию) создаётся:
  - Новый `AppDbContext`.
  - Новый `IPatientService`, который использует **текущий** `AppDbContext`.
- Нет конфликтов, нет утечек памяти.

---

## **3. Почему не Transient?**
- **`Transient`** создаёт **новый экземпляр каждый раз**, когда запрашивается зависимость.
- В случае с `IPatientService` это **неэффективно**:
  - Если в рамках одной операции (например, обработки одного пациента) сервис запрашивается несколько раз, то `Transient` создаст **несколько экземпляров**, что **лишнее**.
- **`Scoped` оптимален**:
  - Один экземпляр на операцию → **экономия ресурсов**.
  - Нет риска конфликтов (как в `Singleton`).

---

## **4. Как это работает в консольном приложении?**
В консольном приложении **нет HTTP-запросов**, поэтому `Scoped` привязывается к **явно созданному "scope"** (блоку кода):
```csharp
using var scope = serviceProvider.CreateScope();
// Внутри этого блока все Scoped-сервисы будут одинаковыми
var patientService = scope.ServiceProvider.GetRequiredService<IPatientService>();
```
- Это **эмулирует поведение веб-приложения**, где `Scoped` привязан к запросу.
- Гарантирует, что **все зависимости в рамках одной операции используют один и тот же контекст**.

---

## **5. Итог: Почему Scoped?**
| Причина                          | Пояснение                                                                                     |
|----------------------------------|---------------------------------------------------------------------------------------------|
| **Безопасность**                 | Избегает конфликтов с EF Core (контекст не потокобезопасен).                                |
| **Корректная работа с БД**        | Один контекст на одну операцию → нет проблем с отслеживанием изменений.                     |
| **Эффективность**                | Один экземпляр сервиса на операцию (не создаётся лишних объектов, как в `Transient`).        |
| **Совместимость с ASP.NET Core**| В веб-приложениях `Scoped` привязан к запросу, что удобно для миграции кода между проектами. |

---
### **Вывод**
- **`Scoped`** — оптимальный выбор для сервисов, работающих с **Entity Framework Core** или другими **непотокобезопасными ресурсами**.
- Гарантирует, что **все зависимости в рамках одной операции используют один и тот же контекст**.
- Избегает проблем с **многопоточностью** и **утечками памяти**.