from .write_metrics import get_output_schema
from .process_metrics import process_metrics
from pyspark.sql import SparkSession
from .gcs_read_file import read_file_gcs, read_config_file_gcs
import logging
from .parse_input_config import read_spark_files
from .get_connection import get_connection_details
def process_deequ(bucket_name, file_path, batch_id):
    logging.info("Inside process_deequ function")
    staging_data = read_file_gcs(bucket_name, file_path)
    spark = loadspark("spark")
    config_data = read_spark_files()
    output_schema = get_output_schema()
    for data in staging_data:
        process_metrics(data, output_schema, spark, batch_id, config_data)


def loadspark(option):
    logging.info("Inside loadspark function")
    if option == "spark":
        logging.info("Spark option")
        return (
            SparkSession.builder.getOrCreate())
    else:
         return (
            SparkSession.builder.getOrCreate())

