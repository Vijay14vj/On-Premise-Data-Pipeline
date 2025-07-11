from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Define schema for weather data
weather_schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("city", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("pressure", DoubleType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("weather_description", StringType(), True)
])


def main():
    spark = SparkSession.builder \
        .appName("KafkaToParquetStreaming") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("hive.metastore.uris", "thrift://hive:9083") \
        .enableHiveSupport() \
        .getOrCreate()

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "weather-topic") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON and apply schema
    parsed_df = df.select(
        from_json(col("value").cast("string"), weather_schema).alias("data")
    ).select("data.*")

    # Write to Parquet files every 5 minutes
    query = parsed_df.writeStream \
        .outputMode("append") \
        .format("parquet") \
        .option("path", "/data/weather_parquet") \
        .option("checkpointLocation", "/data/checkpoints") \
        .trigger(processingTime="5 minutes") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()