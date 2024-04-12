from cassandra.cluster import Cluster
from forecast import GetWeatherForecast
from forecast import GetWeatherHistory
import uuid
from datetime import datetime

# Connect to Cassandra
cluster = Cluster(['172.17.0.2']) # Cassandra Node 1 Server
session = cluster.connect('weather_data')

# Fetch data
file_path = 'worldcities_sample.csv'
w_forecast = GetWeatherForecast(file_path)
w_actual = GetWeatherHistory(file_path)
start_date, end_date = w_forecast.calculate_forecast_dates(days_ahead=1)
forecasts = w_forecast.get_forecasts(start_date, end_date)
actuals = w_actual.get_actuals(days_back =1)
#breakpoint()
# Generate a unique run_id with a date prefix in the format YYYYMMDD
date_prefix = datetime.now().strftime("%Y%m%d")
run_id = f"{date_prefix}_{uuid.uuid4().int}"  # Example: '20230101_12345678901234567890'
print(run_id)
# Insert data into Cassandra
insert_actual = session.prepare("""
    INSERT INTO actual_weather (run_id, id, city_ascii, country, date, 
    temperature_2m, pressure_msl, windspeed_10m, relativehumidity_2m, lon, lat, day, month, year)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""")
insert_forecast = session.prepare("""
    INSERT INTO forecast_weather (run_id, id, city_ascii, country, date, 
    temperature_2m, pressure_msl, windspeed_10m, relativehumidity_2m, lon, lat, day, month, year)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""")
# Define the new insert statement for the combined data
insert_combined = session.prepare("""
    INSERT INTO weather_data_combined (date, lat, lon, city_ascii, country, 
    data_type, temperature_2m, pressure_msl, windspeed_10m, relativehumidity_2m)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""")
print('Generating actuals...')
for actual in actuals:
    hourly_data = actual['hourly']
    times = hourly_data['time']
    
    for time_point in times:
        index = times.index(time_point)
        date_object = datetime.strptime(time_point, "%Y-%m-%dT%H:%M")
        session.execute(insert_actual, (
            run_id,
            str(actual['id']),
            actual['city_ascii'],
            actual['country'],
            date_object,
            hourly_data['temperature_2m'][index],
            hourly_data['pressure_msl'][index],
            hourly_data['windspeed_10m'][index],
            hourly_data['relativehumidity_2m'][index],
            actual['lon'],
            actual['lat'],
            date_object.day,
            date_object.month,
            date_object.year
            ))
        session.execute(insert_combined, (
            date_object,
            actual['lat'],
            actual['lon'],
            actual['city_ascii'],
            actual['country'],
            'actual',  # data_type is 'actual' for actual weather data
            actual['temperature_2m'],
            actual['pressure_msl'],
            actual['windspeed_10m'],
            actual['relativehumidity_2m']
        ))

print('Generating forecasts...')
for forecast in forecasts:
    city_id = str(forecast['id'])  # Convert ID to string if necessary
    city_name = forecast['city_ascii']
    country = forecast['country']
    hourly_data = forecast['hourly']
    times = hourly_data['time']
    print(f"Generating forecast for: {city_name}")  # Log statement for PM2
    
    for index, time_point in enumerate(times):
        
            datetime_object = datetime.strptime(time_point, "%Y-%m-%dT%H:%M")
            session.execute(insert_forecast, (
                run_id,
                city_id,
                city_name,
                country,
                datetime_object,
                hourly_data['temperature_2m'][index],
                hourly_data['pressure_msl'][index],
                hourly_data['windspeed_10m'][index],
                hourly_data['relativehumidity_2m'][index],
                forecast['lon'],
                forecast['lat'],
                datetime_object.day,
                datetime_object.month,
                datetime_object.year
            ))
            session.execute(insert_combined, (
                date_object,
                forecast['lat'],
                forecast['lon'],
                forecast['city_ascii'],
                forecast['country'],
                'forecast',  # data_type is 'forecast' for forecast weather data
                hourly_data['temperature_2m'][index],  # Access the temperature using the index
                hourly_data['pressure_msl'][index],    # Access the pressure using the index
                hourly_data['windspeed_10m'][index],   # Access the windspeed using the index
                hourly_data['relativehumidity_2m'][index]  # Access the humidity using the index
            ))
print("Done")
# Close the connection
cluster.shutdown()