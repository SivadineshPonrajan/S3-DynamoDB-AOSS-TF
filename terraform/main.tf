terraform {             # Will be overrided from the github action workflow
  backend "s3" {
    bucket         = ""
    key            = ""
    region         = ""
    dynamodb_table = ""
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "landing_zone" {
  bucket = var.s3_bucket
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.landing_zone.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_transform.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }
  depends_on = [aws_lambda_permission.allow_s3]
}

output "opensearch_endpoint" {
  description = "The endpoint of the OpenSearch instance - to use it with search script"
  value       = aws_opensearch_domain.customer_search.endpoint
}