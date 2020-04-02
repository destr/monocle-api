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

function archiveValid(body) {
  var archive = JSON.parse(body)
  return archive.datetimes.length != 0
}
hooks.beforeEachValidation(function(transaction) {
    var obj = JSON.parse(transaction.expected.body)
    removeComments(obj)
    transaction.expected.body = JSON.stringify(obj)
});

hooks.after('СМРЛП > СМРЛП > АС СМРЛП > Получить список СМРЛП', function(transaction) {
  var st = JSON.parse(transaction.real.body)

});

hooks.before('СМРЛП > СМРЛП > Получить параметры СМРЛП', function(transaction) {
});

hooks.before('СМРЛП > СМРЛП > Обновить параметры СМРЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('Параметры константные > Справочник типов РЛП > Получить перечень типов РЛП', function(transaction) {
});

hooks.before('Параметры константные > Справочник типов КС > Получить перечень типов КС', function(transaction) {
});

hooks.before('Параметры константные > Каналы излучения > Получить', function(transaction) {
	transaction.skip = false;
});

hooks.before('Настройки > Калибровка изотермы > Получить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Калибровка изотермы > Обновить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки критериев МЯ для отдельного СМРЛП > Получить', function(transaction) {
	transaction.skip = false;
});

hooks.before('Настройки > Настройки критериев МЯ для отдельного СМРЛП > Обновить настройки СМРЛП', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки МРЛС > Получить настройки МРЛС', function(transaction) {
	transaction.skip = false;
});

hooks.before('Настройки > Настройки МРЛС > Обновить настройки МРЛС', function(transaction) {
	transaction.skip = true;
});

hooks.before('СМРЛП > Расписание СМРЛП > Получить расписание СМРЛП', function(transaction) {
	transaction.skip = false;
});

hooks.before('СМРЛП > Расписание СМРЛП > Обновить расписание СМРЛП', function(transaction) {
	transaction.skip = true;
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

hooks.before('Продукты и данные > Данные метео > Получить', function(transaction) {
});

hooks.after('Продукты и данные > Список дат измерений метео > Получить', function(transaction) {
  if (transaction.skip) return
  if (!archiveValid(transaction.real.body))
    transaction.fail = 'Список дат обзоров не может быть пустым'
});

hooks.before('Продукты и данные > Получение данных метеостатистики > Получить', function(transaction) {
	transaction.skip = false;
});

hooks.after('Продукты и данные > Список архивных обзоров > Получить', function(transaction) {
  if (transaction.skip) return
  // не может быть в тестовом окружении
  if(!archiveValid(transaction.real.body))
    transaction.fail = 'Список дат обзоров не может быть пустым'
});


hooks.before('Продукты и данные > Получение карт РЛП > Получить', function(transaction) {
	transaction.skip = false;
});

hooks.before('Продукты и данные > Получение высот для некоторых РЛП > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Получение высот для КС > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Получение КС > Получить', function(transaction) {
	transaction.skip = false;
});

hooks.before('Продукты и данные > Получение углов места > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Метеоинформация в указанной точке > Получить', function(transaction) {
});

hooks.before('Настройки > Программы > Получить список программ', function(transaction) {
});

hooks.before('Настройки > Программа > Получить', function(transaction) {
	transaction.skip = false;
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

hooks.before('Настройки > Настройки экспорта BUFR > Получить список настроек экспорта BUFR', function(transaction) {
});

hooks.before('Настройки > Настройки экспорта BUFR > Обновить список настроек экспорта BUFR', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Построение карт РЛП > Получить настройки для построения карт РЛП', function(transaction) {
});

hooks.before('Настройки > Построение карт РЛП > Обновить настройки для построения карт', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Список настроек цветовых шкал > Получить список настроек цветовых шкал', function(transaction) {
	transaction.skip = false;
});

hooks.before('Настройки > Настройки цветовой шкалы > Обновить настройки цветовой шкалы', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Настройки цветовой шкалы по умолчанию > Получить настройки цветовой шкалы по умолчанию', function(transaction) {
	transaction.skip = false;
});

hooks.before('Параметры константные > Критерии классификации типов метеоявлений по умолчанию > Получить', function(transaction) {
});

hooks.before('Настройки > Поправка на север > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Поправка на север > Установить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Параметры алгоритмов обработки метео данных > Обновить параметры', function(transaction) {
    transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальное сечение для Карты РЛП > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Вертикальное сечение для КС > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Вертикальный профиль > Получить', function(transaction) {
});

hooks.before('Настройки > Текущие значения параметров работы МРЛС > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Список уведомлений об опасных метеоявлениях > Получить', function(transaction) {
    transaction.fullPath += "?date"
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
});

hooks.after('MТП-5 > Выдача списка дат архивных данных температурного профилимера > Получить', function(transaction) {
  if (transaction.skip) return
  // не может быть в тестовом окружении
  if(!archiveValid(transaction.real.body))
    transaction.fail = "Список дат МТП-5 не может быть пустым"
});

hooks.before('MТП-5 > Выдача данных температурного профилемера > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Выдача паспорта обзора > Получить', function(transaction) {

});

hooks.before('Служебные > Версия API > Получить', function(transaction) {
});

hooks.before('Продукты и данные > Получить данные РЛП в формате GeoJSON > Получить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Актуальные значения оперативных параметров МП > Получить', function(transaction) {
});

hooks.before('Настройки > Актуальные значения оперативных параметров МП > Обновить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Служебные > Test > Get', function(transaction) {
    transaction.skip = true;
});

hooks.before('Служебные > Workaroud CPP types > Get', function(transaction) {
    transaction.skip = true;
});

hooks.before('Служебные > Версия формата имени файла BUFR > Получить', function(transaction) {
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

hooks.after('Настройки > Расписания > Получить список расписаний', function(transaction) {
});
hooks.after('Настройки > Расписания > Создать новое расписание', function(transaction) {
});
hooks.after('Настройки > Управление расписанием > Изменить расписание', function(transaction) {
});
hooks.after('Настройки > Управление расписанием > Удалить расписание', function(transaction) {
});

