import asyncio
import ctypes
import psutil
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading

PASSWORD = "imnick"
unlocked = False

FINGERPRINT_AVAILABLE = False
FINGERPRINT_STATUS = "Fingerprint unavailable. Install winrt in your active Python environment."
try:
    from winrt.windows.security.credentials.ui import (
        UserConsentVerifier,
        UserConsentVerificationResult,
        UserConsentVerifierAvailability,
    )
    try:
        availability = asyncio.run(UserConsentVerifier.check_availability_async())
        FINGERPRINT_AVAILABLE = availability == UserConsentVerifierAvailability.AVAILABLE
        if FINGERPRINT_AVAILABLE:
            FINGERPRINT_STATUS = "Windows Hello available — tap Use Windows Hello."
        else:
            FINGERPRINT_STATUS = "Windows Hello hardware not available."
    except Exception:
        FINGERPRINT_AVAILABLE = False
        FINGERPRINT_STATUS = "Fingerprint support detected, but Windows Hello is unavailable."
except ImportError:
    FINGERPRINT_AVAILABLE = False
    FINGERPRINT_STATUS = "Fingerprint unavailable. Install winrt in your active Python environment."

# ------------------ CHROME CONTROL ------------------
def is_chrome_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'chrome' in proc.info['name'].lower():
            return True
    return False

def kill_chrome():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                proc.terminate()  # nhẹ nhàng hơn kill
        except:
            pass

def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd:
        ctypes.windll.user32.ShowWindow(whnd, 0)

def open_chrome_restore():
    subprocess.Popen(
        ['cmd', '/c', 'start', '', 'chrome', '--restore-last-session'],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

async def verify_fingerprint():
    availability = await UserConsentVerifier.check_availability_async()
    if availability != UserConsentVerifierAvailability.AVAILABLE:
        return False
    result = await UserConsentVerifier.request_verification_async(
        "Unlock Chrome with fingerprint"
    )
    return result == UserConsentVerificationResult.VERIFIED


def prompt_fingerprint():
    if not FINGERPRINT_AVAILABLE:
        return False
    try:
        return asyncio.run(verify_fingerprint())
    except Exception:
        return False

# ------------------ UI ------------------
def show_lock_ui():
    def try_fingerprint():
        if not FINGERPRINT_AVAILABLE:
            error_label.config(text="⚠️ Fingerprint unavailable.")
            return
        verified = prompt_fingerprint()
        if verified:
            unlocked = True
            root.destroy()
            open_chrome_restore()
        else:
            error_label.config(text="❌ Fingerprint not recognized. Try your enrolled finger.")

    def check_password(event=None):
        nonlocal entry
        global unlocked

        pwd = entry.get()

        if pwd == PASSWORD:
            unlocked = True
            root.destroy()
            open_chrome_restore()
        else:
            error_label.config(text="❌ Incorrect passcode. Try again.")

    def toggle_visibility():
        if entry.cget('show') == '':
            entry.config(show='*')
            toggle_btn.config(text='Show')
        else:
            entry.config(show='')
            toggle_btn.config(text='Hide')

    root = tk.Tk()
    root.title("🔒 Nova Chrome Lock")
    root.geometry("480x360")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.96)
    root.configure(bg='#081020')

    canvas = tk.Canvas(root, width=480, height=360, highlightthickness=0, bg='#081020')
    canvas.pack(fill='both', expand=True)

    for i, color in enumerate(['#07111f', '#0c1c35', '#172754', '#11224d', '#091626']):
        canvas.create_rectangle(0, i * 72, 480, (i + 1) * 72, fill=color, outline='')

    canvas.create_rectangle(26, 30, 454, 324, fill='#0e1931', outline='', width=0)
    canvas.create_rectangle(26, 30, 454, 324, outline='#6d8cff', width=2)
    canvas.create_rectangle(34, 38, 446, 316, fill='#ffffff', stipple='gray75', outline='')

    glass_panel = tk.Frame(root, bg='#162544', bd=0)
    canvas.create_window(240, 180, window=glass_panel, width=412, height=262)

    top_glow = canvas.create_line(30, 36, 450, 36, fill='#8ab4ff', width=1)
    canvas.itemconfigure(top_glow, stipple='gray25')

    header = tk.Label(glass_panel, text='Nova Lockdown', font=('Segoe UI', 24, 'bold'), fg='#f3f6ff', bg='#162544')
    header.pack(pady=(20, 4))

    subtitle = tk.Label(glass_panel, text='Restore Chrome with Windows Hello or password.',
                        font=('Segoe UI', 10), fg='#b8c6f7', bg='#162544')
    subtitle.pack()

    status_label = tk.Label(glass_panel, text=FINGERPRINT_STATUS,
                            font=('Segoe UI', 9), fg='#9ce4ff' if FINGERPRINT_AVAILABLE else '#ffbe79', bg='#162544')
    status_label.pack(pady=(8, 14))

    entry_border = tk.Frame(glass_panel, bg='#14203a', bd=1, relief='ridge')
    entry_border.pack(pady=10, ipadx=4, ipady=4)

    entry = tk.Entry(entry_border, show='*', font=('Segoe UI', 14), fg='#edf2ff', bg='#071324',
                     insertbackground='#edf2ff', width=26, bd=0, justify='center')
    entry.pack(ipadx=8, ipady=10)
    entry.focus()

    toggle_btn = tk.Button(glass_panel, text='Show', font=('Segoe UI', 9, 'bold'), bg='#1d2b55', fg='#e5eeff',
                           activebackground='#2f4fd1', activeforeground='white', bd=0,
                           command=toggle_visibility)
    toggle_btn.pack(pady=(10, 8), ipadx=14, ipady=5)

    unlock_btn = tk.Button(glass_panel, text='Unlock Chrome', font=('Segoe UI', 11, 'bold'), bg='#5b4dff', fg='white',
                           activebackground='#7b6cff', activeforeground='white', bd=0, relief='ridge',
                           command=check_password)
    unlock_btn.pack(ipady=10, ipadx=14)

    fingerprint_btn = tk.Button(glass_panel, text='Use Windows Hello', font=('Segoe UI', 10, 'bold'), bg='#1a88ff', fg='white',
                                activebackground='#4da4ff', activeforeground='white', bd=0, relief='groove',
                                command=try_fingerprint)
    if not FINGERPRINT_AVAILABLE:
        fingerprint_btn.config(state='disabled', bg='#4b6f8d', fg='#b8c1d6')
    fingerprint_btn.pack(pady=(12, 0), ipadx=12, ipady=8)

    error_label = tk.Label(glass_panel, text='', font=('Segoe UI', 10), fg='#ff8b8b', bg='#162544')
    error_label.pack(pady=(16, 0))

    hint = tk.Label(glass_panel, text='Tip: Windows Hello is the fastest unlock flow here.',
                    font=('Segoe UI', 8), fg='#99b4ff', bg='#162544')
    hint.pack(side='bottom', pady=(10, 0))

    root.bind('<Return>', check_password)
    root.mainloop()

# ------------------ MAIN LOOP ------------------
def monitor():
    global unlocked
    while True:
        if is_chrome_running():
            if not unlocked:
                kill_chrome()
                show_lock_ui()
        else:
            unlocked = False
        time.sleep(1)

# chạy thread để không bị lag
hide_console()
threading.Thread(target=monitor, daemon=True).start()

# giữ script sống
while True:
    time.sleep(10)