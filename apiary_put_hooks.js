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

var order = [
    'СМРЛП > СМРЛП > Обновить параметры СМРЛП',
    'СМРЛП > СМРЛП > Получить параметры СМРЛП',
    'СМРЛП > Расписание СМРЛП > Обновить расписание СМРЛП',
    'СМРЛП > Расписание СМРЛП > Получить расписание СМРЛП',
    'Настройки > Настройки критериев МЯ для отдельного СМРЛП > Обновить настройки СМРЛП',
    'Настройки > Настройки критериев МЯ для отдельного СМРЛП > Получить',
    'Настройки > Программа > Создать программу',
    'Настройки > Программа > Обновить программу',
    'Настройки > Программы > Получить список программ',
    'Настройки > Программа > Удалить программу', 
    'Настройки > Программа > Получить',
    'Настройки > Построение карт РЛП > Обновить настройки для построения карт',
    'Настройки > Построение карт РЛП > Получить настройки для построения карт РЛП',
    'Настройки > Настройки цветовой шкалы > Обновить настройки цветовой шкалы',
    'Настройки > Список настроек цветовых шкал > Получить список настроек цветовых шкал',
    'Настройки > Актуальные значения оперативных параметров МП > Обновить',
    'Настройки > Актуальные значения оперативных параметров МП > Получить',
    'Настройки > Параметры алгоритмов обработки метео данных > Обновить параметры',
    'Настройки > Параметры алгоритмов обработки метео данных > Получить текущее состояние',
    'Настройки > Калибровка изотермы > Обновить настройки вычисления изотермы',
    'Настройки > Калибровка изотермы > Получить настройки вычисления изотермы',
    'Настройки экспорта > Настройки экспорта BUFR > Обновить список настроек экспорта BUFR',
    'Настройки экспорта > Настройки экспорта BUFR > Получить список настроек экспорта BUFR',
    'Настройки экспорта > Настройка экспорта НАМС > Обновить список настроек экспорта НАМС',
    'Настройки экспорта > Настройка экспорта НАМС > Получить список настроек экспорта НАМС',
    'Настройки экспорта > Настройка экспорта HDF5 > Обновить список настроек экспорта HDF5',
    'Настройки экспорта > Настройка экспорта HDF5 > Получить список настроек экспорта HDF5',
    'Настройки экспорта > Настройка экспорта MTP5 > Обновить список настроек экспорта MTP5',
    'Настройки экспорта > Настройка экспорта MTP5 > Получить список настроек экспорта MTP5'
]

// порядок, в котором будут выполняться запросы
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
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['index'] = '0001';
	// requestBody['baltrad_index'] = 'abcde';
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('СМРЛП > СМРЛП > Получить параметры СМРЛП', function(transaction) {
// 	var station = JSON.parse(transaction.real.body)
// 	// проверяем только обновленные поля, а не эквивалентность json-запроса и json-ответа, потому что Телескоп дозаписывает json-запрос
// 	if ((station.index != '0001') || (station.baltrad_index != 'abcde')) {
// 		transaction.fail = 'Обновление параметров СМРЛП не выполнено'
// 		console.log(JSON.stringify(station))
// 	}
	transaction.skip = true;	
});

