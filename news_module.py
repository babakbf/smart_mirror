# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 21:00:28 2021

@author: Babak Boroujerdi Far
"""
import feedparser
import requests, json 
import pandas as pd


class News():

    def __init__(self):
        self.number_of_rows_defult=5

    def GetNewsUrl(self,NewsType):
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
        elif NewsType=='T': # Technology Science
            url_news='https://www.sciencedaily.com/rss/all.xml'
        elif NewsType=='S': # Technology Science
            url_news='http://feeds.feedburner.com/BreakingScienceNews?format=xml'
        elif NewsType=='TE': # Technology Science
            url_news='https://www.sciencedaily.com/rss/top/technology.xml'
        return url_news
    

#url_radiofarda='https://www.radiofarda.com/api/zrttpoeuoupo'
#url_cbc_world='https://www.cbc.ca/cmlink/rss-world'
    
    def GetTopNews(self,NewsType,NumberofRows):
        objNews = News()
        url = objNews.GetNewsUrl(NewsType)
        dict_news = feedparser.parse(url)
        #
        j=5
        title_new_list = []
        if len(dict_news)<5:
            j=len(dict_news)
            
        for i in range(0, j):
            title = dict_news['entries'][i]["title"]
            title_new = title
            #if(len(title) >= 50):
            #    title_new += title[:50] + '-\n' + title[50:]
            
            title_new_list.append(title_new)       
        print(title_new_list)
        return title_new_list
    
a=News()
a.GetTopNews('TE',5)