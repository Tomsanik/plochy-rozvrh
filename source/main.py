"""Current school schedule on the wallpaper easily"""
import os
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry
from pystray import MenuItem, Icon
from PIL import Image
from communication import get_tokens, get_municipalities, get_schools, get_current_timetable
from magic_casting import Magic
from datetime import datetime
import psswd


def set_text(entry, text):
    entry.delte(0, tk.END)
    entry.insert(0, text)


def withdraw_window(_event=None):
    """Window closes to system tray if update thread is running"""
    def show_window(icon1, _item1):
        icon1.stop()
        root.after(0, root.deiconify)

    if magic.is_running():
        root.withdraw()
        image = Image.open("source/bakalari.ico")
        menu = (MenuItem('Show', show_window, default=True, visible=False),)
        icon = Icon("name", image, "Plozvrh", menu)
        icon.run()
    else:
        root.destroy()


def login(_event):
    """Gets tokens from server and changes UI as needed"""
    url = widgets['en_url'].get()
    if url[-1] != '/':
        url += '/'
    magic.URL = url
    magic.set_week(widgets['de_date'].get_date())
    magic.size = widgets['sc_size'].get()

    name = widgets['en_uname'].get()
    pswd = widgets['en_psswd'].get()
    if len(name) * len(pswd) == 0:
        return
    if not get_tokens(name, pswd, url):
        widgets['lb_output'].config(text='Přihlášení se nezdařilo')
        return

    magic.start()

    widgets['lb_output'].config(text='Přihlášeno!')
    widgets['en_uname'].config(state="disabled")
    widgets['en_psswd'].config(state="disabled")
    widgets['bt_start'].config(state="disabled")
    widgets['bt_stop'].config(state='enabled')
    widgets['bt_quit'].config(text='Minimalizovat')
    widgets['bt_update'].config(state='enabled')
    widgets['cb_munic'].config(state='disabled')
    widgets['cb_school'].config(state='disabled')
    widgets['en_url'].config(state='disabled')
    lines = [widgets['cb_munic'].get(), widgets['cb_school'].get(), url, widgets['en_uname'].get(), widgets['sc_size'].get()]
    with open(PATH+'\\assets\\last_login.txt', 'w') as ff:
        ff.write('\n'.join(map(str, lines)))
    psswd.encrypt_psswd(name, pswd, psswd_filename)


def logout(_event):
    """Disables thread doing the updates and changes UI as needed"""
    widgets['lb_output'].config(text='Odhlašování probíhá, vyčkejte.')
    root.update()
    magic.stop()
    widgets['en_uname'].config(state="enabled")
    widgets['en_psswd'].config(state="enabled")
    widgets['bt_start'].config(state="enabled")
    widgets['bt_stop'].config(state='disabled')
    widgets['bt_quit'].config(text='Ukončit')
    widgets['lb_output'].config(text='Odhlášeno.')
    widgets['bt_update'].config(state='disabled')
    widgets['cb_munic'].config(state='enabled')
    widgets['cb_school'].config(state='enabled')
    widgets['en_url'].config(state='enabled')


def update_now(_event):
    """Click to update"""
    magic.size = widgets['sc_size'].get()
    magic.set_week(widgets['de_date'].get_date())
    magic.update_now()
    widgets['lb_week'].config(text='')


def curr_week(_event):
    """Update wallpaper with current week"""
    widgets['lb_week'].config(text='Aktuální týden')
    widgets['de_date'].set_date(datetime.now())


def show_schools(_event):
    munip = widgets['cb_munic'].get()
    schools, uu = get_schools(munip)
    widgets['cb_school'].config(values=schools)
    widgets['cb_school'].current(0)
    global urls
    urls = uu
    widgets['en_url'].config(text=urls[0])


def show_url(_event):
    school_index = widgets['cb_school'].current()
    url = urls[school_index]
    widgets['en_url'].config(text=url)


