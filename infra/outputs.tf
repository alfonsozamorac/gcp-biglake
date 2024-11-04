output "connection_account_id" {
  description = "Connection account id"
  value       = google_bigquery_connection.connection.cloud_resource
}

output "connection_id" {
  description = "Connection id"
  value       = google_bigquery_connection.connection.id
}

output "connection_name" {
  description = "Connection id"
  value       = google_bigquery_connection.connection.connection_id
}

output "service_account_email" {
  description = "Service Account for BigLake"
  value       = google_service_account.service-account.email
}

output "bucket_datalake" {
  description = "Data Bucket"
  value       = google_storage_bucket.biglake-bucket.url
}

output "bucket_temporary" {
  description = "Temporary files Bucket"
  value       = google_storage_bucket.temporary-files.url
}

output "region" {
  description = "Region"
  value       = var.region
}

output "dataset" {
  description = "Dataset"
  value       = google_bigquery_dataset.dataset.dataset_id
}