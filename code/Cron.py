# Run PlotData.main() every 15 minutes between 8 and 23.
# Run RemoveData.main() every day at 02:00.
import PlotData
import RemoveData
from time import sleep
from datetime import datetime, timedelta
import pause
dt = datetime(2013, 6, 2, 14, 36, 34, 383752)
pause.until(dt)
def loop():
    
    
    while True:
        #If time between 8 and 23
        if 8 <= datetime.now().hour <= 23:
            PlotData.main()
            now = datetime.now()
            minute = (int(now.minute/15) +1) * 15
            pause.until(now + timedelta(minutes=minute))
        elif datetime.now().hour == 0:
                RemoveData.main()
                pause.until(datetime.now() + timedelta(hours=8))
        # else sleep till 8
        else:
            sleep(60*15)

if __name__ == '__main__':
    loop()
        