if __name__ == '__main__':
    PATH = os.getcwd()
    if not os.path.exists(PATH + '\\source'):
        os.chdir('../')
        PATH = os.getcwd()
    psswd_filename = 'assets\\pssdw.xml'

    magic = Magic()
    urls = []

    root = tk.Tk()
    root.title('Plozvrh')
    root.iconbitmap('source\\bakalari.ico')
    root.geometry('350x320+500+200')
    root.resizable(False, False)

    f01 = ttk.Frame()
    f02 = ttk.Frame()
    f03 = ttk.Frame()
    f1 = ttk.Frame()
    f2 = ttk.Frame()
    f3 = ttk.Frame()
    f4 = ttk.Frame()
    widgets = {'lb_munic': ttk.Label(f01, text='Vyber město'),
               'cb_munic': ttk.Combobox(f01, state="readonly", width=40),
               'lb_school': ttk.Label(f02, text='Vyber školu'),
               'cb_school': ttk.Combobox(f02, state="readonly", width=40),
               'lb_url2': ttk.Label(f03, text='URL'), 'en_url': ttk.Entry(f03, width=40),
               # 'lb_url': ttk.Label(text=''),
               'lb_uname': ttk.Label(text='Uživatelské jméno'), 'en_uname': ttk.Entry(),
               'lb_psswd': ttk.Label(text='Heslo'), 'en_psswd': ttk.Entry(show='*'),
               'lb_output': ttk.Label(text=''), 'bt_start': ttk.Button(f1, text='Přihlásit'),
               'bt_stop': ttk.Button(f1, text='Odhlásit'),
               'bt_quit': ttk.Button(f1, text='Ukončit'),
               'de_date': DateEntry(f2, width=12, background='darkblue', foreground='white', borderwidth=2,
                                    locale='cs_CZ', date_pattern='dd. mm. yy'),
               'bt_cweek': ttk.Button(f2, text='dnes'),
               'lb_week': ttk.Label(f3, text='Aktuální týden'),
               'bt_update': ttk.Button(f3, text='Obnovit'),
               'lb_size': ttk.Label(f4, text='Velikost rozvrhu'),
               'sc_size': ttk.Scale(f4, from_=0.2, to=0.9, orient=tk.HORIZONTAL)
               # 'cb_size': ttk.Combobox(f4, state="readonly", width=6)
               }

    f01.pack()
    widgets['lb_munic'].pack(expand=True, side=tk.LEFT)
    municipalities = get_municipalities()
    widgets['cb_munic'].config(values=municipalities)
    widgets['cb_munic'].bind('<<ComboboxSelected>>', show_schools)
    widgets['cb_munic'].pack(expand=True, side=tk.LEFT)
    f02.pack()
    widgets['lb_school'].pack(expand=True, side=tk.LEFT)
    widgets['cb_school'].bind('<<ComboboxSelected>>', show_url)
    widgets['cb_school'].pack(expand=True, side=tk.LEFT)
    widgets['en_url'].pack()
    f03.pack()
    widgets['lb_url2'].pack(expand=True, side=tk.LEFT)
    widgets['en_url'].pack(expand=True, side=tk.RIGHT)

    for wd in ['lb_uname', 'en_uname', 'lb_psswd', 'en_psswd', 'lb_output']:
        widgets[wd].pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

    f1.pack()
    f2.pack()
    f3.pack()
    f4.pack()

    widgets['bt_start'].bind('<Button>', login)
    widgets['bt_start'].pack(expand=True, side=tk.LEFT)

    widgets['bt_stop'].bind('<Button>', logout)
    widgets['bt_stop'].config(state='disabled')
    widgets['bt_stop'].pack(expand=True, side=tk.LEFT)

    widgets['bt_quit'].bind('<Button>', withdraw_window)
    widgets['bt_quit'].pack(expand=True, side=tk.RIGHT)

    widgets['lb_week'].pack(expand=True, side=tk.LEFT)

    widgets['bt_update'].bind('<Button>', update_now)
    widgets['bt_update'].config(state='disabled')
    widgets['bt_update'].pack(expand=True, side=tk.LEFT)

    widgets['de_date'].pack(expand=True, side=tk.LEFT)

    widgets['bt_cweek'].bind('<Button>', curr_week)
    widgets['bt_cweek'].pack(expand=True, side=tk.LEFT)

    widgets['en_uname'].bind('<Return>', login)
    widgets['en_psswd'].bind('<Return>', login)
    widgets['en_uname'].focus_set()

    widgets['lb_size'].pack(expand=True, side=tk.LEFT)
    widgets['sc_size'].set(0.3)
    widgets['sc_size'].pack(expand=True, side=tk.LEFT)
    # widgets['cb_size'].config(values=['25%', '40%', '60%'])
    # widgets['cb_size'].set('40%')
    # widgets['cb_size'].pack(expand=True, side=tk.LEFT)

    if os.path.isfile(psswd_filename):
        f = open(PATH+'\\assets\\last_login.txt')
        loaded = f.read().splitlines()
        if len(loaded) == 5:
            widgets['en_url'].insert(0, loaded[2])
            widgets['cb_school'].set(loaded[1])
            widgets['cb_munic'].set(loaded[0])
            # widgets['en_uname'].insert(0, loaded[3])
            widgets['sc_size'].set(float(loaded[4]))
            widgets['en_uname'].focus_set()

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    if os.path.isfile(psswd_filename):
        u, p = psswd.decrypt_psswd(psswd_filename)
        widgets['en_uname'].insert(0, u)
        widgets['en_psswd'].insert(0, p)
        login(None)

    root.mainloop()
