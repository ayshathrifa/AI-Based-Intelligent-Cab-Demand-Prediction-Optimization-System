import requests

def get_weather(city='default'):
    # Replace with real API key: https://openweathermap.org/api
    API_KEY = 'YOUR_OPENWEATHER_API_KEY'
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        res = requests.get(url, timeout=5)
        data = res.json()
        return {
            'condition': data['weather'][0]['main'].lower(),
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    except Exception:
        return {'condition': 'clear', 'temperature': 28, 'description': 'Clear sky'}
