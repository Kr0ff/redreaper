# Author: Kr0ff
# Version: 1.0

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.1.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}


###  Local variables with hard-coded values  ###
################################################
locals {
  ec2_instance_name    = "ec2_%INSTANCE_NAME%"        #  EC2 Instance Name 
  ec2_instance_key     = "%INSTANCE_NAME%-key"        #  EC2 Instance SSH Key Pair Name (suffix: -key) 
  vpc_cidr_block       = "%CIDR_BLOCK%"               #  CIDR Of The Redirectors' subnet
  vpc_name             = "vpc_%INSTANCE_NAME%"        #  Redirectors' VPC Name
  subnet_name          = "subnet_%INSTANCE_NAME%"     #  Redirectors' Subnet Name
  secgrp_name          = "sg_%INSTANCE_NAME%"         #  Redirectors' Security Group Name
  internetgateway_name = "ig_%INSTANCE_NAME%"         #  Redirectors' Internet Gateway Name
  routetable_name      = "rt_%INSTANCE_NAME%"         #  Redirectors' Route Table Name
}


###  Create a dedicated VPC for the redirectors  ###
####################################################
resource "aws_vpc" "vpc_%INSTANCE_NAME%" {
  cidr_block = local.vpc_cidr_block
  enable_dns_support   = true # Enable DNS support
  enable_dns_hostnames = true # Enable DNS hostname support

  tags = {
    Name = "${local.vpc_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}

### Create a subnet for the redirectors to reside in  ###
#########################################################
resource "aws_subnet" "subnet_%INSTANCE_NAME%" {
  cidr_block              = local.vpc_cidr_block # CIDR block for the subnet (can be anything)
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.vpc_%INSTANCE_NAME%.id
  tags = {
    Name = "${local.subnet_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}


###  Create a security group and allow SSH, HTTP and HTTPS for inbound   ###
############################################################################
resource "aws_security_group" "sg_%INSTANCE_NAME%" {
  name                   = local.secgrp_name
  vpc_id                 = aws_vpc.vpc_%INSTANCE_NAME%.id
  revoke_rules_on_delete = true # Delete rules upon sec group deletion

  # Allow inbound from anywhere for HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound from anywhere for HTTPS
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound from anywhere for SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound to anywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Make sure the security group is first created
  # before being deleted (might not be necessary)
  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${local.secgrp_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}

###  Create a route table in the VPC of the redirectors  ###
############################################################
resource "aws_route_table" "rtb_%INSTANCE_NAME%" {
  #subnet_id = aws_subnet.subnet_redirectors.id
  vpc_id    = aws_vpc.vpc_%INSTANCE_NAME%.id
  tags = {
    Name = "rtb_%INSTANCE_NAME%"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}


###  Create a route to allow internet access  ###
#################################################
resource "aws_route" "rt_%INSTANCE_NAME%" {
  route_table_id         = aws_route_table.rtb_%INSTANCE_NAME%.id
  gateway_id             = aws_internet_gateway.ig_%INSTANCE_NAME%.id
  destination_cidr_block = "0.0.0.0/0"

}

###  Associate the route table with the redirector's subnet and rules    ###
############################################################################
resource "aws_route_table_association" "rta_%INSTANCE_NAME%" {
  subnet_id      = aws_subnet.subnet_%INSTANCE_NAME%.id
  route_table_id = aws_route_table.rtb_%INSTANCE_NAME%.id
}

###  Create an internet gateway to allow the instance to have internet   ###
############################################################################
resource "aws_internet_gateway" "ig_%INSTANCE_NAME%" {
  vpc_id = aws_vpc.vpc_%INSTANCE_NAME%.id
  tags = {
    Name = "${local.internetgateway_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}

###  Add a key pair for the instance  ###
#########################################
resource "aws_key_pair" "%INSTANCE_NAME%-key" {
  key_name   = local.ec2_instance_key
  public_key = "%SSH_PUB_KEY%"
}


# Create a redirector instance which can be either Apache or Nginx
resource "aws_instance" "ec2_%INSTANCE_NAME%" {
  ami                    = "ami-053b0d53c279acc90" # Ubuntu 22.04 LTS Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2023-05-16 ami-053b0d53c279acc90
  instance_type          = "t2.micro" # Free Tier instance type
  key_name               = local.ec2_instance_key # SSH key
  vpc_security_group_ids = ["${aws_security_group.sg_%INSTANCE_NAME%.id}"] # Security group for redirectors
  subnet_id              = aws_subnet.subnet_%INSTANCE_NAME%.id # Select the subnet to associate with

  root_block_device {
    volume_size = 30 # Give it 30 GB of disk size just in case (max for free tier)
  }

  tags = {
    Name = "${local.ec2_instance_name}"
    project = "%INSTANCE_NAME%"
    Comment = "Created with RedReaper"
  }
}


###  Show some results that would be useful after creation of resources  ###
############################################################################

# Show instance name
output "InstanceName" {
  description = "EC2 Instance name"
  value = local.ec2_instance_name

  depends_on = [
    aws_instance.ec2_%INSTANCE_NAME%
  ]
}

# Show instance public IP address
output "InstanceIPAddress" {
  value       = aws_instance.ec2_%INSTANCE_NAME%.public_ip
  description = "The public IP address of the main server instance."

  depends_on = [
    # Security group rule must be created before this IP address could
    # actually be used, otherwise the services will be unreachable.
    aws_instance.ec2_%INSTANCE_NAME%
  ]
}