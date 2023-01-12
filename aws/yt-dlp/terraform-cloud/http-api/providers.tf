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
      name = "http-api"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}