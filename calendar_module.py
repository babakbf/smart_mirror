# -*- coding: utf-8 -*-
"""
Created on Tue Jan  12 06:27:28 2021

@author: Babak Boroujerdi Far
"""
import json
import os.path
import pickle
import time
import datetime
from time import strftime
# from datetime import date, timedelta, datetime, timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Calendar():

    def __init__(self):
        self.next_upcoming_weeks=2
        self.CalendarUrl = ['https://www.googleapis.com/auth/calendar.readonly']

    def GetCalendarEvents(self):
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
                    'credentials.json', self.CalendarUrl)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
            
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        nextDate = datetime.datetime.utcnow() + datetime.timedelta(weeks=+self.next_upcoming_weeks)
        nextDate= nextDate.isoformat()+ 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=nextDate,
                                              maxResults=7, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        event_list = {}
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
            while event_delta>=0:
                event[event_delta] = "event{i}".format(i=event_delta)
                eventItem[event_delta] = ""
                event_list.append("")    
                event_delta = event_delta -1               
        with open('sample_module_output/calendar.json', 'w' ,encoding='utf-8' ) as fp:
            json.dump(event_list, fp)      
        return event_list
       
# a=Calendar() 
# a.GetCalendarEvents()