# Run PlotData.main() every 15 minutes between 8 and 23.
# Run RemoveData.main() every day at 02:00.
import PlotData
import RemoveData
from time import sleep
from datetime import datetime
def loop():
    
    
    while True:
        #If time between 8 and 23
        if 8 <= datetime.now().hour <= 23:
            PlotData.main()
            sleep(15 * 60)
        elif datetime.now().hour == 0:
                RemoveData.main()
                sleep(70*60)
        # else sleep till 8
        else:
            sleep(60*15)

if __name__ == '__main__':
    loop()
        