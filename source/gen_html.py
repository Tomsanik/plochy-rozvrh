import json
from datetime import datetime
import time
import os

max_item = 9  # neměnit

def generate_html(day, hour, zoom):
    def new_item(subj, group, room, type=''):
        add = '''               <div class="item-{ch}">
                    <div class="item-subj">{s}</div>
                    <div class="item-group">{g}</div>
                    <div class="item-room">{r}</div>
                </div>\n'''
        add = add.format(s=subj, g=group, r=room, ch=type)
        return add

    def new_hour(n:int, times:str):
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
        day = ['Po', 'Út', 'St', 'Čt', 'Pá'][n-1]
        add = add.format(day, date)
        return add

    def val_in_dict(lst, val, keyname='Id'):
        # returns item of dictionary with given keyname of given value 
        for d in lst:
            if d[keyname] == val:
                return d
        return None
    
    PATH = os.getcwd()+'\\assets'
    with open(PATH+'\\rozvrh-aktualni.json', encoding='utf-8') as js:
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
    html = html.format(zoom=zoom)

    html += new_hour('', '')

    for hh in hors:
        html += new_hour(hh['Caption'], hh['BeginTime']+'-'+hh['EndTime'])
        if hh['Id'] == max_item+2:
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

        s = ''
        i = 3
        for i in range(3, 12, 1):
            h = val_in_dict(hodiny, i, 'HourId')

            type = ''
            if (d['DayOfWeek']-1 == day) and (i-3 == hour):
                    type = 'ac'

            if h is None:
                type += '0'
                html += new_item('', '', '', type)
                continue

            if h['Change'] is not None:
                type += 'ch'
                change = h['Change']['ChangeType']
                match change:
                    case 'RoomChanged':
                        ss = h['Change']['Description']
                        n1, n2 = ss.find(':'), ss.find('(')
                        rom = ss[n1+1:n2-1]
                        sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                        grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']
                    case 'Removed':
                        rom = 'zrušeno'
                        ss = h['Change']['Description']
                        n = ss.find(',')
                        ss = ss[n+1:]
                        n1 = ss.find('(')+1
                        n2 = ss.find(',')
                        n3 = ss.find(')')
                        grp = ss[n1:n2]
                        sub = ss[n2+1:n3]
                    case 'Added':
                        sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                        rom = val_in_dict(roms, h['RoomId'])['Abbrev']
                        grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']  
                    case 'Canceled':
                        sub = h['Change']['TypeAbbrev']  
                        rom = ''
                        grp = ''       
            else:    
                type += 'nm'
                sub = val_in_dict(subs, h['SubjectId'])['Abbrev']
                grp = val_in_dict(grps, h['GroupIds'][0])['Abbrev']
                rom = val_in_dict(roms, h['RoomId'])['Abbrev']
            
            html += new_item(sub, grp, rom, type=type)

    html += '''                        </div>
                    </div>
            <div class="update-bar">aktualizováno: {now}</div>
        </body>
    </html>'''
    html = html.format(now=time.strftime("%H:%M:%S", time.localtime()))

    with open(PATH+'\\rozvrh.html', 'w' ,encoding='utf-8') as f:
        f.write(html)
        f.close()
    
    return round(zoom*10*50), round(zoom*(days_count*61.1+47.6+6))
