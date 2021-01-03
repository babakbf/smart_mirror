import feedparser
import time
import sys
import requests, json 
import pytz
from datetime import datetime, timezone

url_persian='http://www.bbc.co.uk/persian/index.xml'
urlradiofarda='https://www.radiofarda.com/api/zrttpoeuoupo'
url_america='http://feeds.bbci.co.uk/news/rss.xml?edition=us'
dict_persian = feedparser.parse(url_persian)
dict_america = feedparser.parse(url_america)



tz = pytz.timezone('Asia/Tehran')
berlin_now = datetime.now(tz)
print(berlin_now)
def getTopNews():
    i=0
    print(">"*100)
    while i < len(dict_persian):
        print(dict_persian['entries'][i]["title"])
        i=i+1
    j=0
    print("-"*20)
    while j < len(dict_america):
        print(dict_america['entries'][j]["title"])
        j=j+1
    print("-"*20)
    weather_utl='http://api.openweathermap.org/data/2.5/weather?id=524901&appid=c9cdea1f63b108c6311423e7fe4686a9&q=montreal'
    # while True:
    #     from datetime import datetime
    #     now = datetime.now()  
    #     print ("%s/%s/%s %s:%s:%s" % (now.month,now.day,now.year,now.hour,now.minute,now.second)) 
    #     sys.stdout.flush()
    #     print("\r")
    response = requests.get(weather_utl) 
    x = response.json()
    if x["cod"] != "404": 
      
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
      
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
      
        # store the value corresponding 
        # to the "pressure" key of y 
        current_pressure = y["pressure"] 
      
        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidiy = y["humidity"] 
      
        # store the value of "weather" 
        # key in variable z 
        z = x["weather"] 
      
        # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
        weather_description = z[0]["description"] 
        
        a = x["visibility"]/1000
        
        print(" Temperature (in Celsius unit): " +
                            str(round(current_temperature-273.15)) + 
                  "\n Atmospheric pressure (in hPa unit):" +
                            str(current_pressure) +
                  "\n Humidity: " +
                            str(current_humidiy) + "%"
                  "\n Description: " +
                            str(weather_description)) 
        print(" Visibility:"+str(round(a,2))+" KM")
    else: 
        print(" City Not Found ")     

getTopNews()