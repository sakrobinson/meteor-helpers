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
    hourly_data = actual['hourly']
    times = hourly_data['time']
    
    for time_point in times:
        index = times.index(time_point)
        session.execute(insert_actual, (
            run_id,
            str(actual['id']),  # Convert ID to string if necessary
            actual['city_ascii'],
            actual['country'],
            datetime.strptime(time_point, "%Y-%m-%dT%H:%M"),  # Convert time to datetime object
            hourly_data['temperature_2m'][index],
            hourly_data['pressure_msl'][index],
            hourly_data['windspeed_10m'][index],
            hourly_data['relativehumidity_2m'][index]
        ))

for forecast in forecasts:
    city_ids = forecast['id'].tolist()  # Convert pandas Series to list
    city_names = forecast['city_ascii'].tolist()  # Convert pandas Series to list
    countries = forecast['country'].tolist()  # Convert pandas Series to list
    hourly_data = forecast['hourly']
    times = hourly_data['time']
    
    for i, time_point in enumerate(times):
        for j, city_id in enumerate(city_ids):
            session.execute(insert_forecast, (
                run_id,
                str(city_id),  # Ensure the ID is a string
                city_names[j],
                countries[j],
                datetime.strptime(time_point, "%Y-%m-%dT%H:%M"),  # Convert time to datetime object
                hourly_data['temperature_2m'][i],
                hourly_data['pressure_msl'][i],
                hourly_data['windspeed_10m'][i],
                hourly_data['relativehumidity_2m'][i]
            ))

# Close the connection
cluster.shutdown()