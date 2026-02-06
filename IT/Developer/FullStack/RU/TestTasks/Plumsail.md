# A task for candidates for full-stack developer (C#, JavaScript).



## Оглавление
  - [Prerequisites](#prerequisites)
  - [Part 1](#part-1)
  - [Part 2](#part-2)
  - [Results](#results)
  - [Deadlines](#deadlines)
- [�������� ������� ��� ���������� �� ������� full-stack ������������ (C#, JavaScript).](#full-stack-c-javascript)
  - [��������������� �������](#)
  - [����� 1](#1)
  - [����� 2](#2)
  - [����������](#)
  - [�����](#)

  - [Prerequisites](#prerequisites)
  - [Part 1](#part-1)
  - [Part 2](#part-2)
  - [Results](#results)
  - [Deadlines](#deadlines)
  - [��������������� �������](#)
  - [����� 1](#1)
  - [����� 2](#2)
  - [����������](#)
  - [�����](#)
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
# �������� ������� ��� ���������� �� ������� full-stack ������������ (C#, JavaScript).

## ��������������� �������

���������, ���� �� �� �������� � Vue 2 ��� 3. ���� �� ������ React ��� Angular, �� ������ ��� �������. �� ���������� Vue 3 � ����� ��������.

## ����� 1

��� ���������� ����������� ��������� ���������� ��� �������� ���-����, �������� ������������ ������, �� ��������� � ������.

1.  �������� ������������ ����� � �������������� CSS � Vue � �������� JavaScript-����������. ��������, ���������� ����� ��� ����� ������ ��� ������� � ����� ������ ������ �����: ��������� ����, ���������� ������, ����, �����-������, �������.

2.  �������� ��������� ��� ����� �����.

3.  ���������� REST-������ � �������������� C# � ASP.NET Core:

    a. ������ ������ ������������� ��� ����������� ������ ��� ������ ���������.

    b. �� ������ ��������� ��������� � ��������� ������������ ������ ��� ������ �������� �������. �����������, ��� ���������� ������ ��������-���������� � ������� ������ �����, ������� ���������� ��� �� ������. ������ �� ������ ������ ����� � ��������� ������.

    c. ��� �������� ������ ����������� ���� ���� ������ In-Memory, ���� ����� ������ ���������, ������� �� ��������� �� ��� ��������� �������� ��� ������ ��� ����������� � �����-���� ������-��������. ��� ��� ����� ����� ������� ���� �������.

4.  �������� ���������������� ��������� ��� ��������� ������ � ������ ������������ �������� �� ������ ���� �� ����� ��������.

5.  �������� ��� JS- � CSS-����� ������� � ���� ���� � ������� ��������� ���� ������� ������ (Vite ��� Webpack).

�������� ������� �������� �������, �� �������������� ��� ��� �������� ����������. ����� �������, ������������ ������� ������� ����������� � ������� ����������. �� ����� ��������� �������� ������ ����, ��� ��������������, �������� ������������� ����������������� ���������� � ����������� � �����.

## ����� 2

������ �����������, ��� ���-����� ������������ ������� �������� (~100 ��). ������� � ������, ��� ������������ �������� � ���������� ������ �� ������ ������������ ����, �������� ������ ������������ ���� � ����������� ���������� � ������. �������� �����������, ��������� ������ � REST API.

## ����������

����������� ��� ��� � ����������� GIT. �� ����������� �����, ��������� � "Plumsail", � �������� �����������, ����� ������ ��������� �� ����� ���� ���������� � �� ��������� ���� ���� ������.

��������� ���������� �� ������ <recruitment@plumsail.com> �� ������� �� ���� ������ �� HH.

## �����

�������� �������� ���. �� ��������, ��� ��, ��������, ��������� �� ������ ������. ���� �� �������, ���� �� �� ������ ��������� ��� � ������� ������.