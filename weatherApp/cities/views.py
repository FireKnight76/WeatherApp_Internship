from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import City

# Create your views here.
def cities(request):
    myCities = City.objects.all().values()
    template = loader.get_template('mainPage.html')
    context = {
        'myCities': myCities,
    }
    return HttpResponse(template.render(context, request))