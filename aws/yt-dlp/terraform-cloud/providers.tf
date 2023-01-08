terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.49.0"
    }
  }

  cloud {
    organization = "yt-dlp"

    workspaces {
      name = "yt-dlp"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

variable "AWS_ACCESS_KEY_ID" {}
variable "AWS_SECRET_ACCESS_KEY" {}