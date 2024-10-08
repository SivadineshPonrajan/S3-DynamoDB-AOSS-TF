variable "aws_region" {
  description = "European Server Region - Stockholm"
  type        = string
}

variable "s3_bucket" {
  description = "S3 Bucket for CSV files"
  type        = string
}

variable "dynamodb_table" {
  description = "DynamoDB table - NoSQL database"
  type        = string
}

variable "opensearch_domain" {
  description = "OpenSearch domain"
  type        = string
}

variable "opensearch_username" {
  description = "The master username for OpenSearch."
  type        = string
}

variable "opensearch_password" {
  description = "The master password for OpenSearch."
  type        = string
  sensitive   = true
}

variable "lambda_function" {
  description = "Lambda function to populate the OpenSearch domain and DynamoDB table"
  default     = "lambda_transform"
}

variable "lambda_function_zip" {
  description = "Path to the Lambda transformation function ZIP file"
  default     = "../lambda/package/lambda_transform.zip"
}

variable "lambda_layer_zip" {
  description = "Path to the Lambda layer ZIP file"
  default     = "../lambda/package/lambda_layer.zip"
}

variable "dynamodb_tfstate_lock" {
  description = "DynamoDB table for Terraform state lock"
  type        = string
}