hooks.before('СМРЛП > Расписание СМРЛП > Обновить расписание СМРЛП', function(transaction) {
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['items'][0][0]['date'] = '00:01:02'
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

// hooks.after('СМРЛП > Расписание СМРЛП > Получить расписание СМРЛП', function(transaction) {
// 	var schedule = JSON.parse(transaction.real.body)
// 	if (schedule.items[0].date != '00:01:02') {
// 		transaction.fail = 'Обновление расписания не выполнено'
// 		console.log(JSON.stringify(schedule))
// 	}
// });

hooks.before('СМРЛП > Расписание СМРЛП > Получить расписание СМРЛП', function(transaction) {
	transaction.skip = true;
});


hooks.before('СМРЛП > Включить работу СМРЛП по расписанию > Включить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Остановить работу СМРЛП по расписанию > Остановить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Запустить запись карты местных отражений > Запись карты местных отражений', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Остановить запись карты местных отражений > Остановить запись карты местных отражений', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Запустить работу СМРЛП по программе > Запустить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Остановить работу СМРЛП по программе > Остановить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Запуск программы "КОНТРОЛЬ" для РЛС СМРЛП > Запустить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('СМРЛП > Текущие значения параметров работы МРЛС > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Параметры константные > Справочник типов РЛП > Получить перечень типов РЛП', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Параметры константные > Справочник типов КС > Получить перечень типов КС', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Параметры константные > Критерии классификации типов метеоявлений по умолчанию > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Параметры константные > Каналы излучения > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Выдача паспорта обзора > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Список уведомлений об опасных метеоявлениях > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получить данные РЛП в формате GeoJSON > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальное сечение для Карты РЛП > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальное сечение для КС > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Вертикальный профиль > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Данные метео > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение данных метеостатистики > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.after('Продукты и данные > Список архивных обзоров > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение карт РЛП > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение высот для некоторых РЛП > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение высот для КС > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение КС > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Получение углов места > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Продукты и данные > Метеоинформация в указанной точке > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Настройки > Настройки критериев МЯ для отдельного СМРЛП > Обновить настройки СМРЛП', function(transaction) {
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['min_dangerous_meteo'] = 6;
	// requestBody['max_dangerous_meteo'] = 18;
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки > Настройки критериев МЯ для отдельного СМРЛП > Получить', function(transaction) {
	// var settings = JSON.parse(transaction.real.body)
	// if ((settings.min_dangerous_meteo != 6) || (settings.max_dangerous_meteo != 18)) {
	// 	transaction.fail = 'Обновление настроек критериев МЯ не выполнено'
	// 	console.log(JSON.stringify(settings))
	// }
	transaction.skip = true;
});

hooks.before('Настройки > Настройки МРЛС > Получить настройки МРЛС', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Настройки > Настройки МРЛС > Обновить настройки МРЛС', function(transaction) {
	// Невозможно протестировать
	transaction.skip = true;
});

var programId = "";

hooks.before('Настройки > Программа > Создать программу', function(transaction) {
	// var program = JSON.parse(transaction.real.body);
	// // сохраняем id созданной программы
	// programId = program.id;
	transaction.skip = true;
});

hooks.before('Настройки > Программа > Обновить программу', function(transaction) {
	// transaction.fullPath = transaction.fullPath.replace('default', programId);
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['description'] = 'new_program';
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки > Программы > Получить список программ', function(transaction) {
	// var programList = JSON.parse(transaction.real.body);
	// var programCreated = false;
	// var programUpdated = false;
	// // сначала проверяем, что программа создана
	// programList.items.forEach(function(item, index, array) {
	// 	if (item.id == programId) {
	// 		programCreated = true;
	// 		// если программа есть - проверяем, что поле description обновилось
	// 		// if (item.description == "new_program")
	// 		// 	programUpdated = true;
	// 	}
	// });
	// if (!programCreated)
	// 	transaction.fail = "Программа не создана";
	// if (!programUpdated)
	// 	transaction.fail = "Обновление программы не выполнено";
	transaction.skip = true;
});


hooks.before('Настройки > Программа > Удалить программу', function(transaction) {
	// удаляем созданную программу
	// transaction.fullPath = transaction.fullPath.replace('default', programId);
	transaction.skip = true;
});

hooks.before('Настройки > Программа > Получить', function(transaction) {
	// transaction.fullPath = transaction.fullPath.replace('default', programId);
	// // пытаемся получить удаленную программу, ожидая статус ответа 204
	// delete transaction.expected.body;
	// delete transaction.expected.bodySchema;
	// delete transaction.expected.headers;
	// transaction.expected.statusCode = '204';
	transaction.skip = true;
});

hooks.before('Настройки > Журнал событий > Получить список событий', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Настройки > Построение карт РЛП > Обновить настройки для построения карт', function(transaction) {
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['vector_velocity_field']['circular_horizontal_pitch'] = 8500;
	// requestBody['vector_velocity_field']['circular_vertical_pitch'] = 1500;
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки > Построение карт РЛП > Получить настройки для построения карт РЛП', function(transaction) {
	// var settings = JSON.parse(transaction.real.body);
	// if ((settings.vector_velocity_field.circular_horizontal_pitch != 8500) || (settings.vector_velocity_field.circular_vertical_pitch != 1500)) {
	// 	transaction.fail = 'Обновление настроек построения карт не выполнено'
	// 	console.log(JSON.stringify(settings))
	// }
	transaction.skip = true;	
});

hooks.before('Настройки > Настройки цветовой шкалы > Обновить настройки цветовой шкалы', function(transaction) {
	// var colorScale = JSON.parse(transaction.request.body);
	// colorScale[0]["color"] = "#3399ff";
	// transaction.request.body = JSON.stringify(colorScale);
	transaction.skip = true;
});

hooks.after('Настройки > Список настроек цветовых шкал > Получить список настроек цветовых шкал', function(transaction) {
	// var colorScale = JSON.parse(transaction.real.body);
	// if (colorScale.items[0].items[0].color != "#3399FF") {
	// 	transaction.fail = 'Обновление настроек цветовой шкалы не завершено';
	// 	console.log(JSON.stringify(colorScale))
	// }
	transaction.skip = true;
});

hooks.before('Настройки > Настройки цветовой шкалы по умолчанию > Получить настройки цветовой шкалы по умолчанию', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Настройки > Поправка на север > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Настройки > Поправка на север > Установить', function(transaction) {
	// Нет возможности протестировать
	transaction.skip = true;
});

