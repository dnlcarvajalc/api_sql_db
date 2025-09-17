provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "globant_api" {
  name                 = "globant-api"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  encryption_configuration {
    encryption_type = "AES256"
  }
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

resource "aws_apprunner_service" "globant_api" {
  service_name = "globant-api"
  source_configuration {
    authentication_configuration {
      access_role_arn = "arn:aws:iam::${var.aws_account_id}:role/globant-project"
    }
    image_repository {
      image_identifier      = "${aws_ecr_repository.globant_api.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = "8000"
      }
    }
    auto_deployments_enabled = true
  }
}

resource "aws_iam_role_policy" "ecr_access_policy" {
  name = "AppRunnerECRAccessPolicy"
  role = aws_iam_role.ecr_access.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = "*"
      }
    ]
  })
}