terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 5.78.0"
    }
  }

  # Descomente após criar o bucket S3 manualmente
  # backend "s3" {
  #   bucket         = "el-sabor-terraform-state"
  #   key            = "prod/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-state-lock"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "El Sabor Chatbot"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}