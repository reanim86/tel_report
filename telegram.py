import requests

def send_mes():
    TOKEN = ""
    chat_id = "64619556"
    message = "bot message"
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={chat_id}', document='./stats/2023-09-28.csv')"
    print(requests.get(url).json())  # Эта строка отсылает сообщение
    return
send_mes()