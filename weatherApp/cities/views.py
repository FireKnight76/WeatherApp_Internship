from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from .models import City

# Create your views here.
def cities(request):
    url = 'http://api.weatherapi.com/v1/current.json?key=7773446b649e406e80d123250251312&q={}&aqi=no'
    weather_info = []

    myCities = City.objects.values_list('cityName',flat=True)

    for city in myCities:

        city_status = requests.get(url.format(city)).json()

        situation   = {
            'city': city,
            'time': city_status['location']['localtime'],
            'temp_c': city_status['current']['temp_c'],
        }

        weather_info.append(situation)


    # for city in weather_info:
    #     print(city)

    template = loader.get_template('mainPage.html')
    context = {
        'weather_info': weather_info,
    }

    return HttpResponse(template.render(context, request))
    #return render(request, 'mainPage.html', context)