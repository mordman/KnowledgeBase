

| ![IntraVision\_small][image1] |  ООО «Интравижн»  [info@intravision.ru](mailto:%20info@intravision.ru), [www.intravision.ru](http://www.intravision.ru) 8 (495) 795-23-44 Россия, Москва, пр-т Андропова, д.22, офис 1802 |
| :---- | :---- |

# **ТЕСТОВОЕ ЗАДАНИЕ НА ВАКАНСИЮ**

# **WEB разработчика**

***Введение***  
Основная цель данного задания это понять «подход» кандидата к разработке и его желание и возможности самостоятельно разбираться в новых технологиях, добиваться поставленных целей.   
Мы предполагаем, что кандидат имеет от одного года опыта программирования и имеет базовые знания web технологий.

# **Задание на разработку Web приложения «Автомат по продаже напитков»**

***Описание***  
Веб-приложение имитирует работу автомата по продаже напитков. Напитки представлены названием, картинкой и стоимостью.  
Автомат принимает монеты номиналом в 1, 2, 5, 10 рублей. Предоставляет возможность купить напитки, внеся сумму, равную или превышающую их стоимость.  
Приложение должно иметь пользовательский и административный интерфейс.   
Пользовательский интерфейс предполагает покупку напитков – внесение суммы монетами, выбор напитка, получение сдачи. Доступ в пользовательский интерфейс свободен.   
Административный интерфейс должен предоставлять инструменты для управления автоматом. 

***Возможности пользовательского интерфейса***

* Вносить сумму, щелкая на кнопки с номиналом монет (1, 2, 5, 10). Если монета заблокирована, подсвечивать соответствующую кнопку и блокировать нажатие. Показывать внесенную сумму.  
* Выбирать напиток, щелкнув на соответствующую картинку. При этом не позволять выбирать закончившиеся напитки или напитки, стоимость которых превышает внесенную сумму. После выбора напитка количество оставшихся напитков должно уменьшиться на единицу, количество монет в автомате увеличиться, оставшаяся сумма должна быть возвращена в виде сдачи. В качестве сдачи могут выдаваться заблокированные монеты.

***Возможности административного интерфейса***

* Администрировать ассортимент напитков: добавление, удаление напитков, изменение их количества, стоимости и изображения  
* Управлять монетами в автомате: изменение количества монет, блокирование приема тех или иных монет  
* Доступ в административный интерфейс по секретному ключу, который передаётся как параметр в адресной строке

***Необязательные требования***

* Возможность импорта напитков  
* Возможность покупки нескольких напитков перед получением сдачи

***Требования***  
Необходимо создать Web приложение, с использованием:

* ASP.NET .core  
* В качестве клиентского Framework можно использовать Angular или React. Можно использовать jquery. Можно и без использования framework (просто JavaScript)   
* В качестве СУБД необходимо использовать MS SQL Express (2012, или выше. MS SQL Express – бесплатен, доступен для загрузки с сайта Microsoft). Взаимодействие с базой данных реализовывать через подход «Code First».


  

Приложение должно быть реализовано из двух страниц. Одна страница – это пользовательский интерфейс. Вторая страница – административный интерфейс.

В качестве среды разработки Visual Studio 2019 (или версии выше).  
	  
***Результаты***  
Результаты выслать в архиве. Имя архива “ФамилияИмя\_ТестовоеЗадание.zip” Необходимо в архив с заданием также положить файл readme.txt с кратким описанием реализации проекта, указать какие из необязательных требований выполнены. Какие технологии использовались. 

*Если есть вопросы по заданию, то не стесняйтесь – задавайте. Удачи вам в разработке\!*

[image1]: <data:image/png;base64,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>