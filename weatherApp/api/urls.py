from django.urls import path
from . import views

urlpatterns = [
    path('citylist/', views.getData),
    path('add/', views.addCity)
]