"""Generates HTML file"""
import json
from datetime import datetime
import os


def generate_html(day, hour, max_item: int = 9):
    """All the magic in one def"""
    def new_item(subj, group, room, typ=''):
        add = '''               <div class="item-{ch}">
                    <div class="item-subj">{s}</div>
                    <div class="item-group">{g}</div>
                    <div class="item-room">{r}</div>
                </div>\n'''
        add = add.format(s=subj, g=group, r=room, ch=typ)
        return add

    def new_hour(n, times):
        add = '''               <div class="hours">
                    <div class="hours-title">{}</div>
                    <div class="hours-time">{}</div>
                </div>\n'''
        add = add.format(n, times)
        return add

    def new_day(n, date=None):
        add = '''               <div class="day">
                    <div class="day-name">{}</div>
                    <div class="day-date">{}</div>
                </div>\n'''
        day = ['Po', 'Út', 'St', 'Čt', 'Pá'][n - 1]
        add = add.format(day, date)
        return add

    def val_in_dict(lst, val, keyname='Id'):
        # returns item of dictionary with given keyname of given value
        for d in lst:
            if d[keyname] == val:
                return d
        return None

    PATH = os.getcwd() + '\\assets'
    with open(PATH + '\\rozvrh-aktualni.json', encoding='utf-8') as js:
        rozvrh = json.load(js)

    hors = rozvrh['Hours']
    days = rozvrh['Days']
    subs = rozvrh['Subjects']
    grps = rozvrh['Groups']
    roms = rozvrh['Rooms']

    html = '''<!DOCTYPE html>
    <html>
        <head>
            <Title>Muj vlastni rozvrh</Title>
            <link rel="stylesheet" href="rozvrh.css">
        </head>
        <body>
            <script>
                document.body.style.zoom={zoom}
            </script>
            <div style="
                display: block;
                width: 500px;
                ">
                <div class="main-grid" id="main-grid">\n'''
    # html = html.format(zoom=zoom)

    html += new_hour('', '')

    for hh in hors:
        if int(hh['Caption']) < 1:
            continue
        html += new_hour(hh['Caption'], hh['BeginTime'] + '-' + hh['EndTime'])
        if hh['Id'] == max_item + 2:
            break

    days_count = len(days)
    for d in days:
        hodiny = d['Atoms']
        if len(hodiny) == 0:
            # for i in range(3, 13, 1):
            #     html += new_item('', '', '', '0')
            days_count += -1
            continue
        nt = d['Date'].find('T')
        dt = datetime.strptime(d['Date'][:nt], '%Y-%m-%d')
        html += new_day(d['DayOfWeek'], dt.strftime('%d. %m'))

        i = 3
        for i in range(3, max_item + 3, 1):
            h = val_in_dict(hodiny, i, 'HourId')

            typ = ''
            if (d['DayOfWeek'] - 1 == day) and (i - 3 == hour):
                typ = 'ac'

            if h is None:
                typ += '0'
                html += new_item('', '', '', typ)
                continue

            sub, rom, grp = '', '', ''
            if h['Change'] is not None:
                typ += 'ch'
                change = h['Change']['ChangeType']
                match change:
                    case 'RoomChanged':
                        ss = h['Change']['Description']
                        n1, n2 = ss.find(':'), ss.find('(')
                        rom = ss[n1 + 1:n2 - 1]
                        sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                        grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']
                    case 'Removed':
                        rom = 'zrušeno'
                        ss = h['Change']['Description']
                        n = ss.find(',')
                        ss = ss[n + 1:]
                        n1 = ss.find('(') + 1
                        n2 = ss.find(',')
                        n3 = ss.find(')')
                        grp = ss[n1:n2]
                        sub = ss[n2 + 1:n3]
                    case 'Added':
                        sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                        rom = val_in_dict(roms, h['RoomId'])['Abbrev']
                        grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']
                    case 'Canceled':
                        sub = h['Change']['TypeAbbrev']
                        if sub is None:
                            sub = 'Zruš'
                        rom = ''
                        grp = ''
                    case 'Substitution':
                        sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                        grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']
                        rom = val_in_dict(roms, h['RoomId'])['Abbrev']
            else:
                typ += 'nm'
                sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']
                rom = val_in_dict(roms, h['RoomId'])['Abbrev']

            if h['Theme'] == "":
                sub += '*'
            if h['IsLastRoomLesson'] == 'true':
                rom += '+'
            html += new_item(sub, grp, rom, typ=typ)

    html += '''                        </div>
                    </div>
            <div class="update-bar">aktualizováno: {now}</div>
        </body>
    </html>'''

    with open(PATH + '\\rozvrh.html', 'w', encoding='utf-8') as f:
        f.write(html)
        f.close()

    return round(10 * 50), round(days_count * 61.1 + 47.6 + 6)
