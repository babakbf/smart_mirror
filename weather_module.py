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
            dict_current["cur_wind_speed"]=str(round(cur_weather["wind_speed"]*3.6))+ " KM/H"
            today_sunset=cur_weather["sunset"]
            today_sunrise=cur_weather["sunrise"]
            sunrise_utc_time = datetime.datetime.fromtimestamp(today_sunrise, timezone.utc)
            sunrise_local_time = sunrise_utc_time.astimezone()
            dict_current["today_sunrise"]=sunrise_local_time.strftime("%H:%M")
            sunset_utc_time = datetime.datetime.fromtimestamp(today_sunset, timezone.utc)
            sunset_local_time = sunset_utc_time.astimezone()
            dict_current["today_sunset"]=sunset_local_time.strftime("%H:%M")
            #GUI.icon_label.photo = today_icon  
            today_icon=dict_weather["current"]["weather"][0]["icon"]
            dict_current["today_icon"]= self.icon_path+today_icon+self.icon_ext
            today_weather_id=dict_weather["current"]["weather"][0]["id"]
            dict_current["cur_desc"]=objWeather.GetWeatherDesc(today_weather_id)
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

a=Weather()
a.WeatherInf()