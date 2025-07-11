from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os


def main():
    spark = SparkSession.builder \
        .appName("WeatherBatchETL") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("hive.metastore.uris", "thrift://hive:9083") \
        .enableHiveSupport() \
        .getOrCreate()

    # Read latest CSV file
    csv_dir = "/opt/airflow/data/csv"
    latest_csv = sorted(os.listdir(csv_dir))[-1]
    csv_path = os.path.join(csv_dir, latest_csv)

    csv_df = spark.read.csv(csv_path, header=True, inferSchema=True)

    # Read MySQL table
    mysql_df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://mysql:3306/weather_db") \
        .option("dbtable", "sensor_data") \
        .option("user", "weather_user") \
        .option("password", "weather_pass") \
        .load()

    # Perform transformations
    # Join on city/location and timestamp (simplified for demo)
    joined_df = csv_df.join(
        mysql_df,
        (csv_df.city == mysql_df.location) &
        (abs(unix_timestamp(csv_df.timestamp) - unix_timestamp(mysql_df.timestamp)) < 60),
        "inner"
    ).select(
        csv_df.city,
        csv_df.timestamp,
        csv_df.temperature.alias("user_reported_temp"),
        mysql_df.temp_celsius.alias("sensor_temp"),
        csv_df.humidity.alias("user_reported_humidity"),
        mysql_df.humidity_percent.alias("sensor_humidity"),
        mysql_df.rain_mm,
        mysql_df.sensor_id
    )

    # Add derived columns
    final_df = joined_df.withColumn(
        "temp_diff",
        abs(col("user_reported_temp") - col("sensor_temp"))
    ).withColumn(
        "humidity_diff",
        abs(col("user_reported_humidity") - col("sensor_humidity"))
    ).withColumn(
        "date",
        to_date(col("timestamp"))
    )

    # Write to Hive
    final_df.write.mode("append").saveAsTable("final_weather_table")

    # Write to MySQL
    final_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://mysql:3306/weather_db") \
        .option("dbtable", "final_table") \
        .option("user", "weather_user") \
        .option("password", "weather_pass") \
        .mode("append") \
        .save()

    # Export to CSV
    final_df.write.csv("/data/final_output/final_data.csv", header=True)

    spark.stop()


if __name__ == "__main__":
    main()