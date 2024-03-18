-- Create the keyspace
CREATE KEYSPACE IF NOT EXISTS weather_data
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}; --change replication facto when you have more machines in the cluster

-- Use the keyspace
USE weather_data;

-- Create the table for actual weather data
CREATE TABLE IF NOT EXISTS actual_weather (
    run_id text,
    id text,
    city_ascii text,
    country text,
    date timestamp,
    temperature_2m double,
    pressure_msl double,
    windspeed_10m double,
    relativehumidity_2m double,
    PRIMARY KEY (id, date)
);

-- Create the table for forecast data
CREATE TABLE IF NOT EXISTS forecast_weather (
    run_id text,
    id text,
    city_ascii text,
    country text,
    date timestamp,
    temperature_2m double,
    pressure_msl double,
    windspeed_10m double,
    relativehumidity_2m double,
    PRIMARY KEY (id, date)
);
