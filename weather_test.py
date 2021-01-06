import feedparser
import time
import sys
# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter.font
import pickle
import requests, json 
from datetime import datetime, timezone

openweathermap_appkey='c9cdea1f63b108c6311423e7fe4686a9'
latitude=45.415907100000005
longitude=-73.48298489999999
exclude='hourly,minutely'
units='metric'
args = dict(lon=longitude,
           lat=latitude,
           ex=exclude,
           units=units,
           appid=openweathermap_appkey
           )
weather_api_url='https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={appid}&units={units}'.format(**args)
print(weather_api_url)
sys.exit()
class GUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.largeFont = tkinter.font.Font(family="Piboto", size=70)
        self.mediumFont = tkinter.font.Font(family="Calibri", size=40)
        self.normalFont = tkinter.font.Font(family="Piboto Light", size=20)
        self.enNewsFont = tkinter.font.Font(family="Calibri Light", size=20)

    def setupGUI(self):
        self.grid(row=0, column=0)
        persianFont = tkinter.font.Font(family="Traditional Arabic", size=20)
        # Weather & news frame to contain weather/news info
        # For weather, column 0 = info, column 1 = icon
        today_weather_frame = Frame(self, width=400, height=500, bg='black')
        today_weather_frame.grid(row=0, column=0, sticky=W)
        GUI.weather_label0 = Label(today_weather_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.mediumFont, justify=LEFT)
        GUI.weather_label0.grid(row=0, column=2, sticky=NW)
        
        GUI.weather_label1 = Label(today_weather_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.mediumFont, justify=LEFT)
        GUI.weather_label1.grid(row=0, column=0, sticky=NW)
        
        GUI.weather_label_feels = Label(today_weather_frame, text="Feels Like...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_feels.grid(row=1, column=0, sticky=NW)
        
        GUI.weather_label_humidity = Label(today_weather_frame, text="Humidity...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_humidity.grid(row=1, column=2, sticky=NW)
        
        GUI.weather_label_wind = Label(today_weather_frame, text="Wind...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_wind.grid(row=2, column=0, sticky=NW)

        GUI.weather_label_pressure = Label(today_weather_frame, text="Pressure...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_pressure.grid(row=2, column=2, sticky=NW)        

        GUI.weather_label_sunrise = Label(today_weather_frame, text="Sunrise...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_sunrise.grid(row=3, column=0, sticky=NW)

        GUI.weather_label_sunset = Label(today_weather_frame, text="Sunset...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_sunset.grid(row=3, column=2, sticky=NW)      
        
        GUI.weather_label_cloudiness = Label(today_weather_frame, text="Cloudiness...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_cloudiness.grid(row=4, column=0, sticky=NW)

        GUI.weather_label_visibility = Label(today_weather_frame, text="Visibility...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label_visibility.grid(row=4, column=2, sticky=NW)      


        
        # Frame and labels to hold the forecast
        weather_news_frame = Frame(self, width=200, height=500, bg='black')
        weather_news_frame.grid(row=1, column=0, sticky=W)

        GUI.weather_label2 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label2.grid(row=1, column=0, sticky=W)
        GUI.weather_label3 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label3.grid(row=2, column=0, sticky=W)
        GUI.weather_label4 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label4.grid(row=3, column=0, sticky=W)
        GUI.weather_label5 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label5.grid(row=4, column=0, sticky=W)
        GUI.weather_label6 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label6.grid(row=5, column=0, sticky=W)
        GUI.weather_label7 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label7.grid(row=6, column=0, sticky=W)
        GUI.weather_label8 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label8.grid(row=7, column=0, sticky=W)
        """
        icon = PhotoImage(file="weather_icons/partly-cloudy-day.gif")
        icon = icon.subsample(10)

        # Set up labels to hold weather icons
        GUI.icon_label = Label(today_weather_frame, borderwidth=0, image=icon)
        GUI.icon_label.photo = icon
        GUI.icon_label.grid(row=0, column=1, sticky=W)
        GUI.icon_label2 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label2.grid(row=1, column=1, sticky=W)
        GUI.icon_label3 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label3.grid(row=2, column=1, sticky=W)
        GUI.icon_label4 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label4.grid(row=3, column=1, sticky=W)
        GUI.icon_label5 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label5.grid(row=4, column=1, sticky=W)
        GUI.icon_label6 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label6.grid(row=5, column=1, sticky=W)
        GUI.icon_label7 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label7.grid(row=6, column=1, sticky=W)
        GUI.icon_label8 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label8.grid(row=7, column=1, sticky=W)
        """



        

        self.configure(background='black')
    def getWeather():
        weather_url='http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={appkey}&units={units}'.format(zipcode=zipcode, countrycode=countrycode, units=units, appkey=openweathermap_appkey)
        print(weather_url)
        response = requests.get(weather_url) 
        dict_base = response.json()
        if dict_base["cod"] != "404": 
      
            # store the value of "main" 
            dict_main = dict_base["main"] 
            wind=dict_base["wind"]
            wind_speed=round(wind["speed"]*3.6)
            current_visibility = round(dict_base["visibility"]/1000)
            current_city=dict_base["name"]
            dict_weather = dict_base["weather"] 
            weather_description = dict_weather[0]["description"] 

            current_temperature = dict_main["temp"] 
            feels_like_temperature = round(dict_main["feels_like"] )
            current_pressure = dict_main["pressure"] 
            current_humidiy = dict_main["humidity"] 
            #sunset=dict_base["sys"]["sunrise"] 
            #sunset=datetime.datetime.utcfromtimestamp(dict_base["sys"]["sunrise"]).strftime('%Y-%m-%dT%H:%M:%SZ')
            
            sunrise_utc_time = datetime.datetime.fromtimestamp(dict_base["sys"]["sunrise"], timezone.utc)
            sunrise_local_time = sunrise_utc_time.astimezone()
            sunrise=sunrise_local_time.strftime("%H:%M")

            sunset_utc_time = datetime.datetime.fromtimestamp(dict_base["sys"]["sunset"], timezone.utc)
            sunset_local_time = sunset_utc_time.astimezone()
            sunset=sunset_local_time.strftime("%H:%M")
            
            #sunset=dict_base["sys"]["sunset"]  
            cloudiness=dict_base["clouds"]["all"]  
            if not cloudiness:
                cloudiness=0
            # print(" Temperature (in Celsius unit): " +
            #                     str(round(current_temperature)) + 
            #           "\n Atmospheric pressure (in hPa unit):" +
            #                     str(current_pressure) +
            #           "\n Humidity: " +
            #                     str(current_humidiy) + "%"
            #           "\n Description: " +
            #                     str(weather_description)) 
            # print(" Visibility:"+str(round(a,2))+" KM")
        else: 
            print(" City Not Found ")     
        GUI.weather_label_wind.configure(text='Wind Speed: '+ str(wind_speed) + " KM/H")
        GUI.weather_label1.configure(text='Today in '+current_city+": "+ str(round(current_temperature)) + "| ")
        GUI.weather_label_humidity.configure(text='Humidity: '+ str(round(current_humidiy)) + " %")
        GUI.weather_label_pressure.configure(text='Pressure: '+ str(current_pressure) + " hPa")
        GUI.weather_label_feels.configure(text='Feels Like: '+ str(feels_like_temperature))
        GUI.weather_label_sunrise.configure(text='Sunrise: '+ str(sunrise))
        GUI.weather_label_sunset.configure(text='Sunset: '+ str(sunset))
        GUI.weather_label_visibility.configure(text='Visibility: '+ str(current_visibility)+ " KM")
        GUI.weather_label_cloudiness.configure(text='Cloudiness: '+ str(cloudiness) + " %")
        #GUI.weather_label_feels.configure(text='Feels Like: '+ str(current_pressure) + " hPa")
        window.after(600000, mirror.updateWeatherDetails)

def close_escape(event=None):
    print('Smart mirror closed')
    window.destroy()


window = Tk()
window.title("Smart Mirror")
window.geometry('800x600')
window.configure(background='black')

#Removes borders from GUI and implements quit via esc
window.overrideredirect(1)
window.overrideredirect(0)
window.attributes("-fullscreen", True)
window.wm_attributes("-topmost", 1)
window.focus_set()
window.bind("<Escape>", close_escape)

mirror = GUI(window)
mirror.setupGUI()
window.after(1000, mirror.getWeather)
window.mainloop()