hooks.before('Настройки > Актуальные значения оперативных параметров МП > Обновить', function(transaction) {
	transaction.skip = true;
});

hooks.before('Настройки > Актуальные значения оперативных параметров МП > Получить', function(transaction) {
	// тестируется после обновления актуальных значений оперативных параметров МП, поскольку изначально они отсутствуют вообще
	transaction.skip = true;
});

hooks.before('Настройки > Параметры алгоритмов обработки метео данных > Обновить параметры', function(transaction) {
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['dpm']['dataprocessing']['nominal_cycle_time'] = 606;
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки > Параметры алгоритмов обработки метео данных > Получить текущее состояние', function(transaction) {
	// var settings = JSON.parse(transaction.real.body)
	// if (settings.dpm.dataprocessing.nominal_cycle_time != 606) {
	// 	transaction.fail = 'Обновление параметров алгоритмов обработки метео данных не выполнено';
	// 	console.log(JSON.stringify(settings));
	// }
	transaction.skip = true;	 
});

hooks.before('Настройки > Калибровка изотермы > Обновить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true;
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody['height_temp0'] = 2500;
	// transaction.request.body = JSON.stringify(requestBody);
});

hooks.before('Настройки > Калибровка изотермы > Получить настройки вычисления изотермы', function(transaction) {
	transaction.skip = true;	 
});

// hooks.after('Настройки > Калибровка изотермы > Получить настройки вычисления изотермы', function(transaction) {
// 	var isotherm = JSON.parse(transaction.real.body)
// 	if (isotherm.height_temp0 != 2500) {
// 		transaction.fail = 'Обновление настроек вычисления изотермы не выполнено';
// 		console.log(JSON.stringify(isotherm));
// 	}	 
// });

hooks.before('Уведомления > Уведомление об окончании обработки очередного пакета данных > Отправить уведомление', function(transaction) {
	// отключен в Телескопе
	transaction.skip = true;
});

hooks.before('Уведомления > Уведомление о соcтоянии > Отправить уведомление', function(transaction) {
	// отключен в Телескопе
	transaction.skip = true;
});

hooks.before('Уведомления > Уведомление об обновлении настроек > Отправить уведомление о изменении настроек СМРЛП', function(transaction) {
	// отключен в Телескопе
	transaction.skip = true;
});

hooks.before('Qt-интерфейс > Получение настроек для Qt интерфейса > Получить', function(transaction) {
	// TODO тестирование Qt-интерфейса
    transaction.skip = true;
});

hooks.before('Qt-интерфейс > Получение настроек для Qt интерфейса > Обновить', function(transaction) {
	// TODO тестирование Qt-интерфейса
    transaction.skip = true;
});

