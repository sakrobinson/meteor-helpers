import matplotlib.pyplot as plt
from get_forecast import GetWeatherForecast
from get_actual import GetWeatherHistory

# Function to plot forecast and historical data for all locations
def plot_forecasts_and_history(forecasts, history, cities_df):
    variables = ['temperature_2m', 'pressure_msl', 'windspeed_10m', 'relativehumidity_2m']
    
    # Create a plot for each variable
    for variable in variables:
        plt.figure()
        
        # Plot each location's forecast and history in the same figure
        for forecast, historical, (_, row) in zip(forecasts, history, cities_df.iterrows()):
            hourly_forecast = forecast.get('hourly', {})
            hourly_history = historical.get('hourly', {})
            time_forecast = hourly_forecast.get('time', [])
            time_history = hourly_history.get('time', [])
            data_forecast = hourly_forecast.get(variable, [])
            data_history = hourly_history.get(variable, [])
            location_nm = row['city_ascii']  # Accessing the city name using the column header
            
            # Plot forecast with a dotted line
            plt.plot(time_forecast, data_forecast, 'b:', label=f'Forecast: {location_nm}')
            
            # Plot historical data with a solid line
            plt.plot(time_history, data_history, 'g-', label=f'Actual: {location_nm}')
        
        plt.xlabel('Time')
        plt.ylabel(variable)
        plt.title(f'Forecast vs. History for {variable}')
        plt.legend()
        plt.show()

# Instantiate the WeatherForecast and WeatherHistory
file_path = 'worldcities_sample.csv'  # Updated file path
w_forecast = GetWeatherForecast(file_path)
w_actual = GetWeatherHistory(file_path)


# Get forecasts and historical data
forecasts = w_forecast.get_forecasts()
yesterdays_weather = w_actual.get_yesterdays_weather()
breakpoint()

# Plot them
plot_forecasts_and_history(forecasts, yesterdays_weather, weather_fetcher.cities_df)