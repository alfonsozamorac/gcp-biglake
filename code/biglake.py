from pyspark.sql import SparkSession, DataFrame
from write_type import WriteType
from constants import Constants


class Biglake:

    def __init__(self, spark: SparkSession, bq_connection: str):
        self.bq_connection = bq_connection
        self.spark = spark

    def create_table(self, biglake_db_name: str, dataset: str,  table_name: str, fields: dict, partition_by: list = None) -> None:
        fields_str = ", ".join(
            [f"{field_name} {data_type}" for field_name, data_type in fields.items()])
        if partition_by:
            partition_by_str = f"PARTITIONED BY ({", ".join(partition_by)})"
        else:
            partition_by_str = ""
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS {Constants.CATALOG}.{biglake_db_name}.{table_name} (
                {fields_str}
            )
            USING iceberg
            {partition_by_str}
            TBLPROPERTIES(bq_table='{dataset}.{table_name}',
                          bq_connection='{self.bq_connection}');
            """)

    def load_table(self, db_name: str, table_name: str) -> DataFrame:
        return self.spark.read \
            .format(Constants.FORMAT) \
            .load(f"{Constants.CATALOG}.{db_name}.{table_name}")

    def create_namespace(self) -> None:
        self.spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {Constants.CATALOG};")

    def create_database(self, db_name: str) -> None:
        self.spark.sql(
            f"CREATE DATABASE IF NOT EXISTS {Constants.CATALOG}.{db_name};")

    def drop_table(self, biglake_db_name: str, table_name: str) -> None:
        self.spark.sql(
            f"DROP TABLE IF EXISTS {Constants.CATALOG}.{biglake_db_name}.{table_name};")

    def drop_database(self, biglake_db_name: str) -> None:
        self.spark.sql(
            f"DROP DATABASE IF EXISTS {Constants.CATALOG}.{biglake_db_name};")

    def drop_namespace(self) -> None:
        self.spark.sql(f"DROP NAMESPACE IF EXISTS {Constants.CATALOG};")

    def get_history(self, biglake_db_name: str, table_name: str) -> None:
        self.load_table(db_name=biglake_db_name,
                        table_name=table_name+".history").show(truncate=False)
        self.load_table(db_name=biglake_db_name,
                        table_name=table_name+".snapshots").show(truncate=False)

    def save_data(self, df: DataFrame, db_name: str, table_name: str, write_type: WriteType) -> None:
        df.write \
            .format(Constants.FORMAT) \
            .mode(write_type.name) \
            .saveAsTable(f"{Constants.CATALOG}.{db_name}.{table_name}")
