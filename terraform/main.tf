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