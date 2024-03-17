import requests
import pandas as pd

class GetWeatherForecast:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cities_df = pd.read_csv(self.file_path)

    def fetch_weather_forecast(self, lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,pressure_msl,windspeed_10m,relativehumidity_2m",
            "start": "2024-03-16T00:00",  # Update these dates to match your forecast period
            "end": "2024-03-18T00:00"     # Update these dates to match your forecast period
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_forecasts(self):
        forecasts = []
        for index, row in self.cities_df.iterrows():
            forecast = self.fetch_weather_forecast(row['lat'], row['lng'])
            if forecast:
                forecasts.append(forecast)
            else:
                print(f"Failed to fetch forecast for {row['lat']}, {row['lng']}")
        return forecasts