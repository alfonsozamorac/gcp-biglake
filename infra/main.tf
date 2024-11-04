resource "google_storage_bucket" "temporary-files" {
  project       = var.project_id
  name          = "temporary-files-dataproc"
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket" "biglake-bucket" {
  project       = var.project_id
  name          = "iceberg-data-files-poc"
  location      = var.region
  force_destroy = true
}

resource "google_bigquery_connection" "connection" {
  project       = var.project_id
  connection_id = "biglake_connection"
  location      = var.region
  cloud_resource {
  }
}
resource "google_project_iam_member" "object-viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = format("serviceAccount:%s", google_bigquery_connection.connection.cloud_resource[0].service_account_id)
}

resource "google_project_iam_member" "connection-biglake" {
  project = var.project_id
  role    = "roles/biglake.admin"
  member  = format("serviceAccount:%s", google_bigquery_connection.connection.cloud_resource[0].service_account_id)
}

resource "google_bigquery_dataset" "dataset" {
  project       = var.project_id
  dataset_id    = "shop"
  friendly_name = "shop"
  location      = var.region
}

resource "google_service_account" "service-account" {
  project      = var.project_id
  account_id   = "biglake-sa"
  display_name = "Test SA for BigLake"
}

resource "google_project_iam_member" "bigquery-admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = google_service_account.service-account.member
}

resource "google_project_iam_member" "biglake-admin" {
  project = var.project_id
  role    = "roles/biglake.admin"
  member  = google_service_account.service-account.member
}

resource "google_project_iam_member" "dataproc-worker" {
  project = var.project_id
  role    = "roles/dataproc.worker"
  member  = google_service_account.service-account.member
}

resource "google_project_iam_member" "storage-creator" {
  project = var.project_id
  role    = "roles/storage.objectCreator"
  member  = google_service_account.service-account.member
}

