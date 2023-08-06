import yaml
from pyspark import SparkFiles


def read_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def read_spark_files():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)
