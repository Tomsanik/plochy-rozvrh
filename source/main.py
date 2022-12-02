"""Actual school schedule on the wallpaper easily"""
import os
import tkinter as tk
from tkinter import ttk
from pystray import MenuItem, Icon
from PIL import Image
from communication import get_tokens
from magic_casting import Magic


def withdraw_window(_event=None):
    """Window closes to system tray if update thread is running"""
    def show_window(icon1, _item1):
        icon1.stop()
        root.after(0, root.deiconify)

    if magic.is_running():
        root.withdraw()
        image = Image.open("source/bakalari.ico")
        menu = (MenuItem('Show', show_window, default=True, visible=False), )
        icon = Icon("name", image, "Plozvrh", menu)
        icon.run()
    else:
        root.destroy()


def login(_event):
    """Gets tokens from server and changes UI as needed"""
    name = widgets['en_uname'].get()
    psswd = widgets['en_psswd'].get()
    if len(name) * len(psswd) == 0:
        return
    if not get_tokens(name, psswd):
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


def update_now(_event):
    """Click to update"""
    magic.update_now()
    # widgets['bt_update'].config(state='disabled')
    widgets['lb_week'].config(text='')


def next_week(_event):
    """Update wallpaper with next week's schedule"""
    wk = magic.next_week()
    if wk > 0:
        s = f'Týden +{wk}'
    elif wk == 0:
        s = 'Aktuální týden'
    else:
        s =f'Týden {wk}'
    widgets['lb_week'].config(text=s)
    # widgets['bt_update'].config(state='enabled')


def prev_week(_event):
    """Update wallpaper with previous week's schedule"""
    wk = magic.prev_week()
    if wk > 0:
        s = f'Týden +{wk}'
    elif wk == 0:
        s = 'Aktuální týden'
    else:
        s =f'Týden {wk}'
    widgets['lb_week'].config(text=s)
    # widgets['bt_update'].config(state='enabled')


def actual_week(_event):
    """Update wallpaper with actual week"""
    magic.act_week()
    widgets['lb_week'].config(text='Aktuální týden')
    # widgets['bt_update'].config(state='enabled')


if __name__ == '__main__':
    PATH = os.getcwd()
    if not os.path.exists(PATH + '\\source'):
        os.chdir('../')

    magic = Magic()

    root = tk.Tk()
    root.title('Plozvrh')
    root.iconbitmap('source\\bakalari.ico')
    root.geometry('350x230+500+200')
    root.resizable(False, False)

    f1 = ttk.Frame()
    f2 = ttk.Frame()
    f3 = ttk.Frame()
    widgets = {'lb_uname': ttk.Label(text='Uživatelské jméno'), 'en_uname': ttk.Entry(),
               'lb_psswd': ttk.Label(text='Heslo'), 'en_psswd': ttk.Entry(show='*'),
               'lb_output': ttk.Label(text=''), 'bt_start': ttk.Button(f1, text='Přihlásit'),
               'bt_stop': ttk.Button(f1, text='Odhlásit'),
               'bt_quit': ttk.Button(f1, text='Ukončit'),
               'bt_pweek': ttk.Button(f2, text='Týden -1'),
               'bt_aweek': ttk.Button(f2, text='Teď'),
               'bt_nweek': ttk.Button(f2, text='Týden +1'),
               'lb_week': ttk.Label(f3, text='Aktuální týden'),
               'bt_update': ttk.Button(f3, text='Obnovit')}

    for wd in ['lb_uname', 'en_uname', 'lb_psswd', 'en_psswd', 'lb_output']:
        widgets[wd].pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

    f1.pack()
    f2.pack()
    f3.pack()

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

    widgets['bt_pweek'].bind('<Button>', prev_week)
    widgets['bt_pweek'].pack(expand=True, side=tk.LEFT)

    widgets['bt_aweek'].bind('<Button>', actual_week)
    widgets['bt_aweek'].pack(expand=True, side=tk.LEFT)

    widgets['bt_nweek'].bind('<Button>', next_week)
    widgets['bt_nweek'].pack(expand=True, side=tk.LEFT)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)
    root.mainloop()
