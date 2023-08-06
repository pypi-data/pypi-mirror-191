from pyspark.sql import SparkSession
import requests
from requests.exceptions import HTTPError

def get_connection_details(connection_id):
  try:
    response= requests.get(f"https://img1-ui-ohsvc6fweq-el.a.run.app/connection/{connection_id}") 
    print(response)
    decode_json=response.json()
    print("DECODE JSON",decode_json)
    fetch_connection_details =decode_json['connDetails']['cDetails']
    project_id=fetch_connection_details['ENV_BQ_PROJECT_ID']
    temporary_gcs_bucket=fetch_connection_details['ENV_BQ_TMP_GCS_STORAGE_BUCKET']
    fetch_project_id_temp_bucket={}
    fetch_project_id_temp_bucket['project_id']=project_id
    fetch_project_id_temp_bucket['temp_gcs_bucket']=temporary_gcs_bucket
    return fetch_project_id_temp_bucket
  except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')