# A task for candidates for full-stack developer (C#, JavaScript).

## Prerequisites

It is okay if you didn't work with Vue 2 or 3, if you know React or Angular you will learn it fast. We use Vue 3 in our projects.

## Part 1

You need to develop a tiny application for submitting web forms, storing submissions, listing and searching them.

1. Create an arbitrary form with CSS and Vue as a JavaScript framework. Say, a contact or order form with at least five fields of different types: text, drop-down, date, radio, checkbox.

2. Add validation for the form fields.

3. Implement a REST-service using C# and ASP.NET Core:

   a. The service should provide all necessary methods for your frontend.

   b. It should allow receiving and storing submissions without hard coded models. Imagine there is another frontend application with different form fields that uses the same backend. Backend should know nothing about the data structure

   c. For storing your data, use either In-Memory database or any other storage that won't require us to set up database servers or register in any online services. It is easier for us to review your task this way.

4. Add UI for listing and searching the submitted objects from different forms on one page.

5. Pack all JS- and CSS-files of the project into a single file with the help of a build system of your choice (Vite or Webpack).

The test task is quite basic but consider it as a real-life application. Thus, try to create good architecture and level of abstraction. We will evaluate the quality of your code, your tool chain, usability of the UI and the architecture in general.

## Part 2

Now, let's imagine the web forms support large attachments (~100MB). Describe in text how to handle storage and downloads from the submissions list, considering thousands of submissions with multiple attachments each. Include architecture, data structure, and REST API.

## Results

Publish your code to the GIT repository. Don't use any "Plumsail" related words in the repository to prevent other candidates from finding your implementation and taking credit for it.

Send results to <recruitment@plumsail.com> with the link to your HH resume.

## Deadlines

There is no strict deadline. We understand that you may be working on another job. It would be great if you could complete it in a week.

---
# Тестовое задание для кандидатов на позицию full-stack разработчика (C#, JavaScript).

## Предварительные условия

Нормально, если вы не работали с Vue 2 или 3. Если вы знаете React или Angular, вы быстро его освоите. Мы используем Vue 3 в наших проектах.

## Часть 1

Вам необходимо разработать небольшое приложение для отправки веб-форм, хранения отправленных данных, их просмотра и поиска.

1.  Создайте произвольную форму с использованием CSS и Vue в качестве JavaScript-фреймворка. Например, контактную форму или форму заказа как минимум с пятью полями разных типов: текстовое поле, выпадающий список, дата, радио-кнопки, чекбокс.

2.  Добавьте валидацию для полей формы.

3.  Реализуйте REST-сервис с использованием C# и ASP.NET Core:

    a. Сервис должен предоставлять все необходимые методы для вашего фронтенда.

    b. Он должен позволять принимать и сохранять отправленные данные без жестко заданных моделей. Представьте, что существует другое фронтенд-приложение с другими полями формы, которое использует тот же бэкенд. Бэкенд не должен ничего знать о структуре данных.

    c. Для хранения данных используйте либо базу данных In-Memory, либо любое другое хранилище, которое не потребует от нас настройки серверов баз данных или регистрации в каких-либо онлайн-сервисах. Так нам будет проще оценить ваше задание.

4.  Добавьте пользовательский интерфейс для просмотра списка и поиска отправленных объектов из разных форм на одной странице.

5.  Соберите все JS- и CSS-файлы проекта в один файл с помощью выбранной вами системы сборки (Vite или Webpack).

Тестовое задание довольно базовое, но рассматривайте его как реальное приложение. Таким образом, постарайтесь создать хорошую архитектуру и уровень абстракции. Мы будем оценивать качество вашего кода, ваш инструментарий, удобство использования пользовательского интерфейса и архитектуру в целом.

## Часть 2

Теперь представьте, что веб-формы поддерживают большие вложения (~100 МБ). Опишите в тексте, как организовать хранение и скачивание файлов из списка отправленных форм, учитывая тысячи отправленных форм с несколькими вложениями в каждой. Включите архитектуру, структуру данных и REST API.

## Результаты

Опубликуйте ваш код в репозитории GIT. Не используйте слова, связанные с "Plumsail", в названии репозитория, чтобы другие кандидаты не нашли вашу реализацию и не присвоили себе вашу работу.

Отправьте результаты по адресу <recruitment@plumsail.com> со ссылкой на ваше резюме на HH.

## Сроки

Строгого дедлайна нет. Мы понимаем, что вы, возможно, работаете на другой работе. Было бы здорово, если бы вы смогли выполнить его в течение недели.