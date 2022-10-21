import requests
import json
from datetime import date

url_gpi = 'https://bakalari.gpisnicka.cz/bakaweb/api/'


def get_tokens(username, password, url=url_gpi):
    print('URL accessed: ', url)
    
    # user = input('Username: ')
    # psswd = getpass.getpass("Password: ")
    user, psswd = username, password
    xml_string = 'client_id=ANDR&grant_type=password&username={}&password={}'.format(user, psswd)
    try:
        r = requests.post(url+'login', data=xml_string, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        print("Pravděpodobně chybné přihlašovací údaje.")
        return False
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return False
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return False
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        return False
    
    # data = json.loads(x.text)
    with open('source\\tokens.json', 'w') as file:
        file.write(r.text)
    return True


def refresh_access_token(url=url_gpi):
    with open("source\\tokens.json", "r") as f:
        try:
            toks = json.load(f)
        except:
            get_tokens()
            toks = json.load(f)
    xml_string = 'client_id=ANDR&grant_type=refresh_token&refresh_token={}'.format(toks['refresh_token'])
    x = requests.post(url+'login', data=xml_string, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = json.loads(x.text)
    with open('source\\tokens.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_permanent_timetable(url=url_gpi):
    with open("source\\tokens.json", "r") as f:
        toks = json.load(f)
    y = requests.get(url+'3/timetable/permanent', 
        headers={'Content-Type': 'application/x-www-form-urlencoded', 
        'Authorization': 'Bearer {}'.format(toks['access_token'])})
    data = json.loads(y.text)
    with open('source\\rozvrh.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_actual_timetable(url=url_gpi, day=None):
    with open("source\\tokens.json", "r") as f:
        toks = json.load(f)
    if day is None:
        day = date.today()
    y = requests.get(url+'3/timetable/actual?date={}'.format(day), 
        headers={'Content-Type': 'application/x-www-form-urlencoded', 
        'Authorization': 'Bearer {}'.format(toks['access_token'])})
    data = json.loads(y.text)
    with open('source\\rozvrh-aktualni.json', 'w') as file:
        json.dump(data, file, indent=4)
