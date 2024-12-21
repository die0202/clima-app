from django.shortcuts import render
import requests
import datetime




# Create your views here.
def index(request):
    """API_KEY= open("D:\\proyects\\clima\\weather_project\\weather_project\\api_key.txt","r").read()"""
    API_KEY = "a2670893d35b4b5a0c38928a5d3da4fe"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method =="POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2',None)
        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1":daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2":daily_forecasts2,
        }
        return render(request, "weather_app/index.html", context)

    else:
        return render(request, "weather_app/index.html")
    


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    
    if 'coord' not in response:
        raise ValueError(f"Error fetching weather for city '{city}'. Response: {response}")
    
    # Procesar los datos del clima actual
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }
    
    # Obtener el pronóstico con el endpoint alternativo
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}"
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    if 'list' not in forecast_response:
        raise ValueError(f"'list' data not found in forecast response for city '{city}'. Response: {forecast_response}")
    
    # Procesar el pronóstico diario
    daily_forecasts = []
    for forecast in forecast_response['list'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(forecast['dt']).strftime("%A"),
            "min_temp": round(forecast['main']['temp_min'] - 273.15, 2),
            "max_temp": round(forecast['main']['temp_max'] - 273.15, 2),
            "description": forecast['weather'][0]['description'],
            "icon": forecast['weather'][0]['icon']
        })

    return weather_data, daily_forecasts




"""
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response=requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat,lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature":round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    daily_forecasts=[]
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['temp']['min']- 273.15, 2),
            "max_temp": round(daily_data['temp']['max']- 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })

    return weather_data, daily_forecasts

    """


    
