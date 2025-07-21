from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.weather_history, name='history'),
    path('api/<str:city>/', views.api_weather, name='api_weather'),
]