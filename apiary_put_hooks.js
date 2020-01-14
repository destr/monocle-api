const hooks = require('hooks')

function removeComments(o) {
    for (k in o) {
        if (typeof o[k] === "object") {
            removeComments(o[k]);
            continue;
        }
        if (k.startsWith("_comment")) {
            delete o[k];
        }
    }
}
hooks.beforeEachValidation(function(transaction) {
    var obj = JSON.parse(transaction.expected.body)
    removeComments(obj)
    transaction.expected.body = JSON.stringify(obj)
});

var order = [
    'СМРЛП > СМРЛП > Обновить параметры СМРЛП',
    'СМРЛП > СМРЛП > Получить параметры СМРЛП',
    'СМРЛП > Расписание СМРЛП > Обновить расписание СМРЛП',
    'СМРЛП > Расписание СМРЛП > Получить расписание СМРЛП'
]

hooks.beforeAll(function(transactions, done) {
    transactions.sort(function(a, b) {
        var aIdx = order.indexOf(a.name)
        var bIdx = order.indexOf(b.name)
        return aIdx - bIdx
    })
    done()
})

hooks.before('СМРЛП > АС СМРЛП > Получить список СМРЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > СМРЛП > Обновить параметры СМРЛП', function(transaction) {
	var requestBody = JSON.parse(transaction.request.body);
	requestBody['index'] = '0001';
	requestBody['baltrad_index'] = 'abcde';
	transaction.request.body = JSON.stringify(requestBody);
});

hooks.after('СМРЛП > СМРЛП > Получить параметры СМРЛП', function(transaction) {
	var station = JSON.parse(transaction.real.body)
	// проверяем только обновленные поля, а не эквивалентность json-запроса и json-ответа, потому что Телескоп дозаписывает json-запрос
	if ((station.index != '0001') || (station.baltrad_index != 'abcde'))
		transaction.fail = 'Обновление параметров СМРЛП не выполнено'
});


hooks.before('СМРЛП > Расписание СМРЛП > Обновить расписание СМРЛП', function(transaction) {
	var requestBody = JSON.parse(transaction.request.body);
	requestBody['items'][0][0]['date'] = '00:01:02'
	transaction.request.body = JSON.stringify(requestBody);
});

hooks.after('СМРЛП > Расписание СМРЛП > Получить расписание СМРЛП', function(transaction) {
	var schedule = JSON.parse(transaction.real.body)
	if (schedule.items[0].date != '00:01:02')
		transaction.fail = 'Обновление расписания не выполнено'
});

hooks.before('СМРЛП > Включить работу СМРЛП по расписанию > Включить', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Остановить работу СМРЛП по расписанию > Остановить', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Запустить запись карты местных отражений > Запись карты местных отражений', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Остановить запись карты местных отражений > Остановить запись карты местных отражений', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Запустить работу СМРЛП по программе > Запустить', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Остановить работу СМРЛП по программе > Остановить', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Запуск программы "КОНТРОЛЬ" для РЛС СМРЛП > Запустить', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Текущие значения параметров работы МРЛС > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Параметры константные > Справочник типов РЛП > Получить перечень типов РЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('Параметры константные > Справочник типов КС > Получить перечень типов КС', function(transaction) {
	transaction.skip = true;
});

hooks.before('Параметры константные > Критерии классификации типов метеоявлений по умолчанию > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Параметры константные > Каналы излучения > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Выдача паспорта обзора > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Список уведомлений об опасных метеоявлениях > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получить данные РЛП в формате GeoJSON > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальное сечение для Карты РЛП > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальное сечение для КС > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальный профиль > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Данные метео > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение данных метеостатистики > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.after('Продукты и данные > Список архивных обзоров > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение карт РЛП > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение высот для некоторых РЛП > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение высот для КС > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение КС > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение углов места > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Продукты и данные > Метеоинформация в указанной точке > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки критериев МЯ для отдельного СМРЛП > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки критериев МЯ для отдельного СМРЛП > Обновить настройки СМРЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки МРЛС > Получить настройки МРЛС', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки МРЛС > Обновить настройки МРЛС', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Программы > Получить список программ', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Программа > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Программа > Удалить программу', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Программа > Создать программу', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Программа > Обновить программу', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Журнал событий > Получить список событий', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Построение карт РЛП > Получить настройки для построения карт РЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Построение карт РЛП > Обновить настройки для построения карт', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Список настроек цветовых шкал > Получить список настроек цветовых шкал', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки цветовой шкалы > Обновить настройки цветовой шкалы', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки цветовой шкалы по умолчанию > Получить настройки цветовой шкалы по умолчанию', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Поправка на север > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Поправка на север > Установить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Актуальные значения оперативных параметров МП > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Актуальные значения оперативных параметров МП > Обновить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Параметры алгоритмов обработки метео данных > Получить текущее состояние', function(transaction) {
    transaction.skip = true;
});

hooks.before('Настройки > Параметры алгоритмов обработки метео данных > Обновить параметры', function(transaction) {
    transaction.skip = true;
});

hooks.before('Настройки > Калибровка изотермы > Получить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Калибровка изотермы > Обновить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true;
});

hooks.before('Уведомления > Уведомление об окончании обработки очередного пакета данных > Отправить уведомление', function(transaction) {
	transaction.skip = true;
});

hooks.before('Уведомления > Уведомление о соcтоянии > Отправить уведомление', function(transaction) {
	transaction.skip = true;
});

hooks.before('Уведомления > Уведомление об обновлении настроек > Отправить уведомление о изменении настроек СМРЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('Qt-интерфейс > Получение настроек для Qt интерфейса > Получить', function(transaction) {
  transaction.skip = true;
});

hooks.before('Qt-интерфейс > Получение настроек для Qt интерфейса > Обновить', function(transaction) {
  transaction.skip = true;
});

hooks.before('Qt-интерфейс > Запрос проверки соединения с FTP > Запрос проверки', function(transaction) {
	transaction.skip = true;
});

hooks.before('Qt-интерфейс > Получить список файлов содержащихся в каталоге для воспроизведения > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Qt-интерфейс > Управление вопроизведением голограмм > Установить новые параметры воспроизведения/записи', function(transaction) {
	transaction.skip = true;
});

hooks.before('MТП-5 > Выдача списка дат архивных данных температурного профилимера > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.after('MТП-5 > Выдача списка дат архивных данных температурного профилимера > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('MТП-5 > Выдача данных температурного профилемера > Получить', function(transaction) {
	transaction.skip = true;
});


hooks.before('Настройки экспорта > Настройки экспорта BUFR > Получить список настроек экспорта BUFR', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта НАМС > Получить список настроек экспорта НАМС', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта HDF5 > Получить список настроек экспорта HDF5', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта MTP5 > Получить список настроек экспорта MTP5', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройки экспорта BUFR > Обновить список настроек экспорта BUFR', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта НАМС > Обновить список настроек экспорта НАМС', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта HDF5 > Обновить список настроек экспорта HDF5', function(transaction) {
  transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта MTP5 > Обновить список настроек экспорта MTP5', function(transaction) {
  transaction.skip = true;
});

hooks.before('Служебные > Версия API > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Служебные > Версия формата имени файла BUFR > Получить', function(transaction) {
    transaction.skip = true;
});

hooks.before('Служебные > Test > Get', function(transaction) {
    transaction.skip = true;
});