hooks.before('Qt-интерфейс > Запрос проверки соединения с FTP > Запрос проверки', function(transaction) {
	// TODO тестирование Qt-интерфейса
	transaction.skip = true;
});

hooks.before('Qt-интерфейс > Получить список файлов содержащихся в каталоге для воспроизведения > Получить', function(transaction) {
	// TODO тестирование Qt-интерфейса
	transaction.skip = true;
});

hooks.before('Qt-интерфейс > Управление вопроизведением голограмм > Установить новые параметры воспроизведения/записи', function(transaction) {
	// TODO тестирование Qt-интерфейса
	transaction.skip = true;
});

hooks.before('MТП-5 > Выдача списка дат архивных данных температурного профилимера > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.after('MТП-5 > Выдача списка дат архивных данных температурного профилимера > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('MТП-5 > Выдача данных температурного профилемера > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройки экспорта BUFR > Обновить список настроек экспорта BUFR', function(transaction) {
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody[0]["login"] = "login1";
	// requestBody[0]["password"] = "password1";
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

// hooks.after('Настройки экспорта > Настройки экспорта BUFR > Получить список настроек экспорта BUFR', function(transaction) {
// 	var settings = JSON.parse(transaction.real.body)
// 	if ((settings["items"][0].login != "login1") || (settings["items"][0].password != "password1")) {
// 		transaction.fail = 'Обновление настроек экспорта BUFR не выполнено';
// 		console.log(JSON.stringify(settings));
// 	}	 
// });

hooks.before('Настройки экспорта > Настройки экспорта BUFR > Получить список настроек экспорта BUFR', function(transaction) {
	transaction.skip = true; 
});


hooks.before('Настройки экспорта > Настройка экспорта НАМС > Обновить список настроек экспорта НАМС', function(transaction) {
 	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody[0]["login"] = "login1";
	// requestBody[0]["password"] = "password1";
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта НАМС > Получить список настроек экспорта НАМС', function(transaction) {
	// var settings = JSON.parse(transaction.real.body)
	// if ((settings["items"][0].login != "login1") || (settings["items"][0].password != "password1")) {
	// 	transaction.fail = 'Обновление настроек экспорта НАМС не выполнено';
	// 	console.log(JSON.stringify(settings));
	// }	 
	transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта HDF5 > Обновить список настроек экспорта HDF5', function(transaction) {
 //    var requestBody = JSON.parse(transaction.request.body);
	// requestBody[0]["login"] = "login1";
	// requestBody[0]["password"] = "password1";
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта HDF5 > Получить список настроек экспорта HDF5', function(transaction) {
	// var settings = JSON.parse(transaction.real.body)
	// if ((settings["items"][0].login != "login1") || (settings["items"][0].password != "password1")) {
	// 	transaction.fail = 'Обновление настроек экспорта HDF5 не выполнено';
	// 	console.log(JSON.stringify(settings));
	// }	
	transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта MTP5 > Обновить список настроек экспорта MTP5', function(transaction) {
	// var requestBody = JSON.parse(transaction.request.body);
	// requestBody[0]["login"] = "login1";
	// requestBody[0]["password"] = "password1";
	// transaction.request.body = JSON.stringify(requestBody);
	transaction.skip = true;
});

hooks.before('Настройки экспорта > Настройка экспорта MTP5 > Получить список настроек экспорта MTP5', function(transaction) {
	// var settings = JSON.parse(transaction.real.body)
	// if ((settings["items"][0].login != "login1") || (settings["items"][0].password != "password1")) {
	// 	transaction.fail = 'Обновление настроек экспорта MTP5 не выполнено';
	// 	console.log(JSON.stringify(settings));
	// }
	transaction.skip = true;	
});

hooks.before('Служебные > Версия API > Получить', function(transaction) {
	// тестируется с использованием apiary_get_hooks.js
	transaction.skip = true;
});

hooks.before('Служебные > Версия формата имени файла BUFR > Получить', function(transaction) {
	// не реализовано в Телескопе
    transaction.skip = true;
});

hooks.before('Служебные > Test > Get', function(transaction) {
	// не реализовано в Телескопе
    transaction.skip = true;
});