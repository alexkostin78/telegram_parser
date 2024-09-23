### Общая инструкция по работе с парсером Телеграмм

1. Для работы с парсером создать отдельное виртуальное окружение для Питона.

2. Установить библиотеку `telethon` в этом виртуальном окружении.

```python
pip install Telethon
```

3. Создать ID и Hash для API Telegram.
   
   1. Зарегистрироваться на сайте Телеграм API: [Authorization](https://my.telegram.org/auth)
   
   2. Создать новое приложение (Можно дать любое название, выбрать приложение Desktop)
   
   3. Сгенерировать ID и Hash. Записать их для дальнейшего использования.

4. Парсер состоит из 2-х частей.
   
   1. `group list` выводит названия и ID групп для указанных ID и Hash от API Telegram.
   
   2. `group info parser` выводит информацию выбранного типа в указанную папку, за указанный период из указанного (по ID-канала) канала.

5. В каждой из программ заполнить ячейку `Константы`, где задать данные из Телеграмм IP, номер телефона, ID-группы, период скачивания информации, лимит скачивания файлов каждого типа (None - скачать всё). Также указать путь для вывода скачанной информации.

6. При первом запуске программы `group list` API Telegram создает в папке, где находится программа, служебный файл `session_name.session` в котором хрянятся учетные данные для повторного подключения. В первый раз программа запросит пароль для подключения в выпадающем окне. Затем, если оставлять этот файл неизменным, пароль не запрашивается.

7. При необходимости можно удалить в списке `filters` функции `download_files` не нужные типы информации. К примеру можно оставить только Документы (InputMessagesFilterDocument) и фотографии (InputMessagesFilterPhotos).
