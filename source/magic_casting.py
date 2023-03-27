"""Expeliarmus etc."""
import threading
from datetime import datetime
import time
from communication import get_actual_timetable, refresh_access_token
from gen_html import generate_html
from html_to_image import html_img
from wallpaper import get_set_wallpaper
from win10toast import ToastNotifier


def _the_magic(hour, week_change):
    """
    wekk_change: o kolik tydnu posunout rozvrh
    """
    zoom = 1.28
    max_hour = 9
    dow = datetime.now().weekday()
    refresh_access_token()
    get_actual_timetable(week_change)
    if week_change != 0:  # pokud nechci současný týden, ale posunutý
        dow = 5  # set day of week to saturday, so that no hour is highlighted
    width, height = generate_html(dow, hour, max_hour, zoom)
    html_img(width, height)
    get_set_wallpaper(width, height)
    _throw_notif(week_change, hour)


def _throw_notif(week, hour):
    if week != 0:
        note = 'Zobrazuji rozvrh {} {} {}. '
        if week >= 5:
            note = note.format('za', week, 'týdnů')
        elif week > 1:
            note = note.format('za', week, 'týdny')
        elif week == 1:
            note = note.format('za', week, 'týden')
        elif week == -1:
            note = note.format('před', abs(week), 'týdnem')
        else:
            note = note.format('před', abs(week), 'týdny')
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
        self.week = 0  # 0=actual, >0=future, <0=past

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

    def next_week(self):
        """Shows next week's schedule"""
        self.week += 1
        return self.week

    def prev_week(self):
        """Shows previous week's schedule"""
        self.week += -1
        return self.week

    def act_week(self):
        """Show actual week"""
        self.week = 0

    def is_running(self):
        """Are you even magical or what?"""
        return self.running

    def _run(self):
        def dt_sec(ti_, tf_):
            return round((tf_ - ti_).total_seconds())

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
            if self.cast_now:
                last_update = datetime(2022, 1, 1, 0, 0, 0, 0)
            for i in reversed(range(len(utimes))):
                tupdate = datetime.combine(tnow.date(), datetime.time(utimes[i]))
                ldt = dt_sec(last_update, tupdate)
                adt = dt_sec(tnow, tupdate)
                if adt * ldt < 0:
                    print(f'\tupdate = {tupdate.time()} \tdt = {adt} \tldt = {ldt}')
                    _the_magic(i, self.week)  # handle exceptions!!
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
