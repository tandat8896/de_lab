import os
import time
import warnings

import loguru

warnings.filterwarnings("ignore")
import delta
import pyspark
from delta import configure_spark_with_delta_pip, tables
from pyspark import SparkContext
from pyspark import pipelines as dp
from pyspark.sql import SparkSession


def config_spark():
    builder = (
        SparkSession.builder.appName("ingestion_data")
        .config("spark.driver.memory", "2g")
        .config("spark.executor.cores", "2")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


def main():
    spark = config_spark()
    print("tạm dừng 5 để vào UI")
    time.sleep(300)


if __name__ == "__main__":
    main()
