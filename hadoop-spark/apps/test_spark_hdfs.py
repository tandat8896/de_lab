"""
Test script to verify Spark cluster + HDFS read/write
Usage:
  docker exec -it spark-master spark-submit /opt/spark-apps/test_spark_hdfs.py
"""

from pyspark.sql import SparkSession


def main():
    print(">>> Initializing SparkSession...")
    spark = (
        SparkSession.builder.appName("TestHDFSAndSpark")
        .master("spark://spark-master:7077")
        .config("spark.driver.memory", "512m")
        .config("spark.executor.memory", "512m")
        .getOrCreate()
    )

    data = [
        ("Alice", 25, "Engineering"),
        ("Bob", 30, "Data"),
        ("Charlie", 35, "Product"),
        ("David", 40, "Marketing"),
    ]
    columns = ["Name", "Age", "Department"]

    print(">>> Creating DataFrame...")
    df = spark.createDataFrame(data, columns)
    df.show()

    hdfs_path = "hdfs://namenode:9000/test/users_data"
    print(f">>> Writing DataFrame to HDFS: {hdfs_path}...")
    df.write.mode("overwrite").parquet(hdfs_path)
    print(">>> Write to HDFS successful!")

    print(f">>> Reading DataFrame back from HDFS: {hdfs_path}...")
    df_read = spark.read.parquet(hdfs_path)
    df_read.show()
    print(f">>> Total rows read: {df_read.count()}")

    print(">>> ALL TESTS PASSED! Hadoop HDFS & Spark Cluster are working perfectly together.")
    spark.stop()


if __name__ == "__main__":
    main()
