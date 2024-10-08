resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_transform.function_name
  principal     = "s3.amazonaws.com"

  source_arn = aws_s3_bucket.landing_zone.arn
}

resource "aws_lambda_function" "lambda_transform" {
  filename      = var.lambda_function_zip
  function_name = var.lambda_function
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_transform.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60

  layers = [aws_lambda_layer_version.lambda_layer.arn]

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.customer_data.name
      OPENSEARCH_ENDPOINT = aws_opensearch_domain.customer_search.endpoint
      OPENSEARCH_USERNAME = var.opensearch_username
      OPENSEARCH_PASSWORD = var.opensearch_password
    }
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = var.lambda_layer_zip
  layer_name = "lambda_layer"

  compatible_runtimes = ["python3.11"]
}