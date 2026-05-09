import telebot
from telebot import types
import time

TOKEN = '8298701250:AAHfhWw3wk6Xw15UumisaB4avPyKDuid_SU'
MY_ID = 7497410701
bot = telebot.TeleBot(TOKEN)

active_servers = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == MY_ID:
        bot.reply_to(message, "Сервер управления запущен.")

@bot.message_handler(commands=['off'])
def ask_off(message):
    if message.from_user.id == MY_ID:
        if not active_servers:
            bot.send_message(MY_ID, "Нет активных серверов в сети.")
            return

        count = len(active_servers)
        ip_list = "\n".join([f"• {ip}" for ip in active_servers.keys()])
        
        text = f"Вы уверены, что хотите отключить {count} серверов?\n\nСписок IP:\n{ip_list}\n\nЕсли да, введите /off-confirm"
        bot.send_message(MY_ID, text)

@bot.message_handler(commands=['off-confirm'])
def confirm_off(message):
    if message.from_user.id == MY_ID:
        bot.send_message(MY_ID, "Сигнал на выключение отправлен всем серверам!")
        for ip in active_servers:
            active_servers[ip] = "SHUTDOWN"

@bot.message_handler(func=lambda m: m.text and m.text.startswith("PING_FROM_PC"))
def handle_ping(message):
    try:
        ip = message.text.split(":")[1]
        active_servers[ip] = time.time()
    except:
        pass

bot.polling(none_stop=True)