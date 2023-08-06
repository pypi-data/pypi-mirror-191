from pyspark.sql.types import StructField
from pyspark.sql.types import StringType
from pyspark.sql.types import DecimalType
from pyspark.sql.types import StructType
import logging
from pyspark.sql import DataFrame
def get_output_schema():
    logging.info("Inside Get Outside Schema Function")
    return StructType([
        StructField("DomainName", StringType(), True),
        StructField("SubDomainName", StringType(), True),
        StructField("DatasetName", StringType(), True),
        StructField("ColumnName", StringType(), True),
        StructField("MetricName", StringType(), True),
        StructField("MetricUOM", StringType(), True),
        StructField("MetricValue", DecimalType(), True),
        StructField("Insert_Timestamp", StringType(), True),
        StructField("Alert_Type", StringType(), True),
        StructField("Alert_Message", StringType(), True),
        StructField("ComplianceCondition", StringType(), True),
        StructField("RegexPattern", StringType(), True),
        StructField("BatchId", StringType(), True)
    ])
def output_csv(dataframe: DataFrame,config):
    logging.info("Inside Get Output CSV Function")
    fetch_target_table = config["configdetails"]["MetricsPath"]
    dataframe.coalesce(1).write.mode("append").csv(fetch_target_table)


def output_bigquery(dataframe: DataFrame,config):
    logging.info("Inside Get Output Bigquery CSV Function")
    fetch_temp_gcsbucket = config["configdetails"]["TemporaryBucket"]
    fetch_target_table = config["configdetails"]["MetricsPath"] 
    dataframe.write.mode("append").format('bigquery').option("temporaryGcsBucket", fetch_temp_gcsbucket).option("table",fetch_target_table).save()

def write_metrics(dataframe: DataFrame,config):
    logging.info("Inside Get Write Metrics CSV Function")
    fetch_input_bigquery = config["configdetails"]["TargetType"]
    if fetch_input_bigquery=="bigquery":
       output_bigquery(dataframe,config)
    elif fetch_input_bigquery=="csv":
        output_csv(dataframe,config)

    
