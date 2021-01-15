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
import json


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
        self.activity_main_wind_speed_threshold=40
        self.activity_main_min_temp_threshold=-18
        self.activity_drone_min_temp_threshold=-5
        self.activity_drone_wind_speed_threshold=20
        self.activity_drone_visibility_threshold=5
        self.activity_kayak_wind_speed_threshold=20
        self.activity_kayak_min_temp_threshold=22
        self.activity_BBQ_min_temp_threshold=-5
        self.activity_BIKE_min_temp_threshold=15
        self.activity_main_dew_threshold=-28
        self.activity_main_max_temp_threshold=40
        self.activity_main_hum_threshold=95
        self.activity_min_jogging_offset_seconds_threshold=14400
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
        # print(url)
        response = requests.get(url) 
        dict_weather = response.json()
        dict_current = {}
        activity_condition = True
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
            dict_current["today_icon"]= objWeather.GetIconFile(dict_weather["current"]["weather"][0]["icon"]) 
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
            dict_current["day0_temp_max"]=round(dict_day0["temp"]["max"])
            dict_current["day0_temp_min"]=round(dict_day0["temp"]["min"])
            dict_current["day0_temp_mor"]=round(dict_day0["temp"]["morn"])
            dict_current["day0_temp_day"]=round(dict_day0["temp"]["day"])
            dict_current["day0_temp_eve"]=round(dict_day0["temp"]["eve"])
            dict_current["day0_temp_night"]=round(dict_day0["temp"]["night"])
            dict_current["day0_feels_mor"]=round(dict_day0["feels_like"]["morn"])
            dict_current["day0_feels_day"]=round(dict_day0["feels_like"]["day"])
            dict_current["day0_feels_eve"]=round(dict_day0["feels_like"]["eve"])
            dict_current["day0_feels_night"]=round(dict_day0["feels_like"]["night"])
            dict_current["day0_dew_point"]=round(dict_day0["dew_point"])
            dict_current["day0_pressure"]=str(dict_day0["pressure"]) + " hPa"
            dict_current["day0_humidity"]=str(dict_day0["humidity"]) + " %"
            dict_current["day0_wind_speed"]=str(round(dict_day0["wind_speed"]*3.6))+ " KM/H"
            dict_current["day0_id"]=dict_day0["weather"][0]["id"]
            dict_current["day0_desc"]=objWeather.GetWeatherDesc(dict_current["day0_id"])
            dict_current["day0_activity"]=objWeather.GetActivity(dict_current["day0_id"], \
              dict_current["day0_temp_max"],dict_current["day0_temp_min"], \
                  (dict_day0["wind_speed"]*3.6), \
                      dict_current["day0_dew_point"], \
                      cur_weather["visibility"],dict_current["day0_sunset"],1)            
            dict_current["day0_icon"]= objWeather.GetIconFile(dict_day0["weather"][0]["icon"])
            
            # Day 1 
            dict_day1=dict_daily[1]
            dict_current["day1_name"]=objWeather.UnixTimeToLocal(dict_day1["dt"]).strftime("%A")
            dict_current["day1_sunrise"] = objWeather.UnixTimeToLocal(dict_day1["sunrise"]).strftime("%H:%M")
            dict_current["day1_sunset"] = objWeather.UnixTimeToLocal(dict_day1["sunset"]).strftime("%H:%M")
            dict_current["day1_temp_max"]=round(dict_day1["temp"]["max"])
            dict_current["day1_temp_min"]=round(dict_day1["temp"]["min"])
            dict_current["day1_temp_mor"]=round(dict_day1["temp"]["morn"])
            dict_current["day1_temp_day"]=round(dict_day1["temp"]["day"])
            dict_current["day1_temp_eve"]=round(dict_day1["temp"]["eve"])
            dict_current["day1_temp_night"]=round(dict_day1["temp"]["night"])
            dict_current["day1_feels_mor"]=round(dict_day1["feels_like"]["morn"])
            dict_current["day1_feels_day"]=round(dict_day1["feels_like"]["day"])
            dict_current["day1_feels_eve"]=round(dict_day1["feels_like"]["eve"])
            dict_current["day1_feels_night"]=round(dict_day1["feels_like"]["night"])
            dict_current["day1_dew_point"]=round(dict_day1["dew_point"])
            dict_current["day1_pressure"]=str(dict_day1["pressure"]) + " hPa"
            dict_current["day1_humidity"]=str(dict_day1["humidity"]) + " %"
            dict_current["day1_wind_speed"]=str(round(dict_day1["wind_speed"]*3.6))+ " KM/H"
            dict_current["day1_id"]=dict_day1["weather"][0]["id"]
            dict_current["day1_desc"]=objWeather.GetWeatherDesc(dict_current["day1_id"])
            dict_current["day1_activity"]=objWeather.GetActivity(dict_current["day1_id"], \
                    dict_current["day1_temp_max"],dict_current["day1_temp_min"], \
                        (dict_day1["wind_speed"]*3.6), \
                            dict_current["day1_dew_point"],100,"00:00",0)
            dict_current["day1_icon"]= objWeather.GetIconFile(dict_day1["weather"][0]["icon"])                

            
            
            # Day 2
            dict_day2=dict_daily[2]
            dict_current["day2_name"]=objWeather.UnixTimeToLocal(dict_day2["dt"]).strftime("%A")
            dict_current["day2_sunrise"] = objWeather.UnixTimeToLocal(dict_day2["sunrise"]).strftime("%H:%M")
            dict_current["day2_sunset"] = objWeather.UnixTimeToLocal(dict_day2["sunset"]).strftime("%H:%M")
            dict_current["day2_temp_max"]=round(dict_day2["temp"]["max"])
            dict_current["day2_temp_min"]=round(dict_day2["temp"]["min"])
            dict_current["day2_temp_mor"]=round(dict_day2["temp"]["morn"])
            dict_current["day2_temp_day"]=round(dict_day2["temp"]["day"])
            dict_current["day2_temp_eve"]=round(dict_day2["temp"]["eve"])
            dict_current["day2_temp_night"]=round(dict_day2["temp"]["night"])
            dict_current["day2_feels_mor"]=round(dict_day2["feels_like"]["morn"])
            dict_current["day2_feels_day"]=round(dict_day2["feels_like"]["day"])
            dict_current["day2_feels_eve"]=round(dict_day2["feels_like"]["eve"])
            dict_current["day2_feels_night"]=round(dict_day2["feels_like"]["night"])
            dict_current["day2_dew_point"]=round(dict_day2["dew_point"])
            dict_current["day2_pressure"]=str(dict_day2["pressure"]) + " hPa"
            dict_current["day2_humidity"]=str(dict_day2["humidity"]) + " %"
            dict_current["day2_wind_speed"]=str(round(dict_day2["wind_speed"]*3.6))+ " KM/H"
            dict_current["day2_id"]=dict_day2["weather"][0]["id"]
            dict_current["day2_desc"]=objWeather.GetWeatherDesc(dict_current["day2_id"])
            dict_current["day2_activity"]=objWeather.GetActivity(dict_current["day2_id"], \
                    dict_current["day2_temp_max"],dict_current["day2_temp_min"], \
                        (dict_day2["wind_speed"]*3.6), \
                            dict_current["day2_dew_point"],100,"00:00",0)
            dict_current["day2_icon"]= objWeather.GetIconFile(dict_day2["weather"][0]["icon"])       

            # Day 3
            dict_day3=dict_daily[3]
            dict_current["day3_name"]=objWeather.UnixTimeToLocal(dict_day3["dt"]).strftime("%A")
            dict_current["day3_sunrise"] = objWeather.UnixTimeToLocal(dict_day3["sunrise"]).strftime("%H:%M")
            dict_current["day3_sunset"] = objWeather.UnixTimeToLocal(dict_day3["sunset"]).strftime("%H:%M")
            dict_current["day3_temp_max"]=round(dict_day3["temp"]["max"])
            dict_current["day3_temp_min"]=round(dict_day3["temp"]["min"])
            dict_current["day3_temp_mor"]=round(dict_day3["temp"]["morn"])
            dict_current["day3_temp_day"]=round(dict_day3["temp"]["day"])
            dict_current["day3_temp_eve"]=round(dict_day3["temp"]["eve"])
            dict_current["day3_temp_night"]=round(dict_day3["temp"]["night"])
            dict_current["day3_feels_mor"]=round(dict_day3["feels_like"]["morn"])
            dict_current["day3_feels_day"]=round(dict_day3["feels_like"]["day"])
            dict_current["day3_feels_eve"]=round(dict_day3["feels_like"]["eve"])
            dict_current["day3_feels_night"]=round(dict_day3["feels_like"]["night"])
            dict_current["day3_dew_point"]=round(dict_day3["dew_point"])
            dict_current["day3_pressure"]=str(dict_day3["pressure"]) + " hPa"
            dict_current["day3_humidity"]=str(dict_day3["humidity"]) + " %"
            dict_current["day3_wind_speed"]=str(round(dict_day3["wind_speed"]*3.6))+ " KM/H"
            dict_current["day3_id"]=dict_day3["weather"][0]["id"]
            dict_current["day3_desc"]=objWeather.GetWeatherDesc(dict_current["day3_id"])
            dict_current["day3_activity"]=objWeather.GetActivity(dict_current["day3_id"], \
                    dict_current["day3_temp_max"],dict_current["day3_temp_min"], \
                        (dict_day3["wind_speed"]*3.6), \
                            dict_current["day3_dew_point"],100,"00:00",0)
            dict_current["day3_icon"]= objWeather.GetIconFile(dict_day3["weather"][0]["icon"])   

            # Day 4
            dict_daily=dict_weather["daily"]
            dict_day4=dict_daily[4]
            dict_current["day4_name"]=objWeather.UnixTimeToLocal(dict_day4["dt"]).strftime("%A")
            dict_current["day4_sunrise"] = objWeather.UnixTimeToLocal(dict_day4["sunrise"]).strftime("%H:%M")
            dict_current["day4_sunset"] = objWeather.UnixTimeToLocal(dict_day4["sunset"]).strftime("%H:%M")
            dict_current["day4_temp_max"]=round(dict_day4["temp"]["max"])
            dict_current["day4_temp_min"]=round(dict_day4["temp"]["min"])
            dict_current["day4_temp_mor"]=round(dict_day4["temp"]["morn"])
            dict_current["day4_temp_day"]=round(dict_day4["temp"]["day"])
            dict_current["day4_temp_eve"]=round(dict_day4["temp"]["eve"])
            dict_current["day4_temp_night"]=round(dict_day4["temp"]["night"])
            dict_current["day4_feels_mor"]=round(dict_day4["feels_like"]["morn"])
            dict_current["day4_feels_day"]=round(dict_day4["feels_like"]["day"])
            dict_current["day4_feels_eve"]=round(dict_day4["feels_like"]["eve"])
            dict_current["day4_feels_night"]=round(dict_day4["feels_like"]["night"])
            dict_current["day4_dew_point"]=round(dict_day4["dew_point"])
            dict_current["day4_pressure"]=str(dict_day4["pressure"]) + " hPa"
            dict_current["day4_humidity"]=str(dict_day4["humidity"]) + " %"
            dict_current["day4_wind_speed"]=str(round(dict_day4["wind_speed"]*3.6))+ " KM/H"
            dict_current["day4_id"]=dict_day4["weather"][0]["id"]
            dict_current["day4_desc"]=objWeather.GetWeatherDesc(dict_current["day4_id"])
            dict_current["day4_activity"]=objWeather.GetActivity(dict_current["day4_id"], \
                    dict_current["day4_temp_max"],dict_current["day4_temp_min"], \
                        (dict_day4["wind_speed"]*3.6), \
                            dict_current["day4_dew_point"],100,"00:00",0)
            dict_current["day4_icon"]= objWeather.GetIconFile(dict_day4["weather"][0]["icon"])    
            
            # Day 5
            dict_daily=dict_weather["daily"]
            dict_day5=dict_daily[5]
            dict_current["day5_name"]=objWeather.UnixTimeToLocal(dict_day5["dt"]).strftime("%A")
            dict_current["day5_sunrise"] = objWeather.UnixTimeToLocal(dict_day5["sunrise"]).strftime("%H:%M")
            dict_current["day5_sunset"] = objWeather.UnixTimeToLocal(dict_day5["sunset"]).strftime("%H:%M")
            dict_current["day5_temp_max"]=round(dict_day5["temp"]["max"])
            dict_current["day5_temp_min"]=round(dict_day5["temp"]["min"])
            dict_current["day5_temp_mor"]=round(dict_day5["temp"]["morn"])
            dict_current["day5_temp_day"]=round(dict_day5["temp"]["day"])
            dict_current["day5_temp_eve"]=round(dict_day5["temp"]["eve"])
            dict_current["day5_temp_night"]=round(dict_day5["temp"]["night"])
            dict_current["day5_feels_mor"]=round(dict_day5["feels_like"]["morn"])
            dict_current["day5_feels_day"]=round(dict_day5["feels_like"]["day"])
            dict_current["day5_feels_eve"]=round(dict_day5["feels_like"]["eve"])
            dict_current["day5_feels_night"]=round(dict_day5["feels_like"]["night"])
            dict_current["day5_dew_point"]=round(dict_day5["dew_point"])
            dict_current["day5_pressure"]=str(dict_day5["pressure"]) + " hPa"
            dict_current["day5_humidity"]=str(dict_day5["humidity"]) + " %"
            dict_current["day5_wind_speed"]=str(round(dict_day5["wind_speed"]*3.6))+ " KM/H"
            dict_current["day5_id"]=dict_day5["weather"][0]["id"]
            dict_current["day5_desc"]=objWeather.GetWeatherDesc(dict_current["day5_id"])
            dict_current["day5_activity"]=objWeather.GetActivity(dict_current["day5_id"], \
                    dict_current["day5_temp_max"],dict_current["day5_temp_min"], \
                        (dict_day5["wind_speed"]*3.6), \
                            dict_current["day5_dew_point"],100,"00:00",0)
            dict_current["day5_icon"]= objWeather.GetIconFile(dict_day5["weather"][0]["icon"])   

            # Day 6
            dict_daily=dict_weather["daily"]
            dict_day6=dict_daily[6]
            dict_current["day6_name"]=objWeather.UnixTimeToLocal(dict_day6["dt"]).strftime("%A")
            dict_current["day6_sunrise"] = objWeather.UnixTimeToLocal(dict_day6["sunrise"]).strftime("%H:%M")
            dict_current["day6_sunset"] = objWeather.UnixTimeToLocal(dict_day6["sunset"]).strftime("%H:%M")
            dict_current["day6_temp_max"]=round(dict_day6["temp"]["max"])
            dict_current["day6_temp_min"]=round(dict_day6["temp"]["min"])
            dict_current["day6_temp_mor"]=round(dict_day6["temp"]["morn"])
            dict_current["day6_temp_day"]=round(dict_day6["temp"]["day"])
            dict_current["day6_temp_eve"]=round(dict_day6["temp"]["eve"])
            dict_current["day6_temp_night"]=round(dict_day6["temp"]["night"])
            dict_current["day6_feels_mor"]=round(dict_day6["feels_like"]["morn"])
            dict_current["day6_feels_day"]=round(dict_day6["feels_like"]["day"])
            dict_current["day6_feels_eve"]=round(dict_day6["feels_like"]["eve"])
            dict_current["day6_feels_night"]=round(dict_day6["feels_like"]["night"])
            dict_current["day6_dew_point"]=round(dict_day6["dew_point"])
            dict_current["day6_pressure"]=str(dict_day6["pressure"]) + " hPa"
            dict_current["day6_humidity"]=str(dict_day6["humidity"]) + " %"
            dict_current["day6_wind_speed"]=str(round(dict_day6["wind_speed"]*3.6))+ " KM/H"
            dict_current["day6_id"]=dict_day6["weather"][0]["id"]
            dict_current["day6_desc"]=objWeather.GetWeatherDesc(dict_current["day6_id"])
            dict_current["day6_activity"]=objWeather.GetActivity(dict_current["day6_id"], \
                    dict_current["day6_temp_max"],dict_current["day6_temp_min"], \
                        (dict_day6["wind_speed"]*3.6), \
                            dict_current["day6_dew_point"],100,"00:00",0)
            dict_current["day6_icon"]= objWeather.GetIconFile(dict_day6["weather"][0]["icon"])    
            
            # Day 7
            dict_daily=dict_weather["daily"]
            dict_day7=dict_daily[7]
            dict_current["day7_name"]=objWeather.UnixTimeToLocal(dict_day7["dt"]).strftime("%A")
            dict_current["day7_sunrise"] = objWeather.UnixTimeToLocal(dict_day7["sunrise"]).strftime("%H:%M")
            dict_current["day7_sunset"] = objWeather.UnixTimeToLocal(dict_day7["sunset"]).strftime("%H:%M")
            dict_current["day7_temp_max"]=round(dict_day7["temp"]["max"])
            dict_current["day7_temp_min"]=round(dict_day7["temp"]["min"])
            dict_current["day7_temp_mor"]=round(dict_day7["temp"]["morn"])
            dict_current["day7_temp_day"]=round(dict_day7["temp"]["day"])
            dict_current["day7_temp_eve"]=round(dict_day7["temp"]["eve"])
            dict_current["day7_temp_night"]=round(dict_day7["temp"]["night"])
            dict_current["day7_feels_mor"]=round(dict_day7["feels_like"]["morn"])
            dict_current["day7_feels_day"]=round(dict_day7["feels_like"]["day"])
            dict_current["day7_feels_eve"]=round(dict_day7["feels_like"]["eve"])
            dict_current["day7_feels_night"]=round(dict_day7["feels_like"]["night"])
            dict_current["day7_dew_point"]=round(dict_day7["dew_point"])
            dict_current["day7_pressure"]=str(dict_day7["pressure"]) + " hPa"
            dict_current["day7_humidity"]=str(dict_day7["humidity"]) + " %"
            dict_current["day7_wind_speed"]=str(round(dict_day7["wind_speed"]*3.6))+ " KM/H"
            dict_current["day7_id"]=dict_day7["weather"][0]["id"]
            dict_current["day7_desc"]=objWeather.GetWeatherDesc(dict_current["day7_id"])
            dict_current["day7_activity"]=objWeather.GetActivity(dict_current["day7_id"], \
                    dict_current["day7_temp_max"],dict_current["day7_temp_min"], \
                        (dict_day7["wind_speed"]*3.6), \
                            dict_current["day7_dew_point"],100,"00:00",0)
            dict_current["day7_icon"]= objWeather.GetIconFile(dict_day7["weather"][0]["icon"])       

        with open('sample_module_output/weather.json', 'w' ,encoding='utf-8' ) as fp:
            json.dump(dict_current, fp)
        return dict_current
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

    def GetActivity(self, weather_id,max_tem,min_temp,wind_speed,dew_point,visibility,sunset, CurDayFlag):
        activity_condition = True
        if wind_speed >= self.activity_main_wind_speed_threshold or \
            dew_point <= self.activity_main_dew_threshold or \
            max_tem >= self.activity_main_max_temp_threshold or \
            min_temp <= self.activity_main_min_temp_threshold :
            activity_condition= False        
        
        dict_activity={}
        if activity_condition == True:
            df=pd.read_csv("weather_conditions.csv")
            df_new=df.query('ID=='+str(weather_id))
            Activity=''
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            for item in df_new["Jogging"].values:
                Activity={"Jogging":1}
                if CurDayFlag==1:
                    if current_time < sunset or \
                        str((datetime.datetime.strptime(current_time,"%H:%M")- \
                        datetime.datetime.strptime(sunset,"%H:%M")).seconds) \
                            < str(self.activity_min_jogging_offset_seconds_threshold)  :
                            #Activity = 'Nice Weather for Jogging and Walking '
                            Activity={"Jogging":1}
                    else:
                        #Activity = 'Stay at home'
                        Activity={"Jogging":0}
                else:
                    #Activity = 'Nice Weather for Jogging and Walking '
                    Activity={"jogging":1}
                dict_activity.update(Activity)
                    
            for item in df_new["Drone"].values:
                Activity={"Drone":0}
                if item == 'YES' and min_temp > self.activity_drone_min_temp_threshold and \
                    wind_speed < self.activity_drone_wind_speed_threshold and \
                    visibility > self.activity_drone_visibility_threshold :
                    if CurDayFlag == 1 and  sunset > current_time:
                        #Activity += ''
                        Activity={"Drone":0}
                    else:
                        Activity={"Drone":1}
                dict_activity.update(Activity)                        
                        
            for item in df_new["Ski"].values:
                Activity={"Ski":0}
                if item == 'YES':
                    if CurDayFlag == 1 and  sunset > current_time:
                        Activity={"Ski":0}
                    else:
                        Activity={"Ski":1}
                dict_activity.update(Activity)                        

            for item in df_new["Kayaking"].values:
                Activity={"Kayaking":0}
                if item == 'YES' and wind_speed < self.activity_kayak_wind_speed_threshold and min_temp >= self.activity_kayak_min_temp_threshold:
                    if CurDayFlag == 1 and  sunset > current_time:
                        Activity={"Kayaking":0}
                    else:
                        Activity={"Kayaking":1}
                dict_activity.update(Activity)      

            for item in df_new["BBQ"].values:
                Activity={"BBQ":0}
                if item == 'YES' and min_temp >= self.activity_BBQ_min_temp_threshold:
                    if CurDayFlag == 1 and  sunset > current_time:
                        Activity={"BBQ":0}
                    else:
                        Activity={"BBQ":1}
                dict_activity.update(Activity) 
                
                        
            for item in df_new["Biking"].values:
                Activity={"Biking":0}
                if item == 'YES' and min_temp >= self.activity_BIKE_min_temp_threshold:
                    if CurDayFlag == 1 and  sunset > current_time:
                        Activity={"Biking":0}
                    else:
                        Activity={"Biking":1}
                dict_activity.update(Activity)                      
        #print(dict_activity)                       
        #print((datetime.datetime.strptime(current_time,"%H:%M")-datetime.datetime.strptime(sunset,"%H:%M")).seconds)         
        return dict_activity
    
a=Weather()
a.WeatherInf()