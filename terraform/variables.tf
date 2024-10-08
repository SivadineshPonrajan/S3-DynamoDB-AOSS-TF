variable "aws_region" {
  description = "European Server Region - Stockholm"
  default     = "eu-north-1"
}

variable "s3_bucket" {
  description = "S3 Bucket for CSV files"
  default     = "second-hand-cars-landing-zone"
}

variable "dynamodb_table" {
  description = "DynamoDB table - NoSQL database"
  default     = "CustomerData"
}

variable "opensearch_domain" {
  description = "OpenSearch domain"
  default     = "customer-search"
}

variable "opensearch_username" {
  description = "The master username for OpenSearch."
  default     = "admin"
}

variable "opensearch_password" {
  description = "The master password for OpenSearch."
  default     = "Batman@123"
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