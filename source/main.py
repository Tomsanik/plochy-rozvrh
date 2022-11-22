import tkinter as tk
from tkinter import ttk
from pystray import MenuItem, Icon
from PIL import Image
import os
from communication import get_tokens
from magic_casting import Magic


def withdraw_window(_event=None):
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


def logout(_event):
    widgets['lb_output'].config(text='Odhlašování probíhá, vyčkejte.')
    root.update()
    magic.stop()
    widgets['en_uname'].config(state="enabled")
    widgets['en_psswd'].config(state="enabled")
    widgets['bt_start'].config(state="enabled")
    widgets['bt_stop'].config(state='disabled')
    widgets['bt_quit'].config(text='Ukončit')
    widgets['lb_output'].config(text='Odhlášeno.')


if __name__ == '__main__':
    PATH = os.getcwd()
    if not os.path.exists(PATH + '\\source'):
        os.chdir('../')

    magic = Magic()

    root = tk.Tk()
    root.title('Plozvrh')
    root.iconbitmap('source\\bakalari.ico')
    root.geometry('350x220+500+200')
    root.resizable(False, False)

    f1 = ttk.Frame()
    widgets = {'lb_uname': ttk.Label(text='Uživatelské jméno'), 'en_uname': ttk.Entry(),
               'lb_psswd': ttk.Label(text='Heslo'), 'en_psswd': ttk.Entry(show='*'),
               'lb_output': ttk.Label(text=''), 'bt_start': ttk.Button(f1, text='Přihlásit'),
               'bt_stop': ttk.Button(f1, text='Odhlásit'), 'bt_quit': ttk.Button(f1, text='Ukončit')}

    for wd in ['lb_uname', 'en_uname', 'lb_psswd', 'en_psswd', 'lb_output']:
        widgets[wd].pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

    f1.pack()

    widgets['bt_start'].bind('<Button>', login)
    widgets['bt_start'].pack(expand=True, side=tk.LEFT)

    widgets['bt_stop'].bind('<Button>', logout)
    widgets['bt_stop'].config(state='disabled')
    widgets['bt_stop'].pack(expand=True, side=tk.LEFT)

    widgets['bt_quit'].bind('<Button>', withdraw_window)
    widgets['bt_quit'].pack(expand=True, side=tk.RIGHT)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)
    root.mainloop()
