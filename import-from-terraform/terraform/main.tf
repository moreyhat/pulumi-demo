terraform {
  required_providers {
      aws = {
          source = "hashicorp/aws"
      }
  }
}

provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "pulumi-demo"
  cidr = "10.0.0.0/16"

  azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

output "public_subnet_ids" {
    value = module.vpc.public_subnets
}