"""
Kiosk Control Panel
Coded by: Sabaz Ali Khan (Cybersecurity Engineer)
Purpose: Educational demo of fullscreen kiosk UI, Matrix-style animation,
         and password-protected exit using Tkinter.

Note: This is a UI-level demo, not a real security/lockdown tool.
It does not perform system exploitation or bypass OS security.
"""

import platform
import os
import sys
import random
from tkinter import *
from tkinter import messagebox

EXIT_PASSWORD = "1234"   # change this before using

# ---------------- OS KEY CONTROL ----------------

def block_windows_key():
    script = "LWin::Return\nRWin::Return"
    with open("block_win.ahk", "w") as f:
        f.write(script)
    os.system("start block_win.ahk")

def restore_windows_key():
    os.system("taskkill /f /im AutoHotkey.exe")

def block_linux_super_key():
    os.system("xmodmap -e 'keycode 133 = '")
    os.system("xmodmap -e 'keycode 134 = '")

def restore_linux_super_key():
    os.system("setxkbmap")

def restore_keys():
    os_name = platform.system()
    if os_name == "Windows":
        restore_windows_key()
    elif os_name == "Linux":
        restore_linux_super_key()

# ---------------- MATRIX ANIMATION ----------------

def start_matrix():
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    canvas.config(width=width, height=height)

    columns = int(width / 20)
    drops = [random.randint(0, height // 20) for _ in range(columns)]
    chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def draw():
        canvas.create_rectangle(0, 0, width, height, fill="black", outline="black")
        for i in range(len(drops)):
            char = random.choice(chars)
            x = i * 20
            y = drops[i] * 20
            canvas.create_text(x, y, text=char, fill="lime", font=("Consolas", 14))
            if y > height and random.random() > 0.975:
                drops[i] = 0
            drops[i] += 1
        root.after(50, draw)

    draw()

# ---------------- KIOSK MODE ----------------

def apply_kiosk_mode():
    os_name = platform.system()
    if os_name == "Windows":
        block_windows_key()
    elif os_name == "Linux":
        block_linux_super_key()

# ---------------- PASSWORD EXIT ----------------

def ask_exit():
    popup = Toplevel(root)
    popup.attributes("-fullscreen", True)
    popup.config(bg="black")
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.focus_force()

    Label(popup, text="ENTER EXIT PASSWORD",
          fg="lime", bg="black", font=("Consolas", 28)).pack(pady=100)

    pwd_entry = Entry(popup, show="*", font=("Consolas", 22), justify="center")
    pwd_entry.pack(pady=20)
    pwd_entry.focus()

    def validate():
        if pwd_entry.get() == EXIT_PASSWORD:
            restore_keys()
            root.destroy()
            sys.exit()
        else:
            pwd_entry.delete(0, END)
            status = Label(popup, text="Wrong password!", fg="red", bg="black",
                            font=("Consolas", 12))
            status.pack()
            popup.after(1500, status.destroy)

    pwd_entry.bind("<Return>", lambda e: validate())

    Button(popup, text="UNLOCK", command=validate,
           width=20, height=2, bg="black", fg="lime",
           font=("Consolas", 14)).pack(pady=40)

# ---------------- PERMISSION FIRST ----------------

def request_permission():
    result = messagebox.askokcancel(
        "System Permission",
        "This app will enter fullscreen kiosk mode.\n\nAllow?"
    )
    if result:
        root.deiconify()
        root.attributes("-fullscreen", True)
        start_matrix()
        apply_kiosk_mode()
        status_label.config(text="Kiosk Mode Active", fg="lime")
    else:
        sys.exit()

# ---------------- MAIN WINDOW ----------------

root = Tk()
root.withdraw()
root.title("Coded by cyber security engineer Mr Sabaz ali khan")
root.config(bg="black")
root.protocol("WM_DELETE_WINDOW", lambda: None)

canvas = Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

frame = Frame(root, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")

Label(frame, text="Coded by cyber security engineer Mr Sabaz ali khan",
      fg="lime", bg="black", font=("Consolas", 32)).pack(pady=40)

status_label = Label(frame, text="Initializing...",
                      fg="cyan", bg="black", font=("Consolas", 16))
status_label.pack(pady=20)

Button(frame, text="Exit (Password)", command=ask_exit,
       width=25, height=2, bg="black", fg="red",
       font=("Consolas", 12)).pack(pady=40)

root.after(100, request_permission)
root.mainloop()
