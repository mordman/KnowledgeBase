# 🚀 Tech Stack Encyclopedia: Полный справочник библиотек и фреймворков
## .NET, Java, Python, JavaScript, Go, Rust, C++ и общеплатформенные решения

---

## 📖 Введение

Этот справочник представляет собой **структурированную энциклопедию** популярных библиотек и фреймворков для современных языков программирования. Он охватывает **более 400 инструментов**, сгруппированных по:

- **Языковым экосистемам** (.NET, Java, Python, JS/TS, Go, Rust, C++)
- **Функциональному назначению** (Message Queue, ORM, Testing, Web Framework и т.д.)
- **Кросс-платформенным решениям** (инфраструктура, DevOps, мониторинг)

### 🎯 Как использовать этот справочник

1. **Выберите экосистему** — начните с раздела, соответствующего вашему стеку
2. **Найдите категорию** — определите тип задачи (очереди сообщений, тестирование, ORM и т.д.)
3. **Сравните альтернативы** — обратите внимание на несколько библиотек в одной категории
4. **Изучите примеры** — в конце приведены примеры кода на C# для ключевых библиотек
5. **Примените паттерны** — раздел о шаблонах проектирования поможет правильно интегрировать инструменты

---

## 🗺️ Архитектура современных приложений: Визуальная схема

```mermaid
graph TB
    subgraph "Frontend Layer"
        FE[React / Vue / Angular / Svelte]
        Mobile[Flutter / React Native / MAUI]
        Desktop[Electron / WPF / Avalonia]
    end
    
    subgraph "API Gateway"
        GW[Ocelot / YARP / Kong / Envoy]
    end
    
    subgraph "Backend Services"
        NET[.NET / ASP.NET Core]
        Java[Spring Boot / Quarkus]
        Py[FastAPI / Django]
        Node[NestJS / Express]
        Go[Gin / Echo]
        Rust[Axum / Actix]
    end
    
    subgraph "Message Brokers"
        MQ1[Kafka]
        MQ2[RabbitMQ]
        MQ3[Azure Service Bus]
        MQ4[NATS / Pulsar]
    end
    
    subgraph "Data Layer"
        DB1[(PostgreSQL / SQL Server)]
        DB2[(MongoDB / Cosmos DB)]
        DB3[(Redis)]
        DB4[(Elasticsearch)]
    end
    
    subgraph "Observability"
        Log[Serilog / NLog / Seq]
        Trace[OpenTelemetry / Jaeger]
        Metric[Prometheus / Grafana]
    end
    
    subgraph "Infrastructure"
        K8s[Kubernetes]
        Docker[Docker]
        Terraform[Terraform]
    end
    
    FE --> GW
    Mobile --> GW
    Desktop --> GW
    GW --> NET
    GW --> Java
    GW --> Py
    GW --> Node
    GW --> Go
    GW --> Rust
    
    NET --> MQ1
    NET --> MQ2
    Java --> MQ1
    Py --> MQ2
    Node --> MQ3
    
    NET --> DB1
    NET --> DB2
    NET --> DB3
    Java --> DB1
    Py --> DB2
    
    NET --> Log
    NET --> Trace
    NET --> Metric
    
    NET --> K8s
    Java --> Docker
```

---

## 📊 Критерии выбора библиотек

При выборе библиотеки или фреймворка рекомендуется оценивать следующие критерии:

| Критерий | Описание | Вес (рекомендуемый) |
|----------|----------|---------------------|
| **Активность разработки** | Частота коммитов, releases, реакция на issues | ⭐⭐⭐⭐⭐ |
| **Сообщество и поддержка** | Размер сообщества, количество вопросов на StackOverflow | ⭐⭐⭐⭐ |
| **Производительность** | Benchmark-тесты, потребление памяти, latency | ⭐⭐⭐⭐ |
| **Документация** | Качество docs, примеры, tutorials | ⭐⭐⭐⭐⭐ |
| **Лицензия** | Совместимость с вашим проектом (MIT, Apache, GPL, коммерческая) | ⭐⭐⭐⭐⭐ |
| **Совместимость** | Поддержка версий языка, интеграция с другими инструментами | ⭐⭐⭐⭐ |
| **Безопасность** | История уязвимостей, скорость патчинга | ⭐⭐⭐⭐⭐ |
| **Кривая обучения** | Простота освоения, наличие learning resources | ⭐⭐⭐ |

---

## 🔧 .NET ЭКОСИСТЕМА (C#, F#, VB.NET)

