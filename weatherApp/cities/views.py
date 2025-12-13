from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from .models import City

# Create your views here.
def cities(request):
    url = 'http://api.weatherapi.com/v1/current.json?key=7773446b649e406e80d123250251312&q={}&aqi=no'
    weather_info = []

    myCities = City.objects.values('cityName')

    for city in myCities:

        
        get_city_weather = requests.get(url.format(city)).json()
        
        weather_info.append(get_city_weather)


    for city in weather_info:
        print(city)

    template = loader.get_template('mainPage.html')
    context = {
        'weatherInfo': weather_info,
    }
    
    return HttpResponse(template.render(context, request))