from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import requests
from .models import City
from datetime import date

# Create your views here.
def cities(request):
    #the link with my api key to access the weather api
    url = 'http://api.weatherapi.com/v1/current.json?key=7773446b649e406e80d123250251312&q={}'
    city = "Almere"

    #method for adding cities
    if request.method == "POST" and "add_city" in request.POST:
        city_name = request.POST.get("city")
        if city_name:
            City.objects.get_or_create(cityName=city_name)
        return redirect("cities")
    

    if request.method == "POST":
        selected_city = request.POST.get('city_list')
        if selected_city:
            city = selected_city


    myCities = City.objects.values_list('cityName',flat=True)

    
    if request.method == "POST" and "view_date" in request.POST:
        weather_date = str(request.POST.get('city_date'))
        url = 'http://api.weatherapi.com/v1/history.json?key=7773446b649e406e80d123250251312&q={}&dt={}'
        
        #requests the data from the api, and inserts the desired locations
        city_status = requests.get(url.format(city, weather_date)).json()

        weather_info   = {
            'city': city_status['location']['name'],
            'date': city_status['forecast']['forecastday'][0]['date'],
            'maxtemp_c': city_status['forecast']['forecastday'][0]['day']['maxtemp_c'],
            'mintemp_c': city_status['forecast']['forecastday'][0]['day']['mintemp_c'],
            'mode': 'history'
        }
    else:
        city_status = requests.get(url.format(city)).json()
        
        weather_info   = {
            'city': city_status['location']['name'],
            'time': city_status['location']['localtime'],
            'temp_c': city_status['current']['temp_c'],
            'mode': 'current'
        }


    


    template = loader.get_template('mainPage.html')
    context = {
        'myCities': myCities,
        'weather_info': weather_info,
    }

    print(city_status)

    return HttpResponse(template.render(context, request))