# Author: Kr0ff
# Version: 1.0

provider "aws" {
  region = "eu-west-2"
  # access_key = "" # AWS_ACCESS_KEY entry if you want to hardcode instead of env var
  # secret_key = "" # AWS_SECRET_KEY entry if you want to hardcode instead of env var
}

resource "random_id" "rid_networking" {
    byte_length = 6
}

#  EC2 Instance Name
variable "ec2_instance_name" {
    default = "ec2_%INSTANCE_NAME%" 
}

#  EC2 Instance SSH Key Pair Name (suffix: -key) 
variable "ec2_instance_key" {
    default = "%INSTANCE_NAME%-key"
}

#  CIDR Of The Redirectors' subnet
variable "vpc_cidr_block" {
    default = "%CIDR_BLOCK%"    
}

#  Redirectors' VPC Name
variable "vpc_name" {
    default = "vpc_%INSTANCE_NAME%"
}

#  Redirectors' Subnet Name
variable "subnet_name" {
    default = "subnet_%INSTANCE_NAME%"
}

#  Redirectors' Security Group Name
variable "secgrp_name" {
    default = "sg_%INSTANCE_NAME%"
}

#  Redirectors' Internet Gateway Name
variable "internetgateway_name" {
    default = "ig_%INSTANCE_NAME%"
}

#  Redirectors' Route Table Name
variable "routetable_name" {
    default = "rt_%INSTANCE_NAME%" 
}