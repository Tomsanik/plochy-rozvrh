from communication import get_actual_timetable, get_tokens, refresh_access_token
from gen_html import generate_html
from html_to_image import html_img
from wallpaper import get_set_wallpaper
from datetime import datetime
import threading
import time
from win10toast import ToastNotifier
import sys


def the_magic(day, hour):
    zoom = 1.28
    refresh_access_token()
    get_actual_timetable()
    w, h = generate_html(day, hour, zoom)
    html_img(w, h)
    get_set_wallpaper(w, h)


if __name__ == "__main__":
    args = sys.argv
    # args = ['', 'konopova', 'thnnuaz25Klet!']
    if not get_tokens(args[1], args[2]):
        input("Ukončit stisknutím klávesy ENTER")
        exit()
    print('Úspěšně přihlášení')
    # start v 7:30
    sleeps = [75, 55, 65, 55, 55, 55, 55, 50, 16*60 + 15]
    sleeps = [s*60 for s in sleeps]
    i = 0
    dt = 0
    while True:
        dt = 0
        if i == 0:
            t1 = datetime.strptime(datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")
            t2 = datetime.strptime('07:30:00', "%H:%M:%S")

            dt = round((t1-t2).total_seconds())
            print('dt = ', dt)
            if dt > 0:
                while dt > sleeps[i]:
                    dt += -sleeps[i]
                    i = (i+1) % len(sleeps)
        
        thr = threading.Thread(target=the_magic, args=[datetime.now().weekday(), i])
        thr.start()

        print('i = ', i+1, '. hodina')
        if dt < 0:
            dts = -dt
        else:
            dts = sleeps[i] - dt
        print('dts = ', dts)
        s = 'Příští obnovení za '
        dtm = dts // 60
        if dtm // 60 > 0:
            s += str(dtm // 60) + ' h '
        if dtm % 60 > 0:
            s += str(dtm % 60) + ' min '
        s += str(dts % 60) + ' s.'
        
        print('Právě je ' + datetime.now().strftime("%H:%M:%S"))
        print(s)

        toast = ToastNotifier()
        toast.show_toast(
            "Tapeta s rozvrhem obnovena",
            s,
            duration=5,
            # icon_path = "icon.ico",
            threaded=True,
        )

        time.sleep(sleeps[i]-dt)
        i = (i+1) % len(sleeps)

        


