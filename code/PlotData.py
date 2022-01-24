import pytz
from datetime import datetime
import GetData
from city import city, getcsv


tz = pytz.timezone('Europe/Berlin')
now = datetime.now(tz)
weekday = now.weekday()


def PlotCity(Stadt):
    tz = pytz.timezone('Europe/Berlin')
    now = datetime.now(tz)
    weekday = now.weekday()
    if not (Stadt.Times[weekday][0] <= now.hour <= Stadt.Times[weekday][1]):
        Stadt.pngfile = "./png/Closed.png"
        Stadt.OldAverage = 0
        Stadt.belegung = 0
        return
        
    GetData.getnow(Stadt)

    


def odd(number):
    if number % 2 == 0:
        return number - 1
    return number




def main():

    cities = []
    for cit in getcsv():
        cithere = city(cit)
        PlotCity(cithere)
    
    

if __name__ == '__main__':
    main()
