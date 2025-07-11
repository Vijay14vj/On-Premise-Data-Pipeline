from faker import Faker
import csv
import os
from datetime import datetime
import time

fake = Faker()

CSV_DIR = '/opt/airflow/data/csv'
os.makedirs(CSV_DIR, exist_ok=True)


def generate_fake_csv():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(CSV_DIR, f'weather_logs_{timestamp}.csv')

    fieldnames = ['name', 'city', 'temperature', 'humidity', 'timestamp']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(100):  # Generate 100 records per file
            writer.writerow({
                'name': fake.name(),
                'city': fake.city(),
                'temperature': fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=-10, max_value=40),
                'humidity': fake.pyint(min_value=0, max_value=100),
                'timestamp': datetime.now().isoformat()
            })

    print(f"Generated fake weather logs CSV: {filename}")


if __name__ == "__main__":
    while True:
        generate_fake_csv()
        time.sleep(60)  # Generate every minute