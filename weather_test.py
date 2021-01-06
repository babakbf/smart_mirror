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
longitude=45.415907100000005
latitude=-73.48298489999999
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
        weather_utl2='http://api.openweathermap.org/data/2.5/forecast/daily?q=Montreal&cnt=10&appid=c9cdea1f63b108c6311423e7fe4686a9'
        weather_url3='https://api.openweathermap.org/data/2.5/onecall?lat=45.4&lon=-73.5&exclude=hourly,minutely&appid=c9cdea1f63b108c6311423e7fe4686a'
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