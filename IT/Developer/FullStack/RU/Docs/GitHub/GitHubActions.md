### **GitHub Actions: что это и как использовать**



## Оглавление
  - [**GitHub Actions: что это и как использовать**](#github-actions-что-это-и-как-использовать)
- [**Зачем нужен GitHub Actions?**](#зачем-нужен-github-actions)
- [**Основные понятия**](#основные-понятия)
  - [**1. Workflow**](#1-workflow)
  - [**2. Event (Событие)**](#2-event-событие)
  - [**3. Job**](#3-job)
  - [**4. Step**](#4-step)
  - [**5. Runner**](#5-runner)
- [**Как использовать GitHub Actions?**](#как-использовать-github-actions)
  - [**1. Создание первого workflow**](#1-создание-первого-workflow)
  - [**2. Пример простого workflow**](#2-пример-простого-workflow)
  - [**3. Объяснение ключевых элементов**](#3-объяснение-ключевых-элементов)
  - [**4. Пример workflow с Docker**](#4-пример-workflow-с-docker)
  - [**5. Использование секретов**](#5-использование-секретов)
  - [**6. Пример workflow с расписанием**](#6-пример-workflow-с-расписанием)
  - [**7. Пример workflow с матрицей**](#7-пример-workflow-с-матрицей)
- [**Преимущества GitHub Actions**](#преимущества-github-actions)
- [**Недостатки**](#недостатки)
- [**Когда использовать?**](#когда-использовать)
- [**GitHub Actions и Docker**](#github-actions-и-docker)
  - [**Зачем использовать GitHub Actions с Docker?**](#зачем-использовать-github-actions-с-docker)
- [**Как использовать GitHub Actions с Docker?**](#как-использовать-github-actions-с-docker)
  - [**1. Создание workflow-файла**](#1-создание-workflow-файла)
  - [**2. Пример workflow для сборки и публикации Docker-образа**](#2-пример-workflow-для-сборки-и-публикации-docker-образа)
  - [**3. Объяснение шагов**](#3-объяснение-шагов)
  - [**4. Настройка секретов**](#4-настройка-секретов)
  - [**5. Пример с тестированием в контейнере**](#5-пример-с-тестированием-в-контейнере)
  - [**6. Пример развёртывания на сервер**](#6-пример-развёртывания-на-сервер)
- [**Преимущества использования GitHub Actions с Docker**](#преимущества-использования-github-actions-с-docker)
- [**Недостатки**](#недостатки)
- [**Когда использовать?**](#когда-использовать)

  - [**GitHub Actions: что это и как использовать**](#github-actions-что-это-и-как-использовать)
  - [**1. Workflow**](#1-workflow)
  - [**2. Event (Событие)**](#2-event-событие)
  - [**3. Job**](#3-job)
  - [**4. Step**](#4-step)
  - [**5. Runner**](#5-runner)
  - [**1. Создание первого workflow**](#1-создание-первого-workflow)
  - [**2. Пример простого workflow**](#2-пример-простого-workflow)
  - [**3. Объяснение ключевых элементов**](#3-объяснение-ключевых-элементов)
  - [**4. Пример workflow с Docker**](#4-пример-workflow-с-docker)
  - [**5. Использование секретов**](#5-использование-секретов)
  - [**6. Пример workflow с расписанием**](#6-пример-workflow-с-расписанием)
  - [**7. Пример workflow с матрицей**](#7-пример-workflow-с-матрицей)
  - [**Зачем использовать GitHub Actions с Docker?**](#зачем-использовать-github-actions-с-docker)
  - [**1. Создание workflow-файла**](#1-создание-workflow-файла)
  - [**2. Пример workflow для сборки и публикации Docker-образа**](#2-пример-workflow-для-сборки-и-публикации-docker-образа)
  - [**3. Объяснение шагов**](#3-объяснение-шагов)
  - [**4. Настройка секретов**](#4-настройка-секретов)
  - [**5. Пример с тестированием в контейнере**](#5-пример-с-тестированием-в-контейнере)
  - [**6. Пример развёртывания на сервер**](#6-пример-развёртывания-на-сервер)
**GitHub Actions** — это платформа для автоматизации рабочих процессов (CI/CD и не только) прямо в репозиториях GitHub. Она позволяет создавать **workflows** (последовательности задач), которые запускаются по событиям (например, при пуше в репозиторий, создании pull request, по расписанию и т. д.).

---

## **Зачем нужен GitHub Actions?**
- **Автоматизация CI/CD**: Сборка, тестирование и развёртывание кода.
- **Автоматизация рутинных задач**: Проверка кода, генерация документации, отправка уведомлений.
- **Интеграция с другими сервисами**: Развёртывание в облака, отправка сообщений в Slack, обновление баз данных и т. д.
- **Гибкость**: Поддержка любых языков и инструментов.

---

## **Основные понятия**

### **1. Workflow**
Файл в формате YAML, который описывает последовательность задач (jobs). Хранится в папке `.github/workflows/` в репозитории.

### **2. Event (Событие)**
Триггер, который запускает workflow. Примеры:
- `push` — при пуше в ветку.
- `pull_request` — при создании pull request.
- `schedule` — по расписанию (например, каждый день в 10:00).
- `workflow_dispatch` — ручной запуск.

### **3. Job**
Набор шагов (steps), выполняемых на одном runners (виртуальной машине или контейнере).

### **4. Step**
Отдельная команда или действие (action). Например:
- Выполнение скрипта.
- Запуск готовой action из GitHub Marketplace.

### **5. Runner**
Среда выполнения workflow. Бывает:
- **GitHub-hosted**: Виртуальные машины от GitHub (Ubuntu, Windows, macOS).
- **Self-hosted**: Ваши собственные серверы.

---

## **Как использовать GitHub Actions?**

---

### **1. Создание первого workflow**
1. В репозитории создайте папку:
   `.github/workflows/`
2. Добавьте файл, например, `ci.yml`.

---

### **2. Пример простого workflow**
```yaml
name: CI  # Название workflow

on: [push]  # Запускать при каждом пуше в репозиторий

jobs:
  build-and-test:  # Название job
    runs-on: ubuntu-latest  # Среда выполнения

    steps:
      - name: Checkout code  # Шаг 1: Клонировать репозиторий
        uses: actions/checkout@v4  # Готовая action из Marketplace

      - name: Install dependencies  # Шаг 2: Установить зависимости
        run: npm install  # Команда для выполнения

      - name: Run tests  # Шаг 3: Запустить тесты
        run: npm test
```

---

### **3. Объяснение ключевых элементов**
- **`name`**: Название workflow.
- **`on`**: Событие, которое запускает workflow.
- **`jobs`**: Список задач.
- **`runs-on`**: Операционная система для выполнения.
- **`steps`**: Последовательность действий.
  - **`uses`**: Использование готовой action (например, `actions/checkout` для клонирования репозитория).
  - **`run`**: Выполнение команд в терминале.

---

### **4. Пример workflow с Docker**
```yaml
name: Docker Build and Push

on:
  push:
    branches: ["main"]

env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
  IMAGE_NAME: my-app

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        run: echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

      - name: Build Docker image
        run: docker build -t $DOCKER_USERNAME/$IMAGE_NAME:latest .

      - name: Push to Docker Hub
        run: docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
```

---

### **5. Использование секретов**
Для хранения конфиденциальных данных (паролей, токенов) используйте **GitHub Secrets**:
1. Перейдите в репозиторий → **Settings** → **Secrets and variables** → **Actions**.
2. Добавьте секреты (например, `DOCKER_USERNAME` и `DOCKER_PASSWORD`).
3. Используйте их в workflow через `${{ secrets.NAME }}`.

---

### **6. Пример workflow с расписанием**
```yaml
name: Scheduled Task

on:
  schedule:
    - cron: '0 10 * * *'  # Каждый день в 10:00 UTC

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running cleanup task..."
```

---

### **7. Пример workflow с матрицей**
Можно запускать задачи для разных версий языка или ОС:
```yaml
name: Test Matrix

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm install
      - run: npm test
```

---

## **Преимущества GitHub Actions**
- **Встроенность в GitHub**: Не нужно настраивать внешние CI/CD-системы.
- **Гибкость**: Поддержка любых языков и инструментов.
- **Готовые action**: Тысячи готовых решений в [GitHub Marketplace](https://github.com/marketplace?type=actions).
- **Бесплатные минуты**: Для публичных и приватных репозиториев.

---

## **Недостатки**
- **Ограничения бесплатного тарифа**: Ограниченное количество минут для приватных репозиториев.
- **Зависимость от GitHub**: Если GitHub недоступен, CI/CD не работает.

---

## **Когда использовать?**
- Для автоматизации тестирования и развёртывания.
- Для запуска скриптов по расписанию.
- Для интеграции с облачными сервисами (AWS, Azure, GCP).
- Для уведомлений в Slack, Telegram и другие мессенджеры.

---

1. **GitHub Actions для работы с Docker** – автоматизация сборки, тестирования и развёртывания Docker-контейнеров в CI/CD-пайплайнах GitHub.
2. **Docker в составе других "Actions"** – например, использование Docker в скриптах или автоматизации (например, в GitLab CI/CD, Jenkins и т. д.).
3. **Docker Events или Hooks** – автоматические действия при событиях в Docker (например, запуск контейнера, остановка и т. д.).

---
Давай разберём самый популярный вариант: **GitHub Actions для работы с Docker**.

---

## **GitHub Actions и Docker**
**GitHub Actions** – это инструмент для автоматизации рабочих процессов (CI/CD) в репозиториях GitHub. С его помощью можно автоматически собирать, тестировать и развёртывать Docker-образы.

---

### **Зачем использовать GitHub Actions с Docker?**
- Автоматическая сборка Docker-образов при каждом коммите.
- Запуск тестов в контейнерах.
- Развёртывание контейнеров в облачные сервисы (AWS, GCP, Azure) или на серверы.
- Публикация образов в Docker Hub или другие реестры.

---

## **Как использовать GitHub Actions с Docker?**

### **1. Создание workflow-файла**
В репозитории создайте папку `.github/workflows` и добавьте файл, например, `docker-build.yml`.

---

### **2. Пример workflow для сборки и публикации Docker-образа**
```yaml
name: Docker Build and Push

on:
  push:
    branches: [ "main" ]  # Запускать при пуше в ветку main

env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
  IMAGE_NAME: my-docker-image

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build Docker image
        run: docker build -t $DOCKER_USERNAME/$IMAGE_NAME:latest .

      - name: Push Docker image
        run: docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
```

---

### **3. Объяснение шагов**
- **`on`**: Указывает, когда запускать workflow (например, при пуше в ветку `main`).
- **`env`**: Переменные окружения, включая секреты (например, логин и пароль от Docker Hub).
- **`jobs`**: Определяет задачи, которые нужно выполнить:
  - **Checkout code**: Клонирует репозиторий.
  - **Login to Docker Hub**: Авторизуется в Docker Hub.
  - **Build Docker image**: Собирает Docker-образ.
  - **Push Docker image**: Публикует образ в Docker Hub.

---

### **4. Настройка секретов**
1. Перейдите в репозиторий на GitHub → **Settings** → **Secrets and variables** → **Actions**.
2. Добавьте секреты:
   - `DOCKER_USERNAME` – ваш логин в Docker Hub.
   - `DOCKER_PASSWORD` – ваш пароль или токен от Docker Hub.

---

### **5. Пример с тестированием в контейнере**
```yaml
name: Docker Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t my-app:test .

      - name: Run tests
        run: docker run my-app:test npm test
```

---

### **6. Пример развёртывания на сервер**
```yaml
name: Deploy to Server

on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t my-app:latest .

      - name: Deploy to server
        run: |
          ssh user@server "docker pull my-app:latest && docker stop my-app || true && docker rm my-app || true"
          ssh user@server "docker run -d --name my-app -p 80:80 my-app:latest"
```

---

## **Преимущества использования GitHub Actions с Docker**
- **Автоматизация**: Все процессы (сборка, тестирование, развёртывание) выполняются автоматически.
- **Интеграция с GitHub**: Не нужно настраивать внешние CI/CD-системы.
- **Гибкость**: Можно настроить любые сценарии (мультистадийные пайплайны, параллельные задачи и т. д.).
- **Безопасность**: Секреты хранятся в GitHub, не попадают в код.

---

## **Недостатки**
- **Ограничения бесплатного тарифа**: Ограниченное количество минут для выполнения задач.
- **Зависимость от GitHub**: Если GitHub недоступен, CI/CD не работает.

---

## **Когда использовать?**
- Для автоматизации сборки и публикации Docker-образов.
- Для запуска тестов в контейнерах.
- Для развёртывания приложений в облака или на серверы.

---