import configparser
import telebot

def send_mes_telebot(file, chat):
    """
    Отправка файла в телеграм с помощь. бота
    :param file: путь к файлу
    :param chat: id чата
    """
    bot = telebot.TeleBot(token)
    f = open(file, "rb")
    bot.send_document(chat, f)
    return

config = configparser.ConfigParser()
config.read('settings.ini')
token = config['Tg']['token']
chat_id = "64619556"