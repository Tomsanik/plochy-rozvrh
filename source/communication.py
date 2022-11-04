import requests
import json
from datetime import date
import os

url_gpi = 'https://bakalari.gpisnicka.cz/bakaweb/api/'


def get_tokens(username, password, url=url_gpi):
    if url[-1] != '/':
        url += '/'
    print('URL accessed: ', url)

    # user = input('Username: ')
    # psswd = getpass.getpass("Password: ")
    user, psswd = username, password
    xml_string = f'client_id=ANDR&grant_type=password&username={user}&password={psswd}'
    try:
        r = requests.post(url + 'login', data=xml_string, headers={'Content-Type': 'application/x-www-form-urlencoded'},
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
    with open(PATH + '\\tokens.json', 'w') as file:
        file.write(r.text)
    return True


def refresh_access_token(url=url_gpi):
    PATH = os.getcwd()
    with open(PATH + "\\assets\\tokens.json", "r") as f:
        try:
            toks = json.load(f)
        except FileNotFoundError:
            print('No login tokens found.')
            exit()
    xml_string = 'client_id=ANDR&grant_type=refresh_token&refresh_token={}'.format(toks['refresh_token'])
    x = requests.post(url + 'login', data=xml_string, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = json.loads(x.text)
    with open(PATH + "\\assets\\tokens.json", 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_permanent_timetable(url=url_gpi):
    PATH = os.getcwd()
    with open(PATH + "\\assets\\tokens.json", "r") as f:
        toks = json.load(f)
    y = requests.get(url + '3/timetable/permanent',
                     headers={'Content-Type': 'application/x-www-form-urlencoded',
                              'Authorization': 'Bearer {}'.format(toks['access_token'])})
    data = json.loads(y.text)
    with open(PATH + "\\assets\\tokens.json", 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_actual_timetable(url=url_gpi, day=None):
    PATH = os.getcwd()
    with open(PATH + "\\assets\\tokens.json", "r") as f:
        toks = json.load(f)
    if day is None:
        day = date.today()
    y = requests.get(url + '3/timetable/actual?date={}'.format(day),
                     headers={'Content-Type': 'application/x-www-form-urlencoded',
                              'Authorization': 'Bearer {}'.format(toks['access_token'])})
    data = json.loads(y.text)
    with open(PATH + '\\assets\\rozvrh-aktualni.json', 'w') as file:
        json.dump(data, file, indent=4)
