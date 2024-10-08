resource "aws_dynamodb_table" "customer_data" {
  name           = var.dynamodb_table
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name               = "EmailIndex"
    hash_key           = "email"
    projection_type    = "ALL"
  }
}

# # Creation of dynamodb for tf state management
# resource "aws_dynamodb_table" "terraform_lock" {
#   name          = var.dynamodb_tfstate_lock
#   billing_mode  = "PAY_PER_REQUEST"
#   hash_key      = "LockID"

#   attribute {
#     name = "LockID"
#     type = "S"
#   }

#   tags = {
#     Name = "Terraform Lock Table"
#   }
# }