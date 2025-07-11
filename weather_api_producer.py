import requests
from kafka import KafkaProducer
import json
import time
import os
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'kafka:9092'
TOPIC_NAME = 'weather-topic'

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
CITIES = ['London', 'New York', 'Tokyo', 'Paris', 'Berlin', 'Moscow', 'Sydney', 'Beijing']

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def fetch_weather_data():
    for city in CITIES:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            # Transform the data
            weather_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'city': city,
                'latitude': data['coord']['lat'],
                'longitude': data['coord']['lon'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'weather_description': data['weather'][0]['description']
            }

            # Send to Kafka
            producer.send(TOPIC_NAME, value=weather_data)
            print(f"Sent weather data for {city} to Kafka")

        except Exception as e:
            print(f"Error fetching weather data for {city}: {str(e)}")

    producer.flush()


if __name__ == "__main__":
    while True:
        fetch_weather_data()
        time.sleep(60)  # Fetch data every minute