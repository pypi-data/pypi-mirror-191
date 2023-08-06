from pyspark.sql import DataFrame
import logging

def read_csv(file_path,batchid,spark) -> DataFrame:
   logging.info("Inside read_csv function")
   df = spark.read.format('csv').option('header', 'true').option('inferSchema','True').load(file_path)
   if batchid == None or batchid == "":
      return df
   else:
      return df.filter(df.batch_id==  batchid)


def read_big_query(tablepath, batchid, spark) ->DataFrame:
   logging.info("Inside read_big_query function")
   df = spark.read.format('bigquery').option('table',tablepath).option('header','true').option('inferSchema','true').load()
   if batchid == None or batchid == "":
      return df
   else:
      return df.filter(df.batch_id==  batchid)


def read_connectiontype(connection_type,dataset_path,batch_id,spark)->DataFrame:
    logging.info("Inside Get Write Metrics CSV Function")
    if connection_type=="BigQuery":
       bigquery_df= read_big_query(dataset_path,batch_id,spark)
       print("type",type(bigquery_df))
       bigquery_df.show()
       return bigquery_df
    elif connection_type=="csv":
       csv_df= read_csv(dataset_path,batch_id,spark)
       return csv_df