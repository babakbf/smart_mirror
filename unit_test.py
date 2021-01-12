import weather_module as w
import news_module as n

objWeather=w.Weather()
a=objWeather.WeatherInf()
print(a)
objnews=n.News()
b=objnews.GetTopNews('BI',5)
print(b)