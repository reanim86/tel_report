import requests
from datetime import date, timedelta, datetime
import csv


def get_data():
    result = []
    start_date = date.today() - timedelta(days=2)
    yesterday = date.today() - timedelta(days=1)
    n = 0
    while True:
        headers = {
            'X-MPBX-API-AUTH-TOKEN': '',
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
    result = []
    for call in full_list:
        if 'department' in call:
            result.append(call)
    return result

def get_csv_file(commerce_list):
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
    return


if __name__ == '__main__':
    all_call = get_data()
    commerce_data = get_commerce_data(all_call)
    get_csv_file(commerce_data)
    # to_csv = [
    #     {'name': 'bob', 'age': 25, 'weight': 200},
    #     {'name': 'jim', 'age': 31, 'weight': 180},
    # ]
    #
    #
    # with open('people.csv', 'w', newline='') as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(to_csv)
