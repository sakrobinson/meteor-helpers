from forecast import GetWeatherForecast, GetWeatherHistory
import pandas as pd

# Path to the CSV file
file_path = 'worldcities_sample.csv'

# Read the CSV and get the first city's data
cities_df = pd.read_csv(file_path)
first_city = cities_df.iloc[0]
latitude = first_city['lat']
longitude = first_city['lng']
id = first_city['id']
name = first_city['city_ascii'] 
country = first_city['country']


# Instantiate the classes
forecast_instance = GetWeatherForecast(file_path)
history_instance = GetWeatherHistory(file_path)

# Calculate dates for forecast and actuals
forecast_start_date, forecast_end_date = forecast_instance.calculate_forecast_dates(days_ahead=1)
actuals_start_date, actuals_end_date = history_instance.calculate_history_dates(days_back=1)


# Get forecast and actual weather data for the first city
forecast_data = forecast_instance.get_weather_data(latitude, longitude, forecast_start_date, forecast_end_date, id, name, country)
actuals_data = history_instance.get_weather_data(latitude, longitude, actuals_start_date, actuals_end_date, id, name, country)

# Print the results
print("Forecast Data for the first city:", forecast_data)
print("Actuals Data for the first city:", actuals_data)