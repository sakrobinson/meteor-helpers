from cassandra.cluster import Cluster
from get_actual import GetWeatherHistory
from get_forecast import GetWeatherForecast
import uuid
from datetime import datetime

# Connect to Cassandra
cluster = Cluster(['172.17.0.2']) # Cassandra Node 1 Server
session = cluster.connect('weather_data')

# Fetch data
file_path = 'worldcities_sample.csv'
w_forecast = GetWeatherForecast(file_path)
w_actual = GetWeatherHistory(file_path)
forecasts = w_forecast.get_forecasts()
actuals = w_actual.get_yesterdays_weather()

# Generate a unique run_id with a date prefix in the format YYYYMMDD
date_prefix = datetime.now().strftime("%Y%m%d")
run_id = f"{date_prefix}_{uuid.uuid4().int}"  # Example: '20230101_12345678901234567890'

# Insert data into Cassandra
insert_actual = session.prepare("""
    INSERT INTO actual_weather (run_id, id, city_ascii, country, date, temperature_2m, pressure_msl, windspeed_10m, relativehumidity_2m)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""")
insert_forecast = session.prepare("""
    INSERT INTO forecast_weather (run_id, id, city_ascii, country, date, temperature_2m, pressure_msl, windspeed_10m, relativehumidity_2m)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""")

for actual in actuals:
    # Assuming 'actual' is a dictionary with keys corresponding to the column names
    session.execute(insert_actual, (
        run_id,
        actual['id'],
        actual['city_ascii'],
        actual['country'],
        actual['date'],
        actual['temperature_2m'],
        actual['pressure_msl'],
        actual['windspeed_10m'],
        actual['relativehumidity_2m'],
        run_id
    ))

for forecast in forecasts:
    # Assuming 'forecast' is a dictionary with keys corresponding to the column names
    session.execute(insert_forecast, (
        run_id,
        forecast['id'],
        forecast['city_ascii'],
        forecast['country'],
        forecast['date'],
        forecast['temperature_2m'],
        forecast['pressure_msl'],
        forecast['windspeed_10m'],
        forecast['relativehumidity_2m'],
        run_id
    ))

# Close the connection
cluster.shutdown()