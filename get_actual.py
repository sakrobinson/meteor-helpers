import requests
import pandas as pd
from datetime import datetime, timedelta
from get_forecast import GetWeatherForecast

class GetWeatherHistory(GetWeatherForecast):
    def fetch_weather_history(self, lat, lon):
        # Calculate yesterday's date
        yesterday = datetime.now() - timedelta(days=1)
        start_date = yesterday.strftime("%Y-%m-%dT00:00")
        end_date = yesterday.strftime("%Y-%m-%dT23:59")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,pressure_msl,windspeed_10m,relativehumidity_2m",
            "start": start_date,
            "end": end_date,
            "timezone": "auto"  # Ensure the timezone is handled correctly - local timezones used throughout
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_yesterdays_weather(self):
        weather_data = []
        for index, row in self.cities_df.iterrows():
            history = self.fetch_weather_history(row['lat'], row['lng'])
            if history:
                weather_data.append(history)
            else:
                print(f"Failed to get history for {row['lat']}, {row['lng']}")
        return weather_data
