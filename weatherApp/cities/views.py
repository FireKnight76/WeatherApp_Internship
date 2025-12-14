from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import requests
from .models import City

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
    
    #checks the current value of the select tag on the mainPage
    if request.method == "POST":
        selected_city = request.POST.get('city_list')
        if selected_city:
            city = selected_city


    #list that checks which cities have been added by the user
    my_cities = City.objects.values_list('cityName',flat=True)

    #checks if the user requests a specific date
    if request.method == "POST" and "view_date" in request.POST:
        #saves the selected date as a string to put into the url
        weather_date = str(request.POST.get('city_date'))
        #the url for historical data that overwrites the original url to get the desired data
        url = 'http://api.weatherapi.com/v1/history.json?key=7773446b649e406e80d123250251312&q={}&dt={}'
        
        #requests the data from the api, and inserts the desired locations
        city_status = requests.get(url.format(city, weather_date)).json()

        #the created object to fit with the returned data regarding the city's past weather conditions
        weather_info   = {
            'city': city_status['location']['name'],
            'date': city_status['forecast']['forecastday'][0]['date'],
            'maxtemp_c': city_status['forecast']['forecastday'][0]['day']['maxtemp_c'],
            'mintemp_c': city_status['forecast']['forecastday'][0]['day']['mintemp_c'],
            'mode': 'history'
        }
    else:
        city_status = requests.get(url.format(city)).json()
        
        #the created object to fit with the returned data regarding the city's current weather conditions
        weather_info   = {
            'city': city_status['location']['name'],
            'time': city_status['location']['localtime'],
            'temp_c': city_status['current']['temp_c'],
            'mode': 'current'
        }

    template = loader.get_template('mainPage.html')
    #saves the list and object for the mainPage to use
    context = {
        'my_cities': my_cities,
        'weather_info': weather_info,
    }

    return HttpResponse(template.render(context, request))