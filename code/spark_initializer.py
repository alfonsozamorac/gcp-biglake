from pyspark.sql import SparkSession
from constants import Constants


class SparkInitializer:

    def __init__(self, project_id: str, region: str, bucket: str):
        self.spark_session = SparkSession \
            .builder \
            .appName("BigLake Iceberg App") \
            .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.13:1.6.1") \
            .config(f"spark.sql.catalog.{Constants.CATALOG}", "org.apache.iceberg.spark.SparkCatalog") \
            .config(f"spark.sql.catalog.{Constants.CATALOG}.catalog-impl", "org.apache.iceberg.gcp.biglake.BigLakeCatalog") \
            .config(f"spark.sql.catalog.{Constants.CATALOG}.gcp_project", project_id) \
            .config(f"spark.sql.catalog.{Constants.CATALOG}.gcp_location", region) \
            .config(f"spark.sql.catalog.{Constants.CATALOG}.blms_catalog", Constants.CATALOG) \
            .config(f"spark.sql.catalog.{Constants.CATALOG}.warehouse", bucket) \
            .enableHiveSupport() \
            .getOrCreate()

    def get_spark_session(self) -> SparkSession:
        return self.spark_session
