# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter.font
import time
from time import strftime
#from darksky import forecast
import pytz
from datetime import date, timedelta, datetime, timezone
import pandas as pd
#from newsapi.articles import Articles
import datetime
import pickle
import os.path
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
import feedparser
import requests, json 
WIDTH = 800
HEIGHT = 600

# Weather API credentials
#key = '93a522f375502ea4e4a091c06d034ff1'
#ORANGE = 45.415907100000005, (-73.48298489999999)

# News API credentials
#apikey = '455e01c84ca44ff387187f10f202bed3'
zipcode='J5R'
countrycode='ca'
units='metric'
openweathermap_appkey='c9cdea1f63b108c6311423e7fe4686a9'
latitude=45.415907100000005
longitude=-73.48298489999999
exclude='hourly,minutely'
units='metric'
weather_api_url='https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={appkey}&units={units}'.format(lat=latitude,appkey=openweathermap_appkey,lon=longitude,units=units,ex=exclude)
rweather_api_url='https://api.openweathermap.org/data/2.5/onecall?lat1={lat}&lon1={lon}&exclude1={ex}&appid=1{appkey}&units={units}'.format(lat=latitude,appkey=openweathermap_appkey,lon=longitude,units=units,ex=exclude)
print(weather_api_url)
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
        
        
        icon = PhotoImage(file="weather_icons/02d.gif")
        icon = icon.subsample(10)

        # Set up labels to hold weather icons
        GUI.icon_label = Label(today_weather_frame, borderwidth=0, image=icon ,background='black')
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
        



        # Adjust this width for spacing
        frame_placeholder = Frame(self, width=WIDTH/2.65, height=10, bg='black')
        frame_placeholder.grid(row=0, column=1)




        


        self.configure(background='black')

        
        
    def updateWeatherDetails(self):
        response = requests.get(weather_api_url) 
        dict_weather = response.json()
        if "current" in dict_weather:
            cur_weather=dict_weather["current"]
            cur_feels=cur_weather["feels_like"]
            cur_humidity=cur_weather["humidity"]
            cur_temp=cur_weather["temp"]
            cur_dew=cur_weather["dew_point"]
            cur_pressure=cur_weather["pressure"]
            cur_visibility=cur_weather["visibility"]
            cur_wind_speed=cur_weather["wind_speed"]
            today_icon=dict_weather["current"]["weather"][0]["icon"]
            today_sunset=cur_weather["sunset"]
            today_sunrise=cur_weather["sunrise"]
            sunrise_utc_time = datetime.datetime.fromtimestamp(today_sunset, timezone.utc)
            sunrise_local_time = sunrise_utc_time.astimezone()
            sunrise=sunrise_local_time.strftime("%H:%M")
            sunset_utc_time = datetime.datetime.fromtimestamp(today_sunrise, timezone.utc)
            sunset_local_time = sunset_utc_time.astimezone()
            sunset=sunset_local_time.strftime("%H:%M")
            #GUI.icon_label.photo = today_icon  
            icon_path = 'weather_icons/'
            today_icon += '.png'
            icon_path += today_icon
            print(icon_path)
            icon = PhotoImage(file='weather_icons/drone.gif')  
            GUI.icon_label.configure(image=icon)
            GUI.icon_label.photo = icon            
        else:
            print("bye")
        
        #weather_url='http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={appkey}&units={units}'.format(zipcode=zipcode, countrycode=countrycode, units=units, appkey=openweathermap_appkey)
        #response = requests.get(weather_url) 
        #dict_base = response.json()
        # if dict_base["cod"] != "404": 
      
        #     # store the value of "main" 
        #     dict_main = dict_base["main"] 
        #     wind=dict_base["wind"]
        #     wind_speed=round(wind["speed"]*3.6)
        #     current_visibility = round(dict_base["visibility"]/1000)
        #     current_city=dict_base["name"]
        #     dict_weather = dict_base["weather"] 
        #     weather_description = dict_weather[0]["description"] 

        #     current_temperature = dict_main["temp"] 
        #     feels_like_temperature = round(dict_main["feels_like"] )
        #     current_pressure = dict_main["pressure"] 
        #     current_humidiy = dict_main["humidity"] 
        #     #sunset=dict_base["sys"]["sunrise"] 
        #     #sunset=datetime.datetime.utcfromtimestamp(dict_base["sys"]["sunrise"]).strftime('%Y-%m-%dT%H:%M:%SZ')
            
        #     sunrise_utc_time = datetime.datetime.fromtimestamp(dict_base["sys"]["sunrise"], timezone.utc)
        #     sunrise_local_time = sunrise_utc_time.astimezone()
        #     sunrise=sunrise_local_time.strftime("%H:%M")

        #     sunset_utc_time = datetime.datetime.fromtimestamp(dict_base["sys"]["sunset"], timezone.utc)
        #     sunset_local_time = sunset_utc_time.astimezone()
        #     sunset=sunset_local_time.strftime("%H:%M")
            
        #     #sunset=dict_base["sys"]["sunset"]  
        #     cloudiness=dict_base["clouds"]["all"]  
        #     if not cloudiness:
        #         cloudiness=0
        #     # print(" Temperature (in Celsius unit): " +
        #     #                     str(round(current_temperature)) + 
        #     #           "\n Atmospheric pressure (in hPa unit):" +
        #     #                     str(current_pressure) +
        #     #           "\n Humidity: " +
        #     #                     str(current_humidiy) + "%"
        #     #           "\n Description: " +
        #     #                     str(weather_description)) 
        #     # print(" Visibility:"+str(round(a,2))+" KM")
        # else: 
        #     print(" City Not Found ")     
        # GUI.weather_label_wind.configure(text='Wind Speed: '+ str(wind_speed) + " KM/H")
        # GUI.weather_label1.configure(text='Today in '+current_city+": "+ str(round(current_temperature)) + "| ")
        # GUI.weather_label_humidity.configure(text='Humidity: '+ str(round(current_humidiy)) + " %")
        # GUI.weather_label_pressure.configure(text='Pressure: '+ str(current_pressure) + " hPa")
        # GUI.weather_label_feels.configure(text='Feels Like: '+ str(feels_like_temperature))
        # GUI.weather_label_sunrise.configure(text='Sunrise: '+ str(sunrise))
        # GUI.weather_label_sunset.configure(text='Sunset: '+ str(sunset))
        # GUI.weather_label_visibility.configure(text='Visibility: '+ str(current_visibility)+ " KM")
        # GUI.weather_label_cloudiness.configure(text='Cloudiness: '+ str(cloudiness) + " %")
        # #GUI.weather_label_feels.configure(text='Feels Like: '+ str(current_pressure) + " hPa")
        window.after(600000, mirror.updateWeatherDetails)
        
    def updateWeather(self):
        # Updates the weather information
        weekday = date.today()
        daily_summary = ''
        weather_today = ''
        weather_list = []
        today_icon = ''
        icons_list = []

        # Gets weather info
        counter = 0
        with forecast(key, *ORANGE) as orange:
            daily_summary += orange.daily.summary
            for day in orange.daily:
                day = dict(day=date.strftime(weekday, '%a'),
                           sum=day.summary,
                           tempMin=round((day.temperatureMin-32)*5/9),
                           tempMax=round((day.temperatureMax-32)*5/9),
                           icon=day.icon
                           )
                # Save each of these in a list to display to GUI
                if counter == 0:
                    weather_today += ('MAX {tempMax} | MIN {tempMin}'.format(**day))
                    today_icon = ('{icon}'.format(**day))
                    weekday += timedelta(days=1)
                    counter += 1
                else:
                    weather_list.append('{day}: MAX {tempMax} | MIN {tempMin}'.format(**day))
                    icons_list.append('{icon}'.format(**day))
                    weekday += timedelta(days=1)
                    counter += 1

        GUI.weather_label0.configure(text=weather_today)

        # Set icon for weather today
        icon_path = 'weather_icons/'
        today_icon += '.gif'
        icon_path += today_icon
        icon = PhotoImage(file=icon_path)
        icon = icon.subsample(9)
        GUI.icon_label.configure(image=icon)
        GUI.icon_label.photo = icon

        # Push updated weather info to each label along with icons
        for x in range(0, len(weather_list)):
            temp_icon_path = 'weather_icons/'
            temp_icon_name = icons_list[x]
            temp_icon_name += '.gif'
            temp_icon_path += temp_icon_name
            temp_icon = PhotoImage(file=temp_icon_path)
            temp_icon = temp_icon.subsample(15)

            if x == 0:
                GUI.weather_label2.configure(text='•'+weather_list[x])
                GUI.icon_label2.configure(image=temp_icon)
                GUI.icon_label2.photo = temp_icon
            if x == 1:
                GUI.weather_label3.configure(text='•'+weather_list[x])
                GUI.icon_label3.configure(image=temp_icon)
                GUI.icon_label3.photo = temp_icon
            if x == 2:
                GUI.weather_label4.configure(text='•'+weather_list[x])
                GUI.icon_label4.configure(image=temp_icon)
                GUI.icon_label4.photo = temp_icon
            if x == 3:
                GUI.weather_label5.configure(text='•'+weather_list[x])
                GUI.icon_label5.configure(image=temp_icon)
                GUI.icon_label5.photo = temp_icon
            if x == 4:
                GUI.weather_label6.configure(text='•'+weather_list[x])
                GUI.icon_label6.configure(image=temp_icon)
                GUI.icon_label6.photo = temp_icon
            if x == 5:
                GUI.weather_label7.configure(text='•'+weather_list[x])
                GUI.icon_label7.configure(image=temp_icon)
                GUI.icon_label7.photo = temp_icon
            if x == 6:
                GUI.weather_label8.configure(text='•'+weather_list[x])
                GUI.icon_label8.configure(image=temp_icon)
                GUI.icon_label8.photo = temp_icon

        window.after(600000, mirror.updateWeather)


        
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
            
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        nextDate = datetime.datetime.utcnow() + datetime.timedelta(weeks=+2)
        nextDate= nextDate.isoformat()+ 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=nextDate,
                                              maxResults=7, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        event_list = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            event_str = ''
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start[0:10] +" "+ start[11:16] # Remove unnecessary characters at end of string
            year = start.find('-')
            start_day = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M').strftime('%a %b %d %H:%M')
            event_date = start[year + 1:year + 6]
            summary = event['summary'].encode('ascii', 'ignore').decode('ascii') # Remove emojis
            event_str += summary + ' | ' + start_day
            event_list.append(event_str)

        # Update calendar text
        event_delta= 5 - len(event_list)
        i=0
        if event_delta > 0:
            while i < event_delta+1:
                event_list.append("")    
                i=i+1         
        GUI.calendar_label1.configure(text=event_list[0])           
        GUI.calendar_label2.configure(text=event_list[1])
        GUI.calendar_label3.configure(text=event_list[2])
        GUI.calendar_label4.configure(text=event_list[3])
        GUI.calendar_label5.configure(text=event_list[4])
        
        if event_delta==5:
            GUI.calendar_label1.configure(text="No upcoming events!")    
            
        window.after(600000, mirror.updateCalendar)

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
window.after(1000, mirror.updateWeatherDetails)
#window.after(1000, mirror.updateWeather)
#window.after(1000, mirror.updateNews)
#window.after(1000, mirror.updateNews_en)
#window.after(1000, mirror.updateCalendar)
window.mainloop()
