CREATE DATABASE IF NOT EXISTS weather_db;

USE weather_db;

CREATE TABLE IF NOT EXISTS final_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    user_reported_temp FLOAT NOT NULL,
    sensor_temp FLOAT NOT NULL,
    user_reported_humidity FLOAT NOT NULL,
    sensor_humidity FLOAT NOT NULL,
    rain_mm FLOAT NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    temp_diff FLOAT NOT NULL,
    humidity_diff FLOAT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);