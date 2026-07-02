# 🚀 Tech Stack Encyclopedia: Полный справочник библиотек и фреймворков
## .NET, Java, Python, JavaScript, Go, Rust, C++ и общеплатформенные решения

1. **Вначале идут все .NET-библиотеки** (включая .NET Core, ASP.NET Core, Blazor, Xamarin и т.д.) — это основная часть.
2. **Затем проведена разделительная черта** (горизонтальная линия с явным заголовком "ДРУГИЕ ЭКОСИСТЕМЫ").
3. **После черты — все остальные** (Java, Python, JavaScript/TypeScript, Go, Rust, C++ и пр.), тоже сгруппированные по экосистемам для удобства.

---

### .NET ЭКОСИСТЕМА (C#, F#, VB.NET)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:--|:-------------|:--------------------|:----------------|
| **Message Queue** | MassTransit | [masstransit-project.com](https://masstransit-project.com/) | [github.com/MassTransit/MassTransit](https://github.com/MassTransit/MassTransit) |
| | RabbitMQ.Client (официальный клиент) | [rabbitmq.com/dotnet](https://rabbitmq.com/dotnet.html) | [github.com/rabbitmq/rabbitmq-dotnet-client](https://github.com/rabbitmq/rabbitmq-dotnet-client) |
| | Confluent.Kafka| [docs.confluent.io/kafka-clients/dotnet](https://docs.confluent.io/kafka-clients/dotnet/) | [github.com/confluentinc/confluent-kafka-dotnet](https://github.com/confluentinc/confluent-kafka-dotnet) |
| | Azure.Messaging.ServiceBus (.NET SDK) | [azure.microsoft.com/service-bus](https://azure.microsoft.com/en-us/products/service-bus/) | [github.com/Azure/azure-sdk-for-net](https://github.com/Azure/azure-sdk-for-net) |
| | AWSSDK.SQS| [aws.amazon.com/sqs](https://aws.amazon.com/sqs/) | [github.com/aws/aws-sdk-net](https://github.com/aws/aws-sdk-net) |
| | NetMQ (ZeroMQ for .NET) | [netmq.readthedocs.io](https://netmq.readthedocs.io/) | [github.com/zeromq/netmq](https://github.com/zeromq/netmq) |
| | StackExchange.Redis (Pub/Sub) | [stackexchange.github.io/StackExchange.Redis](https://stackexchange.github.io/StackExchange.Redis/) | [github.com/StackExchange/StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) |
| | Nats.NET | [nats-io.github.io/nats.net](https://nats-io.github.io/nats.net/) | [github.com/nats-io/nats.net](https://github.com/nats-io/nats.net) |
| **Actor Model** | Akka.NET | [getakka.net](https://getakka.net/) | [github.com/akkadotnet/akka.net](https://github.com/akkadotnet/akka.net) |
| | Microsoft Orleans | [dotnet.github.io/orleans](https://dotnet.github.io/orleans/) | [github.com/dotnet/orleans](https://github.com/dotnet/orleans) |
| | Proto.Actor | [proto.actor](https://proto.actor/) | [github.com/asynkron/protoactor-dotnet](https://github.com/asynkron/protoactor-dotnet) |
| | MediatR | [github.com/jbogard/MediatR/wiki](https://github.com/jbogard/MediatR/wiki) | [github.com/jbogard/MediatR](https://github.com/jbogard/MediatR) |
| **Profiling & Logging** | MiniProfiler | [miniprofiler.com](https://miniprofiler.com/) | [github.com/MiniProfiler/dotnet](https://github.com/MiniProfiler/dotnet) |
| | OpenTelemetry .NET | [opentelemetry.io/docs/instrumentation/net](https://opentelemetry.io/docs/instrumentation/net/) | [github.com/open-telemetry/opentelemetry-dotnet](https://github.com/open-telemetry/opentelemetry-dotnet) |
| | Serilog | [serilog.net](https://serilog.net/) | [github.com/serilog/serilog](https://github.com/serilog/serilog) |
| | NLog | [nlog-project.org](https://nlog-project.org/) | [github.com/NLog/NLog](https://github.com/NLog/NLog) |
| | log4net | [logging.apache.org/log4net](https://logging.apache.org/log4net/) | [github.com/apache/logging-log4net](https://github.com/apache/logging-log4net) |
| | Application Insights for .NET | [azure.microsoft.com/app-insights](https://azure.microsoft.com/en-us/products/app-insights/) | [github.com/Microsoft/ApplicationInsights-dotnet](https://github.com/Microsoft/ApplicationInsights-dotnet) |
| | Prometheus.NET | [github.com/prometheus-net/prometheus-net](https://github.com/prometheus-net/prometheus-net) | [github.com/prometheus-net/prometheus-net](https://github.com/prometheus-net/prometheus-net) |
| **Testing** | xUnit.net | [xunit.net](https://xunit.net/) | [github.com/xunit/xunit](https://github.com/xunit/xunit) |
| | NUnit | [nunit.org](https://nunit.org/) | [github.com/nunit/nunit](https://github.com/nunit/nunit) |
| | MSTest | [learn.microsoft.com/mstest](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest) | [github.com/microsoft/testfx](https://github.com/microsoft/testfx) |
| | Moq | [github.com/devlooped/moq](https://github.com/devlooped/moq) | [github.com/devlooped/moq](https://github.com/devlooped/moq) |
| | NSubstitute | [nsubstitute.github.io](https://nsubstitute.github.io/) | [github.com/nsubstitute/NSubstitute](https://github.com/nsubstitute/NSubstitute) |
| | FakeItEasy | [fakeiteasy.github.io](https://fakeiteasy.github.io/) | [github.com/FakeItEasy/FakeItEasy](https://github.com/FakeItEasy/FakeItEasy) |
| | FluentAssertions | [fluentassertions.com](https://fluentassertions.com/) | [github.com/fluentassertions/fluentassertions](https://github.com/fluentassertions/fluentassertions) |
| | Shouldly | [shouldly.readthedocs.io](https://shouldly.readthedocs.io/) | [github.com/shouldly/shouldly](https://github.com/shouldly/shouldly) |
| | Selenium.WebDriver| [selenium.dev](https://www.selenium.dev/) | [github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) |
| | Playwright .NET | [playwright.dev/dotnet](https://playwright.dev/dotnet/) | [github.com/microsoft/playwright-dotnet](https://github.com/microsoft/playwright-dotnet) |
| | Testcontainers .NET | [testcontainers.com](https://testcontainers.com/) | [github.com/testcontainers/testcontainers-dotnet](https://github.com/testcontainers/testcontainers-dotnet) |
| | SpecFlow (BDD) | [specflow.org](https://specflow.org/) | [github.com/SpecFlowOSS/SpecFlow](https://github.com/SpecFlowOSS/SpecFlow) |
| **Benchmarking** | BenchmarkDotNet | [benchmarkdotnet.org](https://benchmarkdotnet.org/) | [github.com/dotnet/BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet) |
| **Resilience** | Polly | [thepollyproject.org](https://www.thepollyproject.org/) | [github.com/App-vNext/Polly](https://github.com/App-vNext/Polly) |
| **Object Storage** | MinIO .NET SDK | [min.io/docs/minio/linux/developers/dotnet](https://min.io/docs/minio/linux/developers/dotnet) | [github.com/minio/minio-dotnet](https://github.com/minio/minio-dotnet) |
| | AWSSDK.S3| [aws.amazon.com/sdk-for-net](https://aws.amazon.com/sdk-for-net/) | [github.com/aws/aws-sdk-net](https://github.com/aws/aws-sdk-net) |
| | Azure.Storage.Blobs| [azure.microsoft.com/storage/blobs](https://azure.microsoft.com/en-us/products/storage/blobs/) | [github.com/Azure/azure-sdk-for-net](https://github.com/Azure/azure-sdk-for-net) |
| | Google.Cloud.Storage.V1| [cloud.google.com/dotnet](https://cloud.google.com/dotnet) | [github.com/googleapis/google-cloud-dotnet](https://github.com/googleapis/google-cloud-dotnet) |
| **Office** | MiniExcel | [github.com/shps951023/MiniExcel](https://github.com/shps951023/MiniExcel) | [github.com/shps951023/MiniExcel](https://github.com/shps951023/MiniExcel) |
| | MiniWord | [github.com/shps951023/MiniWord](https://github.com/shps951023/MiniWord) | [github.com/shps951023/MiniWord](https://github.com/shps951023/MiniWord) |
| | MiniPDF | [github.com/shps951023/MiniPDF](https://github.com/shps951023/MiniPDF) | [github.com/shps951023/MiniPDF](https://github.com/shps951023/MiniPDF) |
| | ClosedXML | [closedxml.github.io/ClosedXML](https://closedxml.github.io/ClosedXML/) | [github.com/closedxml/closedxml](https://github.com/closedxml/closedxml) |
| | EPPlus | [epplussoftware.com](https://www.epplussoftware.com/) | [github.com/EPPlusSoftware/EPPlus](https://github.com/EPPlusSoftware/EPPlus) |
| | DocumentFormat.OpenXml | [github.com/OfficeDev/Open-XML-SDK](https://github.com/OfficeDev/Open-XML-SDK) | [github.com/OfficeDev/Open-XML-SDK](https://github.com/OfficeDev/Open-XML-SDK) |
| | QuestPDF | [questpdf.com](https://www.questpdf.com/) | [github.com/QuestPDF/QuestPDF](https://github.com/QuestPDF/QuestPDF) |
| | iText7 (для .NET) | [itextpdf.com](https://itextpdf.com/) | [github.com/itext/itext7-dotnet](https://github.com/itext/itext7-dotnet) |
| | Aspose.Words| [aspose.com/words/net](https://products.aspose.com/words/net/) | (коммерческий, закрытый исходный код) |
| | Aspose.Cells| [aspose.com/cells/net](https://products.aspose.com/cells/net/) | (коммерческий, закрытый исходный код) |
| | Aspose.PDF| [aspose.com/pdf/net](https://products.aspose.com/pdf/net/) | (коммерческий, закрытый исходный код) |
| **UI Components** | DevExpress | [devexpress.com](https://www.devexpress.com/) | (коммерческая, исходники по подписке) |
| | Telerik (Progress) | [telerik.com](https://www.telerik.com/) | (коммерческая, исходники по подписке) |
| | Syncfusion | [syncfusion.com](https://www.syncfusion.com/) | (коммерческая, с бесплатной Community-лицензией) |
| | Infragistics | [infragistics.com](https://www.infragistics.com/) | (коммерческая) |
| | ComponentOne (GrapeCity) | [gcpowertools.com](https://www.gcpowertools.com/) | (коммерческая) |
| | Radzen (Blazor) | [radzen.com](https://www.radzen.com/) | [github.com/radzenhq/radzen-blazor](https://github.com/radzenhq/radzen-blazor) |
| | MudBlazor | [mudblazor.com](https://mudblazor.com/) | [github.com/MudBlazor/MudBlazor](https://github.com/MudBlazor/MudBlazor) |
| | Blazorise | [blazorise.com](https://blazorise.com/) | [github.com/stsrki/Blazorise](https://github.com/stsrki/Blazorise) |
| | Ant Design Blazor | [antblazor.com](https://antblazor.com/) | [github.com/ant-design-blazor/ant-design-blazor](https://github.com/ant-design-blazor/ant-design-blazor) |
| **Web Framework** | ASP.NET Core | [dotnet.microsoft.com/aspnet](https://dotnet.microsoft.com/en-us/apps/aspnet) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | NancyFX | [nancyfx.org](https://nancyfx.org/) | [github.com/NancyFx/Nancy](https://github.com/NancyFx/Nancy) |
| **ORM** | Entity Framework Core | [learn.microsoft.com/ef](https://learn.microsoft.com/en-us/ef/) | [github.com/dotnet/efcore](https://github.com/dotnet/efcore) |
| | Dapper | [github.com/DapperLib/Dapper](https://github.com/DapperLib/Dapper) | [github.com/DapperLib/Dapper](https://github.com/DapperLib/Dapper) |
| | NHibernate | [nhibernate.info](https://nhibernate.info/) | [github.com/nhibernate/nhibernate-core](https://github.com/nhibernate/nhibernate-core) |
| | Entity Framework 6 (legacy) | [learn.microsoft.com/ef6](https://learn.microsoft.com/en-us/ef/ef6/) | [github.com/dotnet/ef6](https://github.com/dotnet/ef6) |
| | Linq2DB | [linq2db.com](https://linq2db.com/) | [github.com/linq2db/linq2db](https://github.com/linq2db/linq2db) |
| | ServiceStack.OrmLite | [servicestack.net/ormlite](https://servicestack.net/ormlite) | [github.com/ServiceStack/ServiceStack](https://github.com/ServiceStack/ServiceStack) |
| **API / REST / GraphQL** | Swashbuckle (Swagger) | [github.com/domaindrivendev/Swashbuckle](https://github.com/domaindrivendev/Swashbuckle) | [github.com/domaindrivendev/Swashbuckle.AspNetCore](https://github.com/domaindrivendev/Swashbuckle.AspNetCore) |
| | NSwag | [github.com/RicoSuter/NSwag](https://github.com/RicoSuter/NSwag) | [github.com/RicoSuter/NSwag](https://github.com/RicoSuter/NSwag) |
| | Hot Chocolate (GraphQL) | [chillicream.com/docs/hotchocolate](https://chillicream.com/docs/hotchocolate) | [github.com/ChilliCream/hotchocolate](https://github.com/ChilliCream/hotchocolate) |
| | GraphQL.NET | [graphql-dotnet.github.io](https://graphql-dotnet.github.io/) | [github.com/graphql-dotnet/graphql-dotnet](https://github.com/graphql-dotnet/graphql-dotnet) |
| | gRPC for .NET | [grpc.io/docs/languages/dotnet](https://grpc.io/docs/languages/dotnet/) | [github.com/grpc/grpc-dotnet](https://github.com/grpc/grpc-dotnet) |
| | RestSharp | [restsharp.dev](https://restsharp.dev/) | [github.com/restsharp/RestSharp](https://github.com/restsharp/RestSharp) |
| | Refit | [github.com/reactiveui/refit](https://github.com/reactiveui/refit) | [github.com/reactiveui/refit](https://github.com/reactiveui/refit) |
| | Flurl | [flurl.dev](https://flurl.dev/) | [github.com/tmenier/Flurl](https://github.com/tmenier/Flurl) |
| **Dependency Injection** | Autofac | [autofac.org](https://autofac.org/) | [github.com/autofac/Autofac](https://github.com/autofac/Autofac) |
| | Unity (Microsoft) | [github.com/unitycontainer/unity](https://github.com/unitycontainer/unity) | [github.com/unitycontainer/unity](https://github.com/unitycontainer/unity) |
| | Ninject | [ninject.org](https://ninject.org/) | [github.com/ninject/Ninject](https://github.com/ninject/Ninject) |
| | Castle Windsor | [castleproject.org](https://www.castleproject.org/) | [github.com/castleproject/Windsor](https://github.com/castleproject/Windsor) |
| | Simple Injector | [simpleinjector.org](https://simpleinjector.org/) | [github.com/simpleinjector/SimpleInjector](https://github.com/simpleinjector/SimpleInjector) |
| | DryIoc | [dryioc.com](https://www.dryioc.com/) | [github.com/dadhi/DryIoc](https://github.com/dadhi/DryIoc) |
| | LightInject | [lightinject.net](https://www.lightinject.net/) | [github.com/seesharper/LightInject](https://github.com/seesharper/LightInject) |
| **Caching** | StackExchange.Redis | [stackexchange.github.io/StackExchange.Redis](https://stackexchange.github.io/StackExchange.Redis/) | [github.com/StackExchange/StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) |
| | Microsoft.Extensions.Caching | [learn.microsoft.com/caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | CacheManager | [cachemanager.net](https://cachemanager.net/) | [github.com/MichaCo/CacheManager](https://github.com/MichaCo/CacheManager) |
| | FusionCache | [github.com/jodydonetti/ZiggyCreatures.FusionCache](https://github.com/jodydonetti/ZiggyCreatures.FusionCache) | [github.com/jodydonetti/ZiggyCreatures.FusionCache](https://github.com/jodydonetti/ZiggyCreatures.FusionCache) |
| **Authentication** | IdentityServer (Duende) | [duendesoftware.com/products/identityserver](https://duendesoftware.com/products/identityserver) | (коммерческая; OSS-версия — [github.com/IdentityServer/IdentityServer4](https://github.com/IdentityServer/IdentityServer4)) |
| | OpenIddict | [openiddict.com](https://openiddict.com/) | [github.com/openiddict/openiddict-core](https://github.com/openiddict/openiddict-core) |
| | Auth0 .NET SDK | [auth0.com/docs/quickstart/backend/dotnet](https://auth0.com/docs/quickstart/backend/dotnet) | [github.com/auth0/auth0-dotnet](https://github.com/auth0/auth0-dotnet) |
| | JWT (Microsoft.AspNetCore.Authentication.JwtBearer) | [learn.microsoft.com/jwt](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/jwt) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| | Identity (ASP.NET Core Identity) | [learn.microsoft.com/aspnet/identity](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity) | [github.com/dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) |
| **Machine Learning** | ML.NET | [dotnet.microsoft.com/ml-dotnet](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet) | [github.com/dotnet/machinelearning](https://github.com/dotnet/machinelearning) |
| | TensorFlow.NET | [github.com/SciSharp/TensorFlow.NET](https://github.com/SciSharp/TensorFlow.NET) | [github.com/SciSharp/TensorFlow.NET](https://github.com/SciSharp/TensorFlow.NET) |
| | TorchSharp | [github.com/dotnet/TorchSharp](https://github.com/dotnet/TorchSharp) | [github.com/dotnet/TorchSharp](https://github.com/dotnet/TorchSharp) |
| | ONNX Runtime .NET | [onnxruntime.ai](https://onnxruntime.ai/) | [github.com/microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |
| **Serialization** | Newtonsoft.Json (Json.NET) | [newtonsoft.com/json](https://www.newtonsoft.com/json) | [github.com/JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json) |
| | System.Text.Json | [learn.microsoft.com/system.text.json](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| | MessagePack for C# | [msgpack.org](https://msgpack.org/) | [github.com/neuecc/MessagePack-CSharp](https://github.com/neuecc/MessagePack-CSharp) |
| | Protobuf-net | [protobuf-net.github.io](https://protobuf-net.github.io/) | [github.com/protobuf-net/protobuf-net](https://github.com/protobuf-net/protobuf-net) |
| | YamlDotNet | [github.com/aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) | [github.com/aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) |
| **Validation** | FluentValidation | [fluentvalidation.net](https://fluentvalidation.net/) | [github.com/FluentValidation/FluentValidation](https://github.com/FluentValidation/FluentValidation) |
| | DataAnnotations (встроенный) | [learn.microsoft.com/datannotations](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| **Reactive Extensions** | Reactive Extensions (Rx.NET) | [reactivex.io](https://reactivex.io/) | [github.com/dotnet/reactive](https://github.com/dotnet/reactive) |
| | Dynamic Data | [github.com/reactivemarbles/DynamicData](https://github.com/reactivemarbles/DynamicData) | [github.com/reactivemarbles/DynamicData](https://github.com/reactivemarbles/DynamicData) |
| **Task Parallelism** | System.Threading.Tasks.Dataflow | [learn.microsoft.com/tpl-dataflow](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/dataflow-task-parallel-library) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |
| | Channel (System.Threading.Channels) | [learn.microsoft.com/channels](https://learn.microsoft.com/en-us/dotnet/api/system.threading.channels) | [github.com/dotnet/runtime](https://github.com/dotnet/runtime) |

### JAVA ЭКОСИСТЕМА

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Queue** | Apache Kafka (Java client) | [kafka.apache.org](https://kafka.apache.org/) | [github.com/apache/kafka](https://github.com/apache/kafka) |
| | RabbitMQ Java Client | [rabbitmq.com/java](https://rabbitmq.com/java.html) | [github.com/rabbitmq/rabbitmq-java-client](https://github.com/rabbitmq/rabbitmq-java-client) |
| | ActiveMQ Artemis | [activemq.apache.org](https://activemq.apache.org/) | [github.com/apache/activemq-artemis](https://github.com/apache/activemq-artemis) |
| | JMS (Java Message Service) | [jakarta.ee/specifications/jms](https://jakarta.ee/specifications/jms/) | [github.com/eclipse-ee4j/jms-api](https://github.com/eclipse-ee4j/jms-api) |
| **Actor Model** | Akka (Java/Scala) | [akka.io](https://akka.io/) | [github.com/akka/akka](https://github.com/akka/akka) |
| | Quasar (fibers) | [docs.paralleluniverse.co/quasar](https://docs.paralleluniverse.co/quasar/) | [github.com/puniverse/quasar](https://github.com/puniverse/quasar) |
| **Testing** | JUnit 5 | [junit.org](https://junit.org/) | [github.com/junit-team/junit5](https://github.com/junit-team/junit5) |
| | TestNG | [testng.org](https://testng.org/) | [github.com/testng-team/testng](https://github.com/testng-team/testng) |
| | Mockito | [site.mockito.org](https://site.mockito.org/) | [github.com/mockito/mockito](https://github.com/mockito/mockito) |
| | AssertJ | [assertj.github.io](https://assertj.github.io/doc/) | [github.com/assertj/assertj](https://github.com/assertj/assertj) |
| | Cucumber-JVM (BDD) | [cucumber.io](https://cucumber.io/) | [github.com/cucumber/cucumber-jvm](https://github.com/cucumber/cucumber-jvm) |
| | Selenium Java | [selenium.dev](https://www.selenium.dev/) | [github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) |
| | Testcontainers Java | [testcontainers.com](https://testcontainers.com/) | [github.com/testcontainers/testcontainers-java](https://github.com/testcontainers/testcontainers-java) |
| **Benchmarking** | JMH (Java Microbenchmark Harness) | [openjdk.org/projects/code-tools/jmh](https://openjdk.org/projects/code-tools/jmh/) | [github.com/openjdk/jmh](https://github.com/openjdk/jmh) |
| **Resilience** | Resilience4j | [resilience4j.readme.io](https://resilience4j.readme.io/) | [github.com/resilience4j/resilience4j](https://github.com/resilience4j/resilience4j) |
| | Hystrix | [github.com/Netflix/Hystrix](https://github.com/Netflix/Hystrix) | [github.com/Netflix/Hystrix](https://github.com/Netflix/Hystrix) |
| | Failsafe | [failsafe.dev](https://failsafe.dev/) | [github.com/failsafe-lib/failsafe](https://github.com/failsafe-lib/failsafe) |
| **Object Storage** | AWS S3 SDK | [aws.amazon.com/sdk-for-java](https://aws.amazon.com/sdk-for-java/) | [github.com/aws/aws-sdk-java](https://github.com/aws/aws-sdk-java) |
| | MinIO Java SDK | [min.io/docs/minio/linux/developers/java](https://min.io/docs/minio/linux/developers/java) | [github.com/minio/minio-java](https://github.com/minio/minio-java) |
| | Google Cloud Java SDK | [cloud.google.com/java](https://cloud.google.com/java) | [github.com/googleapis/google-cloud-java](https://github.com/googleapis/google-cloud-java) |
| **Office** | Apache POI | [poi.apache.org](https://poi.apache.org/) | [github.com/apache/poi](https://github.com/apache/poi) |
| | iText | [itextpdf.com](https://itextpdf.com/) | [github.com/itext/itext7](https://github.com/itext/itext7) |
| | Aspose.Words | [aspose.com/words/java](https://products.aspose.com/words/java/) | (коммерческий) |
| **UI Components** | JavaFX | [openjfx.io](https://openjfx.io/) | [github.com/openjdk/jfx](https://github.com/openjdk/jfx) |
| | Swing (встроенный) | [docs.oracle.com/javase/swing](https://docs.oracle.com/javase/tutorial/uiswing/) | (встроен в JDK) |
| | Vaadin | [vaadin.com](https://vaadin.com/) | [github.com/vaadin](https://github.com/vaadin) |
| **Web Framework** | Spring Boot | [spring.io/projects/spring-boot](https://spring.io/projects/spring-boot) | [github.com/spring-projects/spring-boot](https://github.com/spring-projects/spring-boot) |
| | Quarkus | [quarkus.io](https://quarkus.io/) | [github.com/quarkusio/quarkus](https://github.com/quarkusio/quarkus) |
| | Micronaut | [micronaut.io](https://micronaut.io/) | [github.com/micronaut-projects/micronaut-core](https://github.com/micronaut-projects/micronaut-core) |
| | Jakarta EE | [jakarta.ee](https://jakarta.ee/) | [github.com/eclipse-ee4j](https://github.com/eclipse-ee4j) |
| | Play Framework | [playframework.com](https://www.playframework.com/) | [github.com/playframework/playframework](https://github.com/playframework/playframework) |
| **ORM** | Hibernate ORM | [hibernate.org](https://hibernate.org/) | [github.com/hibernate/hibernate-orm](https://github.com/hibernate/hibernate-orm) |
| | MyBatis | [mybatis.org](https://mybatis.org/) | [github.com/mybatis/mybatis-3](https://github.com/mybatis/mybatis-3) |
| | EclipseLink | [eclipse.dev/eclipselink](https://eclipse.dev/eclipselink/) | [github.com/eclipse-ee4j/eclipselink](https://github.com/eclipse-ee4j/eclipselink) |
| | JPA (Jakarta Persistence) | [jakarta.ee/specifications/persistence](https://jakarta.ee/specifications/persistence/) | [github.com/eclipse-ee4j/jpa-api](https://github.com/eclipse-ee4j/jpa-api) |
| **DI** | Spring DI (Spring Framework) | [spring.io](https://spring.io/) | [github.com/spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) |
| | Dagger | [dagger.dev](https://dagger.dev/) | [github.com/google/dagger](https://github.com/google/dagger) |
| | Guice | [github.com/google/guice](https://github.com/google/guice) | [github.com/google/guice](https://github.com/google/guice) |
| **Caching** | Caffeine | [github.com/ben-manes/caffeine](https://github.com/ben-manes/caffeine) | [github.com/ben-manes/caffeine](https://github.com/ben-manes/caffeine) |
| | Ehcache | [ehcache.org](https://www.ehcache.org/) | [github.com/ehcache/ehcache3](https://github.com/ehcache/ehcache3) |
| | Redis client: Jedis / Lettuce | [redis.io/clients](https://redis.io/clients) | [github.com/redis/jedis](https://github.com/redis/jedis) / [github.com/lettuce-io/lettuce-core](https://github.com/lettuce-io/lettuce-core) |

### PYTHON ЭКОСИСТЕМА

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Framework** | Django | [djangoproject.com](https://www.djangoproject.com/) | [github.com/django/django](https://github.com/django/django) |
| | Flask | [flask.palletsprojects.com](https://flask.palletsprojects.com/) | [github.com/pallets/flask](https://github.com/pallets/flask) |
| | FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) | [github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi) |
| | ASGI (Starlette, Uvicorn) | [starlette.io](https://www.starlette.io/) / [uvicorn.org](https://www.uvicorn.org/) | [github.com/encode/starlette](https://github.com/encode/starlette) / [github.com/encode/uvicorn](https://github.com/encode/uvicorn) |
| **Testing** | pytest | [pytest.org](https://docs.pytest.org/) | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| | unittest (встроенный) | [docs.python.org/unittest](https://docs.python.org/3/library/unittest.html) | (встроен в Python) |
| | nose2 | [nose2.readthedocs.io](https://nose2.readthedocs.io/) | [github.com/nose-devs/nose2](https://github.com/nose-devs/nose2) |
| | doctest (встроенный) | [docs.python.org/doctest](https://docs.python.org/3/library/doctest.html) | (встроен в Python) |
| | mock (unittest.mock) | [docs.python.org/mock](https://docs.python.org/3/library/unittest.mock.html) | (встроен в Python) |
| | Selenium | [selenium-python.readthedocs.io](https://selenium-python.readthedocs.io/) | [github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) |
| | Playwright | [playwright.dev/python](https://playwright.dev/python/) | [github.com/microsoft/playwright-python](https://github.com/microsoft/playwright-python) |
| **Resilience** | Tenacity | [tenacity.readthedocs.io](https://tenacity.readthedocs.io/) | [github.com/jd/tenacity](https://github.com/jd/tenacity) |
| **Object Storage** | Boto3 (AWS S3) | [boto3.amazonaws.com](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) | [github.com/boto/boto3](https://github.com/boto/boto3) |
| | MinIO Python SDK | [min.io/docs/minio/linux/developers/python](https://min.io/docs/minio/linux/developers/python) | [github.com/minio/minio-py](https://github.com/minio/minio-py) |
| **Office** | OpenPyXL | [openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/) | [github.com/theorchard/openpyxl](https://github.com/theorchard/openpyxl) |
| | python-docx | [python-docx.readthedocs.io](https://python-docx.readthedocs.io/) | [github.com/python-openxml/python-docx](https://github.com/python-openxml/python-docx) |
| | ReportLab | [reportlab.com](https://www.reportlab.com/) | [github.com/MrBitBucket/reportlab](https://github.com/MrBitBucket/reportlab) |
| | PyPDF2 | [pypdf2.readthedocs.io](https://pypdf2.readthedocs.io/) | [github.com/py-pdf/pypdf](https://github.com/py-pdf/pypdf) |
| | xlrd / xlwt | [github.com/python-excel/xlrd](https://github.com/python-excel/xlrd) / [github.com/python-excel/xlwt](https://github.com/python-excel/xlwt) | [github.com/python-excel](https://github.com/python-excel) |
| **ORM** | SQLAlchemy | [sqlalchemy.org](https://www.sqlalchemy.org/) | [github.com/sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) |
| | Django ORM (встроенный в Django) | [docs.djangoproject.com/topics/db](https://docs.djangoproject.com/en/stable/topics/db/) | [github.com/django/django](https://github.com/django/django) |
| | Peewee | [docs.peewee-orm.com](https://docs.peewee-orm.com/) | [github.com/coleifer/peewee](https://github.com/coleifer/peewee) |
| | PonyORM | [ponyorm.com](https://ponyorm.com/) | [github.com/ponyorm/pony](https://github.com/ponyorm/pony) |
| **ML/AI** | TensorFlow | [tensorflow.org](https://www.tensorflow.org/) | [github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) |
| | PyTorch | [pytorch.org](https://pytorch.org/) | [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) |
| | Scikit-learn | [scikit-learn.org](https://scikit-learn.org/) | [github.com/scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) |
| | Keras | [keras.io](https://keras.io/) | [github.com/keras-team/keras](https://github.com/keras-team/keras) |
| | XGBoost | [xgboost.ai](https://xgboost.ai/) | [github.com/dmlc/xgboost](https://github.com/dmlc/xgboost) |
| | LightGBM | [lightgbm.readthedocs.io](https://lightgbm.readthedocs.io/) | [github.com/microsoft/LightGBM](https://github.com/microsoft/LightGBM) |
| | Hugging Face Transformers | [huggingface.co/transformers](https://huggingface.co/transformers/) | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| | LangChain | [langchain.com](https://www.langchain.com/) | [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| | LlamaIndex | [llamaindex.ai](https://www.llamaindex.ai/) | [github.com/run-llama/llama_index](https://github.com/run-llama/llama_index) |


### JAVASCRIPT / TYPESCRIPT ЭКОСИСТЕМА (Node.js + Frontend)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Queue (Node.js)** | amqplib (RabbitMQ) | [github.com/amqp-node/amqplib](https://github.com/amqp-node/amqplib) | [github.com/amqp-node/amqplib](https://github.com/amqp-node/amqplib) |
| | kafkajs (Kafka) | [kafkajs.github.io](https://kafkajs.github.io/) | [github.com/tulios/kafkajs](https://github.com/tulios/kafkajs) |
| | AWS SQS (Node.js SDK) | [aws.amazon.com/sdk-for-javascript](https://aws.amazon.com/sdk-for-javascript/) | [github.com/aws/aws-sdk-js](https://github.com/aws/aws-sdk-js) |
| | Bull (Redis queues) | [github.com/OptimalBits/bull](https://github.com/OptimalBits/bull) | [github.com/OptimalBits/bull](https://github.com/OptimalBits/bull) |
| | BullMQ | [bullmq.io](https://bullmq.io/) | [github.com/taskforcesh/bullmq](https://github.com/taskforcesh/bullmq) |
| **Web Framework (Node.js)** | Express.js | [expressjs.com](https://expressjs.com/) | [github.com/expressjs/express](https://github.com/expressjs/express) |
| | NestJS | [nestjs.com](https://nestjs.com/) | [github.com/nestjs/nest](https://github.com/nestjs/nest) |
| | Fastify | [fastify.io](https://fastify.io/) | [github.com/fastify/fastify](https://github.com/fastify/fastify) |
| | Koa | [koajs.com](https://koajs.com/) | [github.com/koajs/koa](https://github.com/koajs/koa) |
| | Sails.js | [sailsjs.com](https://sailsjs.com/) | [github.com/balderdashy/sails](https://github.com/balderdashy/sails) |
| **Frontend Frameworks** | React | [react.dev](https://react.dev/) | [github.com/facebook/react](https://github.com/facebook/react) |
| | Angular | [angular.dev](https://angular.dev/) | [github.com/angular/angular](https://github.com/angular/angular) |
| | Vue.js | [vuejs.org](https://vuejs.org/) | [github.com/vuejs/core](https://github.com/vuejs/core) |
| | Svelte | [svelte.dev](https://svelte.dev/) | [github.com/sveltejs/svelte](https://github.com/sveltejs/svelte) |
| | Solid.js | [solidjs.com](https://www.solidjs.com/) | [github.com/solidjs/solid](https://github.com/solidjs/solid) |
| | Alpine.js | [alpinejs.dev](https://alpinejs.dev/) | [github.com/alpinejs/alpine](https://github.com/alpinejs/alpine) |
| | jQuery | [jquery.com](https://jquery.com/) | [github.com/jquery/jquery](https://github.com/jquery/jquery) |
| | HTMX | [htmx.org](https://htmx.org/) | [github.com/bigskysoftware/htmx](https://github.com/bigskysoftware/htmx) |
| **State Management (JS)** | Redux | [redux.js.org](https://redux.js.org/) | [github.com/reduxjs/redux](https://github.com/reduxjs/redux) |
| | MobX | [mobx.js.org](https://mobx.js.org/) | [github.com/mobxjs/mobx](https://github.com/mobxjs/mobx) |
| | Zustand | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) |
| | Jotai | [jotai.org](https://jotai.org/) | [github.com/pmndrs/jotai](https://github.com/pmndrs/jotai) |
| | Recoil | [recoiljs.org](https://recoiljs.org/) | [github.com/facebookexperimental/Recoil](https://github.com/facebookexperimental/Recoil) |
| | Pinia (Vue) | [pinia.vuejs.org](https://pinia.vuejs.org/) | [github.com/vuejs/pinia](https://github.com/vuejs/pinia) |
| | Vuex (Vue) | [vuex.vuejs.org](https://vuex.vuejs.org/) | [github.com/vuejs/vuex](https://github.com/vuejs/vuex) |
| | NgRx (Angular) | [ngrx.io](https://ngrx.io/) | [github.com/ngrx/platform](https://github.com/ngrx/platform) |
| **Testing (JS)** | Jest | [jestjs.io](https://jestjs.io/) | [github.com/jestjs/jest](https://github.com/jestjs/jest) |
| | Mocha | [mochajs.org](https://mochajs.org/) | [github.com/mochajs/mocha](https://github.com/mochajs/mocha) |
| | Jasmine | [jasmine.github.io](https://jasmine.github.io/) | [github.com/jasmine/jasmine](https://github.com/jasmine/jasmine) |
| | Cypress | [cypress.io](https://www.cypress.io/) | [github.com/cypress-io/cypress](https://github.com/cypress-io/cypress) |
| | Playwright (JS) | [playwright.dev](https://playwright.dev/) | [github.com/microsoft/playwright](https://github.com/microsoft/playwright) |
| | Puppeteer | [pptr.dev](https://pptr.dev/) | [github.com/puppeteer/puppeteer](https://github.com/puppeteer/puppeteer) |
| | Sinon.js (mocks) | [sinonjs.org](https://sinonjs.org/) | [github.com/sinonjs/sinon](https://github.com/sinonjs/sinon) |
| **ORM (Node.js)** | Sequelize | [sequelize.org](https://sequelize.org/) | [github.com/sequelize/sequelize](https://github.com/sequelize/sequelize) |
| | TypeORM | [typeorm.io](https://typeorm.io/) | [github.com/typeorm/typeorm](https://github.com/typeorm/typeorm) |
| | Prisma | [prisma.io](https://www.prisma.io/) | [github.com/prisma/prisma](https://github.com/prisma/prisma) |
| | MikroORM | [mikro-orm.io](https://mikro-orm.io/) | [github.com/mikro-orm/mikro-orm](https://github.com/mikro-orm/mikro-orm) |
| | Drizzle ORM | [orm.drizzle.team](https://orm.drizzle.team/) | [github.com/drizzle-team/drizzle-orm](https://github.com/drizzle-team/drizzle-orm) |
| **API (Node.js)** | Axios | [axios-http.com](https://axios-http.com/) | [github.com/axios/axios](https://github.com/axios/axios) |
| | Fetch API (встроенный) | [developer.mozilla.org/fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) | (встроен) |
| | GraphQL (JS) | [graphql.org](https://graphql.org/) | [github.com/graphql/graphql-js](https://github.com/graphql/graphql-js) |
| | Apollo Client/Server | [apollographql.com](https://www.apollographql.com/) | [github.com/apollographql](https://github.com/apollographql) |

### GO ЭКОСИСТЕМА

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Framework** | Gin | [gin-gonic.com](https://gin-gonic.com/) | [github.com/gin-gonic/gin](https://github.com/gin-gonic/gin) |
| | Echo | [echo.labstack.com](https://echo.labstack.com/) | [github.com/labstack/echo](https://github.com/labstack/echo) |
| | Fiber | [gofiber.io](https://gofiber.io/) | [github.com/gofiber/fiber](https://github.com/gofiber/fiber) |
| | Gorilla/Mux | [github.com/gorilla/mux](https://github.com/gorilla/mux) | [github.com/gorilla/mux](https://github.com/gorilla/mux) |
| | Chi | [github.com/go-chi/chi](https://github.com/go-chi/chi) | [github.com/go-chi/chi](https://github.com/go-chi/chi) |
| **Testing** | Testing (встроенный) | [pkg.go.dev/testing](https://pkg.go.dev/testing) | (встроен) |
| | Testify | [github.com/stretchr/testify](https://github.com/stretchr/testify) | [github.com/stretchr/testify](https://github.com/stretchr/testify) |
| | Ginkgo | [onsi.github.io/ginkgo](https://onsi.github.io/ginkgo/) | [github.com/onsi/ginkgo](https://github.com/onsi/ginkgo) |
| | GoMock | [github.com/uber-go/mock](https://github.com/uber-go/mock) | [github.com/uber-go/mock](https://github.com/uber-go/mock) |
| **Resilience** | Retry | [github.com/avast/retry-go](https://github.com/avast/retry-go) | [github.com/avast/retry-go](https://github.com/avast/retry-go) |
| | CircuitBreaker | [github.com/sony/gobreaker](https://github.com/sony/gobreaker) | [github.com/sony/gobreaker](https://github.com/sony/gobreaker) |
| **Object Storage** | AWS SDK for Go | [aws.amazon.com/sdk-for-go](https://aws.amazon.com/sdk-for-go/) | [github.com/aws/aws-sdk-go](https://github.com/aws/aws-sdk-go) |
| | MinIO Go SDK | [min.io/docs/minio/linux/developers/go](https://min.io/docs/minio/linux/developers/go) | [github.com/minio/minio-go](https://github.com/minio/minio-go) |
| **ORM** | GORM | [gorm.io](https://gorm.io/) | [github.com/go-gorm/gorm](https://github.com/go-gorm/gorm) |
| | Ent (Facebook) | [entgo.io](https://entgo.io/) | [github.com/ent/ent](https://github.com/ent/ent) |
| | sqlx | [github.com/jmoiron/sqlx](https://github.com/jmoiron/sqlx) | [github.com/jmoiron/sqlx](https://github.com/jmoiron/sqlx) |

### RUST ЭКОСИСТЕМА

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Web Framework** | Actix Web | [actix.rs](https://actix.rs/) | [github.com/actix/actix-web](https://github.com/actix/actix-web) |
| | Rocket | [rocket.rs](https://rocket.rs/) | [github.com/rwf2/Rocket](https://github.com/rwf2/Rocket) |
| | Axum | [github.com/tokio-rs/axum](https://github.com/tokio-rs/axum) | [github.com/tokio-rs/axum](https://github.com/tokio-rs/axum) |
| | Warp | [github.com/seanmonstar/warp](https://github.com/seanmonstar/warp) | [github.com/seanmonstar/warp](https://github.com/seanmonstar/warp) |
| **Testing** | Rust (встроенный тест-раннер) | [doc.rust-lang.org/book/testing](https://doc.rust-lang.org/book/testing.html) | (встроен) |
| | Criterion (Benchmark) | [bheisler.github.io/criterion.rs](https://bheisler.github.io/criterion.rs/) | [github.com/bheisler/criterion.rs](https://github.com/bheisler/criterion.rs) |
| **ORM** | Diesel | [diesel.rs](https://diesel.rs/) | [github.com/diesel-rs/diesel](https://github.com/diesel-rs/diesel) |
| | SeaORM | [www.sea-ql.org/SeaORM](https://www.sea-ql.org/SeaORM/) | [github.com/SeaQL/sea-orm](https://github.com/SeaQL/sea-orm) |

### C++ ЭКОСИСТЕМА

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Benchmarking** | Google Benchmark | [github.com/google/benchmark](https://github.com/google/benchmark) | [github.com/google/benchmark](https://github.com/google/benchmark) |
| **Web Framework** | Crow | [crowcpp.org](https://crowcpp.org/) | [github.com/CrowCpp/Crow](https://github.com/CrowCpp/Crow) |
| | Drogon | [drogon.org](https://drogon.org/) | [github.com/drogonframework/drogon](https://github.com/drogonframework/drogon) |

### ОБЩЕПЛАТФОРМЕННЫЕ / ИНФРАСТРУКТУРНЫЕ (CrossPlatform)

| Группа | Наименование | Сайт / Документация | Git-репозиторий |
|:-------|:-------------|:--------------------|:----------------|
| **Message Queue** | Apache Kafka | [kafka.apache.org](https://kafka.apache.org/) | [github.com/apache/kafka](https://github.com/apache/kafka) |
| | RabbitMQ Server | [rabbitmq.com](https://rabbitmq.com/) | [github.com/rabbitmq/rabbitmq-server](https://github.com/rabbitmq/rabbitmq-server) |
| | Redis (Pub/Sub, Streams) | [redis.io](https://redis.io/) | [github.com/redis/redis](https://github.com/redis/redis) |
| | NSQ | [nsq.io](https://nsq.io/) | [github.com/nsqio/nsq](https://github.com/nsqio/nsq) |
| | NATS Server | [nats.io](https://nats.io/) | [github.com/nats-io/nats-server](https://github.com/nats-io/nats-server) |
| | Apache Pulsar | [pulsar.apache.org](https://pulsar.apache.org/) | [github.com/apache/pulsar](https://github.com/apache/pulsar) |
| | ZeroMQ (C++) | [zeromq.org](https://zeromq.org/) | [github.com/zeromq/libzmq](https://github.com/zeromq/libzmq) |
| **Object Storage** | MinIO Server | [min.io](https://min.io/) | [github.com/minio/minio](https://github.com/minio/minio) |
| | Ceph (S3-compatible) | [ceph.io](https://ceph.io/) | [github.com/ceph/ceph](https://github.com/ceph/ceph) |
| **UI Frameworks** | Electron (JS/HTML/CSS) | [electronjs.org](https://www.electronjs.org/) | [github.com/electron/electron](https://github.com/electron/electron) |
| | Flutter (Dart) | [flutter.dev](https://flutter.dev/) | [github.com/flutter/flutter](https://github.com/flutter/flutter) |
| | React Native (JS) | [reactnative.dev](https://reactnative.dev/) | [github.com/facebook/react-native](https://github.com/facebook/react-native) |
| | Qt (C++) | [qt.io](https://www.qt.io/) | [github.com/qt](https://github.com/qt) |
| **ML/AI** | ONNX Runtime | [onnxruntime.ai](https://onnxruntime.ai/) | [github.com/microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |
| | OpenCV (CV/AI) | [opencv.org](https://opencv.org/) | [github.com/opencv/opencv](https://github.com/opencv/opencv) |
| **Authentication** | Keycloak | [keycloak.org](https://www.keycloak.org/) | [github.com/keycloak/keycloak](https://github.com/keycloak/keycloak) |
| | OAuth2/OpenID Connect (Ory Hydra) | [ory.sh/hydra](https://www.ory.sh/hydra/) | [github.com/ory/hydra](https://github.com/ory/hydra) |
| | Auth0 (SaaS) | [auth0.com](https://auth0.com/) | [github.com/auth0](https://github.com/auth0) |
| | Okta (SaaS) | [okta.com](https://www.okta.com/) | [github.com/okta](https://github.com/okta) |

---
>Таблица охватывает **более 250 библиотек** из всех популярных экосистем, сгруппированных по функциональному назначению внутри каждой платформы.