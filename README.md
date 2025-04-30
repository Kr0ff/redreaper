## The tool is under development !!
# redreaper
A terraform based project to automatically create a cloud environment for red team or phishing engagements

# Description
This project was created to understand better the usage of terraform and the various different modules for cloud environments such as Digital Ocean, AWS and Azure. The project aims to automate the creation of red team and/or phishing infrastructure in various cloud providers such as those aforementioned.

Redreaper uses python3 to take some information regarding the infrastructure that will be deployed and uses terraform templates stored in each provider's folder. After the generation of the final terraform files the user can then run terraform and deploy the environment.

# Credits
This tool was insipired by the various other tools that already exist out there. Some of which are mentioned below:
- https://github.com/SecuraBV/RedWizard
- https://github.com/guidepointsecurity/RedCommander
- https://github.com/mantvydasb/Red-Team-Infrastructure-Automation

# Disclaimer
The author of this does not take any responsibility of how this tool is used. This was created for educational purposes only. Responsibility and usage of this tool fall strictly on the user's side.


# Legend

* `ec2_instance_name    = "ec2_%INSTANCE_NAME%"`        #  EC2 Instance Name 
* `ec2_instance_key     = "%INSTANCE_NAME%-key"`        #  EC2 Instance SSH Key Pair Name (suffix: -key) 
* `vpc_cidr_block       = "%CIDR_BLOCK%"`               #  CIDR Of The Redirectors' subnet
* `vpc_name             = "vpc_%INSTANCE_NAME%"`        #  Redirectors' VPC Name
* `subnet_name          = "subnet_%INSTANCE_NAME%"`     #  Redirectors' Subnet Name
* `secgrp_name          = "sg_%INSTANCE_NAME%"`         #  Redirectors' Security Group Name
* `internetgateway_name = "ig_%INSTANCE_NAME%"`         #  Redirectors' Internet Gateway Name
* `routetable_name      = "rt_%INSTANCE_NAME%"`         #  Redirectors' Route Table Name