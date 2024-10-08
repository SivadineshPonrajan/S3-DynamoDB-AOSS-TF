resource "aws_opensearch_domain" "customer_search" {
  domain_name    = var.opensearch_domain
  engine_version = "OpenSearch_1.0"

  cluster_config {
    instance_type = "t3.small.search"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }

  advanced_security_options {
    enabled                        = true
    internal_user_database_enabled = true
    master_user_options {
      master_user_name     = var.opensearch_username
      master_user_password = var.opensearch_password
    }
  }

  encrypt_at_rest {
    enabled = true
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

}

resource "aws_opensearch_domain_policy" "customer_search" {
  domain_name = aws_opensearch_domain.customer_search.domain_name

  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "*"
        }
        Action = "es:*"
        Resource = "${aws_opensearch_domain.customer_search.arn}/*"
      }
    ]
  })
}