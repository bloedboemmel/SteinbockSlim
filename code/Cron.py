# Run PlotData.main() every 15 minutes between 8 and 23.
# Run RemoveData.main() every day at 02:00.
from msilib.schema import Error
import PlotData
import RemoveData
from time import sleep
from datetime import datetime, timedelta
import pause

def loop():
    
    
    while True:
        try:
        #If time between 8 and 23
            if 8 <= datetime.now().hour <= 23:
                PlotData.main()
                minutesToSleep = 15 - datetime.now().minute % 15
                sleep(minutesToSleep * 60)
            elif datetime.now().hour == 0:
                    RemoveData.main()
                    pause.until(datetime.now() + timedelta(hours=7, minutes=45))
            # else sleep till 8
            else:
                sleep(60*15)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
        except Error as e:
            print(e)
            
            

if __name__ == '__main__':
    loop()
        
