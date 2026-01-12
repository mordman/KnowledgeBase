### **Official**
- **Официальный сайт**: https://xmlgraphics.apache.org/fop/
- **Разработчик**: Apache Software Foundation
- **Лицензия**: Apache License 2.0
- **Статус**: Активно развивается

### **Docker**
- Нет официального образа от Apache; доступны неофициальные сборки в Docker Hub.
- Пример `Dockerfile` для запуска FOP:
  ```dockerfile
  FROM openjdk:11-jre-slim
  RUN apt-get update && apt-get install -y wget
  RUN wget https://downloads.apache.org/xmlgraphics/fop/binaries/fop-2.9-bin.tar.gz && \
      tar -xzf fop-2.9-bin.tar.gz -C /opt && \
      ln -s /opt/fop-2.9 /opt/fop
  ENV PATH="/opt/fop:$PATH"
  CMD ["fop", "-version"]
  ```
- **Использование**: запуск в контейнере для генерации PDF/PNG из XSL-FO.

### **Git**
- **Исходный код**: https://github.com/apache/xmlgraphics-fop
- Репозиторий — часть проекта Apache XML Graphics.
- Вклад и баг-репорты принимаются через GitHub или JIRA Apache.

### **Documentation**
- **Официальная документация**: https://xmlgraphics.apache.org/fop/2.9/
- **Руководства**:
  - Quick Start Guide: https://xmlgraphics.apache.org/fop/2.9/quickstartguide.html
  - Running FOP: https://xmlgraphics.apache.org/fop/2.9/running.html
  - XSL-FO Reference: https://www.w3.org/TR/xsl11/
- **Примеры**: XSL-FO и XML поставляются в комплекте с дистрибутивом.

### **Files**
- **Дистрибутивы**:
  - Скачать FOP (binaries и исходники): https://xmlgraphics.apache.org/fop/download.html
  - Форматы: `.tar.gz`, `.zip`
- **Основные файлы в дистрибутиве**:
  - `fop.jar` — основной исполняемый файл
  - `fop.xconf` — конфигурационный файл
  - `examples/` — примеры XML, XSLT, XSL-FO
  - `docs/` — локальная копия документации
- **Конфигурация**: `fop.xconf` для настройки шрифтов, рендереров и других параметров.
