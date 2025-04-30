# Author: Kr0ff
# Version: 1.0

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.1.0"
    }
    
    random = {
      source = "hashicorp/random"
      version = "3.7.2"
    }
  }
}