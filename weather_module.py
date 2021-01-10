# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 21:00:28 2021

@author: babak
"""
import time
from time import strftime
from datetime import date, timedelta, datetime, timezone
import datetime
import os.path
import feedparser
import requests, json 
import pandas as pd


class Weather():

    def __init__(self):
        self.zipcode='J5R'
        self.countrycode='ca'
        self.units='metric'
        self.openweathermap_appkey='c9cdea1f63b108c6311423e7fe4686a9'
        self.latitude=45.415907100000005
        self.longitude=-73.48298489999999
        self.exclude='hourly,minutely'
        self.icon_path = 'weather_icons/'
        self.icon_ext = '.png'
        self.base_url='https://api.openweathermap.org/data/2.5/'
        self.activity_main_wind_speed_threshold=20
        #self.weather_api_url='https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={appkey}&units={units}'.format(lat=latitude,appkey=openweathermap_appkey,lon=longitude,units=units,ex=exclude)

    def GetWeatherUrl(self,WeatherType):
        # Weather Type C: Today/Current D:Daily Forecast 7 days A: Alert
        
        if WeatherType=='C': # Today/Current
            # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
            url=self.base_url+"weather?lat={lat}&lon={lon}&appid={API_key}&units={units}".format(lat=self.latitude,lon=self.longitude, API_key=self.openweathermap_appkey,units=self.units)
        elif WeatherType=='D': # Daily Forecast 7 days
            # https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
            url=self.base_url+"onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_key}&units={units}".format(lat=self.latitude,lon=self.longitude, API_key=self.openweathermap_appkey,part=self.exclude,units=self.units)
        elif WeatherType=='A': # Alert 
            # https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
            url=self.base_url+"onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_key}&units={units}".format(lat=self.latitude,lon=self.longitude, API_key=self.openweathermap_appkey, part=self.exclude,units=self.units)        
        else: # Current
            # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
            url=self.base_url+"weather?lat={lat}&lon={lon}&appid={API_key}&units={units}".format(lat=self.latitude,lon=self.longitude(), API_key=self.openweathermap_appkey,units=self.units)
        return url
    
    def WeatherInf(self):
        objWeather=Weather()
        url=objWeather.GetWeatherUrl('D')
        print(url)
        response = requests.get(url) 
        dict_weather = response.json()
        dict_current = {}
        if "current" in dict_weather:
            cur_weather=dict_weather["current"]
            dict_current["cur_feels_Like"]=round(cur_weather["feels_like"])
            dict_current["cur_humidity"]=str(round(cur_weather["humidity"])) + " %"
            dict_current["cur_temp"]=round(cur_weather["temp"])
            dict_current["cur_dew"]=round(cur_weather["dew_point"])
            dict_current["cur_pressure"]=cur_weather["pressure"]
            dict_current["cur_visibility"]=str(round(cur_weather["visibility"]/1000)) +" KM"
            wind_speed=round(cur_weather["wind_speed"]*3.6)
            dict_current["cur_wind_speed"]=str(wind_speed)+ " KM/H"
            dict_current["today_sunrise"]=objWeather.UnixTimeToLocal(cur_weather["sunrise"]).strftime("%H:%M")
            dict_current["today_sunset"]=objWeather.UnixTimeToLocal(cur_weather["sunset"]).strftime("%H:%M")
            dict_current["today_icon"]= objWeather.GetIconFile(dict_weather["current"]["weather"][0]["icon"]) #self.icon_path+today_icon+self.icon_ext
            dict_current["cur_desc"]=objWeather.GetWeatherDesc(dict_weather["current"]["weather"][0]["id"])
            if wind_speed >= self.activity_main_wind_speed_threshold:
                activity_condition= False
                
        if "daily" in dict_weather:
            
            # Day 0 
            dict_daily=dict_weather["daily"]
            dict_day0=dict_daily[0]
            dict_current["day0_name"]=objWeather.UnixTimeToLocal(dict_day0["dt"]).strftime("%A")
            dict_current["day0_sunrise"]=objWeather.UnixTimeToLocal(dict_day0["sunrise"]).strftime("%H:%M")
            dict_current["day0_sunset"]=objWeather.UnixTimeToLocal(dict_day0["sunset"]).strftime("%H:%M")
            dict_current["day0_temp_max"]=dict_day0["temp"]["max"]
            dict_current["day0_temp_min"]=dict_day0["temp"]["min"]
            
            
            # Day 1 
            dict_daily=dict_weather["daily"]
            dict_day1=dict_daily[1]
            dict_current["day1_name"]=objWeather.UnixTimeToLocal(dict_day1["dt"]).strftime("%A")
            dict_current["day1_sunrise"]=objWeather.UnixTimeToLocal(dict_day1["sunrise"]).strftime("%H:%M")
            dict_current["day1_sunset"]=objWeather.UnixTimeToLocal(dict_day1["sunset"]).strftime("%H:%M")
            dict_current["day1_temp_max"]=dict_day1["temp"]["max"]
            dict_current["day1_temp_min"]=dict_day1["temp"]["min"]
            
            # Day 2
            dict_day2=dict_daily[2]
            day2_date_utc = datetime.datetime.fromtimestamp(dict_day2["dt"], timezone.utc)
            day2_local_date = day2_date_utc.astimezone()
            dict_current["day2_name"]=day2_local_date.strftime("%A")

            # Day 3
            dict_daily=dict_weather["daily"]
            dict_day3=dict_daily[3]
            day3_date_utc = datetime.datetime.fromtimestamp(dict_day3["dt"], timezone.utc)
            day3_local_date = day3_date_utc.astimezone()
            dict_current["day3_name"]=day3_local_date.strftime("%A")

            # Day 4
            dict_daily=dict_weather["daily"]
            dict_day4=dict_daily[4]
            day4_date_utc = datetime.datetime.fromtimestamp(dict_day4["dt"], timezone.utc)
            day4_local_date = day4_date_utc.astimezone()
            dict_current["day4_name"]=day4_local_date.strftime("%A") 
            
            # Day 5
            dict_daily=dict_weather["daily"]
            dict_day5=dict_daily[5]
            day5_date_utc = datetime.datetime.fromtimestamp(dict_day5["dt"], timezone.utc)
            day5_local_date = day5_date_utc.astimezone()
            dict_current["day5_name"]=day5_local_date.strftime("%A")

            # Day 6
            dict_daily=dict_weather["daily"]
            dict_day6=dict_daily[6]
            day6_date_utc = datetime.datetime.fromtimestamp(dict_day6["dt"], timezone.utc)
            day6_local_date = day6_date_utc.astimezone()
            dict_current["day6_name"]=day6_local_date.strftime("%A")
            
            # Day 7
            dict_daily=dict_weather["daily"]
            dict_day7=dict_daily[7]
            day7_date_utc = datetime.datetime.fromtimestamp(dict_day7["dt"], timezone.utc)
            day7_local_date = day7_date_utc.astimezone()
            dict_current["day7_name"]=day7_local_date.strftime("%A")            

        print(dict_current)
        #     today_icon += '.png'
        #     icon_path += today_icon
        #     print(icon_path)
        #     #icon = PhotoImage(file='weather_icons/04n.png')  
        #     GUI.icon_label.configure(image=icon)
        #     GUI.icon_label.photo = icon  
    def GetWeatherDesc(self, weather_id):
        df=pd.read_csv("weather_conditions.csv")
        df_new=df.query('ID=='+str(weather_id))
        weather_desc=''
        for item in df_new["Description"].values:
            weather_desc += item
        return str(weather_desc)

    def UnixTimeToLocal(self, dt):
        date_utc = datetime.datetime.fromtimestamp(dt, timezone.utc)
        local_date = date_utc.astimezone()
        return local_date
    
    def GetIconFile(self, icon_name):
        icon_file=self.icon_path+icon_name+self.icon_ext
        return icon_file

    def GetActivity(self, weather_id):
        df=pd.read_csv("weather_conditions.csv")
        df_new=df.query('ID=='+str(weather_id))
        Activity=''
        for item in df_new["Description"].values:
            Activity += item
        return str(Activity)
    
a=Weather()
a.WeatherInf()