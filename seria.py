import tkinter as tk
from tkinter import messagebox
import wmi


def get_usb_serial_numbers():
    c = wmi.WMI()
    usb_devices = c.Win32_DiskDrive(InterfaceType="USB")

    if usb_devices:
        serials = []
        for device in usb_devices:
            serial_number = device.SerialNumber if device.SerialNumber else "No Serial Number"
            serials.append(f"Device: {device.Caption}, Serial Number: {serial_number}")
        result = "\n".join(serials)
    else:
        result = "No USB devices found."

    messagebox.showinfo("USB Serial Numbers", result)


# Tkinter window setup
root = tk.Tk()
root.title("USB Serial Number Detector")
root.geometry("300x150")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Press the button to check USB devices:")
label.pack()

btn_check = tk.Button(frame, text="Get USB Serial Numbers", command=get_usb_serial_numbers)
btn_check.pack(pady=10)

root.mainloop()
