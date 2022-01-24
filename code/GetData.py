import calendar
import csv
import json
from weather import currentweather
from datetime import datetime, date
import pytz
from bs4 import BeautifulSoup
import requests
import os

header = ['Zeit', 'Besucher', 'Frei', 'Auslastung']
url = 'https://www.dersteinbock-nuernberg.de/'
tz = pytz.timezone('Europe/Berlin')


def getnow(Stadt):
    ans = requests.get(Stadt.BoulderadoUrl)
    soup = BeautifulSoup(ans.content, 'html.parser')
    aktuellbesetzt = soup.find_all(class_="actcounter-content")
    besetzt = int(aktuellbesetzt[0].text)
    aktuellfrei = soup.find_all(class_="freecounter-content")
    frei = int(aktuellfrei[0].text)
    zeit = datetime.now(tz).replace(minute=((datetime.now(tz).minute // 15) * 15)).strftime("%H:%M")
    Stadt.belegt = besetzt
    Stadt.frei = frei
    Stadt.max = frei+besetzt
    Stadt.prozent = int(100 * besetzt / (besetzt + frei))
    dumpit(zeit, Stadt)


def dumpit(zeit, Stadt):
    avg = ifnotexistcreatewithaverage(Stadt)
    Anteil = Stadt.prozent

    avg[zeit]['TODAY'] = [Anteil, Stadt.frei, Stadt.belegt]
    #interpolate missing values till now
    save0 = None
    keys = list(avg.keys())
    #Run through all keys backwards
    for key in keys[(keys.index(zeit)-1)::-1]:
        if avg[key]['TODAY'][0] is not None:
            save0 = key
            break
    if save0 is not None:
        for key in keys[keys.index(save0):keys.index(zeit)]:
            if avg[key]['TODAY'][0] is None:
                interpol_avg = int((avg[save0]['TODAY'][0] + (avg[zeit]['TODAY'][0] - avg[save0]['TODAY'][0]) * (keys.index(key) - keys.index(save0)) / (keys.index(zeit) - keys.index(save0))))
                interpol_frei = int(Stadt.max * (interpol_avg / 100))
                interpol_belegt = Stadt.max - interpol_frei
                avg[key]['TODAY'] = [interpol_avg, interpol_frei, interpol_belegt]

    with open(f'today/{Stadt.ShortForm}Belegung.json', 'w') as outfile:
        json.dump(avg, outfile)
    write_average(Anteil, Stadt)
        


def ifnotexistcreatewithaverage(Stadt):
    if not os.path.exists(f'today/{Stadt.ShortForm}Belegung.json'):
        my_date = date.today()
        dayname = calendar.day_name[my_date.weekday()]
        avg_dict = {}
        with open(f'days/{Stadt.ShortForm}/{dayname}.txt') as file:
            d = json.load(file)
        for key in d:
            try:
                avg = int(sum(d[key]) / len(d[key]))
                belegt = int(Stadt.max * (avg / 100))
                frei = Stadt.max - belegt
                avg_dict[key] = {'AVG': [avg, frei, belegt]}
            except ZeroDivisionError:
                avg = None
                avg_dict[key] = None
        
        # Interpolate missing values
        save0 = None
        save1 = None
        keys = list(avg_dict.keys())
        for key in keys:
            if avg_dict[key] is None:
                save1 = None
                if save0 is None:
                    avg_dict[key] = {'AVG': [0, 0, 0]}
                for key2 in keys[keys.index(key):]:
                    if avg_dict[key2] is not None:
                        save1 = key2
                        break
                if save0 is not None and save1 is not None:
                    interpol_avg = int((avg_dict[save1]['AVG'][0] - avg_dict[save0]['AVG'][0]) / (keys.index(save1) - keys.index(save0)))
                    interpol_frei = int(Stadt.max * (interpol_avg / 100))
                    interpol_belegt = Stadt.max - interpol_frei
                    avg_dict[key] = {'AVG': [interpol_avg, interpol_frei, interpol_belegt]}
                else:
                    avg_dict[key] = {'AVG': [0, 0, 0]}
            else:
                save0 = key
            if 'TODAY' not in list(avg_dict[key].keys()):
                avg_dict[key]['TODAY'] = [None, None, None]
        with open(f'today/{Stadt.ShortForm}Belegung.json', 'w') as outfile:
            json.dump(avg_dict, outfile)
        return avg_dict
    else:
        with open(f'today/{Stadt.ShortForm}Belegung.json') as file:
            d = json.load(file)
        return d


def dumpwithweather(data, Stadt):
    temp, weather = currentweather(Stadt.ShortForm)
    if temp is not None:
        data.append(temp)
        data.append(weather)
        with open(f'all/{Stadt.ShortForm}BelegungWithWeather.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(data)

def write_average(Anteil, Stadt):
    my_date = date.today()
    dayname = calendar.day_name[my_date.weekday()]
    with open(f'days/{Stadt.ShortForm}/{dayname}.txt') as file:
        d = json.load(file)
    d[datetime.now(tz).replace(minute=((datetime.now(tz).minute // 15) * 15)).strftime("%H:%M")].append(Anteil)

    with open(f'days/{Stadt.ShortForm}/{dayname}.txt', 'w') as outfile:
        json.dump(d, outfile)

