import os

import requests


url = "http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric"
try:
    from keys import weather_key
    key = weather_key()
except:
    key = os.environ.get('WEATHER_KEY')
def currentweather(City):
    if key is None:
        return "None", "None"
    query = url.format(city_name=City, API_key=key)
    ans = requests.get(query) 


    if ans.status_code == 200:
        data = ans.json()
        temp = data['main']['temp']
        temp = round(temp)
        temp = str(temp) + "°C"
        weather_type = data['weather'][0]['main']
        return temp, weather_type
    else:
        print(f"The city {str(City)} you entered is not valid")
        return None, None

if __name__ == "__main__":
    City = input("Enter the name of the city: ")
    temp, weather_type = currentweather(City)
    if temp == None:
        print("The city you entered is not valid")
    else:
        print("The current weather is " + weather_type + " in " + City + " is " + temp)
