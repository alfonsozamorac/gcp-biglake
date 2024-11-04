# Data Lakehouse with Iceberg, Dataproc, and BigLake on GCP

## Overview
This project utilizes Google Cloud Platform (GCP) services (Bigquery, GCS, Dataproc, and BigLake) to create a scalable data lakehouse architecture optimized for analytics. Apache Iceberg serves as the table format, providing data management with ACID compliance, while Dataproc handles large-scale data processing. BigLake enables seamless querying and data federation, unifying access across various data sources. The infrastructure setup is automated with Terraform, ensuring consistent and scalable provisioning of resources, including GCS storage, BigLake tables, and Dataproc serverless, to build a high-performance data lakehouse solution on GCP.

## Installation

 1. Export your credentials, replace with your correct values:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="your_credentials_file.json"
   export TF_VAR_project_id="my_gcp_project"
   ```

2. Create infra:

  ```bash
  terraform -chdir="./infra" apply --auto-approve
  ```

 3. Get parameters from terraform:

   ```bash
   export SA_BIGLAKE="$(terraform -chdir="./infra" output -raw service_account_email)"
   export REGION="$(terraform -chdir="./infra" output -raw region)"
   export BUCKET="$(terraform -chdir="./infra" output -raw bucket_datalake)"
   export BUCKET_TEMPORARY="$(terraform -chdir="./infra" output -raw bucket_temporary)"
   export DATASET="$(terraform -chdir="./infra" output -raw dataset)"
   export BQ_CONNECTION="$(terraform -chdir="./infra" output -raw connection_name)"
   ```

 4. Upload iceberg jar:

   ```bash
   gcloud storage cp ./jar/iceberg-spark-runtime-3.5_2.13-1.6.1.jar ${BUCKET_TEMPORARY}
   ```


 5. Launch Dataproc create tables and insert data:

   ```bash
   PY_FILES=$(echo code/*.py | tr ' ' ',')
   gcloud dataproc batches submit pyspark code/app_insert.py \
   --batch=iceberg-poc-$RANDOM \
   --region="europe-west1" \
   --deps-bucket=${BUCKET_TEMPORARY} \
   --project=${TF_VAR_project_id} \
   --service-account=${SA_BIGLAKE} \
   --version=2.2 \
   --py-files=$PY_FILES \
   --jars="${BUCKET_TEMPORARY}/iceberg-spark-runtime-3.5_2.13-1.6.1.jar,gs://spark-lib/biglake/biglake-catalog-iceberg1.2.0-0.1.0-with-dependencies.jar" \
   -- ${TF_VAR_project_id} ${REGION} ${BUCKET} ${DATASET} ${BQ_CONNECTION} 
   ```

 6. Launch Dataproc drop tables:

   ```bash
   gcloud dataproc batches submit pyspark code/app_destroy.py \
   --batch=iceberg-poc-$RANDOM \
   --region="europe-west1" \
   --deps-bucket=${BUCKET_TEMPORARY} \
   --project=${TF_VAR_project_id} \
   --service-account=${SA_BIGLAKE} \
   --version=2.2 \
   --py-files=$PY_FILES \
   --jars="${BUCKET_TEMPORARY}/iceberg-spark-runtime-3.5_2.13-1.6.1.jar,gs://spark-lib/biglake/biglake-catalog-iceberg1.2.0-0.1.0-with-dependencies.jar" \
   -- ${TF_VAR_project_id} ${REGION} ${BUCKET} ${DATASET} ${BQ_CONNECTION}
   ```

4. Destroy infra:

  ```bash
  terraform -chdir="./infra" destroy --auto-approve
  ```
