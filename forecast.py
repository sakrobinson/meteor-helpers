import requests
import pandas as pd
from datetime import datetime, timedelta

class GetWeatherForecast:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cities_df = pd.read_csv(self.file_path)

    def get_weather_data(self, lat, lon, start_date, end_date, city_id, city_name, country):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,pressure_msl,windspeed_10m,relativehumidity_2m",
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "auto"  # Handle timezone automatically
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            # Add city information to the weather data
            weather_data['id'] = city_id
            weather_data['city_ascii'] = city_name
            weather_data['country'] = country
            weather_data['lat'] = lat  # Ensure this line is present
            weather_data['lon'] = lon  # Ensure this line is present
            return weather_data
        else:
            return None

    def get_forecasts(self, start_date, end_date):
        forecasts = []
        for index, row in self.cities_df.iterrows():
            forecast = self.get_weather_data(
                lat=row['lat'],
                lon=row['lng'],
                start_date=start_date,
                end_date=end_date,
                city_id=row['id'],
                city_name=row['city_ascii'],
                country=row['country']
            )
            if forecast:
                forecasts.append(forecast)
            else:
                print(f"Failed to return forecast for {row['city_ascii']}")
        return forecasts

    # Additional method to calculate the start and end dates for the forecast
    def calculate_forecast_dates(self, days_ahead):
        start_date = datetime.now() + timedelta(days=days_ahead)
        end_date = start_date + timedelta(days=2)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    # Additional method to calculate the start and end dates for the history
    def calculate_history_dates(self, days_back=1):
        target_date = datetime.now() - timedelta(days=days_back)
        start_date = target_date.strftime("%Y-%m-%d")
        end_date = target_date.strftime("%Y-%m-%d")
        return start_date, end_date
    

class GetWeatherHistory(GetWeatherForecast):
    def get_actuals(self, days_back):
        actuals = []
        start_date, end_date = self.calculate_history_dates(days_back)
        for index, row in self.cities_df.iterrows():
            actual = self.get_weather_data(
                lat=row['lat'],
                lon=row['lng'],
                start_date=start_date,
                end_date=end_date,
                city_id=row['id'],
                city_name=row['city_ascii'],
                country=row['country']
            )
            if actual:
                actuals.append(actual)
        return actuals