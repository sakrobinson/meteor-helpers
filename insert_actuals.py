from cassandra.cluster import Cluster
from forecast import GetWeatherHistory
from datetime import datetime
import uuid

# days back
actual_days = 4

# Connect to Cassandra
cluster = Cluster(['172.17.0.2'])  # Adjust IP as needed
session = cluster.connect('weather_data')

# Fetch data
file_path = 'worldcities_sample.csv'
w_actual = GetWeatherHistory(file_path)

# Calculate dates for the last 10 days
start_date, end_date = w_actual.calculate_history_dates(days_back=10)

# Fetch historical data for the last n days
actuals = w_actual.get_actuals(days_back=actual_days)

# Generate a unique run_id
date_prefix = datetime.now().strftime("%Y%m%d")
run_id = f"{date_prefix}_{uuid.uuid4().int}"

# Prepare the insert statement
insert_actual = session.prepare("""
    INSERT INTO actual_weather (run_id, id, city_ascii, country, date, temperature_2m, pressure_msl, windspeed_10m, relativehumidity_2m)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""")

# Insert data into Cassandra
for actual in actuals:
    hourly_data = actual['hourly']
    times = hourly_data['time']
    
    for time_point in times:
        index = times.index(time_point)
        session.execute(insert_actual, (
            run_id,
            str(actual['id']),
            actual['city_ascii'],
            actual['country'],
            datetime.strptime(time_point, "%Y-%m-%dT%H:%M"),
            hourly_data['temperature_2m'][index],
            hourly_data['pressure_msl'][index],
            hourly_data['windspeed_10m'][index],
            hourly_data['relativehumidity_2m'][index]
        ))

# Close the connection
cluster.shutdown()