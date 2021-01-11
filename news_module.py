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


class News(NewsType,NumberOfRows):

    def __init__(self):
        self.number_of_rows_defult=5

    def GetNews(self,NewsType):
        # News Type T: Technology Science BI:BBC Persian Iran  R: Radio Farda CW: 
        #    CBC World  CC: CBC CANADA   B: BBC Perisan
        
        if NewsType=='BI': # BBC Persian Iran
            url_news='http://www.bbc.co.uk/persian/iran/full.xml'
        elif NewsType=='B': # BBC Perisan
            url_news='http://www.bbc.co.uk/persian/index.xml'
        elif NewsType=='BE': # BBC English
            url_news='http://feeds.bbci.co.uk/news/rss.xml?edition=us'
        elif NewsType=='R': # Radio Farda (Perisan)
            url_news='https://www.radiofarda.com/api/zrttpoeuoupo'
        elif NewsType=='CW': # CBC World (English)
            url_news='https://www.cbc.ca/cmlink/rss-world'
        elif NewsType=='CW': # Radio Farda (Perisan)
            url_news='https://www.cbc.ca/cmlink/rss-canada'
        else: # Current
            # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
            url=self.base_url+"weather?lat={lat}&lon={lon}&appid={API_key}&units={units}".format(lat=self.latitude,lon=self.longitude(), API_key=self.openweathermap_appkey,units=self.units)
        return url
    

url_radiofarda='https://www.radiofarda.com/api/zrttpoeuoupo'
url_cbc_world='https://www.cbc.ca/cmlink/rss-world'
    
    def GetTopNews(self):
            dict_iran = feedparser.parse(url_radiofarda)
        #
        j=5
        title_new_list = []
        if len(dict_iran)<5:
            j=len(dict_iran)
            
        for i in range(0, j):
            title = dict_iran['entries'][i]["title"]
            title_new = title
            #if(len(title) >= 50):
            #    title_new += title[:50] + '-\n' + title[50:]
            
            title_new_list.append(title_new)       
        
        return dict_activity
    
a=Weather()
a.WeatherInf()