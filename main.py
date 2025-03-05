import shutil
import subprocess
import os
import sys
import winreg
import wmi
import ctypes
import time

# Administrator huquqlari bilan skriptni ishga tushirish
def run_as_admin():
    try:
        # Agar administrator bo'lsa, to'g'ridan-to'g'ri qaytadi
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
    except:
        return False

    # Administrator sifatida qayta ishga tushirish
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    return False

# Skriptni avtomatik ishga tushiriladigan dasturlar ro'yxatiga qo'shish uchun funksiya
def adder_auto_run():
    private_folder = os.path.join(os.environ["APPDATA"], "usb.exe")
    if not os.path.exists(private_folder):
        shutil.copyfile(sys.executable, private_folder)
        subprocess.call(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v usb /t REG_SZ /d "{private_folder}"', shell=True)


# Klaviatura va sichqonchani bloklash funksiyasi
def block_input():
    ctypes.windll.user32.BlockInput(True)  # Barcha kiritishlarni bloklaydi

# Klaviatura va sichqonchani blokdan chiqarish funksiyasi
def unblock_input():
    ctypes.windll.user32.BlockInput(False)  # Barcha kiritishlarni qayta faollashtiradi

# Oldingi kodlar
# Oldingi kodlarni o'zgartirib to'g'ri yo'l olish
def get_correct_directory():
    if getattr(sys, 'frozen', False):
        # Agar .exe fayl sifatida ishlayotgan bo'lsa
        return os.path.dirname(sys.executable)
    else:
        # Agar Python muhiti ichida ishlayotgan bo'lsa
        return os.path.dirname(os.path.abspath(__file__))

current_directory = get_correct_directory()
path = os.path.join(current_directory, 'serialnumber.txt')

def read_serials_from_file(file_path=path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            serials = [line.strip() for line in file.readlines()]
        return serials
    else:
        return []


def get_usb_devices():
    c = wmi.WMI()
    usb_devices = c.Win32_DiskDrive(InterfaceType="USB")
    return usb_devices

def check_usb_devices():
    allowed_serials = read_serials_from_file()
    devices = get_usb_devices()
    all_devices_allowed = True

    for device in devices:
        serial = device.PNPDeviceID.strip().split("\\")[-1]
        if serial in allowed_serials:
            pass
        else:
            block_input()  # USB ruxsat berilmagan bo'lsa klaviatura va sichqonchani bloklash
            all_devices_allowed = False

    # USB qurilmasi chiqarilgandan so'ng klaviatura va sichqonchani qayta faollashtirish
    if all_devices_allowed:
        unblock_input()

if __name__ == "__main__":
    if run_as_admin():
        adder_auto_run()  # Skriptni avtomatik ishga tushirish ro'yxatiga qo'shish
        while True:
            check_usb_devices()
            time.sleep(3)  # 3 soniya interval bilan USB qurilmalarni tekshirish
    else:
        pass
