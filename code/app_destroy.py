
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

    def drop_example_app(self, database: str) -> None:
        self.biglake.drop_table(biglake_db_name=database,
                                table_name=Constants.CUSTOMERS_TABLE_NAME)
        self.biglake.drop_table(biglake_db_name=database,
                                table_name=Constants.SALES_TABLE_NAME)
        self.biglake.drop_database(biglake_db_name=database)
        self.biglake.drop_namespace()


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
    main.drop_example_app(database=args.dataset)
