import requests
from datetime import date, timedelta, datetime
import csv
from telegram import send_mes_telebot
import configparser


def get_data(key_beeline):
    """
    Делаем запрос в Билайн на получение всей статистики за вчерашний день (сутки)
    :return: словарь со статистикой
    """
    result = []
    start_date = date.today() - timedelta(days=2)
    yesterday = date.today() - timedelta(days=1)
    n = 0
    while True:
        headers = {
            'X-MPBX-API-AUTH-TOKEN': key_beeline,
        }
        params = {
            'dateFrom': f'{start_date.strftime("%Y-%m-%d")}T21:00:00.000Z',
            'dateTo': f'{yesterday.strftime("%Y-%m-%d")}T21:59:59.000Z',
            'page': n,
            'pageSize': '100',
        }
        response = requests.get('https://cloudpbx.beeline.ru/apis/portal/v2/statistics', params=params, headers=headers)
        if response.json():
            result.extend(response.json())
            n += 1
        else:
            return result

def get_commerce_data(full_list):
    """
    Сортируем поступивший json на предмет наличия номера в какой либо группе (на момент написания скрипта группа только
    одна "Ком")
    :param full_list: словарь с полным перечнем звонков
    :return: словарь с отфильтрованными звонками
    """
    result = []
    for call in full_list:
        if 'department' in call:
            result.append(call)
    return result

def get_csv_file(commerce_list):
    """
    Преобразуем словарь в csv файл со именем согласно вчерашней дате и кладем его в ./stats/
    :param commerce_list: словарь со статистикой звонков
    """
    processed_list = []
    for call in commerce_list:
        processed_call = {}
        time = int(str(call['startDate'])[0:10]) + 10800
        processed_call['Дата, время'] = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        processed_call['Тип вызова'] = call['direction']
        if 'phone_from' in call:
            processed_call['С номера'] = call['phone_from']
        if 'phone_to' in call:
            processed_call['На номер'] = call['phone_to']
        processed_call['Абонент'] = call['abonent']['lastName']
        processed_call['Длительность'] = datetime.utcfromtimestamp((call['duration']) // 1000).strftime('%H:%M:%S')
        processed_call['Статус'] = call['status']
        processed_list.append(processed_call)
    keys = processed_list[0].keys()
    with open(f'./stats/{date.today() - timedelta(days=1)}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(processed_list)
    return f'./stats/{date.today() - timedelta(days=1)}.csv'


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    key = config['Beeline']['key']
    all_call = get_data(key)
    commerce_data = get_commerce_data(all_call)
    csv_file = get_csv_file(commerce_data)
    chat_id = "64619556"
    send_mes_telebot(csv_file, chat_id)
