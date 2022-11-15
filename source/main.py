from source.communication import get_actual_timetable, get_tokens, refresh_access_token
from source.gen_html import generate_html
from source.html_to_image import html_img
from source.wallpaper import get_set_wallpaper
from datetime import datetime
import threading
import time
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import ttk
import pystray
from pystray import MenuItem as item
from PIL import Image
import os


def the_magic(day, hour):
    zoom = 1.28
    max_hour = 9
    refresh_access_token()
    get_actual_timetable()  # day=datetime(2022, 11, 7))
    w, h = generate_html(day, hour, max_hour, zoom)
    html_img(w, h)
    get_set_wallpaper(w, h)


def throw_notif(note):
    toast = ToastNotifier()
    toast.show_toast(
        "Tapeta s rozvrhem obnovena",
        note,
        duration=5,
        # icon_path = "icon.ico",
        threaded=True)


def update(lesson: int):
    thr1 = threading.Thread(target=the_magic, args=[datetime.now().weekday(), lesson])
    thr1.start()
    throw_notif(f'Následuje {lesson+1}. hodina')


def run():
    def dt_sec(ti, tf):
        return round((tf - ti).total_seconds())

    print('Úspěšně přihlášení')
    # start v 7:30
    utimes = ['07:30:00', '08:45:00', '09:40:00', '10:45:00',
              '11:40:00', '12:35:00', '13:30:00', '14:25:00', '15:15:00']
    utimes = [datetime.strptime(tt, "%H:%M:%S") for tt in utimes]

    last_update = datetime(2022, 1, 1, 0, 0, 0, 0)
    quick_sleep = 0
    sleep_time = 10  # seconds

    while True:
        tnow = datetime.now()
        print(f'Last update before {dt_sec(last_update, tnow)} s')
        print(f'\tlast = {last_update} \n\ttnow = {tnow}')
        for i in reversed(range(len(utimes))):
            tupdate = datetime.combine(tnow.date(), datetime.time(utimes[i]))
            ldt = dt_sec(last_update, tupdate)
            dt = dt_sec(tnow, tupdate)
            if dt * ldt < 0:
                print(f'\tupdate = {tupdate.time()} \tdt = {dt} \tldt = {ldt}')
                update(i)
                last_update = tnow
                break
            if 0 < dt < sleep_time:
                quick_sleep = dt + 1

        if quick_sleep > 0:
            time.sleep(quick_sleep)
            quick_sleep = 0
        else:
            time.sleep(sleep_time)
        if not RUNNING:
            break


def withdraw_window():
    def quit_window(icon1, item):
        icon1.stop()
        root.destroy()

    def show_window(icon1, item):
        icon1.stop()
        root.after(0, root.deiconify)

    if RUNNING:
        root.withdraw()
        image = Image.open("source/bakalari.ico")
        menu = (item('Quit', quit_window), item('Show', show_window))
        icon = pystray.Icon("name", image, "title", menu)
        icon.run()
    else:
        root.destroy()


def login(event):
    global thr, RUNNING
    name = widgets['un_entry'].get()
    psswd = widgets['ps_entry'].get()
    if len(name) * len(psswd) == 0:
        return
    if not get_tokens(name, psswd):
        widgets['out_label'].config(text='Přihlášení se nezdařilo')
        return
    widgets['out_label'].config(text='Přihlášeno!')
    widgets['un_entry'].config(state="disabled")
    widgets['ps_entry'].config(state="disabled")
    login_button.config(state="disabled")
    stop_button.config(state='enabled')
    RUNNING = True
    thr = threading.Thread(target=run)
    thr.start()


def stop(event):
    global thr, RUNNING
    RUNNING = False
    thr.join()
    thr = None
    widgets['un_entry'].config(state="enabled")
    widgets['ps_entry'].config(state="enabled")
    login_button.config(state="enabled")
    stop_button.config(state='disabled')


if __name__ == '__main__':
    PATH = os.getcwd()
    if not os.path.exists(PATH + '\\source'):
        os.chdir('../')
    RUNNING = False
    thr = None

    root = tk.Tk()
    root.title('Plozvrh')
    root.geometry('350x220+500+200')
    root.resizable(False, False)

    widgets = {'un_label': ttk.Label(text='Uživatelské jméno'), 'un_entry': ttk.Entry(),
               'ps_label': ttk.Label(text='Heslo'), 'ps_entry': ttk.Entry(show='*'), 'out_label': ttk.Label(text='')}

    for wd in widgets.values():
        wd.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

    login_button = ttk.Button(text='Přihlásit')
    login_button.bind('<Button>', login)
    login_button.pack(anchor=tk.W, padx=10, pady=5)

    stop_button = ttk.Button(text='Ukončit')
    stop_button.bind('<Button>', stop)
    stop_button.pack(anchor=tk.E, padx=10, pady=5)
    stop_button.config(state='disabled')

    root.protocol('WM_DELETE_WINDOW', withdraw_window)
    root.mainloop()
