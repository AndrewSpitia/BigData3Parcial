from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
import pyspark.sql.functions as f

spark = SparkSession \
    .builder \
    .appName("App") \
    .getOrCreate()

input_data = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "quickstart-events") \
    .load()

data = input_data.selectExpr( "CAST(value AS STRING)").selectExpr("CAST(value AS DOUBLE)")


acciones = data.agg(f.mean("value").alias("Promedio"), f.max("value").alias("Maximo"), f.min("value").alias("Minimo"))

query = acciones \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()