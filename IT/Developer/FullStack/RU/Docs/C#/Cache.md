https://habr.com/ru/companies/otus/articles/502974/

В C# существует несколько подходов к кэшированию данных, которые можно разделить на **встроенные механизмы** (например, `MemoryCache`) и **внешние решения** (например, **Redis**). Рассмотрим основные типы кэша и примеры их использования.

---

## 1. **MemoryCache (встроенный кэш в памяти)**
Это простейший способ кэширования данных в оперативной памяти приложения. Подходит для небольших объёмов данных и однопроцессных приложений.

### Пример использования `MemoryCache`:
```csharp
using System;
using System.Runtime.Caching;

class Program
{
    static void Main()
    {
        // Создаём экземпляр MemoryCache
        ObjectCache cache = MemoryCache.Default;

        // Ключ для кэша
        string cacheKey = "MyData";

        // Проверяем, есть ли данные в кэше
        if (cache[cacheKey] == null)
        {
            // Если нет — добавляем
            var data = "Данные из базы данных или другого источника";
            cache.Set(cacheKey, data, DateTimeOffset.Now.AddMinutes(5));
            Console.WriteLine("Данные добавлены в кэш.");
        }

        // Получаем данные из кэша
        string cachedData = (string)cache[cacheKey];
        Console.WriteLine($"Данные из кэша: {cachedData}");
    }
}
```

---

## 2. **Distributed Cache (распределённый кэш)**
Используется для кэширования данных в распределённой среде (например, в микросервисах или веб-фермах). Популярное решение — **Redis**.

### Пример использования **Redis** в C#:
Для работы с Redis в C# обычно используется библиотека **StackExchange.Redis**.

#### Установка:
```bash
dotnet add package StackExchange.Redis
```

#### Пример кода:
```csharp
using StackExchange.Redis;
using System;

class Program
{
    static void Main()
    {
        // Подключаемся к Redis
        ConnectionMultiplexer redis = ConnectionMultiplexer.Connect("localhost");
        IDatabase db = redis.GetDatabase();

        // Ключ для кэша
        string cacheKey = "MyData";

        // Проверяем, есть ли данные в кэше
        if (!db.KeyExists(cacheKey))
        {
            // Если нет — добавляем
            var data = "Данные из базы данных или другого источника";
            db.StringSet(cacheKey, data, TimeSpan.FromMinutes(5));
            Console.WriteLine("Данные добавлены в Redis.");
        }

        // Получаем данные из Redis
        string cachedData = db.StringGet(cacheKey);
        Console.WriteLine($"Данные из Redis: {cachedData}");
    }
}
```

---

## 3. **Response Caching (кэширование HTTP-ответов)**
Используется в веб-приложениях (например, ASP.NET Core) для кэширования HTTP-ответов.

### Пример использования в ASP.NET Core:
```csharp
// В Startup.cs или Program.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddResponseCaching();
    services.AddControllers();
}

// В контроллере
[ResponseCache(Duration = 60)] // Кэшировать ответ на 60 секунд
public IActionResult Get()
{
    return Ok("Данные из контроллера");
}
```

---

## 4. **Output Caching (кэширование вывода)**
Используется для кэширования HTML-вывода в веб-приложениях.

### Пример использования в ASP.NET Core:
```csharp
// В Startup.cs или Program.cs
public void ConfigureServices(IServiceCollection services)
{
    services.AddOutputCache();
    services.AddControllers();
}

// В контроллере
[OutputCache(Duration = 30)] // Кэшировать вывод на 30 секунд
public IActionResult Index()
{
    return View();
}
```

---

## Сравнение подходов

| Тип кэша               | Где хранится       | Подходит для                     | Пример использования          |
|------------------------|--------------------|-----------------------------------|--------------------------------|
| **MemoryCache**        | Оперативная память | Однопроцессные приложения        | Кэширование конфигураций       |
| **Redis**              | Внешний сервер     | Распределённые системы            | Кэширование сессий пользователей |
| **Response Caching**   | HTTP-заголовки     | Веб-приложения                   | Кэширование статических данных |
| **Output Caching**     | Сервер             | Веб-приложения                   | Кэширование HTML-страниц       |

---