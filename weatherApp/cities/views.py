from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import requests
from .models import City

# Create your views here.
def cities(request):
    #the link with my api key to access the weather api
    url = 'http://api.weatherapi.com/v1/current.json?key=7773446b649e406e80d123250251312&q={}&aqi=no'
    weather_info = []

    if request.method == "POST":
        city_name = request.POST.get("city")
        if city_name:
            City.objects.get_or_create(cityName=city_name)
        return redirect("cities")

    myCities = City.objects.values_list('cityName',flat=True)

    for city in myCities:
        
        #requests the data from the api, and inserts the desired locations
        city_status = requests.get(url.format(city)).json()

        situation   = {
            'city': city,
            'time': city_status['location']['localtime'],
            'temp_c': city_status['current']['temp_c'],
        }

        weather_info.append(situation)

    template = loader.get_template('mainPage.html')
    context = {
        'weather_info': weather_info,
    }

    return HttpResponse(template.render(context, request))