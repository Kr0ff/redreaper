#!/usr/bin/env python3

# __version__: {ver}
# __author__: Kr0ff

import sys

from lib.ascii import *
from lib.colours import *
from lib.helpers import *
from lib.ssh import *

from lib.important import *

# BUILDERS
from lib.aws.builder import *
from lib.digitalocean.builder import *

try:
	import argparse
except ImportError as e:
	raise Exception(e)

ver = 0.3

# AWS module to build the AWS terraform templates
def aws(
    cidr, 
    projectName, 
    ssh_pubkey,
    c2domain):   
    
    # Generate the SSH key for the EC2 instance
    _pubkey = SSH.gen_ssh_key(ssh_pubkey)

    #print(_pubkey)
    
    if AWSBuilder.build_aws(
        cidr, 
        projectName, 
        _pubkey, 
        c2domain, 
    ) == True:

        print_important_msg()
        
# Digital Ocean module to build the Digital Ocean terraform templates     
def digitalocean(projectName, ssh_pubkey):    
    
    # Generate the SSH key for the EC2 instance
    _pubkey = SSH.gen_ssh_key(ssh_pubkey)

    #print(_pubkey)
    
    DOBuilder.build_digitalocean(projectName, _pubkey)

def argparser(selection=None):
    
    # Print ASCII cos its cool :)
    print(printAscii())

    parser = argparse.ArgumentParser(description='redreaper - A terraform script builder for cloud deployement of red team and phishing environments')
    
    subparsers = parser.add_subparsers(help="RedReaper Modules", dest="module")
    
    aws_subp = subparsers.add_parser("aws", help="AWS Submodule")
    aws_subp.add_argument("-p",
            "--projectname",
            help="Name of the project to use (Example: Project_Carnivore)",
            required=True
            )
    aws_subp.add_argument("-c",
            "--cidr",
            help="CIDR block for the subnet (Example: 192.168.100.0/24)",
            required=True
            )
    aws_subp.add_argument("-d",
            "--c2domain",
            help="Domain name for the C2 instance to use (Example: secretoperation.com)",
            required=True
            )
    aws_subp.add_argument("-s",
            "--sshkey",
            help="Name of the SSH key that will be used for the EC2 instance",
            required=True
            )
    
    digitalocean_subp = subparsers.add_parser("do", help="DigitalOcean Submodule")
    digitalocean_subp.add_argument("-p",
            "--projectname",
            help="Name of the project to use (Example: Project_Carnivore)",
            required=True
            )
    digitalocean_subp.add_argument("-s",
            "--sshkey",
            help="Name of the SSH key that will be used for the EC2 instance",
            required=True
            )
    
    parser.add_argument("-v", "--version", help="Get RedReaper version", required=False, action="store_true")
    
    # Show help menu if no arguments provided
    args = parser.parse_args(selection)
    
    if args.module == "aws":
        print_info("==== AWS INFO ====")
        print(f"\t- Project Name: {args.projectname}")
        print(f"\t- CIDR: {args.cidr}")
        print(f"\t- SSH Key Name: {args.sshkey}")
        print(f"\t- C2 Domain Name: {args.c2domain}")
        #print(f"\t- Template File: {aws_subp.template}")

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
            )
    
    if args.module == "do":
        print_info("==== DIGITALOCEAN INFO ====")
        print(f"\t- Project Name: {args.projectname}")
        print(f"\t- SSH Key Name: {args.sshkey}")

        verify = input("\nIs everything correct [N/y]: ")
        if verify == "" or verify == "N" or verify == 'No' or verify == "n" or verify == "no":
            sys.exit(-3)
        elif verify == "Y" or verify == "Yes" or verify == "y" or verify == "yes":
            pass
        else:
            print_error("Input was invalid")
            sys.exit(-4)
            
        digitalocean(args.projectname, args.sshkey)
    
    if args.version:
        print_info(f"RedReaper version {ver}")

if __name__ == "__main__":

    try:
        argparser()
    except KeyboardInterrupt as e:
        print_error("User Interrupted Operation")
        sys.exit(-2)
