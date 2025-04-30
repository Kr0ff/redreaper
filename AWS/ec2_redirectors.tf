# Author: Kr0ff
# Version: 1.0

###  Add a key pair for the instance  ###
#########################################
resource "aws_key_pair" "%INSTANCE_NAME%-key" {
  key_name   = var.ec2_instance_key
  public_key = "%SSH_PUB_KEY%"
}

# Create a redirector instance which can be either Apache or Nginx
resource "aws_instance" "ec2_%INSTANCE_NAME%" {
  ami                    = "ami-053b0d53c279acc90" # Ubuntu 22.04 LTS Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2023-05-16 ami-053b0d53c279acc90
  instance_type          = "t2.micro" # Free Tier instance type
  key_name               = var.ec2_instance_key # SSH key
  vpc_security_group_ids = ["${aws_security_group.sg_%INSTANCE_NAME%.id}"]  # Security group for redirectors
  subnet_id              = aws_subnet.subnet_%INSTANCE_NAME%.id             # Select the subnet to associate with

  root_block_device {
    volume_size = 30 # Give it 30 GB of disk size just in case (max for free tier)
  }

  tags = {
    Name = "${var.ec2_instance_name}"
    project = "%INSTANCE_NAME%"
    Comment = "Created with RedReaper"
  }
}