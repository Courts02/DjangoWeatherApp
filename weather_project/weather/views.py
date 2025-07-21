import requests
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .forms import CityForm
from .models import WeatherSearch

def get_weather_data(city):
    """Fetch weather data from OpenWeather API"""
    try:
        api_key = settings.OPENWEATHER_API_KEY
        base_url = settings.OPENWEATHER_BASE_URL
        
        # Construct API URL
        url = f"{base_url}?q={city}&appid={api_key}&units=metric"
        
        # Make API request
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None

def index(request):
    """Main view for weather search"""
    form = CityForm()
    weather_data = None
    recent_searches = WeatherSearch.objects.all()[:5]
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            
            # Get weather data from API
            api_data = get_weather_data(city)
            
            if api_data and api_data.get('cod') == 200:
                # Extract relevant data
                weather_data = {
                    'city': api_data['name'],
                    'country': api_data['sys']['country'],
                    'temperature': round(api_data['main']['temp']),
                    'description': api_data['weather'][0]['description'].title(),
                    'icon': api_data['weather'][0]['icon'],
                    'humidity': api_data['main']['humidity'],
                    'pressure': api_data['main']['pressure'],
                    'wind_speed': api_data['wind']['speed'],
                    'feels_like': round(api_data['main']['feels_like']),
                    'temp_min': round(api_data['main']['temp_min']),
                    'temp_max': round(api_data['main']['temp_max']),
                }
                
                # Save to database
                WeatherSearch.objects.create(
                    city=weather_data['city'],
                    country=weather_data['country'],
                    temperature=weather_data['temperature'],
                    description=weather_data['description'],
                    humidity=weather_data['humidity'],
                    pressure=weather_data['pressure'],
                    wind_speed=weather_data['wind_speed']
                )
                
                messages.success(request, f"Weather data for {weather_data['city']} retrieved successfully!")
                
            else:
                error_msg = "City not found. Please check the spelling and try again."
                if api_data and 'message' in api_data:
                    error_msg = api_data['message'].title()
                messages.error(request, error_msg)
                form = CityForm()  # Clear form on error
    
    context = {
        'form': form,
        'weather_data': weather_data,
        'recent_searches': recent_searches,
    }
    
    return render(request, 'weather/index.html', context)

def weather_history(request):
    """View for displaying weather search history"""
    searches = WeatherSearch.objects.all()[:20]
    return render(request, 'weather/history.html', {'searches': searches})

def api_weather(request, city):
    """JSON API endpoint for weather data"""
    api_data = get_weather_data(city)
    
    if api_data and api_data.get('cod') == 200:
        weather_data = {
            'city': api_data['name'],
            'country': api_data['sys']['country'],
            'temperature': round(api_data['main']['temp']),
            'description': api_data['weather'][0]['description'].title(),
            'humidity': api_data['main']['humidity'],
            'pressure': api_data['main']['pressure'],
            'wind_speed': api_data['wind']['speed'],
        }
        return JsonResponse({'success': True, 'data': weather_data})
    else:
        return JsonResponse({'success': False, 'error': 'City not found'})