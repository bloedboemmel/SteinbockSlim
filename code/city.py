import csv
import calendar
import json
import os
from datetime import datetime, timedelta


class city:
    def __init__(self, Stadt):
        self.Stadt = Stadt
        self.ShortForm = Stadt["ShortForm"]
        self.BoulderName = Stadt["BoulderName"]
        self.WebsiteUrl = Stadt["WebsiteUrl"]
        self.BoulderadoUrl= Stadt["BoulderadoUrl"]
        self.Times = []
        self.OldAverage = 0
        self.besucher = 0
        self.frei = 1
        self.pngfile = ""
        for i in range(0,7):
            weekday = calendar.day_name[i]
            self.Times.append([int(Stadt[f"Open{weekday}"]), int(Stadt[f"Close{weekday}"])])
        self.dummydays()

    def dummydays(self):
        if not os.path.exists('png'):
            os.mkdir('png')
        if not os.path.exists('png/OtherDays'):
            os.mkdir('png/OtherDays')
        if not os.path.exists('today'):
            os.mkdir('today')
        if not os.path.exists('days'):
            os.mkdir('days')
        if not os.path.exists('all'):
            os.mkdir('all')


        if not os.path.exists(f'days/{self.ShortForm}'):
            os.mkdir(f'days/{self.ShortForm}')
        else:
            return
        for my_date in range(0, 7):
            day = calendar.day_name[my_date]

            n = {}
            time = datetime.strptime(f"{self.Times[my_date][0]}:00", "%H:%M")
            while time < datetime.strptime(f"{self.Times[my_date][1]}:00", "%H:%M"):
                new_time = time.replace(minute=((time.minute // 15) * 15)).strftime("%H:%M")
                if new_time not in n.keys() or len(n[new_time]) == 0:
                    n[new_time] = []

                time += timedelta(minutes=15)
            with open(f'days/{self.ShortForm}/{day}.txt', 'w') as outfile:
                json.dump(n, outfile)


def getcsv():
    with open('Cities.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        d = []
        key = [char.strip() for char in next(reader)]
        for row in reader:
            ro = [char.strip() for char in row]
            d.append(dict(zip(key, ro)))
        return d
    return []