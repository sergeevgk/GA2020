## AS Metall



Плагин для Autodesk Advance Steel (2018-2021) предоставляющий возможности для создания технических спецификаций металлоконструкций.



## Установка и запуск



Плагин поставляется на коммерческой основе в составе пакета дополнений. Установка для отдельного пользователя возможна с помощью .msi файла. Для установки необходимо наличие Advance Steel соответствующей версии.



После установки на "ленте быстрого использования" появляется вкладка с кнопкой вызова плагина.



## Постановка задачи



Создать плагин, позволяющий пользователю получать из xml-файла экстракта спецификации в формате таблиц Advance Steel (список шаблонов см. на диаграмме) с дополнительными настройками.



## Диаграмма использования



![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/diagram.png)



## Работа плагина

1. Пользователь открывает модель в Advance Steel

![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/model.png)

2. С помощью встроенного инструмента данные экспортируются в XML формат

![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/export.png)

3. Пользователь выбирает созданный экстракт в плагине

![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/extract.png)

4. Пользователь выбирает шаблон и настраивает его параметры

![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/template.png)

5. По шаблону создаётся таблица и

   + помещается на выбранное место чертежа Advance Steel

![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/table.png)
   + экспортируется в файл Excel

![](https://github.com/sergeevgk/GA2020/blob/asmetall/images/excel.png)