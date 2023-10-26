import requests
import configparser

def send_mes():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    token = config['Tg']['token']
    chat_id = "64619556"
    # message = "bot message"
    with open("./stats/2023-09-28.csv", "rb") as filexlsx:
        files = {"document": filexlsx}
    url = f"https://api.telegram.org/bot{token}/sendDocument?chat_id={chat_id}', files=files)"
    print(requests.get(url).json())  # Эта строка отсылает сообщение
    return
send_mes()