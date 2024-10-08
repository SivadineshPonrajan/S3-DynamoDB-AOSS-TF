resource "aws_iam_role" "lambda_role" {
  name = "lambda_transform_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_s3_dynamodb_opensearch_policy" {
  name = "lambda_s3_dynamodb_opensearch_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "dynamodb:PutItem",
          "dynamodb:BatchWriteItem",
          "es:*"
        ]
        Resource = [
          "${aws_s3_bucket.landing_zone.arn}/*",
          aws_dynamodb_table.customer_data.arn,
          "${aws_opensearch_domain.customer_search.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::tfstate-bucket-assignment", 
          "arn:aws:s3:::tfstate-bucket-assignment/*"
        ]
      }
    ]
  })
}