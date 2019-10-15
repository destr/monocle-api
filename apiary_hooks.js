const hooks = require('hooks')



hooks.before('АС СМРЛП > Получить список СМРЛП', function(transaction) {
	transaction.skip = false;
});

hooks.before('СМРЛП > Получить параметры СМРЛП', function(transaction) {
	transaction.skip = false; 
});

hooks.before('СМРЛП > Обновить параметры СМРЛП', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Справочник типов РЛП > Получить перечень типов РЛП', function(transaction) {
	transaction.skip = false; 
});

hooks.before('Справочник типов КС > Получить перечень типов КС', function(transaction) {
	transaction.skip = false;
});

hooks.before('Калибровка изотермы > Получить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Калибровка изотермы > Обновить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки критериев МЯ для отдельного СМРЛП > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки критериев МЯ для отдельного СМРЛП > Обновить настройки СМРЛП', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки МРЛС > Получить настройки МРЛС', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки МРЛС > Обновить настройки МРЛС', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Расписание СМРЛП > Получить расписание СМРЛП', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Расписание СМРЛП > Обновить расписание СМРЛП', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Включить работу СМРЛП по расписанию > Включить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Остановить работу СМРЛП по расписанию > Остановить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Запустить запись карты местных отражений > Запись карты местных отражений', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Остановить запись карты местных отражений > Остановить запись карты местных отражений', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Запустить работу СМРЛП по программе > Запустить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Остановить работу СМРЛП по программе > Остановить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Запуск программы "КОНТРОЛЬ" для РЛС СМРЛП > Запустить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Данные метео > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение данных метеостатистики > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Список архивных обзоров > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение карт РЛП > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение высот для некоторых РЛП > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение высот для КС > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение КС > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение углов места > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Метеоинформация в указанной точке > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Программы > Получить список программ', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Программа > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Программа > Удалить программу', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Программа > Создать программу', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Программа > Обновить программу', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Журнал событий > Получить список событий', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки экспорта BUFR > Получить список настроек экспорта BUFR', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки экспорта BUFR > Обновить список настроек экспорта BUFR', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Построение карт РЛП > Получить настройки для построения карт РЛП', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Построение карт РЛП > Обновить настройки для построения карт', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Список настроек цветовых шкал > Получить список настроек цветовых шкал', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки цветовой шкалы > Обновить настройки цветовой шкалы', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Настройки цветовой шкалы по умолчанию > Получить настройки цветовой шкалы по умолчанию', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Критерии классификации типов метеоявлений по умолчанию > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Поправка на север > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Поправка на север > Установить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Вертикальное сечение для Карты РЛП > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Вертикальное сечение для КС > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Вертикальный профиль > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Текущие значения параметров работы МРЛС > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Каналы излучения > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Список уведомлений об опасных метеоявлениях > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Уведомление об окончании обработки очередного пакета данных > Отправить уведомление', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Уведомление о соcтоянии > Отправить уведомление', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Уведомление об обновлении настроек > Отправить уведомление о изменении настроек СМРЛП', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получение настроек для Qt интерфейса > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Запрос проверки соединения с FTP > Запрос проверки', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Получить список файлов содержащихся в каталоге для воспроизведения > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Управление вопроизведением голограмм > Установить новые параметры воспроизведения/записи', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Выдача списка дат архивных данных температурного профилимера > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Выдача данных температурного профилемера > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Выдача паспорта обзора > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Версия API > Получить', function(transaction) {
	transaction.skip = false; 
});

hooks.before('Получить данные РЛП в формате GeoJSON > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Актуальные значения оперативных параметров МП > Получить', function(transaction) {
	transaction.skip = true; 
});

hooks.before('Актуальные значения оперативных параметров МП > Обновить', function(transaction) {
	transaction.skip = true; 
});

