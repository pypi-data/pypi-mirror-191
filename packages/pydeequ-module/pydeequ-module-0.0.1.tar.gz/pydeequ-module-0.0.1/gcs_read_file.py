import google.auth
from google.cloud import storage
import yaml
import logging

logging.info("Authentication to connect with GCS")
credentials,project=google.auth.default()
client=storage.Client(credentials=credentials)
buckets= client.list_buckets()

def read_gcs(bucket_name,file_path):
    logging.info("Inside read gcs function")
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)
    data = blob.download_as_string()
    return data

def read_file_gcs(bucket_name,file_path):
    logging.info("Inside read file gcs function")
    input_data=read_gcs(bucket_name,file_path)
    output_data=list(yaml.safe_load_all(input_data.decode()))
    return output_data


def read_config_file_gcs(bucket_name,file_path):
    logging.info("Inside read config file function")
    input_config_data=read_gcs(bucket_name,file_path)
    output_data= yaml.safe_load(input_config_data.decode())
    return output_data