### 📨 Message Queue & Event Bus

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Message Queue** | MassTransit | [masstransit-project.com](https://masstransit-project.com/) | [github.com/MassTransit/MassTransit](https://github.com/MassTransit/MassTransit) |
| | RabbitMQ.Client (официальный клиент) | [rabbitmq.com/dotnet](https://rabbitmq.com/dotnet.html) | [github.com/rabbitmq/rabbitmq-dotnet-client](https://github.com/rabbitmq/rabbitmq-dotnet-client) |
| | Confluent.Kafka | [docs.confluent.io/kafka-clients/dotnet](https://docs.confluent.io/kafka-clients/dotnet/) | [github.com/confluentinc/confluent-kafka-dotnet](https://github.com/confluentinc/confluent-kafka-dotnet) |
| | Azure.Messaging.ServiceBus (.NET SDK) | [azure.microsoft.com/service-bus](https://azure.microsoft.com/en-us/products/service-bus/) | [github.com/Azure/azure-sdk-for-net](https://github.com/Azure/azure-sdk-for-net) |
| | AWSSDK.SQS | [aws.amazon.com/sqs](https://aws.amazon.com/sqs/) | [github.com/aws/aws-sdk-net](https://github.com/aws/aws-sdk-net) |
| | NetMQ (ZeroMQ for .NET) | [netmq.readthedocs.io](https://netmq.readthedocs.io/) | [github.com/zeromq/netmq](https://github.com/zeromq/netmq) |
| | EasyNetQ | [github.com/EasyNetQ/EasyNetQ](https://github.com/EasyNetQ/EasyNetQ) | [github.com/EasyNetQ/EasyNetQ](https://github.com/EasyNetQ/EasyNetQ) |
| | Rebus | [rebus.fm](https://rebus.fm/) | [github.com/rebus-org/Rebus](https://github.com/rebus-org/Rebus) |
| **Pub/Sub & Streaming** | StackExchange.Redis (Pub/Sub) | [stackexchange.github.io/StackExchange.Redis](https://stackexchange.github.io/StackExchange.Redis/) | [github.com/StackExchange/StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) |
| | Nats.NET | [nats-io.github.io/nats.net](https://nats-io.github.io/nats.net/) | [github.com/nats-io/nats.net](https://github.com/nats-io/nats.net) |
| | Apache Pulsar Client | [pulsar.apache.org/docs/client-libraries-dotnet](https://pulsar.apache.org/docs/client-libraries-dotnet/) | [github.com/apache/pulsar-dotpulsar](https://github.com/apache/pulsar-dotpulsar) |

### 🎭 Actor Model & Mediator

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Actor Model** | Akka.NET | [getakka.net](https://getakka.net/) | [github.com/akkadotnet/akka.net](https://github.com/akkadotnet/akka.net) |
| | Microsoft Orleans | [dotnet.github.io/orleans](https://dotnet.github.io/orleans/) | [github.com/dotnet/orleans](https://github.com/dotnet/orleans) |
| | Proto.Actor | [proto.actor](https://proto.actor/) | [github.com/asynkron/protoactor-dotnet](https://github.com/asynkron/protoactor-dotnet) |
| **Mediator / CQRS** | MediatR | [github.com/jbogard/MediatR/wiki](https://github.com/jbogard/MediatR/wiki) | [github.com/jbogard/MediatR](https://github.com/jbogard/MediatR) |
| | Wolverine | [wolverine.net](https://wolverine.net/) | [github.com/JasperFx/wolverine](https://github.com/JasperFx/wolverine) |
| | Brighter | [www.gobrighter.org](https://www.gobrighter.org/) | [github.com/BrighterCommand/Brighter](https://github.com/BrighterCommand/Brighter) |

### 📝 Profiling, Logging & Observability

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Logging** | Serilog | [serilog.net](https://serilog.net/) | [github.com/serilog/serilog](https://github.com/serilog/serilog) |
| | NLog | [nlog-project.org](https://nlog-project.org/) | [github.com/NLog/NLog](https://github.com/NLog/NLog) |
| | log4net | [logging.apache.org/log4net](https://logging.apache.org/log4net/) | [github.com/apache/logging-log4net](https://github.com/apache/logging-log4net) |
| | Microsoft.Extensions.Logging | [learn.microsoft.com/logging](https://learn.microsoft.com/en-us/dotnet/core/extensions/logging) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| **Tracing** | OpenTelemetry .NET | [opentelemetry.io/docs/instrumentation/net](https://opentelemetry.io/docs/instrumentation/net/) | [github.com/open-telemetry/opentelemetry-dotnet](https://github.com/open-telemetry/opentelemetry-dotnet) |
| | Application Insights | [azure.microsoft.com/app-insights](https://azure.microsoft.com/en-us/products/app-insights/) | [github.com/Microsoft/ApplicationInsights-dotnet](https://github.com/Microsoft/ApplicationInsights-dotnet) |
| | Jaeger Client | [jaegertracing.io](https://www.jaegertracing.io/) | [github.com/jaegertracing/jaeger-client-csharp](https://github.com/jaegertracing/jaeger-client-csharp) |
| **Profiling** | MiniProfiler | [miniprofiler.com](https://miniprofiler.com/) | [github.com/MiniProfiler/dotnet](https://github.com/MiniProfiler/dotnet) |
| | BenchmarkDotNet | [benchmarkdotnet.org](https://benchmarkdotnet.org/) | [github.com/dotnet/BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet) |
| **Metrics** | Prometheus.NET | [github.com/prometheus-net/prometheus-net](https://github.com/prometheus-net/prometheus-net) | [github.com/prometheus-net/prometheus-net](https://github.com/prometheus-net/prometheus-net) |
| | App Metrics | [www.app-metrics.io](https://www.app-metrics.io/) | [github.com/AppMetrics/AppMetrics](https://github.com/AppMetrics/AppMetrics) |
| **Log Aggregation** | Seq | [datalust.co/seq](https://datalust.co/seq) | (коммерческий, есть free-лицензия) |
| | Elastic APM .NET | [elastic.co/apm](https://www.elastic.co/apm) | [github.com/elastic/apm-agent-dotnet](https://github.com/elastic/apm-agent-dotnet) |
| | Sentry .NET | [sentry.io/for/dotnet](https://sentry.io/for/dotnet/) | [github.com/getsentry/sentry-dotnet](https://github.com/getsentry/sentry-dotnet) |

### 🧪 Testing & Quality

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Unit Testing** | xUnit.net | [xunit.net](https://xunit.net/) | [github.com/xunit/xunit](https://github.com/xunit/xunit) |
| | NUnit | [nunit.org](https://nunit.org/) | [github.com/nunit/nunit](https://github.com/nunit/nunit) |
| | MSTest | [learn.microsoft.com/mstest](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest) | [github.com/microsoft/testfx](https://github.com/microsoft/testfx) |
| **Mocking** | Moq | [github.com/devlooped/moq](https://github.com/devlooped/moq) | [github.com/devlooped/moq](https://github.com/devlooped/moq) |
| | NSubstitute | [nsubstitute.github.io](https://nsubstitute.github.io/) | [github.com/nsubstitute/NSubstitute](https://github.com/nsubstitute/NSubstitute) |
| | FakeItEasy | [fakeiteasy.github.io](https://fakeiteasy.github.io/) | [github.com/FakeItEasy/FakeItEasy](https://github.com/FakeItEasy/FakeItEasy) |
| | AutoFixture | [github.com/AutoFixture/AutoFixture](https://github.com/AutoFixture/AutoFixture) | [github.com/AutoFixture/AutoFixture](https://github.com/AutoFixture/AutoFixture) |
| **Assertions** | FluentAssertions | [fluentassertions.com](https://fluentassertions.com/) | [github.com/fluentassertions/fluentassertions](https://github.com/fluentassertions/fluentassertions) |
| | Shouldly | [shouldly.readthedocs.io](https://shouldly.readthedocs.io/) | [github.com/shouldly/shouldly](https://github.com/shouldly/shouldly) |
| **UI Testing** | Selenium.WebDriver | [selenium.dev](https://www.selenium.dev/) | [github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) |
| | Playwright .NET | [playwright.dev/dotnet](https://playwright.dev/dotnet/) | [github.com/microsoft/playwright-dotnet](https://github.com/microsoft/playwright-dotnet) |
| | PuppeteerSharp | [github.com/hardkoded/puppeteer-sharp](https://github.com/hardkoded/puppeteer-sharp) | [github.com/hardkoded/puppeteer-sharp](https://github.com/hardkoded/puppeteer-sharp) |
| **Integration Testing** | Testcontainers .NET | [testcontainers.com](https://testcontainers.com/) | [github.com/testcontainers/testcontainers-dotnet](https://github.com/testcontainers/testcontainers-dotnet) |
| | WireMock.Net | [github.com/WireMock-Net/WireMock.Net](https://github.com/WireMock-Net/WireMock.Net) | [github.com/WireMock-Net/WireMock.Net](https://github.com/WireMock-Net/WireMock.Net) |
| | Respawn | [github.com/jbogard/Respawn](https://github.com/jbogard/Respawn) | [github.com/jbogard/Respawn](https://github.com/jbogard/Respawn) |
| **BDD** | SpecFlow | [specflow.org](https://specflow.org/) | [github.com/SpecFlowOSS/SpecFlow](https://github.com/SpecFlowOSS/SpecFlow) |
| | BDDfy | [bddfy.teststack.net](https://bddfy.teststack.net/) | [github.com/TestStack/TestStack.BDDfy](https://github.com/TestStack/TestStack.BDDfy) |
| **Test Data** | Bogus | [github.com/bchavez/Bogus](https://github.com/bchavez/Bogus) | [github.com/bchavez/Bogus](https://github.com/bchavez/Bogus) |
| | Faker.Net | [github.com/Kuree/Faker.Net](https://github.com/Kuree/Faker.Net) | [github.com/Kuree/Faker.Net](https://github.com/Kuree/Faker.Net) |
| **Architecture Testing** | ArchUnitNET | [github.com/TNG/ArchUnitNET](https://github.com/TNG/ArchUnitNET) | [github.com/TNG/ArchUnitNET](https://github.com/TNG/ArchUnitNET) |
| **Performance Testing** | NBomber | [nbomber.com](https://nbomber.com/) | [github.com/PragmaticFlow/NBomber](https://github.com/PragmaticFlow/NBomber) |

### 🛡️ Resilience & Retry

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Resilience** | Polly | [thepollyproject.org](https://www.thepollyproject.org/) | [github.com/App-vNext/Polly](https://github.com/App-vNext/Polly) |
| | Microsoft.Extensions.Http.Polly | [learn.microsoft.com](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/implement-http-call-retries-polly) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |

### 💾 Object Storage & File Systems

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Object Storage** | MinIO .NET SDK | [min.io/docs/minio/linux/developers/dotnet](https://min.io/docs/minio/linux/developers/dotnet) | [github.com/minio/minio-dotnet](https://github.com/minio/minio-dotnet) |
| | AWSSDK.S3 | [aws.amazon.com/sdk-for-net](https://aws.amazon.com/sdk-for-net/) | [github.com/aws/aws-sdk-net](https://github.com/aws/aws-sdk-net) |
| | Azure.Storage.Blobs | [azure.microsoft.com/storage/blobs](https://azure.microsoft.com/en-us/products/storage/blobs/) | [github.com/Azure/azure-sdk-for-net](https://github.com/Azure/azure-sdk-for-net) |
| | Google.Cloud.Storage.V1 | [cloud.google.com/dotnet](https://cloud.google.com/dotnet) | [github.com/googleapis/google-cloud-dotnet](https://github.com/googleapis/google-cloud-dotnet) |
| **File Systems** | System.IO.Abstractions | [github.com/TestableIO/System.IO.Abstractions](https://github.com/TestableIO/System.IO.Abstractions) | [github.com/TestableIO/System.IO.Abstractions](https://github.com/TestableIO/System.IO.Abstractions) |

### 📄 Office & Document Processing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Excel** | MiniExcel | [github.com/shps951023/MiniExcel](https://github.com/shps951023/MiniExcel) | [github.com/shps951023/MiniExcel](https://github.com/shps951023/MiniExcel) |
| | ClosedXML | [closedxml.github.io/ClosedXML](https://closedxml.github.io/ClosedXML/) | [github.com/closedxml/closedxml](https://github.com/closedxml/closedxml) |
| | EPPlus | [epplussoftware.com](https://www.epplussoftware.com/) | [github.com/EPPlusSoftware/EPPlus](https://github.com/EPPlusSoftware/EPPlus) |
| | ExcelDataReader | [github.com/ExcelDataReader/ExcelDataReader](https://github.com/ExcelDataReader/ExcelDataReader) | [github.com/ExcelDataReader/ExcelDataReader](https://github.com/ExcelDataReader/ExcelDataReader) |
| **Word** | MiniWord | [github.com/shps951023/MiniWord](https://github.com/shps951023/MiniWord) | [github.com/shps951023/MiniWord](https://github.com/shps951023/MiniWord) |
| | DocumentFormat.OpenXml | [github.com/OfficeDev/Open-XML-SDK](https://github.com/OfficeDev/Open-XML-SDK) | [github.com/OfficeDev/Open-XML-SDK](https://github.com/OfficeDev/Open-XML-SDK) |
| **PDF** | QuestPDF | [questpdf.com](https://www.questpdf.com/) | [github.com/QuestPDF/QuestPDF](https://github.com/QuestPDF/QuestPDF) |
| | iText7 (для .NET) | [itextpdf.com](https://itextpdf.com/) | [github.com/itext/itext7-dotnet](https://github.com/itext/itext7-dotnet) |
| | PdfPig | [github.com/UglyToad/PdfPig](https://github.com/UglyToad/PdfPig) | [github.com/UglyToad/PdfPig](https://github.com/UglyToad/PdfPig) |
| | MiniPDF | [github.com/shps951023/MiniPDF](https://github.com/shps951023/MiniPDF) | [github.com/shps951023/MiniPDF](https://github.com/shps951023/MiniPDF) |
| **CSV** | CsvHelper | [joshclose.github.io/CsvHelper](https://joshclose.github.io/CsvHelper/) | [github.com/JoshClose/CsvHelper](https://github.com/JoshClose/CsvHelper) |
| **Commercial** | Aspose.Words | [aspose.com/words/net](https://products.aspose.com/words/net/) | (коммерческий) |
| | Aspose.Cells | [aspose.com/cells/net](https://products.aspose.com/cells/net/) | (коммерческий) |
| | Aspose.PDF | [aspose.com/pdf/net](https://products.aspose.com/pdf/net/) | (коммерческий) |

### 🎨 UI Components & Frontend

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Blazor Components** | MudBlazor | [mudblazor.com](https://mudblazor.com/) | [github.com/MudBlazor/MudBlazor](https://github.com/MudBlazor/MudBlazor) |
| | Radzen Blazor | [radzen.com](https://www.radzen.com/) | [github.com/radzenhq/radzen-blazor](https://github.com/radzenhq/radzen-blazor) |
| | Blazorise | [blazorise.com](https://blazorise.com/) | [github.com/stsrki/Blazorise](https://github.com/stsrki/Blazorise) |
| | Ant Design Blazor | [antblazor.com](https://antblazor.com/) | [github.com/ant-design-blazor/ant-design-blazor](https://github.com/ant-design-blazor/ant-design-blazor) |
| | QuickGrid (MS) | [learn.microsoft.com](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/quickgrid) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| **WPF / WinUI** | Material Design In XAML | [github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit](https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit) | [github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit](https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit) |
| | MahApps.Metro | [mahapps.com](https://mahapps.com/) | [github.com/MahApps/MahApps.Metro](https://github.com/MahApps/MahApps.Metro) |
| | Avalonia | [avaloniaui.net](https://avaloniaui.net/) | [github.com/AvaloniaUI/Avalonia](https://github.com/AvaloniaUI/Avalonia) |
| | CommunityToolkit.Maui | [learn.microsoft.com/dotnet/maui](https://learn.microsoft.com/en-us/dotnet/maui/) | [github.com/CommunityToolkit/Maui](https://github.com/CommunityToolkit/Maui) |
| **Commercial Suites** | DevExpress | [devexpress.com](https://www.devexpress.com/) | (коммерческая) |
| | Telerik (Progress) | [telerik.com](https://www.telerik.com/) | (коммерческая) |
| | Syncfusion | [syncfusion.com](https://www.syncfusion.com/) | (коммерческая, есть Community-лицензия) |
| | Infragistics | [infragistics.com](https://www.infragistics.com/) | (коммерческая) |

### 🌐 Web Frameworks & API

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Web Framework** | ASP.NET Core | [dotnet.microsoft.com/aspnet](https://dotnet.microsoft.com/en-us/apps/aspnet) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | Minimal APIs (встроен) | [learn.microsoft.com/minimal-apis](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | Carter | [github.com/CarterCommunity/Carter](https://github.com/CarterCommunity/Carter) | [github.com/CarterCommunity/Carter](https://github.com/CarterCommunity/Carter) |
| | NancyFX (legacy) | [nancyfx.org](https://nancyfx.org/) | [github.com/NancyFx/Nancy](https://github.com/NancyFx/Nancy) |
| **API Gateway** | Ocelot | [ocelot.readthedocs.io](https://ocelot.readthedocs.io/) | [github.com/ThreeMammals/Ocelot](https://github.com/ThreeMammals/Ocelot) |
| | YARP | [microsoft.github.io/reverse-proxy](https://microsoft.github.io/reverse-proxy/) | [github.com/microsoft/reverse-proxy](https://github.com/microsoft/reverse-proxy) |
| **API Documentation** | Swashbuckle (Swagger) | [github.com/domaindrivendev/Swashbuckle](https://github.com/domaindrivendev/Swashbuckle) | [github.com/domaindrivendev/Swashbuckle.AspNetCore](https://github.com/domaindrivendev/Swashbuckle.AspNetCore) |
| | NSwag | [github.com/RicoSuter/NSwag](https://github.com/RicoSuter/NSwag) | [github.com/RicoSuter/NSwag](https://github.com/RicoSuter/NSwag) |
| | Scalar | [scalar.com](https://scalar.com/) | [github.com/scalar/scalar](https://github.com/scalar/scalar) |
| **GraphQL** | Hot Chocolate | [chillicream.com/docs/hotchocolate](https://chillicream.com/docs/hotchocolate) | [github.com/ChilliCream/hotchocolate](https://github.com/ChilliCream/hotchocolate) |
| | GraphQL.NET | [graphql-dotnet.github.io](https://graphql-dotnet.github.io/) | [github.com/graphql-dotnet/graphql-dotnet](https://github.com/graphql-dotnet/graphql-dotnet) |
| **gRPC** | gRPC for .NET | [grpc.io/docs/languages/dotnet](https://grpc.io/docs/languages/dotnet/) | [github.com/grpc/grpc-dotnet](https://github.com/grpc/grpc-dotnet) |
| **HTTP Clients** | RestSharp | [restsharp.dev](https://restsharp.dev/) | [github.com/restsharp/RestSharp](https://github.com/restsharp/RestSharp) |
| | Refit | [github.com/reactiveui/refit](https://github.com/reactiveui/refit) | [github.com/reactiveui/refit](https://github.com/reactiveui/refit) |
| | Flurl | [flurl.dev](https://flurl.dev/) | [github.com/tmenier/Flurl](https://github.com/tmenier/Flurl) |
| | HttpClient (встроенный) | [learn.microsoft.com/httpclient](https://learn.microsoft.com/en-us/dotnet/api/system.net.http.httpclient) | (встроен в .NET) |

### 🗄️ ORM & Data Access

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Full ORM** | Entity Framework Core | [learn.microsoft.com/ef](https://learn.microsoft.com/en-us/ef/) | [github.com/dotnet/efcore](https://github.com/dotnet/efcore) |
| | NHibernate | [nhibernate.info](https://nhibernate.info/) | [github.com/nhibernate/nhibernate-core](https://github.com/nhibernate/nhibernate-core) |
| | Linq2DB | [linq2db.com](https://linq2db.com/) | [github.com/linq2db/linq2db](https://github.com/linq2db/linq2db) |
| | ServiceStack.OrmLite | [servicestack.net/ormlite](https://servicestack.net/ormlite) | [github.com/ServiceStack/ServiceStack](https://github.com/ServiceStack/ServiceStack) |
| **Micro ORM** | Dapper | [github.com/DapperLib/Dapper](https://github.com/DapperLib/Dapper) | [github.com/DapperLib/Dapper](https://github.com/DapperLib/Dapper) |
| | SqlKata | [sqlkata.com](https://sqlkata.com/) | [github.com/sqlkata/querybuilder](https://github.com/sqlkata/querybuilder) |
| | Dommel | [github.com/henkmollema/Dommel](https://github.com/henkmollema/Dommel) | [github.com/henkmollema/Dommel](https://github.com/henkmollema/Dommel) |
| **Document DB** | Marten (PostgreSQL) | [martendb.io](https://martendb.io/) | [github.com/JasperFx/marten](https://github.com/JasperFx/marten) |
| | MongoDB.Driver | [mongodb.com/docs/driver/csharp](https://www.mongodb.com/docs/driver/csharp/) | [github.com/mongodb/mongo-csharp-driver](https://github.com/mongodb/mongo-csharp-driver) |
| **Database Providers** | Npgsql (PostgreSQL) | [www.npgsql.org](https://www.npgsql.org/) | [github.com/npgsql/npgsql](https://github.com/npgsql/npgsql) |
| | MySqlConnector | [mysqlconnector.net](https://mysqlconnector.net/) | [github.com/mysql-net/MySqlConnector](https://github.com/mysql-net/MySqlConnector) |
| | Microsoft.Data.SqlClient | [github.com/dotnet/SqlClient](https://github.com/dotnet/SqlClient) | [github.com/dotnet/SqlClient](https://github.com/dotnet/SqlClient) |
| **Migrations** | EF Core Migrations (встроен) | [learn.microsoft.com/ef/managing-schemas](https://learn.microsoft.com/en-us/ef/core/managing-schemas/) | [github.com/dotnet/efcore](https://github.com/dotnet/efcore) |
| | FluentMigrator | [github.com/fluentmigrator/fluentmigrator](https://github.com/fluentmigrator/fluentmigrator) | [github.com/fluentmigrator/fluentmigrator](https://github.com/fluentmigrator/fluentmigrator) |
| | Roundhouse | [github.com/chucknorris/roundhouse](https://github.com/chucknorris/roundhouse) | [github.com/chucknorris/roundhouse](https://github.com/chucknorris/roundhouse) |

### 💉 Dependency Injection & IoC

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **DI Containers** | Microsoft.Extensions.DependencyInjection (встроен) | [learn.microsoft.com/di](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| | Autofac | [autofac.org](https://autofac.org/) | [github.com/autofac/Autofac](https://github.com/autofac/Autofac) |
| | Simple Injector | [simpleinjector.org](https://simpleinjector.org/) | [github.com/simpleinjector/SimpleInjector](https://github.com/simpleinjector/SimpleInjector) |
| | DryIoc | [dryioc.com](https://www.dryioc.com/) | [github.com/dadhi/DryIoc](https://github.com/dadhi/DryIoc) |
| | LightInject | [lightinject.net](https://www.lightinject.net/) | [github.com/seesharper/LightInject](https://github.com/seesharper/LightInject) |
| | Lamar | [lamarproject.org](https://lamarproject.org/) | [github.com/JasperFx/lamar](https://github.com/JasperFx/lamar) |
| **Legacy** | Unity (Microsoft) | [github.com/unitycontainer/unity](https://github.com/unitycontainer/unity) | [github.com/unitycontainer/unity](https://github.com/unitycontainer/unity) |
| | Ninject | [ninject.org](https://ninject.org/) | [github.com/ninject/Ninject](https://github.com/ninject/Ninject) |
| | Castle Windsor | [castleproject.org](https://www.castleproject.org/) | [github.com/castleproject/Windsor](https://github.com/castleproject/Windsor) |

### 🗂️ Caching & Distributed Cache

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **In-Memory** | Microsoft.Extensions.Caching.Memory | [learn.microsoft.com/caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | FusionCache | [github.com/jodydonetti/ZiggyCreatures.FusionCache](https://github.com/jodydonetti/ZiggyCreatures.FusionCache) | [github.com/jodydonetti/ZiggyCreatures.FusionCache](https://github.com/jodydonetti/ZiggyCreatures.FusionCache) |
| | CacheManager | [cachemanager.net](https://cachemanager.net/) | [github.com/MichaCo/CacheManager](https://github.com/MichaCo/CacheManager) |
| **Distributed** | StackExchange.Redis | [stackexchange.github.io/StackExchange.Redis](https://stackexchange.github.io/StackExchange.Redis/) | [github.com/StackExchange/StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) |
| | NCache | [www.alachisoft.com/ncache](https://www.alachisoft.com/ncache/) | (коммерческий, есть OSS-версия) |
| | Hazelcast .NET Client | [hazelcast.com](https://hazelcast.com/) | [github.com/hazelcast/hazelcast-csharp-client](https://github.com/hazelcast/hazelcast-csharp-client) |

### 🔐 Authentication & Authorization

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Identity Providers** | Duende IdentityServer | [duendesoftware.com/products/identityserver](https://duendesoftware.com/products/identityserver) | (коммерческий) |
| | OpenIddict | [openiddict.com](https://openiddict.com/) | [github.com/openiddict/openiddict-core](https://github.com/openiddict/openiddict-core) |
| | IdentityServer4 (legacy, EOL) | [github.com/IdentityServer/IdentityServer4](https://github.com/IdentityServer/IdentityServer4) | [github.com/IdentityServer/IdentityServer4](https://github.com/IdentityServer/IdentityServer4) |
| **Built-in** | ASP.NET Core Identity | [learn.microsoft.com/aspnet/identity](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | JWT Bearer Auth | [learn.microsoft.com/jwt](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/jwt) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| **SaaS Integration** | Auth0 .NET SDK | [auth0.com/docs/quickstart/backend/dotnet](https://auth0.com/docs/quickstart/backend/dotnet) | [github.com/auth0/auth0-dotnet](https://github.com/auth0/auth0-dotnet) |
| | Okta .NET SDK | [developer.okta.com/docs/guides/sign-into-web-app-redirect/dotnet-aspnetcore-main](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/dotnet-aspnetcore-main/) | [github.com/okta/okta-dotnet](https://github.com/okta/okta-dotnet) |
| | AWS Cognito | [docs.aws.amazon.com/cognito](https://docs.aws.amazon.com/cognito/) | [github.com/aws/aws-sdk-net](https://github.com/aws/aws-sdk-net) |
| **Libraries** | Jose JWT | [github.com/dvsekhvalnov/jose-jwt](https://github.com/dvsekhvalnov/jose-jwt) | [github.com/dvsekhvalnov/jose-jwt](https://github.com/dvsekhvalnov/jose-jwt) |
| | BCrypt.Net-Next | [github.com/BcryptNet/bcrypt.net](https://github.com/BcryptNet/bcrypt.net) | [github.com/BcryptNet/bcrypt.net](https://github.com/BcryptNet/bcrypt.net) |

### 🤖 Machine Learning & AI

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **ML Frameworks** | ML.NET | [dotnet.microsoft.com/ml-dotnet](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet) | [github.com/dotnet/machinelearning](https://github.com/dotnet/machinelearning) |
| | TensorFlow.NET | [github.com/SciSharp/TensorFlow.NET](https://github.com/SciSharp/TensorFlow.NET) | [github.com/SciSharp/TensorFlow.NET](https://github.com/SciSharp/TensorFlow.NET) |
| | TorchSharp | [github.com/dotnet/TorchSharp](https://github.com/dotnet/TorchSharp) | [github.com/dotnet/TorchSharp](https://github.com/dotnet/TorchSharp) |
| **Inference** | ONNX Runtime .NET | [onnxruntime.ai](https://onnxruntime.ai/) | [github.com/microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |
| | OpenCvSharp | [github.com/shimat/opencvsharp](https://github.com/shimat/opencvsharp) | [github.com/shimat/opencvsharp](https://github.com/shimat/opencvsharp) |
| **LLM Integration** | LangChain .NET | [github.com/tryAGI/LangChain](https://github.com/tryAGI/LangChain) | [github.com/tryAGI/LangChain](https://github.com/tryAGI/LangChain) |
| | Betalgo.OpenAI | [github.com/betalgo/openai](https://github.com/betalgo/openai) | [github.com/betalgo/openai](https://github.com/betalgo/openai) |
| | Azure.AI.OpenAI | [learn.microsoft.com/azure/ai-services/openai](https://learn.microsoft.com/en-us/azure/ai-services/openai/) | [github.com/Azure/azure-sdk-for-net](https://github.com/Azure/azure-sdk-for-net) |

### 🔗 Serialization & Data Formats

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **JSON** | System.Text.Json | [learn.microsoft.com/system.text.json](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| | Newtonsoft.Json (Json.NET) | [newtonsoft.com/json](https://www.newtonsoft.com/json) | [github.com/JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json) |
| **Binary** | MessagePack for C# | [msgpack.org](https://msgpack.org/) | [github.com/neuecc/MessagePack-CSharp](https://github.com/neuecc/MessagePack-CSharp) |
| | Protobuf-net | [protobuf-net.github.io](https://protobuf-net.github.io/) | [github.com/protobuf-net/protobuf-net](https://github.com/protobuf-net/protobuf-net) |
| | Google.Protobuf | [github.com/protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) | [github.com/protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) |
| **YAML/XML** | YamlDotNet | [github.com/aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) | [github.com/aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) |
| | SharpYaml | [github.com/xoofx/SharpYaml](https://github.com/xoofx/SharpYaml) | [github.com/xoofx/SharpYaml](https://github.com/xoofx/SharpYaml) |
| **Other** | Tomlyn | [github.com/scriban/tomlyn](https://github.com/scriban/tomlyn) | [github.com/scriban/tomlyn](https://github.com/scriban/tomlyn) |

### ✅ Validation

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Validation** | FluentValidation | [fluentvalidation.net](https://fluentvalidation.net/) | [github.com/FluentValidation/FluentValidation](https://github.com/FluentValidation/FluentValidation) |
| | DataAnnotations (встроенный) | [learn.microsoft.com/dataannotations](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| | MiniValidation | [github.com/DamianEdwards/MiniValidation](https://github.com/DamianEdwards/MiniValidation) | [github.com/DamianEdwards/MiniValidation](https://github.com/DamianEdwards/MiniValidation) |

### 🔄 Reactive & Async Patterns

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Reactive Extensions** | Reactive Extensions (Rx.NET) | [reactivex.io](https://reactivex.io/) | [github.com/dotnet/reactive](https://github.com/dotnet/reactive) |
| | Dynamic Data | [github.com/reactivemarbles/DynamicData](https://github.com/reactivemarbles/DynamicData) | [github.com/reactivemarbles/DynamicData](https://github.com/reactivemarbles/DynamicData) |
| **Task Parallelism** | System.Threading.Tasks.Dataflow | [learn.microsoft.com/tpl-dataflow](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/dataflow-task-parallel-library) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| | System.Threading.Channels | [learn.microsoft.com/channels](https://learn.microsoft.com/en-us/dotnet/api/system.threading.channels) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| **Background Jobs** | Hangfire | [www.hangfire.io](https://www.hangfire.io/) | [github.com/HangfireIO/Hangfire](https://github.com/HangfireIO/Hangfire) |
| | Quartz.NET | [www.quartz-scheduler.net](https://www.quartz-scheduler.net/) | [github.com/quartznet/quartznet](https://github.com/quartznet/quartznet) |
| | Coravel | [docs.coravel.net](https://docs.coravel.net/) | [github.com/jamesmh/coravel](https://github.com/jamesmh/coravel) |

### 🛠️ Utility Libraries

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Mapping** | AutoMapper | [automapper.org](https://automapper.org/) | [github.com/AutoMapper/AutoMapper](https://github.com/AutoMapper/AutoMapper) |
| | Mapster | [github.com/MapsterMapper/Mapster](https://github.com/MapsterMapper/Mapster) | [github.com/MapsterMapper/Mapster](https://github.com/MapsterMapper/Mapster) |
| **Date/Time** | NodaTime | [nodatime.org](https://nodatime.org/) | [github.com/nodatime/nodatime](https://github.com/nodatime/nodatime) |
| | Humanizer | [humanizr.github.io](https://humanizr.github.io/) | [github.com/Humanizr/Humanizer](https://github.com/Humanizr/Humanizer) |
| **Collections** | MoreLINQ | [morelinq.github.io](https://morelinq.github.io/) | [github.com/morelinq/MoreLINQ](https://github.com/morelinq/MoreLINQ) |
| | System.Collections.Immutable | [learn.microsoft.com](https://learn.microsoft.com/en-us/dotnet/api/system.collections.immutable) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| **Functional** | LanguageExt | [github.com/louthy/language-ext](https://github.com/louthy/language-ext) | [github.com/louthy/language-ext](https://github.com/louthy/language-ext) |
| | Optional | [github.com/nlkl/Optional](https://github.com/nlkl/Optional) | [github.com/nlkl/Optional](https://github.com/nlkl/Optional) |
| **CLI** | Spectre.Console | [spectreconsole.net](https://spectreconsole.net/) | [github.com/spectreconsole/spectre.console](https://github.com/spectreconsole/spectre.console) |
| | System.CommandLine | [github.com/dotnet/command-line-api](https://github.com/dotnet/command-line-api) | [github.com/dotnet/command-line-api](https://github.com/dotnet/command-line-api) |
| | CommandLineParser | [github.com/commandlineparser/commandline](https://github.com/commandlineparser/commandline) | [github.com/commandlineparser/commandline](https://github.com/commandlineparser/commandline) |
| **HTML Parsing** | AngleSharp | [anglesharp.github.io](https://anglesharp.github.io/) | [github.com/AngleSharp/AngleSharp](https://github.com/AngleSharp/AngleSharp) |
| | HtmlAgilityPack | [html-agility-pack.net](https://html-agility-pack.net/) | [github.com/zzzprojects/HtmlAgilityPack](https://github.com/zzzprojects/HtmlAgilityPack) |
| **Image Processing** | SixLabors.ImageSharp | [sixlabors.com/imagesharp](https://sixlabors.com/imagesharp/) | [github.com/SixLabors/ImageSharp](https://github.com/SixLabors/ImageSharp) |
| | SkiaSharp | [github.com/mono/SkiaSharp](https://github.com/mono/SkiaSharp) | [github.com/mono/SkiaSharp](https://github.com/mono/SkiaSharp) |
| | Magick.NET | [github.com/dlemstra/Magick.NET](https://github.com/dlemstra/Magick.NET) | [github.com/dlemstra/Magick.NET](https://github.com/dlemstra/Magick.NET) |
| **Compression** | SharpZipLib | [github.com/icsharpcode/SharpZipLib](https://github.com/icsharpcode/SharpZipLib) | [github.com/icsharpcode/SharpZipLib](https://github.com/icsharpcode/SharpZipLib) |
| | K4os.Compression.LZ4 | [github.com/KrzysztofCwalina/K4os.Compression.LZ4](https://github.com/KrzysztofCwalina/K4os.Compression.LZ4) | [github.com/KrzysztofCwalina/K4os.Compression.LZ4](https://github.com/KrzysztofCwalina/K4os.Compression.LZ4) |
| **Cryptography** | BouncyCastle | [www.bouncycastle.org/csharp](https://www.bouncycastle.org/csharp/) | [github.com/bcgit/bc-csharp](https://github.com/bcgit/bc-csharp) |
| | System.Security.Cryptography (встроен) | [learn.microsoft.com](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography) | (встроен в .NET) |
| **Geo / Spatial** | NetTopologySuite | [github.com/NetTopologySuite/NetTopologySuite](https://github.com/NetTopologySuite/NetTopologySuite) | [github.com/NetTopologySuite/NetTopologySuite](https://github.com/NetTopologySuite/NetTopologySuite) |
| | GeoAPI | [github.com/NetTopologySuite/GeoAPI](https://github.com/NetTopologySuite/GeoAPI) | [github.com/NetTopologySuite/GeoAPI](https://github.com/NetTopologySuite/GeoAPI) |

---

## ☕ JAVA ЭКОСИСТЕМА

### 📨 Message Queue & Streaming

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Queue** | Apache Kafka (Java client) | [kafka.apache.org](https://kafka.apache.org/) | [github.com/apache/kafka](https://github.com/apache/kafka) |
| | RabbitMQ Java Client | [rabbitmq.com/java](https://rabbitmq.com/java.html) | [github.com/rabbitmq/rabbitmq-java-client](https://github.com/rabbitmq/rabbitmq-java-client) |
| | ActiveMQ Artemis | [activemq.apache.org](https://activemq.apache.org/) | [github.com/apache/activemq-artemis](https://github.com/apache/activemq-artemis) |
| | JMS (Jakarta Message Service) | [jakarta.ee/specifications/jms](https://jakarta.ee/specifications/jms/) | [github.com/eclipse-ee4j/jms-api](https://github.com/eclipse-ee4j/jms-api) |
| | Spring Kafka | [spring.io/projects/spring-kafka](https://spring.io/projects/spring-kafka) | [github.com/spring-projects/spring-kafka](https://github.com/spring-projects/spring-kafka) |
| | Spring AMQP | [spring.io/projects/spring-amqp](https://spring.io/projects/spring-amqp) | [github.com/spring-projects/spring-amqp](https://github.com/spring-projects/spring-amqp) |

### 🎭 Actor Model & Concurrency

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Actor Model** | Akka (Java/Scala) | [akka.io](https://akka.io/) | [github.com/akka/akka](https://github.com/akka/akka) |
| | Quasar (fibers) | [docs.paralleluniverse.co/quasar](https://docs.paralleluniverse.co/quasar/) | [github.com/puniverse/quasar](https://github.com/puniverse/quasar) |
| **Virtual Threads** | Java 21 Virtual Threads (Project Loom) | [openjdk.org/projects/loom](https://openjdk.org/projects/loom/) | (встроен в JDK 21+) |

### 🧪 Testing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Unit Testing** | JUnit 5 | [junit.org](https://junit.org/) | [github.com/junit-team/junit5](https://github.com/junit-team/junit5) |
| | TestNG | [testng.org](https://testng.org/) | [github.com/testng-team/testng](https://github.com/testng-team/testng) |
| **Mocking** | Mockito | [site.mockito.org](https://site.mockito.org/) | [github.com/mockito/mockito](https://github.com/mockito/mockito) |
| | WireMock | [wiremock.org](https://wiremock.org/) | [github.com/wiremock/wiremock](https://github.com/wiremock/wiremock) |
| **Assertions** | AssertJ | [assertj.github.io](https://assertj.github.io/doc/) | [github.com/assertj/assertj](https://github.com/assertj/assertj) |
| | Hamcrest | [hamcrest.org](http://hamcrest.org/) | [github.com/hamcrest/JavaHamcrest](https://github.com/hamcrest/JavaHamcrest) |
| **BDD** | Cucumber-JVM | [cucumber.io](https://cucumber.io/) | [github.com/cucumber/cucumber-jvm](https://github.com/cucumber/cucumber-jvm) |
| **UI Testing** | Selenium Java | [selenium.dev](https://www.selenium.dev/) | [github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) |
| | Selenide | [selenide.org](https://selenide.org/) | [github.com/selenide/selenide](https://github.com/selenide/selenide) |
| **Integration** | Testcontainers Java | [testcontainers.com](https://testcontainers.com/) | [github.com/testcontainers/testcontainers-java](https://github.com/testcontainers/testcontainers-java) |
| | Awaitility | [github.com/awaitility/awaitility](https://github.com/awaitility/awaitility) | [github.com/awaitility/awaitility](https://github.com/awaitility/awaitility) |
| **Performance** | JMH (Java Microbenchmark Harness) | [openjdk.org/projects/code-tools/jmh](https://openjdk.org/projects/code-tools/jmh/) | [github.com/openjdk/jmh](https://github.com/openjdk/jmh) |
| | Gatling | [gatling.io](https://gatling.io/) | [github.com/gatling/gatling](https://github.com/gatling/gatling) |

### 🛡️ Resilience & Retry

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Resilience** | Resilience4j | [resilience4j.readme.io](https://resilience4j.readme.io/) | [github.com/resilience4j/resilience4j](https://github.com/resilience4j/resilience4j) |
| | Failsafe | [failsafe.dev](https://failsafe.dev/) | [github.com/failsafe-lib/failsafe](https://github.com/failsafe-lib/failsafe) |
| | Hystrix (legacy) | [github.com/Netflix/Hystrix](https://github.com/Netflix/Hystrix) | [github.com/Netflix/Hystrix](https://github.com/Netflix/Hystrix) |
| | Spring Retry | [github.com/spring-projects/spring-retry](https://github.com/spring-projects/spring-retry) | [github.com/spring-projects/spring-retry](https://github.com/spring-projects/spring-retry) |

### 💾 Object Storage

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Object Storage** | AWS S3 SDK (v2) | [aws.amazon.com/sdk-for-java](https://aws.amazon.com/sdk-for-java/) | [github.com/aws/aws-sdk-java-v2](https://github.com/aws/aws-sdk-java-v2) |
| | MinIO Java SDK | [min.io/docs/minio/linux/developers/java](https://min.io/docs/minio/linux/developers/java) | [github.com/minio/minio-java](https://github.com/minio/minio-java) |
| | Google Cloud Java SDK | [cloud.google.com/java](https://cloud.google.com/java) | [github.com/googleapis/google-cloud-java](https://github.com/googleapis/google-cloud-java) |
| | Azure SDK for Java | [azure.github.io/azure-sdk-for-java](https://azure.github.io/azure-sdk-for-java/) | [github.com/Azure/azure-sdk-for-java](https://github.com/Azure/azure-sdk-for-java) |

### 📄 Office & Document Processing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Office** | Apache POI | [poi.apache.org](https://poi.apache.org/) | [github.com/apache/poi](https://github.com/apache/poi) |
| | iText | [itextpdf.com](https://itextpdf.com/) | [github.com/itext/itext7](https://github.com/itext/itext7) |
| | Apache PDFBox | [pdfbox.apache.org](https://pdfbox.apache.org/) | [github.com/apache/pdfbox](https://github.com/apache/pdfbox) |
| | docx4j | [github.com/plutext/docx4j](https://github.com/plutext/docx4j) | [github.com/plutext/docx4j](https://github.com/plutext/docx4j) |
| **Commercial** | Aspose.Words | [aspose.com/words/java](https://products.aspose.com/words/java/) | (коммерческий) |

### 🎨 UI Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Desktop** | JavaFX | [openjfx.io](https://openjfx.io/) | [github.com/openjdk/jfx](https://github.com/openjdk/jfx) |
| | Swing (встроенный) | [docs.oracle.com/javase/swing](https://docs.oracle.com/javase/tutorial/uiswing/) | (встроен в JDK) |
| **Web** | Vaadin | [vaadin.com](https://vaadin.com/) | [github.com/vaadin](https://github.com/vaadin) |
| | GWT (Google Web Toolkit) | [www.gwtproject.org](https://www.gwtproject.org/) | [github.com/gwtproject/gwt](https://github.com/gwtproject/gwt) |

### 🌐 Web Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Framework** | Spring Boot | [spring.io/projects/spring-boot](https://spring.io/projects/spring-boot) | [github.com/spring-projects/spring-boot](https://github.com/spring-projects/spring-boot) |
| | Quarkus | [quarkus.io](https://quarkus.io/) | [github.com/quarkusio/quarkus](https://github.com/quarkusio/quarkus) |
| | Micronaut | [micronaut.io](https://micronaut.io/) | [github.com/micronaut-projects/micronaut-core](https://github.com/micronaut-projects/micronaut-core) |
| | Jakarta EE | [jakarta.ee](https://jakarta.ee/) | [github.com/eclipse-ee4j](https://github.com/eclipse-ee4j) |
| | Play Framework | [playframework.com](https://www.playframework.com/) | [github.com/playframework/playframework](https://github.com/playframework/playframework) |
| | Javalin | [javalin.io](https://javalin.io/) | [github.com/javalin/javalin](https://github.com/javalin/javalin) |
| | SparkJava | [sparkjava.com](http://sparkjava.com/) | [github.com/perwendel/spark](https://github.com/perwendel/spark) |

### 🗄️ ORM & Data Access

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Full ORM** | Hibernate ORM | [hibernate.org](https://hibernate.org/) | [github.com/hibernate/hibernate-orm](https://github.com/hibernate/hibernate-orm) |
| | EclipseLink | [eclipse.dev/eclipselink](https://eclipse.dev/eclipselink/) | [github.com/eclipse-ee4j/eclipselink](https://github.com/eclipse-ee4j/eclipselink) |
| | JPA (Jakarta Persistence) | [jakarta.ee/specifications/persistence](https://jakarta.ee/specifications/persistence/) | [github.com/eclipse-ee4j/jpa-api](https://github.com/eclipse-ee4j/jpa-api) |
| **Data Mapper** | MyBatis | [mybatis.org](https://mybatis.org/) | [github.com/mybatis/mybatis-3](https://github.com/mybatis/mybatis-3) |
| | jOOQ | [www.jooq.org](https://www.jooq.org/) | [github.com/jOOQ/jOOQ](https://github.com/jOOQ/jOOQ) |
| | Querydsl | [querydsl.com](https://querydsl.com/) | [github.com/querydsl/querydsl](https://github.com/querydsl/querydsl) |
| **Spring Data** | Spring Data JPA | [spring.io/projects/spring-data-jpa](https://spring.io/projects/spring-data-jpa) | [github.com/spring-projects/spring-data-jpa](https://github.com/spring-projects/spring-data-jpa) |
| | Spring Data MongoDB | [spring.io/projects/spring-data-mongodb](https://spring.io/projects/spring-data-mongodb) | [github.com/spring-projects/spring-data-mongodb](https://github.com/spring-projects/spring-data-mongodb) |
| | Spring Data Redis | [spring.io/projects/spring-data-redis](https://spring.io/projects/spring-data-redis) | [github.com/spring-projects/spring-data-redis](https://github.com/spring-projects/spring-data-redis) |
| **Migrations** | Flyway | [flywaydb.org](https://flywaydb.org/) | [github.com/flyway/flyway](https://github.com/flyway/flyway) |
| | Liquibase | [liquibase.org](https://www.liquibase.org/) | [github.com/liquibase/liquibase](https://github.com/liquibase/liquibase) |

### 💉 Dependency Injection

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **DI Containers** | Spring DI (Spring Framework) | [spring.io](https://spring.io/) | [github.com/spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) |
| | Dagger | [dagger.dev](https://dagger.dev/) | [github.com/google/dagger](https://github.com/google/dagger) |
| | Guice | [github.com/google/guice](https://github.com/google/guice) | [github.com/google/guice](https://github.com/google/guice) |
| | CDI (Jakarta Contexts and Dependency Injection) | [jakarta.ee/specifications/cdi](https://jakarta.ee/specifications/cdi/) | [github.com/eclipse-ee4j/cdi](https://github.com/eclipse-ee4j/cdi) |

### 🗂️ Caching

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **In-Memory** | Caffeine | [github.com/ben-manes/caffeine](https://github.com/ben-manes/caffeine) | [github.com/ben-manes/caffeine](https://github.com/ben-manes/caffeine) |
| | Ehcache | [ehcache.org](https://www.ehcache.org/) | [github.com/ehcache/ehcache3](https://github.com/ehcache/ehcache3) |
| | Hazelcast | [hazelcast.com](https://hazelcast.com/) | [github.com/hazelcast/hazelcast](https://github.com/hazelcast/hazelcast) |
| **Distributed** | Jedis | [redis.io/clients](https://redis.io/clients) | [github.com/redis/jedis](https://github.com/redis/jedis) |
| | Lettuce | [github.com/lettuce-io/lettuce-core](https://github.com/lettuce-io/lettuce-core) | [github.com/lettuce-io/lettuce-core](https://github.com/lettuce-io/lettuce-core) |
| | Redisson | [redisson.org](https://redisson.org/) | [github.com/redisson/redisson](https://github.com/redisson/redisson) |

### 🔐 Authentication & Security

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Security Frameworks** | Spring Security | [spring.io/projects/spring-security](https://spring.io/projects/spring-security) | [github.com/spring-projects/spring-security](https://github.com/spring-projects/spring-security) |
| | Keycloak (Java Adapter) | [keycloak.org](https://www.keycloak.org/) | [github.com/keycloak/keycloak](https://github.com/keycloak/keycloak) |
| **JWT** | JJWT | [github.com/jwtk/jjwt](https://github.com/jwtk/jjwt) | [github.com/jwtk/jjwt](https://github.com/jwtk/jjwt) |
| | Nimbus JOSE+JWT | [connect2id.com/products/nimbus-jose-jwt](https://connect2id.com/products/nimbus-jose-jwt) | [github.com/okta/okta-jwt-verifier-java](https://github.com/okta/okta-jwt-verifier-java) |
| **OAuth2** | Spring Authorization Server | [spring.io/projects/spring-authorization-server](https://spring.io/projects/spring-authorization-server) | [github.com/spring-projects/spring-authorization-server](https://github.com/spring-projects/spring-authorization-server) |
| | Apache Oltu | [oltu.apache.org](https://oltu.apache.org/) | [github.com/apache/oltu](https://github.com/apache/oltu) |

### 🛠️ Utility Libraries

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Core Utilities** | Apache Commons Lang | [commons.apache.org/lang](https://commons.apache.org/proper/commons-lang/) | [github.com/apache/commons-lang](https://github.com/apache/commons-lang) |
| | Google Guava | [github.com/google/guava](https://github.com/google/guava) | [github.com/google/guava](https://github.com/google/guava) |
| | Vavr (functional) | [www.vavr.io](https://www.vavr.io/) | [github.com/vavr-io/vavr](https://github.com/vavr-io/vavr) |
| **Code Generation** | Lombok | [projectlombok.org](https://projectlombok.org/) | [github.com/projectlombok/lombok](https://github.com/projectlombok/lombok) |
| | MapStruct | [mapstruct.org](https://mapstruct.org/) | [github.com/mapstruct/mapstruct](https://github.com/mapstruct/mapstruct) |
| **JSON** | Jackson | [github.com/FasterXML/jackson](https://github.com/FasterXML/jackson) | [github.com/FasterXML/jackson](https://github.com/FasterXML/jackson) |
| | Gson | [github.com/google/gson](https://github.com/google/gson) | [github.com/google/gson](https://github.com/google/gson) |
| | Moshi | [github.com/square/moshi](https://github.com/square/moshi) | [github.com/square/moshi](https://github.com/square/moshi) |
| **Logging** | Logback | [logback.qos.ch](https://logback.qos.ch/) | [github.com/qos-ch/logback](https://github.com/qos-ch/logback) |
| | Log4j2 | [logging.apache.org/log4j/2.x](https://logging.apache.org/log4j/2.x/) | [github.com/apache/logging-log4j2](https://github.com/apache/logging-log4j2) |
| | SLF4J | [slf4j.org](https://www.slf4j.org/) | [github.com/qos-ch/slf4j](https://github.com/qos-ch/slf4j) |

---

## 🐍 PYTHON ЭКОСИСТЕМА

### 🌐 Web Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Full-Stack** | Django | [djangoproject.com](https://www.djangoproject.com/) | [github.com/django/django](https://github.com/django/django) |
| | TurboGears | [turbogears.org](https://turbogears.org/) | [github.com/TurboGears/tg2](https://github.com/TurboGears/tg2) |
| **Microframeworks** | Flask | [flask.palletsprojects.com](https://flask.palletsprojects.com/) | [github.com/pallets/flask](https://github.com/pallets/flask) |
| | FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) | [github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi) |
| | Litestar | [litestar.dev](https://litestar.dev/) | [github.com/litestar-org/litestar](https://github.com/litestar-org/litestar) |
| | Sanic | [sanic.dev](https://sanic.dev/) | [github.com/sanic-org/sanic](https://github.com/sanic-org/sanic) |
| | Tornado | [tornadoweb.org](https://www.tornadoweb.org/) | [github.com/tornadoweb/tornado](https://github.com/tornadoweb/tornado) |
| | Bottle | [bottlepy.org](https://bottlepy.org/) | [github.com/bottlepy/bottle](https://github.com/bottlepy/bottle) |
| **ASGI** | Starlette | [starlette.io](https://www.starlette.io/) | [github.com/encode/starlette](https://github.com/encode/starlette) |
| | Uvicorn | [uvicorn.org](https://www.uvicorn.org/) | [github.com/encode/uvicorn](https://github.com/encode/uvicorn) |
| | Hypercorn | [github.com/pgjones/hypercorn](https://github.com/pgjones/hypercorn) | [github.com/pgjones/hypercorn](https://github.com/pgjones/hypercorn) |

### 🧪 Testing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Test Frameworks** | pytest | [pytest.org](https://docs.pytest.org/) | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| | unittest (встроенный) | [docs.python.org/unittest](https://docs.python.org/3/library/unittest.html) | (встроен в Python) |
| | nose2 | [nose2.readthedocs.io](https://nose2.readthedocs.io/) | [github.com/nose-devs/nose2](https://github.com/nose-devs/nose2) |
| | doctest (встроенный) | [docs.python.org/doctest](https://docs.python.org/3/library/doctest.html) | (встроен в Python) |
| **Mocking** | mock (unittest.mock) | [docs.python.org/mock](https://docs.python.org/3/library/unittest.mock.html) | (встроен в Python) |
| | pytest-mock | [github.com/pytest-dev/pytest-mock](https://github.com/pytest-dev/pytest-mock) | [github.com/pytest-dev/pytest-mock](https://github.com/pytest-dev/pytest-mock) |
| | responses | [github.com/getsentry/responses](https://github.com/getsentry/responses) | [github.com/getsentry/responses](https://github.com/getsentry/responses) |
| **UI Testing** | Selenium | [selenium-python.readthedocs.io](https://selenium-python.readthedocs.io/) | [github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) |
| | Playwright | [playwright.dev/python](https://playwright.dev/python/) | [github.com/microsoft/playwright-python](https://github.com/microsoft/playwright-python) |
| **BDD** | behave | [behave.readthedocs.io](https://behave.readthedocs.io/) | [github.com/behave/behave](https://github.com/behave/behave) |
| | robotframework | [robotframework.org](https://robotframework.org/) | [github.com/robotframework/robotframework](https://github.com/robotframework/robotframework) |
| **Property-Based** | Hypothesis | [hypothesis.readthedocs.io](https://hypothesis.readthedocs.io/) | [github.com/HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) |
| **Fixtures** | factory_boy | [factoryboy.readthedocs.io](https://factoryboy.readthedocs.io/) | [github.com/FactoryBoy/factory_boy](https://github.com/FactoryBoy/factory_boy) |
| | mixer | [github.com/klen/mixer](https://github.com/klen/mixer) | [github.com/klen/mixer](https://github.com/klen/mixer) |

### 🛡️ Resilience & Retry

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Resilience** | Tenacity | [tenacity.readthedocs.io](https://tenacity.readthedocs.io/) | [github.com/jd/tenacity](https://github.com/jd/tenacity) |
| | backoff | [github.com/litl/backoff](https://github.com/litl/backoff) | [github.com/litl/backoff](https://github.com/litl/backoff) |
| | pybreaker | [github.com/danielfm/pybreaker](https://github.com/danielfm/pybreaker) | [github.com/danielfm/pybreaker](https://github.com/danielfm/pybreaker) |

### 💾 Object Storage

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Cloud Storage** | Boto3 (AWS S3) | [boto3.amazonaws.com](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) | [github.com/boto/boto3](https://github.com/boto/boto3) |
| | MinIO Python SDK | [min.io/docs/minio/linux/developers/python](https://min.io/docs/minio/linux/developers/python) | [github.com/minio/minio-py](https://github.com/minio/minio-py) |
| | google-cloud-storage | [cloud.google.com/python/docs/reference/storage](https://cloud.google.com/python/docs/reference/storage/latest) | [github.com/googleapis/python-storage](https://github.com/googleapis/python-storage) |
| | azure-storage-blob | [learn.microsoft.com/azure/storage/blobs](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python) | [github.com/Azure/azure-sdk-for-python](https://github.com/Azure/azure-sdk-for-python) |

### 📄 Office & Document Processing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Excel** | OpenPyXL | [openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/) | [github.com/theorchard/openpyxl](https://github.com/theorchard/openpyxl) |
| | XlsxWriter | [xlsxwriter.readthedocs.io](https://xlsxwriter.readthedocs.io/) | [github.com/jmcnamara/XlsxWriter](https://github.com/jmcnamara/XlsxWriter) |
| | xlrd / xlwt | [github.com/python-excel/xlrd](https://github.com/python-excel/xlrd) | [github.com/python-excel](https://github.com/python-excel) |
| | pandas (Excel IO) | [pandas.pydata.org](https://pandas.pydata.org/) | [github.com/pandas-dev/pandas](https://github.com/pandas-dev/pandas) |
| **Word** | python-docx | [python-docx.readthedocs.io](https://python-docx.readthedocs.io/) | [github.com/python-openxml/python-docx](https://github.com/python-openxml/python-docx) |
| **PDF** | ReportLab | [reportlab.com](https://www.reportlab.com/) | [github.com/MrBitBucket/reportlab](https://github.com/MrBitBucket/reportlab) |
| | PyPDF (pypdf) | [pypdf.readthedocs.io](https://pypdf.readthedocs.io/) | [github.com/py-pdf/pypdf](https://github.com/py-pdf/pypdf) |
| | pdfplumber | [github.com/jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) | [github.com/jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) |
| | WeasyPrint | [weasyprint.org](https://weasyprint.org/) | [github.com/Kozea/WeasyPrint](https://github.com/Kozea/WeasyPrint) |
| **CSV** | csv (встроенный) | [docs.python.org/csv](https://docs.python.org/3/library/csv.html) | (встроен в Python) |
| | polars | [pola.rs](https://pola.rs/) | [github.com/pola-rs/polars](https://github.com/pola-rs/polars) |

### 🗄️ ORM & Data Access

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Full ORM** | SQLAlchemy | [sqlalchemy.org](https://www.sqlalchemy.org/) | [github.com/sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) |
| | Django ORM (встроенный в Django) | [docs.djangoproject.com/topics/db](https://docs.djangoproject.com/en/stable/topics/db/) | [github.com/django/django](https://github.com/django/django) |
| | Peewee | [docs.peewee-orm.com](https://docs.peewee-orm.com/) | [github.com/coleifer/peewee](https://github.com/coleifer/peewee) |
| | PonyORM | [ponyorm.com](https://ponyorm.com/) | [github.com/ponyorm/pony](https://github.com/ponyorm/pony) |
| | SQLModel | [sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com/) | [github.com/tiangolo/sqlmodel](https://github.com/tiangolo/sqlmodel) |
| **Migrations** | Alembic | [alembic.sqlalchemy.org](https://alembic.sqlalchemy.org/) | [github.com/sqlalchemy/alembic](https://github.com/sqlalchemy/alembic) |
| | Django Migrations (встроенный) | [docs.djangoproject.com/topics/migrations](https://docs.djangoproject.com/en/stable/topics/migrations/) | [github.com/django/django](https://github.com/django/django) |
| **NoSQL** | pymongo | [pymongo.readthedocs.io](https://pymongo.readthedocs.io/) | [github.com/mongodb/mongo-python-driver](https://github.com/mongodb/mongo-python-driver) |
| | motor (async MongoDB) | [motor.readthedocs.io](https://motor.readthedocs.io/) | [github.com/mongodb/motor](https://github.com/mongodb/motor) |
| | redis-py | [redis-py.readthedocs.io](https://redis-py.readthedocs.io/) | [github.com/redis/redis-py](https://github.com/redis/redis-py) |
| | elasticsearch-py | [elasticsearch-py.readthedocs.io](https://elasticsearch-py.readthedocs.io/) | [github.com/elastic/elasticsearch-py](https://github.com/elastic/elasticsearch-py) |

### 🤖 ML/AI & Data Science

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Deep Learning** | TensorFlow | [tensorflow.org](https://www.tensorflow.org/) | [github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) |
| | PyTorch | [pytorch.org](https://pytorch.org/) | [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) |
| | JAX | [jax.readthedocs.io](https://jax.readthedocs.io/) | [github.com/google/jax](https://github.com/google/jax) |
| | Keras | [keras.io](https://keras.io/) | [github.com/keras-team/keras](https://github.com/keras-team/keras) |
| **Classical ML** | Scikit-learn | [scikit-learn.org](https://scikit-learn.org/) | [github.com/scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) |
| | XGBoost | [xgboost.ai](https://xgboost.ai/) | [github.com/dmlc/xgboost](https://github.com/dmlc/xgboost) |
| | LightGBM | [lightgbm.readthedocs.io](https://lightgbm.readthedocs.io/) | [github.com/microsoft/LightGBM](https://github.com/microsoft/LightGBM) |
| | CatBoost | [catboost.ai](https://catboost.ai/) | [github.com/catboost/catboost](https://github.com/catboost/catboost) |
| **NLP / LLM** | Hugging Face Transformers | [huggingface.co/transformers](https://huggingface.co/transformers/) | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| | LangChain | [langchain.com](https://www.langchain.com/) | [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| | LlamaIndex | [llamaindex.ai](https://www.llamaindex.ai/) | [github.com/run-llama/llama_index](https://github.com/run-llama/llama_index) |
| | spaCy | [spacy.io](https://spacy.io/) | [github.com/explosion/spaCy](https://github.com/explosion/spaCy) |
| | NLTK | [nltk.org](https://www.nltk.org/) | [github.com/nltk/nltk](https://github.com/nltk/nltk) |
| **Data Analysis** | pandas | [pandas.pydata.org](https://pandas.pydata.org/) | [github.com/pandas-dev/pandas](https://github.com/pandas-dev/pandas) |
| | NumPy | [numpy.org](https://numpy.org/) | [github.com/numpy/numpy](https://github.com/numpy/numpy) |
| | Polars | [pola.rs](https://pola.rs/) | [github.com/pola-rs/polars](https://github.com/pola-rs/polars) |
| **Visualization** | Matplotlib | [matplotlib.org](https://matplotlib.org/) | [github.com/matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) |
| | Seaborn | [seaborn.pydata.org](https://seaborn.pydata.org/) | [github.com/mwaskom/seaborn](https://github.com/mwaskom/seaborn) |
| | Plotly | [plotly.com/python](https://plotly.com/python/) | [github.com/plotly/plotly.py](https://github.com/plotly/plotly.py) |
| | Bokeh | [bokeh.org](https://bokeh.org/) | [github.com/bokeh/bokeh](https://github.com/bokeh/bokeh) |
| **Computer Vision** | OpenCV | [opencv.org](https://opencv.org/) | [github.com/opencv/opencv](https://github.com/opencv/opencv) |
| | Pillow | [python-pillow.org](https://python-pillow.org/) | [github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow) |
| | scikit-image | [scikit-image.org](https://scikit-image.org/) | [github.com/scikit-image/scikit-image](https://github.com/scikit-image/scikit-image) |

### 📨 Message Queue & Task Queues

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Task Queues** | Celery | [docs.celeryq.dev](https://docs.celeryq.dev/) | [github.com/celery/celery](https://github.com/celery/celery) |
| | RQ (Redis Queue) | [python-rq.org](https://python-rq.org/) | [github.com/rq/rq](https://github.com/rq/rq) |
| | Dramatiq | [dramatiq.io](https://dramatiq.io/) | [github.com/Bogdanp/dramatiq](https://github.com/Bogdanp/dramatiq) |
| | Huey | [huey.readthedocs.io](https://huey.readthedocs.io/) | [github.com/coleifer/huey](https://github.com/coleifer/huey) |
| **Message Brokers** | confluent-kafka-python | [docs.confluent.io/kafka-clients/python](https://docs.confluent.io/kafka-clients/python/) | [github.com/confluentinc/confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python) |
| | pika (RabbitMQ) | [pika.readthedocs.io](https://pika.readthedocs.io/) | [github.com/pika/pika](https://github.com/pika/pika) |
| | aio-pika (async RabbitMQ) | [aio-pika.readthedocs.io](https://aio-pika.readthedocs.io/) | [github.com/mosquito/aio-pika](https://github.com/mosquito/aio-pika) |

### 🛠️ Utility & Tooling

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **HTTP Clients** | requests | [requests.readthedocs.io](https://requests.readthedocs.io/) | [github.com/psf/requests](https://github.com/psf/requests) |
| | httpx (async) | [python-httpx.org](https://www.python-httpx.org/) | [github.com/encode/httpx](https://github.com/encode/httpx) |
| | aiohttp | [docs.aiohttp.org](https://docs.aiohttp.org/) | [github.com/aio-libs/aiohttp](https://github.com/aio-libs/aiohttp) |
| **Web Scraping** | BeautifulSoup4 | [www.crummy.com/software/BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) | [github.com/getanewsletter/BeautifulSoup4](https://github.com/getanewsletter/BeautifulSoup4) |
| | Scrapy | [scrapy.org](https://scrapy.org/) | [github.com/scrapy/scrapy](https://github.com/scrapy/scrapy) |
| | parsel | [parsel.readthedocs.io](https://parsel.readthedocs.io/) | [github.com/scrapy/parsel](https://github.com/scrapy/parsel) |
| **Validation** | Pydantic | [docs.pydantic.dev](https://docs.pydantic.dev/) | [github.com/pydantic/pydantic](https://github.com/pydantic/pydantic) |
| | marshmallow | [marshmallow.readthedocs.io](https://marshmallow.readthedocs.io/) | [github.com/marshmallow-code/marshmallow](https://github.com/marshmallow-code/marshmallow) |
| | attrs | [attrs.readthedocs.io](https://www.attrs.org/) | [github.com/python-attrs/attrs](https://github.com/python-attrs/attrs) |
| **CLI** | Typer | [typer.tiangolo.com](https://typer.tiangolo.com/) | [github.com/tiangolo/typer](https://github.com/tiangolo/typer) |
| | Click | [click.palletsprojects.com](https://click.palletsprojects.com/) | [github.com/pallets/click](https://github.com/pallets/click) |
| | argparse (встроенный) | [docs.python.org/argparse](https://docs.python.org/3/library/argparse.html) | (встроен в Python) |
| **Type Checking** | mypy | [mypy-lang.org](https://mypy-lang.org/) | [github.com/python/mypy](https://github.com/python/mypy) |
| | pyright | [github.com/microsoft/pyright](https://github.com/microsoft/pyright) | [github.com/microsoft/pyright](https://github.com/microsoft/pyright) |
| **Code Quality** | Ruff | [docs.astral.sh/ruff](https://docs.astral.sh/ruff/) | [github.com/astral-sh/ruff](https://github.com/astral-sh/ruff) |
| | Black | [black.readthedocs.io](https://black.readthedocs.io/) | [github.com/psf/black](https://github.com/psf/black) |
| | isort | [pycqa.github.io/isort](https://pycqa.github.io/isort/) | [github.com/PyCQA/isort](https://github.com/PyCQA/isort) |
| | flake8 | [flake8.pycqa.org](https://flake8.pycqa.org/) | [github.com/PyCQA/flake8](https://github.com/PyCQA/flake8) |
| **Package Management** | Poetry | [python-poetry.org](https://python-poetry.org/) | [github.com/python-poetry/poetry](https://github.com/python-poetry/poetry) |
| | uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) | [github.com/astral-sh/uv](https://github.com/astral-sh/uv) |
| | pipenv | [pipenv.pypa.io](https://pipenv.pypa.io/) | [github.com/pypa/pipenv](https://github.com/pypa/pipenv) |
| | hatch | [hatch.pypa.io](https://hatch.pypa.io/) | [github.com/pypa/hatch](https://github.com/pypa/hatch) |
| **Date/Time** | pendulum | [pendulum.eustace.io](https://pendulum.eustace.io/) | [github.com/sdispater/pendulum](https://github.com/sdispater/pendulum) |
| | arrow | [arrow.readthedocs.io](https://arrow.readthedocs.io/) | [github.com/arrow-py/arrow](https://github.com/arrow-py/arrow) |
| **Environment** | python-dotenv | [saurabh-kumar.com/python-dotenv](https://saurabh-kumar.com/python-dotenv/) | [github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv) |
| | dynaconf | [dynaconf.com](https://dynaconf.com/) | [github.com/dynaconf/dynaconf](https://github.com/dynaconf/dynaconf) |

---

## 🟨 JAVASCRIPT / TYPESCRIPT ЭКОСИСТЕМА (Node.js + Frontend)

### 📨 Message Queue (Node.js)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Brokers** | amqplib (RabbitMQ) | [github.com/amqp-node/amqplib](https://github.com/amqp-node/amqplib) | [github.com/amqp-node/amqplib](https://github.com/amqp-node/amqplib) |
| | kafkajs (Kafka) | [kafkajs.github.io](https://kafkajs.github.io/) | [github.com/tulios/kafkajs](https://github.com/tulios/kafkajs) |
| | ioredis | [github.com/redis/ioredis](https://github.com/redis/ioredis) | [github.com/redis/ioredis](https://github.com/redis/ioredis) |
| **Task Queues** | Bull (Redis queues) | [github.com/OptimalBits/bull](https://github.com/OptimalBits/bull) | [github.com/OptimalBits/bull](https://github.com/OptimalBits/bull) |
| | BullMQ | [bullmq.io](https://bullmq.io/) | [github.com/taskforcesh/bullmq](https://github.com/taskforcesh/bullmq) |
| | Bee-Queue | [github.com/bee-queue/bee-queue](https://github.com/bee-queue/bee-queue) | [github.com/bee-queue/bee-queue](https://github.com/bee-queue/bee-queue) |
| **Cloud** | AWS SQS (Node.js SDK) | [aws.amazon.com/sdk-for-javascript](https://aws.amazon.com/sdk-for-javascript/) | [github.com/aws/aws-sdk-js-v3](https://github.com/aws/aws-sdk-js-v3) |

### 🌐 Web Frameworks (Node.js)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Full-Stack** | NestJS | [nestjs.com](https://nestjs.com/) | [github.com/nestjs/nest](https://github.com/nestjs/nest) |
| | AdonisJS | [adonisjs.com](https://adonisjs.com/) | [github.com/adonisjs/core](https://github.com/adonisjs/core) |
| **Microframeworks** | Express.js | [expressjs.com](https://expressjs.com/) | [github.com/expressjs/express](https://github.com/expressjs/express) |
| | Fastify | [fastify.io](https://fastify.io/) | [github.com/fastify/fastify](https://github.com/fastify/fastify) |
| | Koa | [koajs.com](https://koajs.com/) | [github.com/koajs/koa](https://github.com/koajs/koa) |
| | Hono | [hono.dev](https://hono.dev/) | [github.com/honojs/hono](https://github.com/honojs/hono) |
| | Sails.js | [sailsjs.com](https://sailsjs.com/) | [github.com/balderdashy/sails](https://github.com/balderdashy/sails) |
| **Serverless** | Serverless Framework | [serverless.com](https://www.serverless.com/) | [github.com/serverless/serverless](https://github.com/serverless/serverless) |
| | AWS CDK | [docs.aws.amazon.com/cdk](https://docs.aws.amazon.com/cdk/v2/guide/home.html) | [github.com/aws/aws-cdk](https://github.com/aws/aws-cdk) |

### 🎨 Frontend Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **UI Libraries** | React | [react.dev](https://react.dev/) | [github.com/facebook/react](https://github.com/facebook/react) |
| | Angular | [angular.dev](https://angular.dev/) | [github.com/angular/angular](https://github.com/angular/angular) |
| | Vue.js | [vuejs.org](https://vuejs.org/) | [github.com/vuejs/core](https://github.com/vuejs/core) |
| | Svelte / SvelteKit | [svelte.dev](https://svelte.dev/) | [github.com/sveltejs/svelte](https://github.com/sveltejs/svelte) |
| | Solid.js | [solidjs.com](https://www.solidjs.com/) | [github.com/solidjs/solid](https://github.com/solidjs/solid) |
| | Qwik | [qwik.dev](https://qwik.dev/) | [github.com/QwikDev/qwik](https://github.com/QwikDev/qwik) |
| **Meta-Frameworks** | Next.js | [nextjs.org](https://nextjs.org/) | [github.com/vercel/next.js](https://github.com/vercel/next.js) |
| | Nuxt | [nuxt.com](https://nuxt.com/) | [github.com/nuxt/nuxt](https://github.com/nuxt/nuxt) |
| | Remix | [remix.run](https://remix.run/) | [github.com/remix-run/remix](https://github.com/remix-run/remix) |
| | Astro | [astro.build](https://astro.build/) | [github.com/withastro/astro](https://github.com/withastro/astro) |
| | SvelteKit | [kit.svelte.dev](https://kit.svelte.dev/) | [github.com/sveltejs/kit](https://github.com/sveltejs/kit) |
| **Lightweight** | Alpine.js | [alpinejs.dev](https://alpinejs.dev/) | [github.com/alpinejs/alpine](https://github.com/alpinejs/alpine) |
| | HTMX | [htmx.org](https://htmx.org/) | [github.com/bigskysoftware/htmx](https://github.com/bigskysoftware/htmx) |
| | Preact | [preactjs.com](https://preactjs.com/) | [github.com/preactjs/preact](https://github.com/preactjs/preact) |
| | Lit | [lit.dev](https://lit.dev/) | [github.com/lit/lit](https://github.com/lit/lit) |
| **Legacy** | jQuery | [jquery.com](https://jquery.com/) | [github.com/jquery/jquery](https://github.com/jquery/jquery) |
| | Backbone.js | [backbonejs.org](https://backbonejs.org/) | [github.com/jashkenas/backbone](https://github.com/jashkenas/backbone) |
| **UI Component Libraries** | Material UI (MUI) | [mui.com](https://mui.com/) | [github.com/mui/material-ui](https://github.com/mui/material-ui) |
| | Ant Design | [ant.design](https://ant.design/) | [github.com/ant-design/ant-design](https://github.com/ant-design/ant-design) |
| | Chakra UI | [chakra-ui.com](https://chakra-ui.com/) | [github.com/chakra-ui/chakra-ui](https://github.com/chakra-ui/chakra-ui) |
| | shadcn/ui | [ui.shadcn.com](https://ui.shadcn.com/) | [github.com/shadcn-ui/ui](https://github.com/shadcn-ui/ui) |
| | Radix UI | [radix-ui.com](https://www.radix-ui.com/) | [github.com/radix-ui/primitives](https://github.com/radix-ui/primitives) |
| | Tailwind CSS | [tailwindcss.com](https://tailwindcss.com/) | [github.com/tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss) |
| | Bootstrap | [getbootstrap.com](https://getbootstrap.com/) | [github.com/twbs/bootstrap](https://github.com/twbs/bootstrap) |

### 🗂️ State Management (JS)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **React** | Redux Toolkit | [redux-toolkit.ts.org](https://redux-toolkit.ts.org/) | [github.com/reduxjs/redux-toolkit](https://github.com/reduxjs/redux-toolkit) |
| | Zustand | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) |
| | Jotai | [jotai.org](https://jotai.org/) | [github.com/pmndrs/jotai](https://github.com/pmndrs/jotai) |
| | Recoil | [recoiljs.org](https://recoiljs.org/) | [github.com/facebookexperimental/Recoil](https://github.com/facebookexperimental/Recoil) |
| | MobX | [mobx.js.org](https://mobx.js.org/) | [github.com/mobxjs/mobx](https://github.com/mobxjs/mobx) |
| | TanStack Query | [tanstack.com/query](https://tanstack.com/query) | [github.com/TanStack/query](https://github.com/TanStack/query) |
| **Vue** | Pinia | [pinia.vuejs.org](https://pinia.vuejs.org/) | [github.com/vuejs/pinia](https://github.com/vuejs/pinia) |
| | Vuex (legacy) | [vuex.vuejs.org](https://vuex.vuejs.org/) | [github.com/vuejs/vuex](https://github.com/vuejs/vuex) |
| **Angular** | NgRx | [ngrx.io](https://ngrx.io/) | [github.com/ngrx/platform](https://github.com/ngrx/platform) |
| | Akita | [opensource.salesforce.com/akita](https://opensource.salesforce.com/akita/) | [github.com/salesforce/akita](https://github.com/salesforce/akita) |
| **Cross-Framework** | Redux (vanilla) | [redux.js.org](https://redux.js.org/) | [github.com/reduxjs/redux](https://github.com/reduxjs/redux) |
| | XState | [stately.ai/docs](https://stately.ai/docs) | [github.com/statelyai/xstate](https://github.com/statelyai/xstate) |

### 🧪 Testing (JS)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Test Runners** | Vitest | [vitest.dev](https://vitest.dev/) | [github.com/vitest-dev/vitest](https://github.com/vitest-dev/vitest) |
| | Jest | [jestjs.io](https://jestjs.io/) | [github.com/jestjs/jest](https://github.com/jestjs/jest) |
| | Mocha | [mochajs.org](https://mochajs.org/) | [github.com/mochajs/mocha](https://github.com/mochajs/mocha) |
| | Jasmine | [jasmine.github.io](https://jasmine.github.io/) | [github.com/jasmine/jasmine](https://github.com/jasmine/jasmine) |
| **E2E Testing** | Cypress | [cypress.io](https://www.cypress.io/) | [github.com/cypress-io/cypress](https://github.com/cypress-io/cypress) |
| | Playwright (JS) | [playwright.dev](https://playwright.dev/) | [github.com/microsoft/playwright](https://github.com/microsoft/playwright) |
| | Puppeteer | [pptr.dev](https://pptr.dev/) | [github.com/puppeteer/puppeteer](https://github.com/puppeteer/puppeteer) |
| | WebdriverIO | [webdriver.io](https://webdriver.io/) | [github.com/webdriverio/webdriverio](https://github.com/webdriverio/webdriverio) |
| **Mocking** | Sinon.js | [sinonjs.org](https://sinonjs.org/) | [github.com/sinonjs/sinon](https://github.com/sinonjs/sinon) |
| | MSW (Mock Service Worker) | [mswjs.io](https://mswjs.io/) | [github.com/mswjs/msw](https://github.com/mswjs/msw) |
| **Assertions** | Chai | [chaijs.com](https://www.chaijs.com/) | [github.com/chaijs/chai](https://github.com/chaijs/chai) |
| | expect (Jest) | [jestjs.io/docs/expect](https://jestjs.io/docs/expect) | (часть Jest) |
| **React Testing** | React Testing Library | [testing-library.com/docs/react-testing-library](https://testing-library.com/docs/react-testing-library/intro/) | [github.com/testing-library/react-testing-library](https://github.com/testing-library/react-testing-library) |
| **Coverage** | Istanbul / nyc | [istanbul.js.org](https://istanbul.js.org/) | [github.com/istanbuljs/nyc](https://github.com/istanbuljs/nyc) |
| | c8 | [github.com/bcoe/c8](https://github.com/bcoe/c8) | [github.com/bcoe/c8](https://github.com/bcoe/c8) |

### 🗄️ ORM & Data Access (Node.js)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Full ORM** | Prisma | [prisma.io](https://www.prisma.io/) | [github.com/prisma/prisma](https://github.com/prisma/prisma) |
| | TypeORM | [typeorm.io](https://typeorm.io/) | [github.com/typeorm/typeorm](https://github.com/typeorm/typeorm) |
| | Sequelize | [sequelize.org](https://sequelize.org/) | [github.com/sequelize/sequelize](https://github.com/sequelize/sequelize) |
| | MikroORM | [mikro-orm.io](https://mikro-orm.io/) | [github.com/mikro-orm/mikro-orm](https://github.com/mikro-orm/mikro-orm) |
| | Mongoose (MongoDB) | [mongoosejs.com](https://mongoosejs.com/) | [github.com/Automattic/mongoose](https://github.com/Automattic/mongoose) |
| **Query Builders** | Drizzle ORM | [orm.drizzle.team](https://orm.drizzle.team/) | [github.com/drizzle-team/drizzle-orm](https://github.com/drizzle-team/drizzle-orm) |
| | Knex.js | [knexjs.org](https://knexjs.org/) | [github.com/knex/knex](https://github.com/knex/knex) |
| | Kysely | [kysely.dev](https://kysely.dev/) | [github.com/kysely-org/kysely](https://github.com/kysely-org/kysely) |
| | Prisma (query builder mode) | [prisma.io](https://www.prisma.io/) | [github.com/prisma/prisma](https://github.com/prisma/prisma) |
| **NoSQL Clients** | mongodb (official) | [mongodb.com/docs/drivers/node](https://www.mongodb.com/docs/drivers/node/current/) | [github.com/mongodb/node-mongodb-native](https://github.com/mongodb/node-mongodb-native) |
| | @elastic/elasticsearch | [elastic.co/guide/en/elasticsearch/client/javascript-api](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/index.html) | [github.com/elastic/elasticsearch-js](https://github.com/elastic/elasticsearch-js) |

### 🔌 API & HTTP Clients (Node.js)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **HTTP Clients** | Axios | [axios-http.com](https://axios-http.com/) | [github.com/axios/axios](https://github.com/axios/axios) |
| | Fetch API (встроенный) | [developer.mozilla.org/fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) | (встроен в Node.js 18+) |
| | got | [github.com/sindresorhus/got](https://github.com/sindresorhus/got) | [github.com/sindresorhus/got](https://github.com/sindresorhus/got) |
| | node-fetch | [github.com/node-fetch/node-fetch](https://github.com/node-fetch/node-fetch) | [github.com/node-fetch/node-fetch](https://github.com/node-fetch/node-fetch) |
| | undici | [github.com/nodejs/undici](https://github.com/nodejs/undici) | [github.com/nodejs/undici](https://github.com/nodejs/undici) |
| **GraphQL** | Apollo Client | [apollographql.com/docs/react](https://www.apollographql.com/docs/react/) | [github.com/apollographql/apollo-client](https://github.com/apollographql/apollo-client) |
| | urql | [commerce.nearform.com/open-source/urql](https://commerce.nearform.com/open-source/urql/) | [github.com/urql-graphql/urql](https://github.com/urql-graphql/urql) |
| | Relay | [relay.dev](https://relay.dev/) | [github.com/facebook/relay](https://github.com/facebook/relay) |
| | graphql-request | [github.com/prisma-labs/graphql-request](https://github.com/prisma-labs/graphql-request) | [github.com/prisma-labs/graphql-request](https://github.com/prisma-labs/graphql-request) |
| **Realtime** | Socket.IO | [socket.io](https://socket.io/) | [github.com/socketio/socket.io](https://github.com/socketio/socket.io) |
| | ws | [github.com/websockets/ws](https://github.com/websockets/ws) | [github.com/websockets/ws](https://github.com/websockets/ws) |
| | GraphQL Subscriptions | [github.com/apollographql/subscriptions-transport-ws](https://github.com/apollographql/subscriptions-transport-ws) | [github.com/apollographql/subscriptions-transport-ws](https://github.com/apollographql/subscriptions-transport-ws) |

### 🛠️ Utility Libraries

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Validation** | Zod | [zod.dev](https://zod.dev/) | [github.com/colinhacks/zod](https://github.com/colinhacks/zod) |
| | Yup | [github.com/jquense/yup](https://github.com/jquense/yup) | [github.com/jquense/yup](https://github.com/jquense/yup) |
| | Joi | [joi.dev](https://joi.dev/) | [github.com/hapijs/joi](https://github.com/hapijs/joi) |
| | io-ts | [github.com/gcanti/io-ts](https://github.com/gcanti/io-ts) | [github.com/gcanti/io-ts](https://github.com/gcanti/io-ts) |
| | Ajv (JSON Schema) | [ajv.js.org](https://ajv.js.org/) | [github.com/ajv-validator/ajv](https://github.com/ajv-validator/ajv) |
| **Functional** | Lodash | [lodash.com](https://lodash.com/) | [github.com/lodash/lodash](https://github.com/lodash/lodash) |
| | Ramda | [ramdajs.com](https://ramdajs.com/) | [github.com/ramda/ramda](https://github.com/ramda/ramda) |
| | date-fns | [date-fns.org](https://date-fns.org/) | [github.com/date-fns/date-fns](https://github.com/date-fns/date-fns) |
| | dayjs | [day.js.org](https://day.js.org/) | [github.com/iamkun/dayjs](https://github.com/iamkun/dayjs) |
| | Luxon | [moment.github.io/luxon](https://moment.github.io/luxon/) | [github.com/moment/luxon](https://github.com/moment/luxon) |
| **Logging** | winston | [github.com/winstonjs/winston](https://github.com/winstonjs/winston) | [github.com/winstonjs/winston](https://github.com/winstonjs/winston) |
| | pino | [getpino.io](https://getpino.io/) | [github.com/pinojs/pino](https://github.com/pinojs/pino) |
| | debug | [github.com/debug-js/debug](https://github.com/debug-js/debug) | [github.com/debug-js/debug](https://github.com/debug-js/debug) |
| **CLI** | commander | [github.com/tj/commander.js](https://github.com/tj/commander.js) | [github.com/tj/commander.js](https://github.com/tj/commander.js) |
| | yargs | [yargs.dev](https://yargs.dev/) | [github.com/yargs/yargs](https://github.com/yargs/yargs) |
| | inquirer | [github.com/SBoudrias/Inquirer.js](https://github.com/SBoudrias/Inquirer.js) | [github.com/SBoudrias/Inquirer.js](https://github.com/SBoudrias/Inquirer.js) |
| | chalk | [github.com/chalk/chalk](https://github.com/chalk/chalk) | [github.com/chalk/chalk](https://github.com/chalk/chalk) |
| **Config** | dotenv | [github.com/motdotla/dotenv](https://github.com/motdotla/dotenv) | [github.com/motdotla/dotenv](https://github.com/motdotla/dotenv) |
| | config | [github.com/node-config/node-config](https://github.com/node-config/node-config) | [github.com/node-config/node-config](https://github.com/node-config/node-config) |
| **Auth** | Passport.js | [passportjs.org](https://www.passportjs.org/) | [github.com/jaredhanson/passport](https://github.com/jaredhanson/passport) |
| | jsonwebtoken | [github.com/auth0/node-jsonwebtoken](https://github.com/auth0/node-jsonwebtoken) | [github.com/auth0/node-jsonwebtoken](https://github.com/auth0/node-jsonwebtoken) |
| | bcrypt | [github.com/kelektiv/node.bcrypt.js](https://github.com/kelektiv/node.bcrypt.js) | [github.com/kelektiv/node.bcrypt.js](https://github.com/kelektiv/node.bcrypt.js) |
| **File Upload** | multer | [github.com/expressjs/multer](https://github.com/expressjs/multer) | [github.com/expressjs/multer](https://github.com/expressjs/multer) |
| | busboy | [github.com/mscdex/busboy](https://github.com/mscdex/busboy) | [github.com/mscdex/busboy](https://github.com/mscdex/busboy) |
| **Image Processing** | sharp | [sharp.pixelplumbing.com](https://sharp.pixelplumbing.com/) | [github.com/lovell/sharp](https://github.com/lovell/sharp) |
| | jimp | [github.com/jimp-dev/jimp](https://github.com/jimp-dev/jimp) | [github.com/jimp-dev/jimp](https://github.com/jimp-dev/jimp) |
| **PDF** | pdf-lib | [pdf-lib.js.org](https://pdf-lib.js.org/) | [github.com/Hopding/pdf-lib](https://github.com/Hopding/pdf-lib) |
| | pdfkit | [pdfkit.org](https://pdfkit.org/) | [github.com/foliojs/pdfkit](https://github.com/foliojs/pdfkit) |
| **Excel** | ExcelJS | [github.com/exceljs/exceljs](https://github.com/exceljs/exceljs) | [github.com/exceljs/exceljs](https://github.com/exceljs/exceljs) |
| | xlsx (SheetJS) | [sheetjs.com](https://sheetjs.com/) | [github.com/SheetJS/sheetjs](https://github.com/SheetJS/sheetjs) |

### 📦 Build Tools & Bundlers

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Bundlers** | Vite | [vitejs.dev](https://vitejs.dev/) | [github.com/vitejs/vite](https://github.com/vitejs/vite) |
| | Webpack | [webpack.js.org](https://webpack.js.org/) | [github.com/webpack/webpack](https://github.com/webpack/webpack) |
| | Rollup | [rollupjs.org](https://rollupjs.org/) | [github.com/rollup/rollup](https://github.com/rollup/rollup) |
| | esbuild | [esbuild.github.io](https://esbuild.github.io/) | [github.com/evanw/esbuild](https://github.com/evanw/esbuild) |
| | Turbopack | [turbo.build/pack](https://turbo.build/pack) | (от создателей Next.js) |
| **Transpilers** | Babel | [babeljs.io](https://babeljs.io/) | [github.com/babel/babel](https://github.com/babel/babel) |
| | SWC | [swc.rs](https://swc.rs/) | [github.com/swc-project/swc](https://github.com/swc-project/swc) |
| | TypeScript | [typescriptlang.org](https://www.typescriptlang.org/) | [github.com/microsoft/TypeScript](https://github.com/microsoft/TypeScript) |
| | sucrase | [github.com/alangpierce/sucrase](https://github.com/alangpierce/sucrase) | [github.com/alangpierce/sucrase](https://github.com/alangpierce/sucrase) |
| **Task Runners** | npm scripts | [docs.npmjs.com](https://docs.npmjs.com/) | (встроен в npm) |
| | Turborepo | [turbo.build/repo](https://turbo.build/repo) | [github.com/vercel/turborepo](https://github.com/vercel/turborepo) |
| | Nx | [nx.dev](https://nx.dev/) | [github.com/nrwl/nx](https://github.com/nrwl/nx) |
| | pnpm | [pnpm.io](https://pnpm.io/) | [github.com/pnpm/pnpm](https://github.com/pnpm/pnpm) |
| | yarn | [yarnpkg.com](https://yarnpkg.com/) | [github.com/yarnpkg/berry](https://github.com/yarnpkg/berry) |

---

## 🐹 GO ЭКОСИСТЕМА

### 🌐 Web Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Frameworks** | Gin | [gin-gonic.com](https://gin-gonic.com/) | [github.com/gin-gonic/gin](https://github.com/gin-gonic/gin) |
| | Echo | [echo.labstack.com](https://echo.labstack.com/) | [github.com/labstack/echo](https://github.com/labstack/echo) |
| | Fiber | [gofiber.io](https://gofiber.io/) | [github.com/gofiber/fiber](https://github.com/gofiber/fiber) |
| | Chi | [github.com/go-chi/chi](https://github.com/go-chi/chi) | [github.com/go-chi/chi](https://github.com/go-chi/chi) |
| | Gorilla/Mux | [github.com/gorilla/mux](https://github.com/gorilla/mux) | [github.com/gorilla/mux](https://github.com/gorilla/mux) |
| | net/http (встроенный) | [pkg.go.dev/net/http](https://pkg.go.dev/net/http) | (встроен в Go) |
| **Full-Stack** | Buffalo | [gobuffalo.io](https://gobuffalo.io/) | [github.com/gobuffalo/buffalo](https://github.com/gobuffalo/buffalo) |
| | Beego | [beego.me](https://beego.me/) | [github.com/beego/beego](https://github.com/beego/beego) |
| **Microservices** | go-micro | [github.com/go-micro/plugins](https://github.com/go-micro/plugins) | [github.com/go-micro/go-micro](https://github.com/go-micro/go-micro) |
| | Kratos | [go-kratos.dev](https://go-kratos.dev/) | [github.com/go-kratos/kratos](https://github.com/go-kratos/kratos) |

### 🧪 Testing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Testing** | testing (встроенный) | [pkg.go.dev/testing](https://pkg.go.dev/testing) | (встроен) |
| | testify | [github.com/stretchr/testify](https://github.com/stretchr/testify) | [github.com/stretchr/testify](https://github.com/stretchr/testify) |
| | Ginkgo / Gomega | [onsi.github.io/ginkgo](https://onsi.github.io/ginkgo/) | [github.com/onsi/ginkgo](https://github.com/onsi/ginkgo) |
| | go-cmp | [pkg.go.dev/github.com/google/go-cmp](https://pkg.go.dev/github.com/google/go-cmp/cmp) | [github.com/google/go-cmp](https://github.com/google/go-cmp) |
| **Mocking** | GoMock | [github.com/uber-go/mock](https://github.com/uber-go/mock) | [github.com/uber-go/mock](https://github.com/uber-go/mock) |
| | mockery | [github.com/vektra/mockery](https://github.com/vektra/mockery) | [github.com/vektra/mockery](https://github.com/vektra/mockery) |
| | gomock (original) | [github.com/golang/mock](https://github.com/golang/mock) | [github.com/golang/mock](https://github.com/golang/mock) |
| **BDD** | GoConvey | [github.com/smartystreets/goconvey](https://github.com/smartystreets/goconvey) | [github.com/smartystreets/goconvey](https://github.com/smartystreets/goconvey) |
| **Benchmark** | testing.B (встроенный) | [pkg.go.dev/testing](https://pkg.go.dev/testing#hdr-Benchmarks) | (встроен) |
| | go-bench | [pkg.go.dev/golang.org/x/perf/benchstat](https://pkg.go.dev/golang.org/x/perf/benchstat) | [github.com/golang/perf](https://github.com/golang/perf) |
| **Fuzzing** | testing.F (встроенный, Go 1.18+) | [go.dev/doc/fuzz](https://go.dev/doc/fuzz/) | (встроен в Go 1.18+) |

### 🛡️ Resilience & Retry

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Resilience** | retry-go | [github.com/avast/retry-go](https://github.com/avast/retry-go) | [github.com/avast/retry-go](https://github.com/avast/retry-go) |
| | gobreaker | [github.com/sony/gobreaker](https://github.com/sony/gobreaker) | [github.com/sony/gobreaker](https://github.com/sony/gobreaker) |
| | go-resilience | [github.com/mattheath/go-resilience](https://github.com/mattheath/go-resilience) | [github.com/mattheath/go-resilience](https://github.com/mattheath/go-resilience) |
| | sony/gobreaker | [github.com/sony/gobreaker](https://github.com/sony/gobreaker) | [github.com/sony/gobreaker](https://github.com/sony/gobreaker) |

### 💾 Object Storage

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Cloud SDKs** | AWS SDK for Go v2 | [aws.amazon.com/sdk-for-go](https://aws.amazon.com/sdk-for-go/) | [github.com/aws/aws-sdk-go-v2](https://github.com/aws/aws-sdk-go-v2) |
| | MinIO Go SDK | [min.io/docs/minio/linux/developers/go](https://min.io/docs/minio/linux/developers/go) | [github.com/minio/minio-go](https://github.com/minio/minio-go) |
| | Google Cloud Go | [pkg.go.dev/cloud.google.com/go](https://pkg.go.dev/cloud.google.com/go) | [github.com/googleapis/google-cloud-go](https://github.com/googleapis/google-cloud-go) |
| | Azure SDK for Go | [learn.microsoft.com/azure/developer/go](https://learn.microsoft.com/en-us/azure/developer/go/) | [github.com/Azure/azure-sdk-for-go](https://github.com/Azure/azure-sdk-for-go) |

### 🗄️ ORM & Data Access

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Full ORM** | GORM | [gorm.io](https://gorm.io/) | [github.com/go-gorm/gorm](https://github.com/go-gorm/gorm) |
| | Ent (Facebook) | [entgo.io](https://entgo.io/) | [github.com/ent/ent](https://github.com/ent/ent) |
| **Query Builders** | sqlx | [github.com/jmoiron/sqlx](https://github.com/jmoiron/sqlx) | [github.com/jmoiron/sqlx](https://github.com/jmoiron/sqlx) |
| | sqlc | [sqlc.dev](https://sqlc.dev/) | [github.com/sqlc-dev/sqlc](https://github.com/sqlc-dev/sqlc) |
| | squirrel | [github.com/Masterminds/squirrel](https://github.com/Masterminds/squirrel) | [github.com/Masterminds/squirrel](https://github.com/Masterminds/squirrel) |
| | goqu | [github.com/doug-martin/goqu](https://github.com/doug-martin/goqu) | [github.com/doug-martin/goqu](https://github.com/doug-martin/goqu) |
| **Database Drivers** | pq (PostgreSQL) | [pkg.go.dev/github.com/lib/pq](https://pkg.go.dev/github.com/lib/pq) | [github.com/lib/pq](https://github.com/lib/pq) |
| | pgx (PostgreSQL) | [github.com/jackc/pgx](https://github.com/jackc/pgx) | [github.com/jackc/pgx](https://github.com/jackc/pgx) |
| | go-sql-driver/mysql | [github.com/go-sql-driver/mysql](https://github.com/go-sql-driver/mysql) | [github.com/go-sql-driver/mysql](https://github.com/go-sql-driver/mysql) |
| **Migrations** | golang-migrate | [github.com/golang-migrate/migrate](https://github.com/golang-migrate/migrate) | [github.com/golang-migrate/migrate](https://github.com/golang-migrate/migrate) |
| | goose | [github.com/pressly/goose](https://github.com/pressly/goose) | [github.com/pressly/goose](https://github.com/pressly/goose) |
| | atlas | [atlasgo.io](https://atlasgo.io/) | [github.com/ariga/atlas](https://github.com/ariga/atlas) |

### 📨 Message Queue

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Brokers** | confluent-kafka-go | [github.com/confluentinc/confluent-kafka-go](https://github.com/confluentinc/confluent-kafka-go) | [github.com/confluentinc/confluent-kafka-go](https://github.com/confluentinc/confluent-kafka-go) |
| | sarama (Kafka) | [github.com/IBM/sarama](https://github.com/IBM/sarama) | [github.com/IBM/sarama](https://github.com/IBM/sarama) |
| | amqp091-go (RabbitMQ) | [github.com/rabbitmq/amqp091-go](https://github.com/rabbitmq/amqp091-go) | [github.com/rabbitmq/amqp091-go](https://github.com/rabbitmq/amqp091-go) |
| | nats.go | [github.com/nats-io/nats.go](https://github.com/nats-io/nats.go) | [github.com/nats-io/nats.go](https://github.com/nats-io/nats.go) |
| **Task Queues** | Asynq | [github.com/hibiken/asynq](https://github.com/hibiken/asynq) | [github.com/hibiken/asynq](https://github.com/hibiken/asynq) |
| | Machinery | [github.com/RichardKnop/machinery](https://github.com/RichardKnop/machinery) | [github.com/RichardKnop/machinery](https://github.com/RichardKnop/machinery) |

### 🛠️ Utility Libraries

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Logging** | zap | [pkg.go.dev/go.uber.org/zap](https://pkg.go.dev/go.uber.org/zap) | [github.com/uber-go/zap](https://github.com/uber-go/zap) |
| | zerolog | [github.com/rs/zerolog](https://github.com/rs/zerolog) | [github.com/rs/zerolog](https://github.com/rs/zerolog) |
| | logrus | [github.com/sirupsen/logrus](https://github.com/sirupsen/logrus) | [github.com/sirupsen/logrus](https://github.com/sirupsen/logrus) |
| | slog (встроенный, Go 1.21+) | [pkg.go.dev/log/slog](https://pkg.go.dev/log/slog) | (встроен в Go 1.21+) |
| **CLI** | cobra | [github.com/spf13/cobra](https://github.com/spf13/cobra) | [github.com/spf13/cobra](https://github.com/spf13/cobra) |
| | urfave/cli | [cli.urfave.org](https://cli.urfave.org/) | [github.com/urfave/cli](https://github.com/urfave/cli) |
| | kingpin | [github.com/alecthomas/kingpin](https://github.com/alecthomas/kingpin) | [github.com/alecthomas/kingpin](https://github.com/alecthomas/kingpin) |
| **Config** | viper | [github.com/spf13/viper](https://github.com/spf13/viper) | [github.com/spf13/viper](https://github.com/spf13/viper) |
| | envconfig | [github.com/kelseyhightower/envconfig](https://github.com/kelseyhightower/envconfig) | [github.com/kelseyhightower/envconfig](https://github.com/kelseyhightower/envconfig) |
| **HTTP Clients** | resty | [github.com/go-resty/resty](https://github.com/go-resty/resty) | [github.com/go-resty/resty](https://github.com/go-resty/resty) |
| | net/http (встроенный) | [pkg.go.dev/net/http](https://pkg.go.dev/net/http) | (встроен в Go) |
| | gentoo | [github.com/gentleman-go/gentleman](https://github.com/gentleman-go/gentleman) | [github.com/gentleman-go/gentleman](https://github.com/gentleman-go/gentleman) |
| **Validation** | go-playground/validator | [github.com/go-playground/validator](https://github.com/go-playground/validator) | [github.com/go-playground/validator](https://github.com/go-playground/validator) |
| | ozzo-validation | [github.com/go-ozzo/ozzo-validation](https://github.com/go-ozzo/ozzo-validation) | [github.com/go-ozzo/ozzo-validation](https://github.com/go-ozzo/ozzo-validation) |
| **JSON** | encoding/json (встроенный) | [pkg.go.dev/encoding/json](https://pkg.go.dev/encoding/json) | (встроен в Go) |
| | jsoniter | [jsoniter.com](http://jsoniter.com/) | [github.com/json-iterator/go](https://github.com/json-iterator/go) |
| | sonic | [github.com/bytedance/sonic](https://github.com/bytedance/sonic) | [github.com/bytedance/sonic](https://github.com/bytedance/sonic) |
| **gRPC** | grpc-go | [grpc.io/docs/languages/go](https://grpc.io/docs/languages/go/) | [github.com/grpc/grpc-go](https://github.com/grpc/grpc-go) |
| | connect-go | [connectrpc.com](https://connectrpc.com/) | [github.com/connectrpc/connect-go](https://github.com/connectrpc/connect-go) |
| **GraphQL** | gqlgen | [gqlgen.com](https://gqlgen.com/) | [github.com/99designs/gqlgen](https://github.com/99designs/gqlgen) |
| | graphql-go | [github.com/graphql-go/graphql](https://github.com/graphql-go/graphql) | [github.com/graphql-go/graphql](https://github.com/graphql-go/graphql) |
| **Auth** | jwt-go | [github.com/golang-jwt/jwt](https://github.com/golang-jwt/jwt) | [github.com/golang-jwt/jwt](https://github.com/golang-jwt/jwt) |
| | casbin | [casbin.org](https://casbin.org/) | [github.com/casbin/casbin](https://github.com/casbin/casbin) |
| **Caching** | go-cache | [github.com/patrickmn/go-cache](https://github.com/patrickmn/go-cache) | [github.com/patrickmn/go-cache](https://github.com/patrickmn/go-cache) |
| | go-redis | [github.com/redis/go-redis](https://github.com/redis/go-redis) | [github.com/redis/go-redis](https://github.com/redis/go-redis) |
| | bigcache | [github.com/allegro/bigcache](https://github.com/allegro/bigcache) | [github.com/allegro/bigcache](https://github.com/allegro/bigcache) |
| **Date/Time** | now | [github.com/jinzhu/now](https://github.com/jinzhu/now) | [github.com/jinzhu/now](https://github.com/jinzhu/now) |
| | carbon | [github.com/uniplaces/carbon](https://github.com/uniplaces/carbon) | [github.com/uniplaces/carbon](https://github.com/uniplaces/carbon) |

---

## 🦀 RUST ЭКОСИСТЕМА

### 🌐 Web Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Frameworks** | Actix Web | [actix.rs](https://actix.rs/) | [github.com/actix/actix-web](https://github.com/actix/actix-web) |
| | Axum | [docs.rs/axum](https://docs.rs/axum/) | [github.com/tokio-rs/axum](https://github.com/tokio-rs/axum) |
| | Rocket | [rocket.rs](https://rocket.rs/) | [github.com/rwf2/Rocket](https://github.com/rwf2/Rocket) |
| | Warp | [docs.rs/warp](https://docs.rs/warp/) | [github.com/seanmonstar/warp](https://github.com/seanmonstar/warp) |
| | Tide | [docs.rs/tide](https://docs.rs/tide/) | [github.com/http-rs/tide](https://github.com/http-rs/tide) |
| | Poem | [github.com/poem-web/poem](https://github.com/poem-web/poem) | [github.com/poem-web/poem](https://github.com/poem-web/poem) |
| **Full-Stack** | Leptos | [leptos.dev](https://leptos.dev/) | [github.com/leptos-rs/leptos](https://github.com/leptos-rs/leptos) |
| | Yew | [yew.rs](https://yew.rs/) | [github.com/yewstack/yew](https://github.com/yewstack/yew) |
| | Dioxus | [dioxuslabs.com](https://dioxuslabs.com/) | [github.com/DioxusLabs/dioxus](https://github.com/DioxusLabs/dioxus) |
| | Sycamore | [sycamore-rs.netlify.app](https://sycamore-rs.netlify.app/) | [github.com/sycamore-rs/sycamore](https://github.com/sycamore-rs/sycamore) |

### 🧪 Testing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Testing** | cargo test (встроенный) | [doc.rust-lang.org/cargo/commands/cargo-test.html](https://doc.rust-lang.org/cargo/commands/cargo-test.html) | (встроен) |
| | Criterion (Benchmark) | [bheisler.github.io/criterion.rs](https://bheisler.github.io/criterion.rs/) | [github.com/bheisler/criterion.rs](https://github.com/bheisler/criterion.rs) |
| | proptest (Property-based) | [docs.rs/proptest](https://docs.rs/proptest/) | [github.com/proptest-rs/proptest](https://github.com/proptest-rs/proptest) |
| | mockall | [docs.rs/mockall](https://docs.rs/mockall/) | [github.com/asomers/mockall](https://github.com/asomers/mockall) |
| | rstest | [github.com/la10736/rstest](https://github.com/la10736/rstest) | [github.com/la10736/rstest](https://github.com/la10736/rstest) |

### 🗄️ ORM & Data Access

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **ORM** | Diesel | [diesel.rs](https://diesel.rs/) | [github.com/diesel-rs/diesel](https://github.com/diesel-rs/diesel) |
| | SeaORM | [www.sea-ql.org/SeaORM](https://www.sea-ql.org/SeaORM/) | [github.com/SeaQL/sea-orm](https://github.com/SeaQL/sea-orm) |
| | SQLx | [github.com/launchbadge/sqlx](https://github.com/launchbadge/sqlx) | [github.com/launchbadge/sqlx](https://github.com/launchbadge/sqlx) |
| | rustorm | [github.com/ivanceras/rustorm](https://github.com/ivanceras/rustorm) | [github.com/ivanceras/rustorm](https://github.com/ivanceras/rustorm) |
| **Database Drivers** | tokio-postgres | [docs.rs/tokio-postgres](https://docs.rs/tokio-postgres/) | [github.com/sfackler/rust-postgres](https://github.com/sfackler/rust-postgres) |
| | mysql_async | [docs.rs/mysql_async](https://docs.rs/mysql_async/) | [github.com/blackbeam/rust-mysql-simple](https://github.com/blackbeam/rust-mysql-simple) |
| | redis-rs | [github.com/redis-rs/redis-rs](https://github.com/redis-rs/redis-rs) | [github.com/redis-rs/redis-rs](https://github.com/redis-rs/redis-rs) |

### 🛠️ Utility Libraries

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Async Runtime** | tokio | [tokio.rs](https://tokio.rs/) | [github.com/tokio-rs/tokio](https://github.com/tokio-rs/tokio) |
| | async-std | [async-std.rs](https://async-std.rs/) | [github.com/async-rs/async-std](https://github.com/async-rs/async-std) |
| **Serialization** | serde | [serde.rs](https://serde.rs/) | [github.com/serde-rs/serde](https://github.com/serde-rs/serde) |
| | serde_json | [docs.rs/serde_json](https://docs.rs/serde_json/) | [github.com/serde-rs/json](https://github.com/serde-rs/json) |
| | bincode | [docs.rs/bincode](https://docs.rs/bincode/) | [github.com/bincode-org/bincode](https://github.com/bincode-org/bincode) |
| | toml | [docs.rs/toml](https://docs.rs/toml/) | [github.com/toml-rs/toml](https://github.com/toml-rs/toml) |
| | prost (protobuf) | [docs.rs/prost](https://docs.rs/prost/) | [github.com/tokio-rs/prost](https://github.com/tokio-rs/prost) |
| **HTTP Clients** | reqwest | [docs.rs/reqwest](https://docs.rs/reqwest/) | [github.com/seanmonstar/reqwest](https://github.com/seanmonstar/reqwest) |
| | hyper | [hyper.rs](https://hyper.rs/) | [github.com/hyperium/hyper](https://github.com/hyperium/hyper) |
| | ureq | [github.com/algesten/ureq](https://github.com/algesten/ureq) | [github.com/algesten/ureq](https://github.com/algesten/ureq) |
| **CLI** | clap | [clap.rs](https://clap.rs/) | [github.com/clap-rs/clap](https://github.com/clap-rs/clap) |
| | structopt (deprecated, use clap) | [docs.rs/structopt](https://docs.rs/structopt/) | [github.com/TeXitoi/structopt](https://github.com/TeXitoi/structopt) |
| **Logging** | tracing | [tokio-rs.github.io/tracing](https://tokio-rs.github.io/tracing/) | [github.com/tokio-rs/tracing](https://github.com/tokio-rs/tracing) |
| | log + env_logger | [docs.rs/log](https://docs.rs/log/) | [github.com/rust-lang/log](https://github.com/rust-lang/log) |
| | slog | [github.com/slog-rs/slog](https://github.com/slog-rs/slog) | [github.com/slog-rs/slog](https://github.com/slog-rs/slog) |
| **Error Handling** | anyhow | [docs.rs/anyhow](https://docs.rs/anyhow/) | [github.com/dtolnay/anyhow](https://github.com/dtolnay/anyhow) |
| | thiserror | [docs.rs/thiserror](https://docs.rs/thiserror/) | [github.com/dtolnay/thiserror](https://github.com/dtolnay/thiserror) |
| **Regex** | regex | [docs.rs/regex](https://docs.rs/regex/) | [github.com/rust-lang/regex](https://github.com/rust-lang/regex) |
| | fancy-regex | [docs.rs/fancy-regex](https://docs.rs/fancy-regex/) | [github.com/fancy-regex/fancy-regex](https://github.com/fancy-regex/fancy-regex) |
| **Date/Time** | chrono | [docs.rs/chrono](https://docs.rs/chrono/) | [github.com/chronotope/chrono](https://github.com/chronotope/chrono) |
| | time | [time-rs.github.io](https://time-rs.github.io/) | [github.com/time-rs/time](https://github.com/time-rs/time) |
| **Random** | rand | [docs.rs/rand](https://docs.rs/rand/) | [github.com/rust-random/rand](https://github.com/rust-random/rand) |
| **Cryptography** | ring | [github.com/briansmith/ring](https://github.com/briansmith/ring) | [github.com/briansmith/ring](https://github.com/briansmith/ring) |
| | rust-crypto | [github.com/DaGenix/rust-crypto](https://github.com/DaGenix/rust-crypto) | [github.com/DaGenix/rust-crypto](https://github.com/DaGenix/rust-crypto) |
| | rustls (TLS) | [github.com/rustls/rustls](https://github.com/rustls/rustls) | [github.com/rustls/rustls](https://github.com/rustls/rustls) |
| **Concurrency** | rayon (data parallelism) | [docs.rs/rayon](https://docs.rs/rayon/) | [github.com/rayon-rs/rayon](https://github.com/rayon-rs/rayon) |
| | crossbeam | [docs.rs/crossbeam](https://docs.rs/crossbeam/) | [github.com/crossbeam-rs/crossbeam](https://github.com/crossbeam-rs/crossbeam) |
| | parking_lot | [docs.rs/parking_lot](https://docs.rs/parking_lot/) | [github.com/Amanieu/parking_lot](https://github.com/Amanieu/parking_lot) |
| **Memory Safety** | arc-swap | [docs.rs/arc-swap](https://docs.rs/arc-swap/) | [github.com/vorner/arc-swap](https://github.com/vorner/arc-swap) |
| | once_cell | [docs.rs/once_cell](https://docs.rs/once_cell/) | [github.com/matklad/once_cell](https://github.com/matklad/once_cell) |
| | lazy_static | [docs.rs/lazy_static](https://docs.rs/lazy_static/) | [github.com/rust-lang-nursery/lazy-static.rs](https://github.com/rust-lang-nursery/lazy-static.rs) |

---

## ⚙️ C++ ЭКОСИСТЕМА

### 🧪 Testing & Benchmarking

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Testing** | Google Test | [github.com/google/googletest](https://github.com/google/googletest) | [github.com/google/googletest](https://github.com/google/googletest) |
| | Catch2 | [github.com/catchorg/Catch2](https://github.com/catchorg/Catch2) | [github.com/catchorg/Catch2](https://github.com/catchorg/Catch2) |
| | doctest | [github.com/doctest/doctest](https://github.com/doctest/doctest) | [github.com/doctest/doctest](https://github.com/doctest/doctest) |
| | Boost.Test | [boost.org/doc/libs/release/libs/test](https://www.boost.org/doc/libs/release/libs/test/doc/html/index.html) | [github.com/boostorg/test](https://github.com/boostorg/test) |
| **Mocking** | Google Mock | [github.com/google/googletest](https://github.com/google/googletest) | [github.com/google/googletest](https://github.com/google/googletest) |
| | FakeIt | [github.com/eranpeer/FakeIt](https://github.com/eranpeer/FakeIt) | [github.com/eranpeer/FakeIt](https://github.com/eranpeer/FakeIt) |
| | trompeloeil | [github.com/rollbear/trompeloeil](https://github.com/rollbear/trompeloeil) | [github.com/rollbear/trompeloeil](https://github.com/rollbear/trompeloeil) |
| **Benchmarking** | Google Benchmark | [github.com/google/benchmark](https://github.com/google/benchmark) | [github.com/google/benchmark](https://github.com/google/benchmark) |
| | Nonius | [github.com/libnonius/nonius](https://github.com/libnonius/nonius) | [github.com/libnonius/nonius](https://github.com/libnonius/nonius) |

### 🌐 Web Frameworks

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Frameworks** | Drogon | [drogon.org](https://drogon.org/) | [github.com/drogonframework/drogon](https://github.com/drogonframework/drogon) |
| | Crow | [crowcpp.org](https://crowcpp.org/) | [github.com/CrowCpp/Crow](https://github.com/CrowCpp/Crow) |
| | Oat++ | [oatpp.io](https://oatpp.io/) | [github.com/oatpp/oatpp](https://github.com/oatpp/oatpp) |
| | Pistache | [pistacheio.github.io](https://pistacheio.github.io/) | [github.com/pistacheio/pistache](https://github.com/pistacheio/pistache) |
| | cpp-httplib | [github.com/yhirose/cpp-httplib](https://github.com/yhirose/cpp-httplib) | [github.com/yhirose/cpp-httplib](https://github.com/yhirose/cpp-httplib) |
| **gRPC** | gRPC C++ | [grpc.io/docs/languages/cpp](https://grpc.io/docs/languages/cpp/) | [github.com/grpc/grpc](https://github.com/grpc/grpc) |

### 🛠️ Utility Libraries

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Core Libraries** | Boost | [boost.org](https://www.boost.org/) | [github.com/boostorg](https://github.com/boostorg) |
| | Abseil (Google) | [abseil.io](https://abseil.io/) | [github.com/abseil/abseil-cpp](https://github.com/abseil/abseil-cpp) |
| | Folly (Facebook) | [github.com/facebook/folly](https://github.com/facebook/folly) | [github.com/facebook/folly](https://github.com/facebook/folly) |
| **Logging** | spdlog | [github.com/gabime/spdlog](https://github.com/gabime/spdlog) | [github.com/gabime/spdlog](https://github.com/gabime/spdlog) |
| | glog (Google) | [github.com/google/glog](https://github.com/google/glog) | [github.com/google/glog](https://github.com/google/glog) |
| | Boost.Log | [boost.org/doc/libs/release/libs/log](https://www.boost.org/doc/libs/release/libs/log/doc/html/index.html) | [github.com/boostorg/log](https://github.com/boostorg/log) |
| **JSON** | nlohmann/json | [github.com/nlohmann/json](https://github.com/nlohmann/json) | [github.com/nlohmann/json](https://github.com/nlohmann/json) |
| | RapidJSON | [rapidjson.org](https://rapidjson.org/) | [github.com/Tencent/rapidjson](https://github.com/Tencent/rapidjson) |
| | jsoncpp | [github.com/open-source-parsers/jsoncpp](https://github.com/open-source-parsers/jsoncpp) | [github.com/open-source-parsers/jsoncpp](https://github.com/open-source-parsers/jsoncpp) |
| **String Formatting** | fmt | [fmt.dev](https://fmt.dev/) | [github.com/fmtlib/fmt](https://github.com/fmtlib/fmt) |
| **Networking** | Asio / Boost.Asio | [think-async.com/Asio](https://think-async.com/Asio/) | [github.com/chriskohlhoff/asio](https://github.com/chriskohlhoff/asio) |
| | libcurl | [curl.se/libcurl](https://curl.se/libcurl/) | [github.com/curl/curl](https://github.com/curl/curl) |
| | cpp-httplib | [github.com/yhirose/cpp-httplib](https://github.com/yhirose/cpp-httplib) | [github.com/yhirose/cpp-httplib](https://github.com/yhirose/cpp-httplib) |
| **Concurrency** | Thread Building Blocks (TBB) | [oneapi-src.github.io/oneTBB](https://oneapi-src.github.io/oneTBB/) | [github.com/oneapi-src/oneTBB](https://github.com/oneapi-src/oneTBB) |
| | OpenMP | [openmp.org](https://www.openmp.org/) | (стандарт, реализация в компиляторах) |
| **Cryptography** | OpenSSL | [openssl.org](https://www.openssl.org/) | [github.com/openssl/openssl](https://github.com/openssl/openssl) |
| | Botan | [botan.randombit.net](https://botan.randombit.net/) | [github.com/randombit/botan](https://github.com/randombit/botan) |
| | Crypto++ | [cryptopp.com](https://www.cryptopp.com/) | [github.com/weidai11/cryptopp](https://github.com/weidai11/cryptopp) |
| **Image Processing** | OpenCV | [opencv.org](https://opencv.org/) | [github.com/opencv/opencv](https://github.com/opencv/opencv) |
| | CImg | [cimg.eu.org](http://cimg.eu.org/) | [github.com/GreyCat/CImg](https://github.com/GreyCat/CImg) |
| **Math** | Eigen | [eigen.tuxfamily.org](http://eigen.tuxfamily.org/) | [gitlab.com/libeigen/eigen](https://gitlab.com/libeigen/eigen) |
| | Armadillo | [arma.sourceforge.net](http://arma.sourceforge.net/) | [gitlab.com/conradsnicta/armadillo-code](https://gitlab.com/conradsnicta/armadillo-code) |
| **Serialization** | cereal | [uscilab.github.io/cereal](https://uscilab.github.io/cereal/) | [github.com/USCiLab/cereal](https://github.com/USCiLab/cereal) |
| | protobuf (C++) | [protobuf.dev](https://protobuf.dev/) | [github.com/protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) |
| **Package Management** | Conan | [conan.io](https://conan.io/) | [github.com/conan-io/conan](https://github.com/conan-io/conan) |
| | vcpkg (Microsoft) | [vcpkg.io](https://vcpkg.io/) | [github.com/microsoft/vcpkg](https://github.com/microsoft/vcpkg) |
| **Build Systems** | CMake | [cmake.org](https://cmake.org/) | [gitlab.kitware.com/cmake/cmake](https://gitlab.kitware.com/cmake/cmake) |
| | Meson | [mesonbuild.com](https://mesonbuild.com/) | [github.com/mesonbuild/meson](https://github.com/mesonbuild/meson) |
| | Bazel | [bazel.build](https://bazel.build/) | [github.com/bazelbuild/bazel](https://github.com/bazelbuild/bazel) |

---

## 🌍 ОБЩЕПЛАТФОРМЕННЫЕ / ИНФРАСТРУКТУРНЫЕ (CrossPlatform)

### 📨 Message Brokers & Event Streaming

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Brokers** | Apache Kafka | [kafka.apache.org](https://kafka.apache.org/) | [github.com/apache/kafka](https://github.com/apache/kafka) |
| | RabbitMQ Server | [rabbitmq.com](https://rabbitmq.com/) | [github.com/rabbitmq/rabbitmq-server](https://github.com/rabbitmq/rabbitmq-server) |
| | Apache Pulsar | [pulsar.apache.org](https://pulsar.apache.org/) | [github.com/apache/pulsar](https://github.com/apache/pulsar) |
| | NATS Server | [nats.io](https://nats.io/) | [github.com/nats-io/nats-server](https://github.com/nats-io/nats-server) |
| | NSQ | [nsq.io](https://nsq.io/) | [github.com/nsqio/nsq](https://github.com/nsqio/nsq) |
| | Redis (Pub/Sub, Streams) | [redis.io](https://redis.io/) | [github.com/redis/redis](https://github.com/redis/redis) |
| | ZeroMQ (libzmq) | [zeromq.org](https://zeromq.org/) | [github.com/zeromq/libzmq](https://github.com/zeromq/libzmq) |
| | ActiveMQ Artemis | [activemq.apache.org](https://activemq.apache.org/components/artemis/) | [github.com/apache/activemq-artemis](https://github.com/apache/activemq-artemis) |
| | Apache RocketMQ | [rocketmq.apache.org](https://rocketmq.apache.org/) | [github.com/apache/rocketmq](https://github.com/apache/rocketmq) |
| | EMQX (MQTT) | [emqx.io](https://www.emqx.io/) | [github.com/emqx/emqx](https://github.com/emqx/emqx) |
| | Mosquitto (MQTT) | [mosquitto.org](https://mosquitto.org/) | [github.com/eclipse-mosquitto/mosquitto](https://github.com/eclipse-mosquitto/mosquitto) |

### 💾 Object Storage & Databases

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Object Storage** | MinIO Server | [min.io](https://min.io/) | [github.com/minio/minio](https://github.com/minio/minio) |
| | Ceph (S3-compatible) | [ceph.io](https://ceph.io/) | [github.com/ceph/ceph](https://github.com/ceph/ceph) |
| | SeaweedFS | [github.com/seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) | [github.com/seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) |
| **Relational DB** | PostgreSQL | [postgresql.org](https://www.postgresql.org/) | [github.com/postgres/postgres](https://github.com/postgres/postgres) |
| | MySQL | [mysql.com](https://www.mysql.com/) | [github.com/mysql/mysql-server](https://github.com/mysql/mysql-server) |
| | MariaDB | [mariadb.org](https://mariadb.org/) | [github.com/MariaDB/server](https://github.com/MariaDB/server) |
| | CockroachDB | [cockroachlabs.com](https://www.cockroachlabs.com/) | [github.com/cockroachdb/cockroach](https://github.com/cockroachdb/cockroach) |
| | TiDB | [pingcap.com](https://www.pingcap.com/) | [github.com/pingcap/tidb](https://github.com/pingcap/tidb) |
| | YugabyteDB | [yugabyte.com](https://www.yugabyte.com/) | [github.com/yugabyte/yugabyte-db](https://github.com/yugabyte/yugabyte-db) |
| **NoSQL DB** | MongoDB | [mongodb.com](https://www.mongodb.com/) | [github.com/mongodb/mongo](https://github.com/mongodb/mongo) |
| | Cassandra | [cassandra.apache.org](https://cassandra.apache.org/) | [github.com/apache/cassandra](https://github.com/apache/cassandra) |
| | ScyllaDB | [scylladb.com](https://www.scylladb.com/) | [github.com/scylladb/scylladb](https://github.com/scylladb/scylladb) |
| | DynamoDB (AWS) | [aws.amazon.com/dynamodb](https://aws.amazon.com/dynamodb/) | (проприетарный) |
| **Search** | Elasticsearch | [elastic.co/elasticsearch](https://www.elastic.co/elasticsearch/) | [github.com/elastic/elasticsearch](https://github.com/elastic/elasticsearch) |
| | OpenSearch | [opensearch.org](https://opensearch.org/) | [github.com/opensearch-project/OpenSearch](https://github.com/opensearch-project/OpenSearch) |
| | Meilisearch | [meilisearch.com](https://www.meilisearch.com/) | [github.com/meilisearch/meilisearch](https://github.com/meilisearch/meilisearch) |
| | Typesense | [typesense.org](https://typesense.org/) | [github.com/typesense/typesense](https://github.com/typesense/typesense) |
| | Apache Solr | [solr.apache.org](https://solr.apache.org/) | [github.com/apache/solr](https://github.com/apache/solr) |
| **Graph DB** | Neo4j | [neo4j.com](https://neo4j.com/) | [github.com/neo4j/neo4j](https://github.com/neo4j/neo4j) |
| | ArangoDB | [arangodb.com](https://arangodb.com/) | [github.com/arangodb/arangodb](https://github.com/arangodb/arangodb) |
| **Time-Series** | InfluxDB | [influxdata.com](https://www.influxdata.com/) | [github.com/influxdata/influxdb](https://github.com/influxdata/influxdb) |
| | TimescaleDB | [timescale.com](https://www.timescale.com/) | [github.com/timescale/timescaledb](https://github.com/timescale/timescaledb) |
| | Prometheus | [prometheus.io](https://prometheus.io/) | [github.com/prometheus/prometheus](https://github.com/prometheus/prometheus) |
| **Cache** | Redis | [redis.io](https://redis.io/) | [github.com/redis/redis](https://github.com/redis/redis) |
| | Memcached | [memcached.org](https://memcached.org/) | [github.com/memcached/memcached](https://github.com/memcached/memcached) |
| | Dragonfly | [dragonflydb.io](https://www.dragonflydb.io/) | [github.com/dragonflydb/dragonfly](https://github.com/dragonflydb/dragonfly) |
| | KeyDB | [docs.keydb.dev](https://docs.keydb.dev/) | [github.com/Snapchat/KeyDB](https://github.com/Snapchat/KeyDB) |
| **Vector DB** | Milvus | [milvus.io](https://milvus.io/) | [github.com/milvus-io/milvus](https://github.com/milvus-io/milvus) |
| | Pinecone | [pinecone.io](https://www.pinecone.io/) | (проприетарный SaaS) |
| | Weaviate | [weaviate.io](https://weaviate.io/) | [github.com/weaviate/weaviate](https://github.com/weaviate/weaviate) |
| | Qdrant | [qdrant.tech](https://qdrant.tech/) | [github.com/qdrant/qdrant](https://github.com/qdrant/qdrant) |
| | Chroma | [trychroma.com](https://www.trychroma.com/) | [github.com/chroma-core/chroma](https://github.com/chroma-core/chroma) |

### 🎨 UI Frameworks (Cross-Platform Desktop/Mobile)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Desktop** | Electron (JS/HTML/CSS) | [electronjs.org](https://www.electronjs.org/) | [github.com/electron/electron](https://github.com/electron/electron) |
| | Tauri (Rust + WebView) | [tauri.app](https://tauri.app/) | [github.com/tauri-apps/tauri](https://github.com/tauri-apps/tauri) |
| | Qt (C++) | [qt.io](https://www.qt.io/) | [github.com/qt](https://github.com/qt) |
| | .NET MAUI | [learn.microsoft.com/dotnet/maui](https://learn.microsoft.com/en-us/dotnet/maui/) | [github.com/dotnet/maui](https://github.com/dotnet/maui) |
| | Avalonia (.NET) | [avaloniaui.net](https://avaloniaui.net/) | [github.com/AvaloniaUI/Avalonia](https://github.com/AvaloniaUI/Avalonia) |
| | Compose Multiplatform (Kotlin) | [jetbrains.com/lp/compose](https://www.jetbrains.com/lp/compose-multiplatform/) | [github.com/JetBrains/compose-multiplatform](https://github.com/JetBrains/compose-multiplatform) |
| **Mobile** | Flutter (Dart) | [flutter.dev](https://flutter.dev/) | [github.com/flutter/flutter](https://github.com/flutter/flutter) |
| | React Native (JS) | [reactnative.dev](https://reactnative.dev/) | [github.com/facebook/react-native](https://github.com/facebook/react-native) |
| | Kotlin Multiplatform | [kotlinlang.org/lp/multiplatform](https://kotlinlang.org/lp/multiplatform/) | [github.com/JetBrains/kotlin](https://github.com/JetBrains/kotlin) |
| | Ionic | [ionicframework.com](https://ionicframework.com/) | [github.com/ionic-team/ionic-framework](https://github.com/ionic-team/ionic-framework) |
| | Expo | [expo.dev](https://expo.dev/) | [github.com/expo/expo](https://github.com/expo/expo) |
| **Game Engines** | Unity | [unity.com](https://unity.com/) | (проприетарный) |
| | Unreal Engine | [unrealengine.com](https://www.unrealengine.com/) | [github.com/EpicGames/UnrealEngine](https://github.com/EpicGames/UnrealEngine) |
| | Godot | [godotengine.org](https://godotengine.org/) | [github.com/godotengine/godot](https://github.com/godotengine/godot) |

### 🤖 ML/AI & Data Science (Cross-Platform)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Inference Runtimes** | ONNX Runtime | [onnxruntime.ai](https://onnxruntime.ai/) | [github.com/microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |
| | OpenVINO | [docs.openvino.ai](https://docs.openvino.ai/) | [github.com/openvinotoolkit/openvino](https://github.com/openvinotoolkit/openvino) |
| | TensorRT (NVIDIA) | [developer.nvidia.com/tensorrt](https://developer.nvidia.com/tensorrt) | [github.com/NVIDIA/TensorRT](https://github.com/NVIDIA/TensorRT) |
| | llama.cpp | [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) | [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) |
| | Ollama | [ollama.com](https://ollama.com/) | [github.com/ollama/ollama](https://github.com/ollama/ollama) |
| | vLLM | [vllm.readthedocs.io](https://vllm.readthedocs.io/) | [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) |
| **Computer Vision** | OpenCV | [opencv.org](https://opencv.org/) | [github.com/opencv/opencv](https://github.com/opencv/opencv) |
| | YOLO (Ultralytics) | [ultralytics.com](https://ultralytics.com/) | [github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) |
| | MediaPipe | [developers.google.com/mediapipe](https://developers.google.com/mediapipe) | [github.com/google/mediapipe](https://github.com/google/mediapipe) |
| **MLOps** | MLflow | [mlflow.org](https://mlflow.org/) | [github.com/mlflow/mlflow](https://github.com/mlflow/mlflow) |
| | Kubeflow | [kubeflow.org](https://www.kubeflow.org/) | [github.com/kubeflow/kubeflow](https://github.com/kubeflow/kubeflow) |
| | DVC | [dvc.org](https://dvc.org/) | [github.com/iterative/dvc](https://github.com/iterative/dvc) |
| | Weights & Biases | [wandb.ai](https://wandb.ai/) | [github.com/wandb/wandb](https://github.com/wandb/wandb) |
| **Data Processing** | Apache Spark | [spark.apache.org](https://spark.apache.org/) | [github.com/apache/spark](https://github.com/apache/spark) |
| | Apache Flink | [flink.apache.org](https://flink.apache.org/) | [github.com/apache/flink](https://github.com/apache/flink) |
| | Apache Beam | [beam.apache.org](https://beam.apache.org/) | [github.com/apache/beam](https://github.com/apache/beam) |
| | Delta Lake | [delta.io](https://delta.io/) | [github.com/delta-io/delta](https://github.com/delta-io/delta) |
| | Apache Iceberg | [iceberg.apache.org](https://iceberg.apache.org/) | [github.com/apache/iceberg](https://github.com/apache/iceberg) |

### 🔐 Authentication & Identity (Cross-Platform)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Identity Providers** | Keycloak | [keycloak.org](https://www.keycloak.org/) | [github.com/keycloak/keycloak](https://github.com/keycloak/keycloak) |
| | Ory Hydra | [ory.sh/hydra](https://www.ory.sh/hydra/) | [github.com/ory/hydra](https://github.com/ory/hydra) |
| | Ory Kratos | [ory.sh/kratos](https://www.ory.sh/kratos/) | [github.com/ory/kratos](https://github.com/ory/kratos) |
| | Authentik | [goauthentik.io](https://goauthentik.io/) | [github.com/goauthentik/authentik](https://github.com/goauthentik/authentik) |
| | Zitadel | [zitadel.com](https://zitadel.com/) | [github.com/zitadel/zitadel](https://github.com/zitadel/zitadel) |
| | SuperTokens | [supertokens.com](https://supertokens.com/) | [github.com/supertokens/supertokens-core](https://github.com/supertokens/supertokens-core) |
| **SaaS** | Auth0 | [auth0.com](https://auth0.com/) | [github.com/auth0](https://github.com/auth0) |
| | Okta | [okta.com](https://www.okta.com/) | [github.com/okta](https://github.com/okta) |
| | Firebase Authentication | [firebase.google.com/products/auth](https://firebase.google.com/products/auth) | (Google) |
| | AWS Cognito | [aws.amazon.com/cognito](https://aws.amazon.com/cognito/) | (AWS) |
| | Azure AD B2C | [azure.microsoft.com/products/active-directory-external](https://azure.microsoft.com/en-us/products/active-directory-external/) | (Microsoft) |

### 🐳 Containerization & Orchestration

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Containers** | Docker | [docker.com](https://www.docker.com/) | [github.com/moby/moby](https://github.com/moby/moby) |
| | Podman | [podman.io](https://podman.io/) | [github.com/containers/podman](https://github.com/containers/podman) |
| | containerd | [containerd.io](https://containerd.io/) | [github.com/containerd/containerd](https://github.com/containerd/containerd) |
| | CRI-O | [cri-o.io](https://cri-o.io/) | [github.com/cri-o/cri-o](https://github.com/cri-o/cri-o) |
| **Orchestration** | Kubernetes (K8s) | [kubernetes.io](https://kubernetes.io/) | [github.com/kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) |
| | Docker Swarm | [docs.docker.com/engine/swarm](https://docs.docker.com/engine/swarm/) | (часть Docker) |
| | Nomad | [nomadproject.io](https://www.nomadproject.io/) | [github.com/hashicorp/nomad](https://github.com/hashicorp/nomad) |
| | Apache Mesos | [mesos.apache.org](http://mesos.apache.org/) | [github.com/apache/mesos](https://github.com/apache/mesos) |
| **Service Mesh** | Istio | [istio.io](https://istio.io/) | [github.com/istio/istio](https://github.com/istio/istio) |
| | Linkerd | [linkerd.io](https://linkerd.io/) | [github.com/linkerd/linkerd2](https://github.com/linkerd/linkerd2) |
| | Consul Connect | [developer.hashicorp.com/consul](https://developer.hashicorp.com/consul) | [github.com/hashicorp/consul](https://github.com/hashicorp/consul) |
| | Envoy Proxy | [envoyproxy.io](https://www.envoyproxy.io/) | [github.com/envoyproxy/envoy](https://github.com/envoyproxy/envoy) |
| **API Gateway** | Kong | [konghq.com](https://konghq.com/) | [github.com/Kong/kong](https://github.com/Kong/kong) |
| | Apache APISIX | [apisix.apache.org](https://apisix.apache.org/) | [github.com/apache/apisix](https://github.com/apache/apisix) |
| | Traefik | [traefik.io](https://traefik.io/) | [github.com/traefik/traefik](https://github.com/traefik/traefik) |
| | NGINX / NGINX Plus | [nginx.org](https://nginx.org/) | [github.com/nginx/nginx](https://github.com/nginx/nginx) |
| **Helm** | Helm | [helm.sh](https://helm.sh/) | [github.com/helm/helm](https://github.com/helm/helm) |

### 📊 Observability: Monitoring, Logging, Tracing

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Metrics** | Prometheus | [prometheus.io](https://prometheus.io/) | [github.com/prometheus/prometheus](https://github.com/prometheus/prometheus) |
| | Grafana | [grafana.com](https://grafana.com/) | [github.com/grafana/grafana](https://github.com/grafana/grafana) |
| | VictoriaMetrics | [victoriametrics.com](https://victoriametrics.com/) | [github.com/VictoriaMetrics/VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics) |
| | Thanos | [thanos.io](https://thanos.io/) | [github.com/thanos-io/thanos](https://github.com/thanos-io/thanos) |
| | Cortex | [cortexmetrics.io](https://cortexmetrics.io/) | [github.com/cortexproject/cortex](https://github.com/cortexproject/cortex) |
| **Logging** | ELK Stack (Elasticsearch + Logstash + Kibana) | [elastic.co/elastic-stack](https://www.elastic.co/elastic-stack/) | [github.com/elastic](https://github.com/elastic) |
| | Loki | [grafana.com/loki](https://grafana.com/oss/loki/) | [github.com/grafana/loki](https://github.com/grafana/loki) |
| | Fluentd | [fluentd.org](https://www.fluentd.org/) | [github.com/fluent/fluentd](https://github.com/fluent/fluentd) |
| | Fluent Bit | [fluentbit.io](https://fluentbit.io/) | [github.com/fluent/fluent-bit](https://github.com/fluent/fluent-bit) |
| | Vector | [vector.dev](https://vector.dev/) | [github.com/vectordotdev/vector](https://github.com/vectordotdev/vector) |
| | Graylog | [graylog.org](https://www.graylog.org/) | [github.com/Graylog2/graylog2-server](https://github.com/Graylog2/graylog2-server) |
| | Seq | [datalust.co/seq](https://datalust.co/seq) | (коммерческий) |
| **Tracing** | Jaeger | [jaegertracing.io](https://www.jaegertracing.io/) | [github.com/jaegertracing/jaeger](https://github.com/jaegertracing/jaeger) |
| | Zipkin | [zipkin.io](https://zipkin.io/) | [github.com/openzipkin/zipkin](https://github.com/openzipkin/zipkin) |
| | OpenTelemetry | [opentelemetry.io](https://opentelemetry.io/) | [github.com/open-telemetry](https://github.com/open-telemetry) |
| | Tempo | [grafana.com/oss/tempo](https://grafana.com/oss/tempo/) | [github.com/grafana/tempo](https://github.com/grafana/tempo) |
| **Alerting** | Alertmanager | [prometheus.io/docs/alerting](https://prometheus.io/docs/alerting/latest/alertmanager/) | [github.com/prometheus/alertmanager](https://github.com/prometheus/alertmanager) |
| | OpsGenie | [opsgenie.com](https://www.opsgenie.com/) | (Atlassian) |
| | PagerDuty | [pagerduty.com](https://www.pagerduty.com/) | (проприетарный) |
| **APM** | Datadog | [datadoghq.com](https://www.datadoghq.com/) | (проприетарный SaaS) |
| | New Relic | [newrelic.com](https://newrelic.com/) | (проприетарный SaaS) |
| | Dynatrace | [dynatrace.com](https://www.dynatrace.com/) | (проприетарный SaaS) |
| | AppDynamics | [appdynamics.com](https://www.appdynamics.com/) | (Cisco) |

### 🔧 Infrastructure as Code & Configuration Management

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **IaC** | Terraform | [terraform.io](https://www.terraform.io/) | [github.com/hashicorp/terraform](https://github.com/hashicorp/terraform) |
| | OpenTofu | [opentofu.org](https://opentofu.org/) | [github.com/opentofu/opentofu](https://github.com/opentofu/opentofu) |
| | Pulumi | [pulumi.com](https://www.pulumi.com/) | [github.com/pulumi/pulumi](https://github.com/pulumi/pulumi) |
| | AWS CDK | [docs.aws.amazon.com/cdk](https://docs.aws.amazon.com/cdk/v2/guide/home.html) | [github.com/aws/aws-cdk](https://github.com/aws/aws-cdk) |
| | Azure Bicep | [learn.microsoft.com/azure/azure-resource-manager/bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/) | [github.com/Azure/bicep](https://github.com/Azure/bicep) |
| | Crossplane | [crossplane.io](https://www.crossplane.io/) | [github.com/crossplane/crossplane](https://github.com/crossplane/crossplane) |
| **Configuration Management** | Ansible | [ansible.com](https://www.ansible.com/) | [github.com/ansible/ansible](https://github.com/ansible/ansible) |
| | Chef | [chef.io](https://www.chef.io/) | [github.com/chef/chef](https://github.com/chef/chef) |
| | Puppet | [puppet.com](https://www.puppet.com/) | [github.com/puppetlabs/puppet](https://github.com/puppetlabs/puppet) |
| | SaltStack | [saltproject.io](https://saltproject.io/) | [github.com/saltstack/salt](https://github.com/saltstack/salt) |
| **Secret Management** | HashiCorp Vault | [vaultproject.io](https://www.vaultproject.io/) | [github.com/hashicorp/vault](https://github.com/hashicorp/vault) |
| | AWS Secrets Manager | [aws.amazon.com/secrets-manager](https://aws.amazon.com/secrets-manager/) | (AWS) |
| | SOPS | [github.com/getsops/sops](https://github.com/getsops/sops) | [github.com/getsops/sops](https://github.com/getsops/sops) |
| **Service Discovery** | Consul | [developer.hashicorp.com/consul](https://developer.hashicorp.com/consul) | [github.com/hashicorp/consul](https://github.com/hashicorp/consul) |
| | etcd | [etcd.io](https://etcd.io/) | [github.com/etcd-io/etcd](https://github.com/etcd-io/etcd) |
| | ZooKeeper | [zookeeper.apache.org](https://zookeeper.apache.org/) | [github.com/apache/zookeeper](https://github.com/apache/zookeeper) |
| | Eureka (Netflix) | [github.com/Netflix/eureka](https://github.com/Netflix/eureka) | [github.com/Netflix/eureka](https://github.com/Netflix/eureka) |

### 🔄 CI/CD & DevOps

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **CI/CD Platforms** | GitHub Actions | [docs.github.com/actions](https://docs.github.com/en/actions) | (GitHub) |
| | GitLab CI/CD | [docs.gitlab.com/ee/ci](https://docs.gitlab.com/ee/ci/) | (GitLab) |
| | Jenkins | [jenkins.io](https://www.jenkins.io/) | [github.com/jenkinsci/jenkins](https://github.com/jenkinsci/jenkins) |
| | CircleCI | [circleci.com](https://circleci.com/) | (проприетарный SaaS) |
| | Azure DevOps | [azure.microsoft.com/products/devops](https://azure.microsoft.com/en-us/products/devops/) | (Microsoft) |
| | Bitbucket Pipelines | [bitbucket.org/product/features/pipelines](https://bitbucket.org/product/features/pipelines) | (Atlassian) |
| **CI/CD Tools** | Argo CD | [argoproj.github.io/cd](https://argoproj.github.io/cd/) | [github.com/argoproj/argo-cd](https://github.com/argoproj/argo-cd) |
| | Flux | [fluxcd.io](https://fluxcd.io/) | [github.com/fluxcd/flux2](https://github.com/fluxcd/flux2) |
| | Tekton | [tekton.dev](https://tekton.dev/) | [github.com/tektoncd/pipeline](https://github.com/tektoncd/pipeline) |
| | Spinnaker | [spinnaker.io](https://spinnaker.io/) | [github.com/spinnaker](https://github.com/spinnaker) |
| **Artifact Repositories** | Nexus (Sonatype) | [sonatype.com/products/nexus-repository](https://www.sonatype.com/products/nexus-repository) | (Sonatype) |
| | Artifactory (JFrog) | [jfrog.com/artifactory](https://jfrog.com/artifactory/) | (JFrog) |
| | Harbor | [goharbor.io](https://goharbor.io/) | [github.com/goharbor/harbor](https://github.com/goharbor/harbor) |
| **Source Control** | Git | [git-scm.com](https://git-scm.com/) | [github.com/git/git](https://github.com/git/git) |
| | Gitea | [gitea.io](https://gitea.io/) | [github.com/go-gitea/gitea](https://github.com/go-gitea/gitea) |
| | Forgejo | [forgejo.org](https://forgejo.org/) | [github.com/go-gitea/gitea](https://github.com/go-gitea/gitea) |
| | GitLab | [gitlab.com](https://gitlab.com/) | [gitlab.com/gitlab-org/gitlab](https://gitlab.com/gitlab-org/gitlab) |

---

## 💻 Примеры кода на C# (с учетом предпочтений)

Ниже приведены примеры использования ключевых .NET-библиотек с демонстрацией паттернов проектирования.

### 📌 Пример 1: MediatR + CQRS Pattern

```csharp
// ============================================
// CQRS с MediatR — паттерн Command/Query
// ============================================

// 1. Command (изменяет состояние)
public record CreateOrderCommand(
    Guid CustomerId,
    List<OrderItem> Items) : IRequest<Guid>;

// 2. Query (читает данные)
public record GetOrderByIdQuery(Guid OrderId) : IRequest<OrderDto?>;

// 3. Handler для команды
public class CreateOrderCommandHandler 
    : IRequestHandler<CreateOrderCommand, Guid>
{
    private readonly IOrderRepository _repository;
    private readonly IEventPublisher _eventPublisher;

    public CreateOrderCommandHandler(
        IOrderRepository repository,
        IEventPublisher eventPublisher)
    {
        _repository = repository;
        _eventPublisher = eventPublisher;
    }

    public async Task<Guid> Handle(
        CreateOrderCommand request, 
        CancellationToken cancellationToken)
    {
        var order = Order.Create(request.CustomerId, request.Items);
        
        await _repository.AddAsync(order, cancellationToken);
        
        // Публикуем доменное событие
        await _eventPublisher.PublishAsync(
            new OrderCreatedEvent(order.Id, order.CustomerId),
            cancellationToken);
        
        return order.Id;
    }
}

// 4. Handler для запроса
public class GetOrderByIdQueryHandler 
    : IRequestHandler<GetOrderByIdQuery, OrderDto?>
{
    private readonly IOrderRepository _repository;
    private readonly IMapper _mapper;

    public GetOrderByIdQueryHandler(
        IOrderRepository repository,
        IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<OrderDto?> Handle(
        GetOrderByIdQuery request, 
        CancellationToken cancellationToken)
    {
        var order = await _repository.GetByIdAsync(request.OrderId, cancellationToken);
        return order is null ? null : _mapper.Map<OrderDto>(order);
    }
}

// 5. Использование в контроллере
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpPost]
    public async Task<IActionResult> Create(
        [FromBody] CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var command = new CreateOrderCommand(
            request.CustomerId,
            request.Items);
        
        var orderId = await _mediator.Send(command, cancellationToken);
        
        return CreatedAtAction(
            nameof(GetById),
            new { id = orderId },
            new { id = orderId });
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(
        Guid id,
        CancellationToken cancellationToken)
    {
        var query = new GetOrderByIdQuery(id);
        var order = await _mediator.Send(query, cancellationToken);
        
        return order is null ? NotFound() : Ok(order);
    }
}

// 6. Pipeline Behavior (декоратор для валидации, логирования)
public class ValidationBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
            return await next();

        var context = new ValidationContext<TRequest>(request);
        
        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));
        
        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Count != 0)
            throw new ValidationException(failures);

        return await next();
    }
}
```

### 📌 Пример 2: MassTransit с RabbitMQ

```csharp
// ============================================
// MassTransit — обмен сообщениями через RabbitMQ
// ============================================

// 1. Контракт сообщения
public record OrderCreatedEvent(
    Guid OrderId,
    Guid CustomerId,
    decimal TotalAmount,
    DateTime CreatedAt);

// 2. Consumer (обработчик сообщений)
public class OrderCreatedConsumer 
    : IConsumer<OrderCreatedEvent>
{
    private readonly ILogger<OrderCreatedConsumer> _logger;
    private readonly INotificationService _notificationService;

    public OrderCreatedConsumer(
        ILogger<OrderCreatedConsumer> logger,
        INotificationService notificationService)
    {
        _logger = logger;
        _notificationService = notificationService;
    }

    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        _logger.LogInformation(
            "Processing order created event: {OrderId}",
            context.Message.OrderId);

        await _notificationService.SendOrderConfirmation(
            context.Message.CustomerId,
            context.Message.OrderId);

        // Если нужно опубликовать следующее событие
        await context.Publish(new OrderProcessingStartedEvent(
            context.Message.OrderId,
            DateTime.UtcNow));
    }
}

// 3. Saga (долгоживущий процесс)
public class OrderSagaState : SagaStateMachineInstance
{
    public Guid CorrelationId { get; set; }
    public string CurrentState { get; set; } = null!;
    public Guid OrderId { get; set; }
    public Guid CustomerId { get; set; }
    public bool PaymentReceived { get; set; }
    public bool InventoryReserved { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class OrderSaga : MassTransitStateMachine<OrderSagaState>
{
    public State Pending { get; private set; } = null!;
    public State PaymentReceived { get; private set; } = null!;
    public State Completed { get; private set; } = null!;
    public State Failed { get; private set; } = null!;

    public Event<OrderCreatedEvent> OrderCreated { get; private set; } = null!;
    public Event<PaymentReceivedEvent> PaymentReceivedEvent { get; private set; } = null!;
    public Event<InventoryReservedEvent> InventoryReservedEvent { get; private set; } = null!;

    public OrderSaga()
    {
        InstanceState(x => x.CurrentState);

        Event(() => OrderCreated, x => x.CorrelateById(ctx => ctx.Message.OrderId));
        Event(() => PaymentReceivedEvent, x => x.CorrelateById(ctx => ctx.Message.OrderId));
        Event(() => InventoryReservedEvent, x => x.CorrelateById(ctx => ctx.Message.OrderId));

        Initially(
            When(OrderCreated)
                .Then(context =>
                {
                    context.Saga.OrderId = context.Message.OrderId;
                    context.Saga.CustomerId = context.Message.CustomerId;
                    context.Saga.CreatedAt = DateTime.UtcNow;
                })
                .TransitionTo(Pending)
                .Publish(context => new ReserveInventoryCommand(
                    context.Message.OrderId,
                    context.Message.Items))
        );

        During(Pending,
            When(PaymentReceivedEvent)
                .Then(context => context.Saga.PaymentReceived = true)
                .TransitionTo(PaymentReceived),
            When(InventoryReservedEvent)
                .Then(context => context.Saga.InventoryReserved = true)
                .If(context => context.Saga.PaymentReceived && context.Saga.InventoryReserved,
                    then => then
                        .TransitionTo(Completed)
                        .Publish(context => new OrderFulfilledEvent(context.Saga.OrderId))
                )
        );
    }
}

// 4. Конфигурация в Program.cs
builder.Services.AddMassTransit(x =>
{
    x.AddConsumer<OrderCreatedConsumer>();
    x.AddConsumer<PaymentReceivedConsumer>();
    
    x.AddSagaStateMachine<OrderSaga, OrderSagaState>()
        .EntityFrameworkRepository(r =>
        {
            r.ConcurrencyMode = ConcurrencyMode.Pessimistic;
            r.ExistingDbContext<OrderSagaDbContext>();
        });

    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.Host(builder.Configuration.GetConnectionString("RabbitMQ"));

        cfg.ReceiveEndpoint("order-service-queue", e =>
        {
            e.ConfigureConsumer<OrderCreatedConsumer>(context);
            e.ConfigureConsumer<PaymentReceivedConsumer>(context);
        });
    });
});
```

### 📌 Пример 3: Polly — Resilience Patterns

```csharp
// ============================================
// Polly — Retry, Circuit Breaker, Timeout
// ============================================

// 1. Retry с exponential backoff
var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .Or<TimeoutRejectedException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: retryAttempt =>
            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
        onRetry: (exception, timeSpan, retryCount, context) =>
        {
            Log.Warning(
                "Retry {RetryCount} after {Delay}s due to: {Exception}",
                retryCount,
                timeSpan.TotalSeconds,
                exception.Message);
        });

// 2. Circuit Breaker
var circuitBreakerPolicy = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 5,
        durationOfBreak: TimeSpan.FromSeconds(30),
        onBreak: (exception, duration) =>
        {
            Log.Error("Circuit broken for {Duration}s: {Exception}",
                duration, exception.Message);
        },
        onReset: () => Log.Information("Circuit reset"),
        onHalfOpen: () => Log.Information("Circuit half-open"));

// 3. Timeout
var timeoutPolicy = Policy
    .TimeoutAsync(TimeSpan.FromSeconds(10));

// 4. Fallback
var fallbackPolicy = Policy<string>
    .Handle<HttpRequestException>()
    .FallbackAsync(
        fallbackAction: async (cancellationToken) =>
        {
            Log.Warning("Using fallback value");
            return "default-value";
        },
        onFallback: (exception, context) =>
        {
            Log.Error("Fallback triggered: {Exception}", exception.Message);
        });

// 5. Комбинация политик (PolicyWrap)
var policyWrap = Policy
    .WrapAsync(
        fallbackPolicy,
        retryPolicy,
        circuitBreakerPolicy,
        timeoutPolicy);

// 6. Использование с HttpClient
builder.Services.AddHttpClient<IPaymentGateway, PaymentGateway>()
    .AddPolicyHandler((services, request) =>
    {
        var logger = services.GetRequiredService<ILogger<PaymentGateway>>();
        
        return Policy<HttpResponseMessage>
            .Handle<HttpRequestException>()
            .OrResult(msg => msg.StatusCode == HttpStatusCode.RequestTimeout)
            .WaitAndRetryAsync(
                3,
                retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
                onRetry: (outcome, delay, retryCount, context) =>
                {
                    logger.LogWarning(
                        "Retry {RetryCount} for {Url}",
                        retryCount,
                        request.RequestUri);
                });
    });

// 7. Использование в коде
public class PaymentGateway : IPaymentGateway
{
    private readonly HttpClient _httpClient;
    private readonly IAsyncPolicy<HttpResponseMessage> _resiliencePolicy;

    public async Task<PaymentResult> ProcessPaymentAsync(
        PaymentRequest request,
        CancellationToken cancellationToken)
    {
        return await _resiliencePolicy.ExecuteAsync(async () =>
        {
            var response = await _httpClient.PostAsJsonAsync(
                "/api/payments",
                request,
                cancellationToken);
            
            response.EnsureSuccessStatusCode();
            
            return await response.Content
                .ReadFromJsonAsync<PaymentResult>(cancellationToken)
                ?? throw new InvalidOperationException("Invalid response");
        }, cancellationToken);
    }
}
```

### 📌 Пример 4: Serilog — Структурированное логирование

```csharp
// ============================================
// Serilog — конфигурация и использование
// ============================================

// 1. Конфигурация в Program.cs
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .MinimumLevel.Override("System", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithEnvironmentName()
    .Enrich.WithThreadId()
    .Enrich.WithProperty("Application", "OrderService")
    .WriteTo.Console(
        outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} " +
                       "{Properties:j}{NewLine}{Exception}")
    .WriteTo.File(
        path: "logs/log-.txt",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 31,
        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} " +
                       "[{Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
    .WriteTo.Seq("http://localhost:5341")
    .WriteTo.Elasticsearch(new ElasticsearchSinkOptions(new Uri("http://localhost:9200"))
    {
        AutoRegisterTemplate = true,
        IndexFormat = $"orders-{DateTime.UtcNow:yyyy-MM}"
    })
    .CreateLogger();

builder.Host.UseSerilog();

// 2. Использование в коде
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }

    public async Task<Order> CreateOrderAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        // Structured logging с контекстом
        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["CustomerId"] = request.CustomerId,
            ["RequestId"] = Guid.NewGuid()
        }))
        {
            _logger.LogInformation(
                "Creating order for customer {CustomerId} with {ItemCount} items",
                request.CustomerId,
                request.Items.Count);

            try
            {
                var order = await ProcessOrderAsync(request, cancellationToken);
                
                _logger.LogInformation(
                    "Order {OrderId} created successfully. Total: {TotalAmount:C}",
                    order.Id,
                    order.TotalAmount);
                
                return order;
            }
            catch (Exception ex)
            {
                _logger.LogError(
                    ex,
                    "Failed to create order for customer {CustomerId}",
                    request.CustomerId);
                throw;
            }
        }
    }

    public async Task<IEnumerable<Order>> GetOrdersByCustomerAsync(
        Guid customerId,
        CancellationToken cancellationToken)
    {
        _logger.LogDebug(
            "Fetching orders for customer {CustomerId}",
            customerId);

        var stopwatch = Stopwatch.StartNew();
        
        var orders = await _repository.GetByCustomerAsync(customerId, cancellationToken);
        
        stopwatch.Stop();
        
        _logger.LogInformation(
            "Retrieved {OrderCount} orders for customer {CustomerId} in {ElapsedMs}ms",
            orders.Count(),
            customerId,
            stopwatch.ElapsedMilliseconds);

        return orders;
    }
}

// 3. Middleware для логирования HTTP-запросов
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public async Task InvokeAsync(HttpContext context)
    {
        var startTime = DateTime.UtcNow;
        var requestId = Guid.NewGuid();
        
        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["RequestId"] = requestId,
            ["TraceId"] = context.TraceIdentifier,
            ["UserAgent"] = context.Request.Headers.UserAgent.ToString()
        }))
        {
            _logger.LogInformation(
                "Request {Method} {Path} started from {RemoteIp}",
                context.Request.Method,
                context.Request.Path,
                context.Connection.RemoteIpAddress);

            try
            {
                await _next(context);
                
                var elapsed = (DateTime.UtcNow - startTime).TotalMilliseconds;
                
                _logger.LogInformation(
                    "Request {Method} {Path} completed with {StatusCode} in {ElapsedMs}ms",
                    context.Request.Method,
                    context.Request.Path,
                    context.Response.StatusCode,
                    elapsed);
            }
            catch (Exception ex)
            {
                _logger.LogError(
                    ex,
                    "Request {Method} {Path} failed",
                    context.Request.Method,
                    context.Request.Path);
                throw;
            }
        }
    }
}
```

### 📌 Пример 5: Entity Framework Core — Repository Pattern

```csharp
// ============================================
// EF Core + Repository + Unit of Work
// ============================================

// 1. Domain Entity
public class Order
{
    public Guid Id { get; private set; }
    public Guid CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public decimal TotalAmount { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }
    
    private readonly List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();

    // EF Core requires parameterless constructor
    private Order() { }

    public Order(Guid customerId, IEnumerable<OrderItem> items)
    {
        Id = Guid.NewGuid();
        CustomerId = customerId;
        Status = OrderStatus.Pending;
        CreatedAt = DateTime.UtcNow;
        
        foreach (var item in items)
        {
            _items.Add(item);
        }
        
        TotalAmount = _items.Sum(i => i.Price * i.Quantity);
    }

    public void Confirm()
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException(
                $"Cannot confirm order in {Status} status");
        
        Status = OrderStatus.Confirmed;
        UpdatedAt = DateTime.UtcNow;
    }
}

// 2. DbContext
public class OrderDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public DbSet<Customer> Customers => Set<Customer>();

    public OrderDbContext(DbContextOptions<OrderDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Order>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.TotalAmount)
                .HasPrecision(18, 2);
            entity.HasMany(e => e.Items)
                .WithOne()
                .HasForeignKey("OrderId");
            entity.HasQueryFilter(e => !e.IsDeleted);
        });

        modelBuilder.Entity<Customer>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Email)
                .HasMaxLength(255)
                .IsRequired();
            entity.HasIndex(e => e.Email)
                .IsUnique();
        });
    }

    public override async Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default)
    {
        foreach (var entry in ChangeTracker.Entries<IAuditable>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Entity.CreatedAt = DateTime.UtcNow;
                    entry.Entity.CreatedBy = "current-user"; // из контекста
                    break;
                case EntityState.Modified:
                    entry.Entity.UpdatedAt = DateTime.UtcNow;
                    entry.Entity.UpdatedBy = "current-user";
                    break;
            }
        }

        return await base.SaveChangesAsync(cancellationToken);
    }
}

// 3. Generic Repository
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
    Task<IEnumerable<T>> GetAllAsync(CancellationToken cancellationToken);
    Task<IEnumerable<T>> FindAsync(
        Expression<Func<T, bool>> predicate,
        CancellationToken cancellationToken);
    Task AddAsync(T entity, CancellationToken cancellationToken);
    void Update(T entity);
    void Remove(T entity);
}

public class Repository<T> : IRepository<T>
    where T : class, IEntity
{
    protected readonly OrderDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(OrderDbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public async Task<T?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken)
    {
        return await _dbSet.FindAsync(new object[] { id }, cancellationToken);
    }

    public async Task<IEnumerable<T>> GetAllAsync(
        CancellationToken cancellationToken)
    {
        return await _dbSet.ToListAsync(cancellationToken);
    }

    public async Task<IEnumerable<T>> FindAsync(
        Expression<Func<T, bool>> predicate,
        CancellationToken cancellationToken)
    {
        return await _dbSet.Where(predicate).ToListAsync(cancellationToken);
    }

    public async Task AddAsync(
        T entity,
        CancellationToken cancellationToken)
    {
        await _dbSet.AddAsync(entity, cancellationToken);
    }

    public void Update(T entity)
    {
        _dbSet.Update(entity);
    }

    public void Remove(T entity)
    {
        _dbSet.Remove(entity);
    }
}

// 4. Unit of Work
public interface IUnitOfWork : IDisposable
{
    IRepository<Order> Orders { get; }
    IRepository<Customer> Customers { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken);
}

public class UnitOfWork : IUnitOfWork
{
    private readonly OrderDbContext _context;
    private IRepository<Order> _orders;
    private IRepository<Customer> _customers;

    public UnitOfWork(OrderDbContext context)
    {
        _context = context;
    }

    public IRepository<Order> Orders =>
        _orders ??= new Repository<Order>(_context);

    public IRepository<Customer> Customers =>
        _customers ??= new Repository<Customer>(_context);

    public async Task<int> SaveChangesAsync(CancellationToken cancellationToken)
    {
        return await _context.SaveChangesAsync(cancellationToken);
    }

    public void Dispose()
    {
        _context.Dispose();
    }
}

// 5. Использование в сервисе
public class OrderApplicationService
{
    private readonly IUnitOfWork _unitOfWork;
    private readonly IEventPublisher _eventPublisher;

    public async Task<Guid> CreateOrderAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        // Проверка существования клиента
        var customer = await _unitOfWork.Customers
            .GetByIdAsync(request.CustomerId, cancellationToken);
        
        if (customer is null)
            throw new CustomerNotFoundException(request.CustomerId);

        // Создание заказа
        var items = request.Items.Select(i =>
            new OrderItem(i.ProductId, i.Quantity, i.Price)).ToList();
        
        var order = new Order(request.CustomerId, items);
        
        await _unitOfWork.Orders.AddAsync(order, cancellationToken);
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        // Публикация события
        await _eventPublisher.PublishAsync(
            new OrderCreatedEvent(order.Id, order.CustomerId, order.TotalAmount),
            cancellationToken);

        return order.Id;
    }
}

// 6. Конфигурация DI
builder.Services.AddDbContext<OrderDbContext>(options =>
{
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("OrderDb"),
        npgsqlOptions =>
        {
            npgsqlOptions.EnableRetryOnFailure(
                maxRetryCount: 5,
                maxRetryDelay: TimeSpan.FromSeconds(30),
                errorCodesToAdd: null);
            npgsqlOptions.CommandTimeout(30);
        });
    
    options.UseSnakeCaseNamingConvention();
    options.LogTo(Console.WriteLine, LogLevel.Information);
});

builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
```

---

## 🎯 Шаблоны проектирования в современных библиотеках

### 📊 Связь библиотек и паттернов

```mermaid
graph LR
    subgraph "Creational Patterns"
        DI[Dependency Injection<br/>Autofac, SimpleInjector]
        Factory[Factory Pattern<br/>HttpClientFactory]
        Builder[Builder Pattern<br/>FluentValidation]
    end
    
    subgraph "Structural Patterns"
        Adapter[Adapter<br/>Refit, RestSharp]
        Decorator[Decorator<br/>Polly, Middleware]
        Facade[Facade<br/>MediatR]
        Proxy[Proxy<br/>Castle DynamicProxy]
    end
    
    subgraph "Behavioral Patterns"
        Observer[Observer<br/>Rx.NET, Events]
        Strategy[Strategy<br/>IValidator implementations]
        Command[Command<br/>MediatR, MassTransit]
        Chain[Chain of Responsibility<br/>Middleware Pipeline]
        State[State<br/>Akka.NET, Orleans]
    end
    
    subgraph "Architectural Patterns"
        CQRS[CQRS<br/>MediatR]
        ES[Event Sourcing<br/>EventStore]
        Saga[Saga<br/>MassTransit]
        Clean[Clean Architecture<br/>Domain-Driven Design]
    end
    
    DI --> Clean
    Command --> CQRS
    Observer --> ES
    Decorator --> Chain
    Facade --> CQRS
```

### 📚 Паттерны, реализуемые популярными библиотеками

| Паттерн | Библиотеки | Описание |
|---------|-----------|----------|
| **CQRS** | MediatR, Wolverine | Разделение команд и запросов |
| **Event Sourcing** | EventStore, Marten | Хранение состояния как последовательности событий |
| **Saga / Process Manager** | MassTransit, NServiceBus | Управление долгоживущими бизнес-процессами |
| **Repository** | EF Core, Dapper | Абстракция доступа к данным |
| **Unit of Work** | EF Core DbContext | Группировка изменений в транзакцию |
| **Specification** | LINQ, Ardalis.Specification | Инкапсуляция критериев запросов |
| **Factory** | HttpClientFactory, DbProviderFactory | Создание объектов без указания точного класса |
| **Builder** | FluentValidation, NpgsqlConnectionStringBuilder | Пошаговое создание сложных объектов |
| **Decorator** | Polly, ASP.NET Core Middleware | Динамическое добавление ответственности |
| **Observer** | Rx.NET, Event Aggregator | Подписка на изменения |
| **Strategy** | IValidator implementations, Payment strategies | Семейство алгоритмов |
| **Chain of Responsibility** | ASP.NET Core Middleware Pipeline, Serilog Enrichers | Передача запроса по цепочке обработчиков |
| **Proxy** | Castle DynamicProxy, Moq | Заместитель для контроля доступа |
| **Adapter** | Refit, RestSharp, gRPC clients | Преобразование интерфейса |
| **Facade** | MediatR, Service Layer | Упрощенный интерфейс к подсистеме |
| **Singleton** | DI Container (Scoped/Singleton), Logger | Единственный экземпляр |
| **State** | Akka.NET Actors, State Machines | Управление состоянием |

---

# 📈 Тренды разработки 2026 года: Полная таблица

Ниже представлена структурированная таблица актуальных трендов по всем ключевым направлениям современной разработки.

---

## 🎯 Общая визуальная карта трендов

```mermaid
mindmap
  root((Тренды 2026))
    AI & ML
      LLM-интеграция
      AI Agents
      Vector DB
      RAG
      AI-Assisted Dev
    Backend
      .NET 9/10
      Java 21+ Virtual Threads
      Rust в production
      Go в cloud-native
      Python 3.13 no-GIL
    Frontend
      React Server Components
      Signals
      HTMX Renaissance
      WebAssembly
      AI-powered UI
    Architecture
      Platform Engineering
      FinOps
      Green Software
      Edge Computing
      Composable Apps
    Data
      Lakehouse
      Real-time Analytics
      Vector Search
      Data Contracts
    DevOps
      GitOps everywhere
      Internal Developer Platform
      eBPF Observability
      Policy as Code
```

---

## 📊 Таблица 1: Языковые экосистемы и фреймворки

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **.NET** | .NET 9 / .NET 10 с Native AOT | .NET Framework, классический JIT | `dotnet publish -r linux-x64 -c Release /p:PublishAot=true` | Запуск .NET без CLR, холодный старт <10мс, конкурент Go/Rust |
| **.NET** | Minimal APIs + Hybrid APIs | Controllers-heavy MVC | `app.MapGet()`, Carter, FastEndpoints | Меньше boilerplate, лучше производительность |
| **.NET** | Hybrid Blazor (SSR + WebAssembly) | Чистый SPA на Blazor WASM | `@rendermode InteractiveAuto` | Умное переключение между сервером и клиентом |
| **.NET** | Microsoft.Extensions.AI | Прямые SDK от OpenAI/Anthropic | `Microsoft.Extensions.AI`, `Semantic Kernel` | Единый абстрактный API для всех LLM |
| **Java** | Java 21+ Virtual Threads (Project Loom) | Reactive (Reactor, RxJava), CompletableFuture | `Thread.ofVirtual().start()` | Миллионы потоков без callback-hell |
| **Java** | Quarkus / Micronaut на production | Spring Boot (где важен startup time) | Quarkus, Micronaut, Helidon | Sub-second startup, GraalVM native image |
| **Java** | Spring Boot 3.3+ с Virtual Threads | Spring WebFlux для реактивности | `spring.threads.virtual.enabled=true` | Блокирующий код + масштабируемость реактивного подхода |
| **Java** | Kotlin Multiplatform в production | Написание кода отдельно для iOS/Android | KMP, Compose Multiplatform | Один код для Android, iOS, Desktop, Web |
| **Python** | Python 3.13+ free-threaded (no-GIL) | asyncio, multiprocessing | `python3.13 -X gil=0` | Настоящий параллелизм в Python, конец GIL |
| **Python** | FastAPI + Litestar | Flask, Django REST Framework | FastAPI, Litestar, Starlette | Async-first, автоматическая OpenAPI-документация |
| **Python** | SQLModel, Pydantic v2 | SQLAlchemy + Marshmallow отдельно | SQLModel, Pydantic, msgspec | Валидация + ORM из одного источника |
| **Python** | RAG-фреймворки | Классический ML pipeline | LangChain, LlamaIndex, Haystack | Интеграция LLM с внешними данными |
| **JS/TS** | React Server Components | Классический CSR React | Next.js 14+, Remix | Рендеринг на сервере, нулевой JS на клиенте |
| **JS/TS** | Signals (React, Angular, Solid, Vue) | Virtual DOM, Redux, MobX | Angular Signals, Preact Signals, Solid | Fine-grained реактивность без Virtual DOM |
| **JS/TS** | HTMX + серверный рендеринг | SPA на React/Vue/Angular | HTMX, Alpine.js, _hyperscript | Возврат к серверному вебу, меньше JS |
| **JS/TS** | Bun как runtime | Node.js (в некоторых сценариях) | Bun, Deno 2.0 | Встроенный bundler, тест-раннер, npm-клиент |
| **JS/TS** | TypeScript 5.5+ с inferred types | Явные аннотации типов | TypeScript, Zod, tRPC | End-to-end type safety |
| **JS/TS** | Vite + Rolldown | Webpack, Create React App | Vite, Rolldown, Turbopack | Мгновенный HMR, Rollup-совместимость |
| **Go** | Go 1.22+ с range over func | Классические итераторы | `for v := range seq { }` | Генераторы и ленивые вычисления |
| **Go** | Go в AI/ML inference | Python для serving | Ollama, llama.cpp bindings | Высокая производительность + простота деплоя |
| **Go** | Go workspace + monorepo | Отдельные модули | `go work`, Bazel | Управление большими проектами |
| **Rust** | Rust в cloud-native инфраструктуре | C/C++ для системного ПО | Firecracker, Linkerd, Qdrant | Безопасность памяти + производительность |
| **Rust** | Leptos / Dioxus для full-stack | Actix + отдельный frontend | Leptos, Dioxus, Yew | Rust от сервера до браузера (WASM) |
| **Rust** | Async Rust стабилизация | tokio + manual polling | `async fn` в trait, RPITIT | Упрощение асинхронного кода |
| **C++** | C++23/26 в production | C++17/20 | std::expected, std::print, modules | Современный C++ без Boost-зависимостей |
| **C++** | vcpkg + Conan 2.0 | Ручная сборка зависимостей | vcpkg, Conan 2, CMake FetchContent | Пакетные менеджеры как стандарт |

---

## 📊 Таблица 2: Архитектура и паттерны

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **Архитектура** | Modular Monolith | Микросервисы "на старте" | .NET Aspire, Spring Modulith | Микросервисы только там, где нужны |
| **Архитектура** | Composable Architecture | Жёстко связанные монолиты | Backstage, Port, Cortex | Сборка приложений из переиспользуемых компонентов |
| **Архитектура** | Event-Driven Architecture | REST-синхронные вызовы | Kafka, NATS, MassTransit | Асинхронная связь между сервисами |
| **Архитектура** | Cell-based Architecture | Монолит, микросервисы | Cell-based Architecture pattern | Изолированные "ячейки" для multi-tenancy |
| **Архитектура** | Serverless 2.0 | Классические serverless функции | AWS Lambda SnapStart, Azure Container Apps | Холодный старт <100мс, контейнеры |
| **Архитектура** | Edge Computing | Только центральные дата-центры | Cloudflare Workers, Fastly Compute | Выполнение кода ближе к пользователю |
| **Архитектура** | Wasm на сервере | Контейнеры (в некоторых сценариях) | WASI, Wasmtime, Spin | Мгновенный старт, песочница, кросс-платформа |
| **Паттерны** | AI-Augmented Architecture | Классические паттерны | Semantic Kernel, LangChain | Паттерны с LLM-компонентами |
| **Паттерны** | Vertical Slice Architecture | Layered Architecture (по слоям) | MediatR, Ardalis templates | Организация кода по фичам, не по слоям |
| **Паттерны** | Outbox Pattern | Двухфазный коммит (2PC) | MassTransit Outbox, Debezium | Гарантированная доставка событий |
| **Паттерны** | Saga Pattern (оркестрация) | Distributed transactions | MassTransit Sagas, Temporal | Управление распределёнными транзакциями |
| **Паттерны** | CQRS + Event Sourcing | Классический CRUD | EventStoreDB, Marten, Axon | Полный аудит, временные срезы данных |
| **Паттерны** | Strangler Fig Pattern | Big Bang переписывание | YARP, Ocelot, Kong | Постепенная миграция legacy-систем |

---

## 📊 Таблица 3: Базы данных и работа с данными

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **Vector DB** | Векторные БД для RAG | Классический полнотекстовый поиск | Qdrant, Milvus, pgvector, Weaviate | Поиск по эмбеддингам для AI-приложений |
| **Vector DB** | pgvector в PostgreSQL | Отдельные vector-хранилища | pgvector, pgvectorscale | Векторный поиск прямо в PostgreSQL |
| **Lakehouse** | Lakehouse-архитектура | Классические data warehouse | Delta Lake, Apache Iceberg, Apache Hudi | Единое хранилище для data lake и warehouse |
| **OLAP** | ClickHouse, DuckDB в production | Классические OLAP (Vertica, Druid) | ClickHouse, DuckDB, StarRocks | Аналитика в реальном времени, SQL-совместимость |
| **OLAP** | DuckDB как "SQLite для аналитики" | Pandas + SQL-БД для аналитики | DuckDB, Polars | In-process OLAP, работа с Parquet напрямую |
| **Real-time** | Real-time аналитика | Batch-обработка (ETL) | Apache Flink, Materialize, RisingWave | Мгновенная аналитика на потоковых данных |
| **NewSQL** | Distributed SQL | Шардированный MySQL/PostgreSQL | CockroachDB, TiDB, YugabyteDB | Глобальная консистентность, горизонтальное масштабирование |
| **Cache** | Dragonfly, KeyDB | Классический Redis | Dragonfly, KeyDB, Garnet | Многопоточные Redis-совместимые кэши |
| **Cache** | Garnet (.NET от Microsoft) | Memcached, Redis | Garnet | Высокопроизводительный кэш на .NET |
| **Time-Series** | Специализированные TSDB | PostgreSQL для временных рядов | TimescaleDB, InfluxDB, QuestDB | Оптимизированы для временных данных |
| **Embedded** | SQLite Renaissance | File-based хранилища | SQLite, libSQL, rqlite | SQLite в production с репликацией |
| **Migrations** | Schema-as-code | Ручные SQL-миграции | Atlas, Prisma Migrate, Alembic | Декларативное описание схемы БД |
| **Query Builder** | Type-safe query builders | ORM с runtime-ошибками | Kysely, Drizzle, sqlc | SQL-подобный API с проверкой типов |

---

## 📊 Таблица 4: AI/ML и LLM-интеграция

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **LLM Serving** | Локальные LLM на железе | Только облачные API | Ollama, llama.cpp, vLLM, LM Studio | Приватность, отсутствие затрат на API |
| **LLM Serving** | Специализированные inference-серверы | Универсальные ML-фреймворки | vLLM, TensorRT-LLM, SGLang | Оптимизация под LLM, paged attention |
| **RAG** | RAG (Retrieval-Augmented Generation) | Fine-tuning для каждой задачи | LangChain, LlamaIndex, Haystack | Актуальные знания без переобучения |
| **RAG** | GraphRAG | Классический RAG | Microsoft GraphRAG, Neo4j + LLM | Связь сущностей через графы знаний |
| **Agents** | AI Agents / Agentic workflows | Статичные LLM-промпты | LangGraph, AutoGen, CrewAI, Semantic Kernel | Автономные AI-агенты с инструментами |
| **Agents** | Function Calling / Tool Use | Простые промпты | OpenAI Function Calling, Anthropic Tool Use | LLM вызывает функции приложения |
| **MCP** | Model Context Protocol (MCP) | Кастомные интеграции с LLM | MCP от Anthropic | Стандартизированный протокол для LLM-интеграций |
| **Small LLM** | Small Language Models (SLM) | Только большие модели (GPT-4) | Phi-3, Llama 3.2 1B/3B, Gemma 2 | Маленькие модели на edge-устройствах |
| **Multimodal** | Мультимодальные модели | Только текст | GPT-4V, Claude 3.5, Gemini 1.5 | Текст + изображения + аудио + видео |
| **Evaluation** | LLM-as-a-Judge | Ручная оценка | Ragas, DeepEval, PromptFlow | Автоматическая оценка качества LLM |
| **Observability** | LLM Observability | Логи + метрики | LangSmith, Arize Phoenix, Weights & Biases | Трассировка LLM-вызовов, оценка стоимости |
| **On-device** | On-device AI | Облачные вызовы | ONNX Runtime, Core ML, MediaPipe | AI прямо на устройстве пользователя |
| **Fine-tuning** | LoRA / QLoRA fine-tuning | Full fine-tuning | Hugging Face PEFT, Unsloth | Эффективное дообучение на потребительском железе |
| **Vector Search** | Hybrid Search | Только keyword или только vector | BM25 + vector, Elasticsearch 8.x | Комбинация классического и векторного поиска |

---

## 📊 Таблица 5: DevOps, Cloud и инфраструктура

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **Platform Engineering** | Internal Developer Platform (IDP) | Ручная настройка инфраструктуры | Backstage, Port, Cortex, Kratix | Самообслуживание для разработчиков |
| **Platform Engineering** | .NET Aspire | Docker Compose + ручная настройка | .NET Aspire, Spring Boot Dev Services | Оркестрация cloud-ready приложений |
| **GitOps** | GitOps everywhere | Ручной CI/CD | Argo CD, Flux, Crossplane | Инфраструктура как git-репозиторий |
| **IaC** | OpenTofu как Terraform-альтернатива | Terraform (после смены лицензии) | OpenTofu, Pulumi, CDKTF | Open-source форк Terraform |
| **IaC** | Pulumi на родных языках | HCL (Terraform) | Pulumi (TypeScript, Python, Go, .NET) | Инфраструктура на знакомом языке |
| **Observability** | OpenTelemetry как стандарт | Проприетарные агенты (Datadog, New Relic) | OpenTelemetry Collector, Jaeger, Tempo | Единый стандарт телеметрии |
| **Observability** | eBPF для observability | Агенты в user-space | Cilium, Pixie, Parca | Наблюдение без изменения кода |
| **Observability** | Continuous Profiling | Периодический profiling | Parca, Pyroscope | Постоянный profiling в production |
| **FinOps** | FinOps-практики | Оптимизация "post-factum" | Kubecost, Infracost, AWS Cost Explorer | Контроль затрат на cloud на всех этапах |
| **Green Software** | Green Software Engineering | Игнорирование энергопотребления | Carbon Aware SDK, Green Metrics Tool | Углеродный след приложений |
| **Security** | Policy as Code | Ручные security review | OPA, Kyverno, Cedar | Политики безопасности как код |
| **Security** | DevSecShift / Supply Chain Security | Security в конце pipeline | Sigstore, SLSA, SBOM, Cosign | Безопасность цепочки поставок |
| **Security** | Zero Trust Architecture | Perimeter-based security | SPIFFE, SPIRE, OPA | "Никому не доверяй" |
| **Containers** | WASI / WebAssembly контейнеры | Docker-контейнеры (частично) | Spin, Wasmtime, wasmCloud | Мгновенный старт, минимальный размер |
| **Containers** | Distroless-контейнеры | Полноценные Linux-образы | gcr.io/distroless, Chainguard Images | Минимальная поверхность атаки |
| **Kubernetes** | Kubernetes для всех | Только для крупных команд | K3s, K0s, MicroK8s | K8s на edge и в малых проектах |
| **Kubernetes** | Kubernetes Operators | Кастомные контроллеры | Operator SDK, Kubebuilder, Crossplane | Автоматизация сложных приложений |
| **CI/CD** | Self-hosted runners | SaaS CI/CD | GitHub Actions self-hosted, GitLab Runner | Контроль над CI/CD-окружением |
| **CI/CD** | Dagger / Earthly | Классические CI-скрипты | Dagger, Earthly, Nx | Воспроизводимые CI/CD pipelines |

---

## 📊 Таблица 6: Frontend и пользовательский опыт

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **Rendering** | Server-First / Resumability | Классический CSR | Qwik, Astro, Next.js App Router | Минимум JS на клиенте |
| **Rendering** | Partial Hydration | Full hydration | Astro Islands, Next.js | Гидратация только интерактивных частей |
| **Rendering** | Streaming SSR | Blocking SSR | React Suspense, Astro streaming | Постепенная отправка HTML |
| **State** | Signals | Redux, MobX, Vuex | Angular Signals, Preact Signals, Solid | Fine-grained реактивность |
| **State** | Server State libraries | Global state для всего | TanStack Query, SWR, Apollo | Разделение server и client state |
| **Styling** | Tailwind CSS v4 | CSS-in-JS, обычный CSS | Tailwind CSS, UnoCSS | Utility-first как стандарт |
| **Styling** | CSS Layers, Nesting | CSS-препроцессоры | Нативный CSS | Современные CSS-возможности без Sass |
| **Styling** | Zero-runtime CSS-in-JS | Runtime CSS-in-JS | Panda CSS, Stylex, Linaria | Стилизация без runtime-накладных расходов |
| **Components** | Headless UI + Design System | Готовые UI-киты | Radix UI, Headless UI, shadcn/ui | Контроль над стилем, доступность из коробки |
| **Components** | shadcn/ui-подход | npm-пакеты компонентов | shadcn/ui, park-ui | Копирование кода, а не зависимость |
| **Forms** | React Hook Form + Zod | Formik, Redux Form | React Hook Form, Formik + Zod | Type-safe валидация форм |
| **Forms** | HTML-first forms | JS-heavy формы | HTMX, Alpine.js, Web Components | Возврат к нативным HTML-формам |
| **Animations** | View Transitions API | JS-библиотеки анимаций | View Transitions API, Motion One | Нативные переходы между страницами |
| **Animations** | Framer Motion / Motion | GSAP, Anime.js | Framer Motion, Motion | React-ориентированные анимации |
| **Accessibility** | Accessibility-first | Accessibility "в конце" | axe-core, WAVE, ARIA patterns | Доступность с самого начала |
| **Mobile** | React Native New Architecture | Старая архитектура RN | React Native 0.76+, Fabric, TurboModules | Новый рендерер, JSI вместо Bridge |
| **Mobile** | Expo как стандарт | "Ejected" React Native | Expo SDK 52+, EAS | Expo для production-приложений |
| **Desktop** | Tauri 2.0 | Electron | Tauri, Neutralinojs | Меньше размер, Rust backend |
| **Performance** | Core Web Vitals focus | "Работает и ладно" | Lighthouse, WebPageTest | SEO и UX через производительность |
| **Testing** | Playwright как стандарт | Cypress, Selenium | Playwright, WebdriverIO | Кросс-браузерное E2E тестирование |
| **Testing** | Component Testing | Только E2E | Vitest + Testing Library, Playwright CT | Тестирование компонентов в isolation |

---

## 📊 Таблица 7: Безопасность и аутентификация

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **Identity** | Passkeys / WebAuthn | Пароли, SMS-коды | WebAuthn, Passkey, FIDO2 | Беспарольная аутентификация |
| **Identity** | OIDC / OAuth 2.1 | OAuth 2.0 с grants | Keycloak, Authentik, Ory | Строгая спецификация OIDC |
| **Identity** | Self-hosted Identity | SaaS (Auth0, Okta) | Keycloak, Authentik, Zitadel | Контроль над данными пользователей |
| **AuthZ** | ReBAC / Fine-grained authorization | RBAC | Oso, SpiceDB, OpenFGA, Cedar | Авторизация на уровне отношений |
| **AuthZ** | Policy-as-Code | Код в приложении | OPA, Cedar, Casbin | Политики как отдельный артефакт |
| **Secrets** | External Secrets Operator | .env-файлы в репозитории | External Secrets, Sealed Secrets | Секреты из Vault, AWS Secrets Manager |
| **Secrets** | Short-lived credentials | Долгоживущие токены | SPIFFE, Vault dynamic secrets | Временные учётные данные |
| **Supply Chain** | SBOM (Software Bill of Materials) | Игнорирование зависимостей | Syft, Grype, Trivy | Список всех зависимостей |
| **Supply Chain** | SLSA / Sigstore | Подпись релизов вручную | cosign, sigstore, SLSA framework | Проверка целостности артефактов |
| **API Security** | API Security Posture | Ручной аудит | Noname Security, Salt Security | Автоматическое обнаружение уязвимостей API |
| **Zero Trust** | mTLS везде | Только TLS на edge | Istio, Linkerd, SPIFFE | Шифрование между сервисами |
| **AI Security** | AI/LLM Security | Игнорирование рисков AI | Guardrails AI, NeMo Guardrails | Защита от prompt injection, data leakage |

---

## 📊 Таблица 8: Тестирование и качество кода

| Категория | Тренд 2026 | Что приходит на смену | Примеры инструментов | Комментарий |
|-----------|------------|----------------------|---------------------|-------------|
| **Testing** | AI-assisted test generation | Ручное написание тестов | Diffblue, CodiumAI, GitHub Copilot | AI генерирует unit-тесты |
| **Testing** | Contract Testing | Интеграционные тесты между сервисами | Pact, Spring Cloud Contract | Контракты между consumer и provider |
| **Testing** | Testcontainers как стандарт | In-memory базы, mocks | Testcontainers, LocalStack | Реальные зависимости в тестах |
| **Testing** | Property-based testing | Пример-based тесты | Hypothesis (Py), fscheck (C#), QuickCheck | Тестирование свойств, не примеров |
| **Testing** | Mutation Testing | Только coverage | Stryker, PIT, mutmut | Измерение качества тестов |
| **Quality** | AI Code Review | Только ручной review | CodeRabbit, Qodana, SonarQube AI | AI как первый ревьюер |
| **Quality** | Trunk-based development | GitFlow, long-lived branches | GitHub Flow, GitLab Flow | Короткоживущие ветки, частые релизы |
| **Quality** | Feature Flags | Ветвление в коде | LaunchDarkly, Unleash, Flagsmith | Релиз без веток |
| **Static Analysis** | AI-powered static analysis | Классические линтеры | Qodana, SonarQube, CodeQL | AI находит сложные баги |
| **Performance** | Continuous Benchmarking | Ручное тестирование | BenchmarkDotNet, JMH, Criterion | Автоматическое обнаружение регрессий |

---

## 📊 Таблица 9: Организационные и процессные тренды

| Категория | Тренд 2026 | Что приходит на смену | Примеры / Подходы | Комментарий |
|-----------|------------|----------------------|-------------------|-------------|
| **Команды** | Team Topologies | Классические команды | Stream-aligned, Platform, Enabling teams | Организация по потокам ценности |
| **Команды** | Developer Experience (DevEx) | "Терпи и работай" | Backstage, Port, Internal platforms | Фокус на удобстве разработчиков |
| **Процессы** | AI-augmented development | Ручное программирование | GitHub Copilot, Cursor, Qodo | AI как напарник разработчика |
| **Процессы** | Vibe Coding | Классическое программирование | Cursor, Replit Agent, v0.dev | Описание того, что нужно, на естественном языке |
| **Процессы** | Continuous Deployment | Релизы раз в месяц/квартал | GitHub Actions, Argo CD | Несколько релизов в день |
| **Процессы** | Trunk-Based Development | GitFlow | GitHub Flow | Короткоживущие ветки |
| **Документация** | Docs-as-Code | Wiki, Confluence | Markdown + Git, Docusaurus, MkDocs | Документация в репозитории |
| **Документация** | AI-generated docs | Ручное написание | Swashbuckle, TypeDoc, JSDoc | Автогенерация из кода |
| **Метрики** | DORA Metrics | "Чувствуем, что быстро" | Deployment Frequency, Lead Time, MTTR, CFR | Измерение эффективности команд |
| **Метрики** | SPACE Framework | Только производительность | Satisfaction, Performance, Activity, Communication, Efficiency | Многомерная оценка разработчиков |

---

## 🔑 Ключевые выводы

```mermaid
graph TB
    A[Тренды 2026] --> B[AI-First]
    A --> C[Server-First]
    A --> D[Platform Engineering]
    A --> E[Type Safety]
    A --> F[Observability]
    
    B --> B1[LLM интеграция в каждое приложение]
    B --> B2[AI-агенты и RAG]
    B --> B3[AI-assisted разработка]
    
    C --> C1[RSC, HTMX, Astro]
    C --> C2[Edge computing]
    C --> C3[Serverless 2.0]
    
    D --> D1[IDP / Backstage]
    D --> D2[Self-service для разработчиков]
    D --> D3[.NET Aspire, Spring Dev Services]
    
    E --> E1[TypeScript everywhere]
    E --> E2[Rust в инфраструктуре]
    E --> E3[Type-safe query builders]
    
    F --> F1[OpenTelemetry]
    F --> F2[eBPF]
    F --> F3[LLM Observability]
```

### 🎯 Главные мегатренды:

1. **AI как новый стек** — LLM, RAG, агенты становятся такой же частью стека, как база данных или очередь сообщений
2. **Возврат к серверу** — после доминирования SPA, серверный рендеринг снова в моде (RSC, HTMX, Astro)
3. **Platform Engineering** — внутренние платформы для разработчиков заменяют ручную настройку
4. **Type Safety everywhere** — TypeScript, Rust, type-safe ORM и query builders
5. **Observability как стандарт** — OpenTelemetry заменяет проприетарные решения
6. **FinOps и Green Software** — экономика и экология становятся инженерными дисциплинами
7. **Supply Chain Security** — безопасность цепочки поставок ПО критична
8. **Маленькие модели на edge** — не всегда нужен GPT-4, SLM работают локально