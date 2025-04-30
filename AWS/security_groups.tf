###  Create a security group and allow SSH, HTTP and HTTPS for inbound   ###
############################################################################
resource "aws_security_group" "sg_%INSTANCE_NAME%" {
  name                   = var.secgrp_name
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
    Name = "${var.secgrp_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}