import mysql.connector
from faker import Faker
import time
from datetime import datetime

fake = Faker()

# MySQL configuration
MYSQL_CONFIG = {
    'host': 'mysql',
    'user': 'weather_user',
    'password': 'weather_pass',
    'database': 'weather_db'
}


def create_table():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sensor_id VARCHAR(50) NOT NULL,
            location VARCHAR(100) NOT NULL,
            timestamp DATETIME NOT NULL,
            temp_celsius FLOAT NOT NULL,
            humidity_percent FLOAT NOT NULL,
            rain_mm FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("Created sensor_data table if not exists")

    except Exception as e:
        print(f"Error creating table: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def load_mock_data_to_mysql():
    create_table()

    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        for _ in range(50):  # Insert 50 records per run
            sensor_data = {
                'sensor_id': fake.uuid4(),
                'location': fake.city(),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'temp_celsius': fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=-10, max_value=40),
                'humidity_percent': fake.pyint(min_value=0, max_value=100),
                'rain_mm': fake.pyfloat(right_digits=2, positive=True, max_value=50)
            }

            cursor.execute("""
            INSERT INTO sensor_data (sensor_id, location, timestamp, temp_celsius, humidity_percent, rain_mm)
            VALUES (%(sensor_id)s, %(location)s, %(timestamp)s, %(temp_celsius)s, %(humidity_percent)s, %(rain_mm)s)
            """, sensor_data)

        conn.commit()
        print(f"Inserted {cursor.rowcount} records into sensor_data table")

    except Exception as e:
        print(f"Error inserting data: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    while True:
        load_mock_data_to_mysql()
        time.sleep(60)  # Insert data every minute