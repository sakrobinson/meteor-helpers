import requests
import pandas as pd
from datetime import datetime, timedelta

class GetWeatherForecast:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cities_df = pd.read_csv(self.file_path)

    def get_weather_data(self, lat, lon, start_date, end_date):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,pressure_msl,windspeed_10m,relativehumidity_2m",
            "start": start_date,
            "end": end_date,
            "timezone": "auto"  # Handle timezone automatically
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            # Add city information to the weather data
            weather_data['id'] = self.cities_df.id
            weather_data['city_ascii'] = self.cities_df.city_ascii
            weather_data['country'] = self.cities_df.country
            return weather_data
        else:
            return None

    def get_forecasts(self, start_date, end_date):
        forecasts = []
        for index, row in self.cities_df.iterrows():
            forecast = self.get_weather_data(row['lat'], row['lng'], start_date, end_date)
            if forecast:
                forecasts.append(forecast)
            else:
                print(f"Failed to return forecast for {row['lat']}, {row['lng']}")
        return forecasts

    # Additional method to calculate the start and end dates for the forecast
    def calculate_forecast_dates(self, days_ahead):
        start_date = datetime.now() + timedelta(days=days_ahead)
        end_date = start_date + timedelta(days=2)
        return start_date.strftime("%Y-%m-%dT00:00"), end_date.strftime("%Y-%m-%dT00:00")

    # Additional method to calculate the start and end dates for the history
    def calculate_history_dates(self):
        yesterday = datetime.now() - timedelta(days=1)
        start_date = yesterday.strftime("%Y-%m-%dT00:00")
        end_date = yesterday.strftime("%Y-%m-%dT23:59")
        return start_date, end_date
    

class GetWeatherHistory(GetWeatherForecast):
    def get_actuals(self):
        actuals = []
        start_date, end_date = self.calculate_history_dates()
        for index, row in self.cities_df.iterrows():
            actual = self.get_weather_data(row['lat'], row['lng'], start_date, end_date)
            if actual:
                actual['id'] = row['id']
                actual['city_ascii'] = row['city_ascii']
                actual['country'] = row['country']
                actuals.append(actual)
        return actuals