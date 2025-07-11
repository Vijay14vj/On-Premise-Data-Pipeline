CREATE DATABASE IF NOT EXISTS weather;
USE weather;

CREATE EXTERNAL TABLE IF NOT EXISTS final_weather_table (
    city STRING,
    timestamp TIMESTAMP,
    user_reported_temp FLOAT,
    sensor_temp FLOAT,
    user_reported_humidity FLOAT,
    sensor_humidity FLOAT,
    rain_mm FLOAT,
    sensor_id STRING,
    temp_diff FLOAT,
    humidity_diff FLOAT,
    date DATE
)
STORED AS PARQUET
LOCATION '/user/hive/warehouse/weather.db/final_weather_table';