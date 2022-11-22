from communication import get_actual_timetable, refresh_access_token
from gen_html import generate_html
from html_to_image import html_img
from wallpaper import get_set_wallpaper
import threading
from win10toast import ToastNotifier
from datetime import datetime
import time


def _the_magic(day, hour):
    zoom = 1.28
    max_hour = 9
    refresh_access_token()
    get_actual_timetable()  # day=datetime(2022, 11, 7))
    w, h = generate_html(day, hour, max_hour, zoom)
    html_img(w, h)
    get_set_wallpaper(w, h)
    _throw_notif(f'Následuje {hour + 1}. hodina')


def _throw_notif(note):
    toast = ToastNotifier()
    toast.show_toast(
        title="Tapeta s rozvrhem obnovena",
        msg=note,
        duration=3,
        icon_path="source\\bakalari.ico",
        threaded=True)


class Magic:
    def __init__(self):
        self._thr = None
        self.RUNNING = False

    def start(self):
        self._thr = threading.Thread(target=self._run)
        self._thr.start()
        self.RUNNING = True

    def stop(self):
        if self._thr is None:
            return
        self.RUNNING = False
        self._thr.join()
        self._thr = None

    def is_running(self):
        return self.RUNNING

    def _run(self):
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
                    # handle exceptions!!
                    _the_magic(datetime.now().weekday(), i)
                    last_update = tnow
                    break
                if 0 < dt < sleep_time:
                    quick_sleep = dt + 1

            if quick_sleep > 0:
                time.sleep(quick_sleep)
                quick_sleep = 0
            else:
                time.sleep(sleep_time)
            if not self.RUNNING:
                break
