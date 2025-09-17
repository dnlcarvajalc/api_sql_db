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

data "aws_ecr_repository" "globant_api" {
  name = "globant-api"
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

resource "aws_iam_role" "globant_project_apprunner_ecr_access" {
  name = "globant-project-apprunner-ecr-access"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = [
          "build.apprunner.amazonaws.com",
          "tasks.apprunner.amazonaws.com"
        ]
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_full_access" {
  role       = aws_iam_role.globant_project_apprunner_ecr_access.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
}

resource "aws_iam_role_policy_attachment" "apprunner_full_access" {
  role       = aws_iam_role.globant_project_apprunner_ecr_access.id
  policy_arn = "arn:aws:iam::aws:policy/AWSAppRunnerFullAccess"
}

resource "aws_apprunner_service" "globant_api" {
  service_name = "globant-api"
  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.globant_project_apprunner_ecr_access.arn
    }
    image_repository {
      image_identifier      = "${data.aws_ecr_repository.globant_api.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = "8000"
      }
    }
    auto_deployments_enabled = true
  }
}
