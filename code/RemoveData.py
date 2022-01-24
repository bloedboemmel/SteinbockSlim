import calendar
import json
import pytz
from datetime import datetime, date
from city import city, getcsv


tz = pytz.timezone('Europe/Berlin')
now = datetime.now(tz)
weekday = now.weekday()

def addNewAverage(Stadt):
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

def main():

    cities = []
    for cit in getcsv():
        cithere = city(cit)
        addNewAverage(cithere)

if __name__ == '__main__':
    main()
