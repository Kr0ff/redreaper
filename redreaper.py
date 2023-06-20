#!/usr/bin/env python3

# __version__: 0.2
# __author__: Kr0ff

import sys

from lib.ascii import *
from lib.colours import *
from lib.helpers import *
from lib.aws.builder import *
from lib.ssh import *

from lib.important import *

try:
	import argparse
except ImportError as e:
	raise Exception(e)

def aws(
    cidr, 
    projectName, 
    ssh_pubkey,
    c2domain, 
    tf_file):    
    
    # Generate the SSH key for the EC2 instance
    _pubkey = SSH.gen_ssh_key(ssh_pubkey)

    print(_pubkey)
    
    if Builder.build_aws(
        cidr, 
        projectName, 
        _pubkey, 
        c2domain, 
        tf_file
    ) == True:

        print_important_msg()

def argparser():

    # Print ASCII cos its cool :)
    print(printAscii())

    parser = argparse.ArgumentParser(description='redreaper - A terraform script builder for cloud deployement of red team and phishing environments')

    parser.add_argument("-p",
            "--projectname",
            help="Name of the project to use (Example: Project_Carnivore)",
            required=True
            )
    
    parser.add_argument("-c",
            "--cidr",
            help="CIDR block for the subnet (Example: 192.168.100.0/24)",
            required=True
            )
    
    parser.add_argument("-d",
            "--c2domain",
            help="Domain name for the C2 instance to use (Example: secretoperation.com)",
            required=True
            )

    parser.add_argument("-s",
            "--sshkey",
            help="Name of the SSH key that will be used for the EC2 instance",
            required=True
            )

    parser.add_argument("-t",
            "--template",
            help="Path to the terraform template file. This should be a file in ./AWS/ folder (Example: ./AWS/aws_terraform_redirectors.tf)",
            required=True
            )

    # Show help menu if no arguments provided
    args = parser.parse_args(args=None if sys.argv[1:] else ['-h'])

    print_info("==== INFO ====")
    print(f"\t- Project Name: {args.projectname}")
    print(f"\t- CIDR: {args.cidr}")
    print(f"\t- SSH Key Name: {args.sshkey}")
    print(f"\t- C2 Domain Name: {args.c2domain}")
    print(f"\t- Template File: {args.template}")

    verify = input("\nIs everything correct [N/y]: ")
    if verify == "" or verify == "N" or verify == 'No' or verify == "n" or verify == "no":
        sys.exit(-3)
    elif verify == "Y" or verify == "Yes" or verify == "y" or verify == "yes":
        pass
    else:
        print_error("Input was invalid")
        sys.exit(-4) 

    aws(
        args.cidr, 
        args.projectname,
        args.sshkey,
        args.c2domain,
        args.template
        )

if __name__ == "__main__":

    try:
        argparser()
    except KeyboardInterrupt as e:
        print_error("User Interrupted Operation")
        sys.exit(-2)
