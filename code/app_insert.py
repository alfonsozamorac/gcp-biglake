import argparse
from spark_initializer import SparkInitializer
from constants import Constants
from biglake import Biglake
from write_type import WriteType


class Main:

    def __init__(self, project_id: str, region: str, bucket: str, bigquery_connection: str):
        self.project_id = project_id
        self.region = region
        self.bucket = bucket
        initializer = SparkInitializer(
            project_id=self.project_id, region=self.region, bucket=self.bucket)
        self.spark = initializer.get_spark_session()
        self.biglake = Biglake(self.spark, bigquery_connection)

    def _create_tables(self, database: str) -> None:
        self.biglake.create_namespace()
        self.biglake.create_database(database)
        self.biglake.create_table(biglake_db_name=database, dataset=database,
                                  table_name=Constants.CUSTOMERS_TABLE_NAME, fields=Constants.CUSTOMERS_FIELDS)
        self.biglake.create_table(biglake_db_name=database, dataset=database,
                                  table_name=Constants.SALES_TABLE_NAME, fields=Constants.SALES_FIELDS, partition_by=Constants.PARTITIONS)

    def _example_app(self, database: str) -> None:
        self._create_tables(database)
        df_customers = self.spark.createDataFrame(
            Constants.CUSTOMERS_DATA, Constants.CUSTOMERS_COLUMS)
        df_sales = self.spark.createDataFrame(
            Constants.SALES_DATA, Constants.SALES_COLUMNS)
        self.biglake.save_data(df=df_customers, db_name=database,
                               table_name=Constants.CUSTOMERS_TABLE_NAME, write_type=WriteType.append)
        self.biglake.save_data(df=df_sales, db_name=database,
                               table_name=Constants.SALES_TABLE_NAME, write_type=WriteType.append)
        self.biglake.get_history(
            biglake_db_name=database, table_name=Constants.CUSTOMERS_TABLE_NAME)
        self.biglake.get_history(
            biglake_db_name=database, table_name=Constants.SALES_TABLE_NAME)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BigLake with Dataproc.')
    parser.add_argument('project_id')
    parser.add_argument('region')
    parser.add_argument('bucket')
    parser.add_argument('dataset')
    parser.add_argument('bq_connection')
    args = parser.parse_args()

    main = Main(project_id=args.project_id, region=args.region,
                bucket=args.bucket, bigquery_connection=args.bq_connection)
    main._example_app(database=args.dataset)
