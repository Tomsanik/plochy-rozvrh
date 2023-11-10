"""Expeliarmus etc."""
import os
import threading
from datetime import datetime, timedelta
import time
from communication import get_current_timetable, refresh_access_token
from gen_html import generate_html
from html_to_image import html_img
from wallpaper import get_set_wallpaper
from win10toast import ToastNotifier
import json


def _throw_notif(day, hour, dweek):
    if dweek != 0:
        note = 'Zobrazuji rozvrh na den {}'
        note.format(day.strftime('%d. %m. %Y'))
    else:
        note = f'Následuje {hour + 1}. hodina'
    toast = ToastNotifier()
    toast.show_toast(
        title="Tapeta s rozvrhem obnovena",
        msg=note,
        duration=3,
        icon_path="source\\bakalari.ico",
        threaded=True)


class Magic:
    """Class full of magic and beautiful spells"""

    def __init__(self):
        self._thr = None
        self.running = False
        self.cast_now = False
        self.week = datetime.now()
        self.URL = None
        self.size = ''

    def start(self):
        """Start all the magic"""
        self._thr = threading.Thread(target=self._run)
        self._thr.start()
        self.running = True

    def stop(self):
        """Stops magic from happening"""
        if self._thr is None:
            return
        self.running = False
        self._thr.join()
        self._thr = None

    def update_now(self):
        """Updates at next opportunity"""
        self.cast_now = True

    def set_week(self, day):
        """Sets week to show on schedule"""
        self.week = day

    def is_running(self):
        """Are you even magical or what?"""
        return self.running

    def _run(self):
        def dt_sec(ti_, tf_):
            return round((tf_ - ti_).total_seconds())

        print('Úspěšně přihlášení')

        # Getting update times from downloaded timetable
        PATH = os.getcwd() + '\\assets'
        with open(PATH + '\\rozvrh-aktualni.json', encoding='utf-8') as js:
            rozvrh = json.load(js)
        hors = rozvrh['Hours']
        utimes = []
        uhours = []
        for i, h in enumerate(hors):
            if i == 0:
                utimes.append(datetime.strptime(h["BeginTime"], "%H:%M"))
                uhours.append(0)
            utimes.append(datetime.strptime(h["EndTime"], "%H:%M"))
            uhours.append(i)

        last_update = datetime(2022, 1, 1, 0, 0, 0, 0)
        quick_sleep = 0
        sleep_time = 10  # seconds

        while True:
            tnow = datetime.now()
            print(f'Last update before {dt_sec(last_update, tnow)} s')
            print(f'\tlast = {last_update} \n\ttnow = {tnow}')
            if self.cast_now:
                last_update = datetime(2022, 1, 1, 0, 0, 0, 0)
            for uhour, utime in zip(reversed(uhours), reversed(utimes)):
                tupdate = datetime.combine(tnow.date(), datetime.time(utime))
                ldt = dt_sec(last_update, tupdate)
                adt = dt_sec(tnow, tupdate)
                if adt * ldt < 0:
                    print(f'\tupdate = {tupdate.time()} \tdt = {adt} \tldt = {ldt}')
                    self._the_magic(uhour, self.week, self.URL)  # handle exceptions!!
                    last_update = tnow
                    self.cast_now = False
                    break
                if 0 < adt < sleep_time:
                    quick_sleep = adt + 1

            if quick_sleep > 0:
                time.sleep(quick_sleep)
                quick_sleep = 0
            else:
                for i in range(sleep_time):
                    time.sleep(1)
                    if self.cast_now or not self.running:
                        break
            if not self.running:
                break

    def _the_magic(self, hour, day, URL):
        """
        day: week around this day will show up
        """
        # zoom = 1.28
        zoom = 1.6
        max_hour = 9
        refresh_access_token(URL)
        week0 = day.isocalendar().week
        week1 = datetime.now().isocalendar().week
        if week0 != week1:
            dow = 5  # set the day of the week to saturday, so that no hour is highlighted
        else:
            dow = datetime.now().weekday()
        get_current_timetable(day, URL)
        width, height = generate_html(dow, hour, max_hour, zoom)
        html_img(width, height)
        # get_set_wallpaper(width, height)
        _throw_notif(day, hour, week0 - week1)