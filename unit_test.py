#import weather_module as w
import news_module as n
import calendar_module as g

#objWeather=w.Weather()
#a=objWeather.WeatherInf()
#print ("\n---------------Weather Dictionary----------------------")
#print(a)
#objnews=n.News()
#b=objnews.GetTopNews('B',5)
#print ("\n---------------News Dictionary----------------------")
#print(b)
objCalendar=g.Calendar()
c=objCalendar.GetCalendarEvents(5)
print ("\n---------------Calendar Dictionary----------------------")
print(c["event1"])
