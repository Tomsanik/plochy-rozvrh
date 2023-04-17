"""Communication with server"""
from datetime import date, timedelta
import os
import json
import sys
import requests

URL_GPI = 'https://bakalari.gpisnicka.cz/bakaweb/api/'


def get_tokens(username, password, url=URL_GPI):
    """gets tokens from server"""
    if url[-1] != '/':
        url += '/'
    print('URL accessed: ', url)

    # user = input('Username: ')
    # psswd = getpass.getpass("Password: ")
    user, psswd = username, password
    xml_string = f'client_id=ANDR&grant_type=password&username={user}&password={psswd}'
    try:
        r = requests.post(url + 'api/login', data=xml_string,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'},
                          timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        print("Pravděpodobně chybné přihlašovací údaje.")
        return False
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return False
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return False
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        return False

    # data = json.loads(x.text)
    PATH = os.getcwd() + '\\assets'
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    with open(PATH + '\\tokens.json', 'w', encoding='utf-8') as file:
        file.write(r.text)
    return True


def refresh_access_token(url=URL_GPI):
    """Refreshes access token"""
    PATH = os.getcwd()
    try:
        with open(PATH + "\\assets\\tokens.json", "r", encoding='utf-8') as f:
            toks = json.load(f)
    except FileNotFoundError:
        print('No login tokens found.')
        # start the program anew and exit current one?
        sys.exit()
    rtok = toks['refresh_token']
    xml_string = f'client_id=ANDR&grant_type=refresh_token&refresh_token={rtok}'
    x = requests.post(url + 'api/login', data=xml_string,
                      headers={'Content-Type': 'application/x-www-form-urlencoded'},
                      timeout=3)
    data = json.loads(x.text)
    with open(PATH + "\\assets\\tokens.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_permanent_timetable(url=URL_GPI):
    """Gets permament timetable"""
    PATH = os.getcwd()
    with open(PATH + "\\assets\\tokens.json", "r", encoding='utf-8') as f:
        toks = json.load(f)
    rtok = toks['access_token']
    y = requests.get(url + 'api/3/timetable/permanent',
                     headers={'Content-Type': 'application/x-www-form-urlencoded',
                              'Authorization': f'Bearer {rtok}'}, timeout=3)
    data = json.loads(y.text)
    with open(PATH + "\\assets\\tokens.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_current_timetable(day, url=URL_GPI):
    """Get timetable of a week
    day: date of the day"""
    PATH = os.getcwd()
    with open(PATH + "\\assets\\tokens.json", "r", encoding='utf-8') as file:
        toks = json.load(file)
    # day = date.today()+timedelta(days=week*7)
    rtok = toks['access_token']
    print(day)
    y = requests.get(url + f'api/3/timetable/actual?date={day}',
                     headers={'Content-Type': 'application/x-www-form-urlencoded',
                              'Authorization': f'Bearer {rtok}'}, timeout=3)
    data = json.loads(y.text)
    with open(PATH + '\\assets\\rozvrh-aktualni.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def get_municipalities():
    y = requests.get('https://sluzby.bakalari.cz/api/v1/municipality',
                     headers={'Accept': 'application/json'})
    data = json.loads(y.text)
    res = [a["name"] for a in data]
    res = res[1:]  # delete first one, because it's empty string nonsense
    return res


def get_schools(munip: str):
    y = requests.get(f'https://sluzby.bakalari.cz/api/v1/municipality/{munip}',
                     headers={'Accept': 'application/json'})
    data = json.loads(y.text)['schools']
    names = [a['name'] for a in data]
    urls = [a['schoolUrl'] for a in data]
    return names, urls

