###  Create a dedicated VPC for the redirectors  ###
####################################################
resource "aws_vpc" "vpc_%INSTANCE_NAME%" {
  cidr_block = var.vpc_cidr_block
  enable_dns_support   = true # Enable DNS support
  enable_dns_hostnames = true # Enable DNS hostname support

  tags = {
    Name = "${var.vpc_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}

### Create a subnet for the redirectors to reside in  ###
#########################################################
resource "aws_subnet" "subnet_%INSTANCE_NAME%" {
  cidr_block              = var.vpc_cidr_block # CIDR block for the subnet (can be anything)
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.vpc_%INSTANCE_NAME%.id
  tags = {
    Name = "${var.subnet_name}"
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
    Name = "${var.routetable_name} rtb_%INSTANCE_NAME%"
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
    Name = "${var.internetgateway_name}"
    project = "%INSTANCE_NAME%"
    comment = "Created with RedReaper"
  }
}
