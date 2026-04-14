import asyncio
import ctypes
import psutil
import time
import tkinter as tk
import subprocess
import threading
from tkinter import messagebox

# ================= CONFIG =================
PASSWORD = "imnick"

TARGET_APPS = [
    "chrome.exe",
    "discord.exe",
    "steam.exe"
]

# ================= STATE =================
class LockState:
    LOCKED = 0
    UNLOCKING = 1
    UNLOCKED = 2

state = LockState.LOCKED
state_lock = threading.Lock()

# ================= WINDOW CONTROL =================
def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd:
        ctypes.windll.user32.ShowWindow(whnd, 0)

def open_app_again(app_name):
    try:
        subprocess.Popen(app_name, shell=True)
    except:
        pass

# ================= PROCESS MONITOR =================
def get_target_process():
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name and name.lower() in TARGET_APPS:
                return proc
        except:
            pass
    return None


def kill_process(proc):
    try:
        proc.terminate()
    except:
        pass


# ================= AUTH UI =================
def show_lock_ui():
    global state

    def unlock_password():
        global state
        if entry.get() == PASSWORD:
            with state_lock:
                state = LockState.UNLOCKED
            root.destroy()
        else:
            error_label.config(text="Wrong password bro 💀")
            entry.delete(0, tk.END)

    def toggle():
        if entry.cget("show") == "":
            entry.config(show="*")
            toggle_btn.config(text="Show")
        else:
            entry.config(show="")
            toggle_btn.config(text="Hide")

    root = tk.Tk()
    root.title("App Locker 🔒")
    root.geometry("360x220")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    tk.Label(root, text="Locked App Detected", font=("Arial", 14, "bold")).pack(pady=10)

    entry = tk.Entry(root, show="*", font=("Arial", 12))
    entry.pack(pady=5)
    entry.focus()

    toggle_btn = tk.Button(root, text="Show", command=toggle)
    toggle_btn.pack()

    tk.Button(root, text="Unlock", command=unlock_password).pack(pady=5)

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.bind("<Return>", lambda e: unlock_password())
    root.mainloop()


# ================= MONITOR LOOP =================
def monitor():
    global state

    while True:
        proc = get_target_process()

        with state_lock:
            current_state = state

        if proc and current_state != LockState.UNLOCKED:
            kill_process(proc)

            with state_lock:
                state = LockState.UNLOCKING

            show_lock_ui()

        elif not proc:
            with state_lock:
                state = LockState.LOCKED

        time.sleep(1)


# ================= START =================
hide_console()

threading.Thread(target=monitor, daemon=True).start()

while True:
    time.sleep(10)