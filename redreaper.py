#!/usr/bin/env python3

# __version__: 0.1

import sys
import os
import json
import subprocess
import shlex
import re
import fileinput

from lib.ascii import *
from lib.colours import *
from lib.helpers import *

try:
	import argparse
except ImportError as e:
	raise Exception(e)

def gen_ssh_key(key_name):

    print_info(f"Generating SSH key - \"{key_name}\"")

    _cmd_ = f"ssh-keygen -f {key_name}"

    try:
        subprocess.run(shlex.split(_cmd_, posix=True), shell=False)
    except Exception as e:
        raise Exception(e)
    
    print_success("Successfully generated SSH key")

    # After generation of SSH key, read the pub key
    with open(key_name+".pub", "r") as sshkey:
        content = sshkey.read()
        return content.rstrip("\n")

def build_tf(cidr, projectName, ssh_pubkey, tf_file):

    if Helpers.check_folder_exists("./AWS") == False:
        print_error("AWS module folder does not exist")
        sys.exit(-1)

    if Helpers.check_file_exists(f"{tf_file}") == False:
        print_error(f"Terraform file \"{tf_file}\" does not exist")
        sys.exit(-1)

    # Generate the SSH key for the EC2 instance
    _pubkey = gen_ssh_key(ssh_pubkey)

    print(_pubkey)
    input()

    if Helpers.check_file_exists(ssh_pubkey) == False:
        print_error("File does not exist")
        sys.exit(-1)

    print_info(f"Using \"{tf_file}\" to create environment")
    
    # Create a new file in root of the project folder
    with open(f"./{projectName}-main.tf", "a+") as TF_NEW:

        # Open the template terraform file and replace values
        with open(f"{tf_file}", "r") as TF_ORIG:
            
            replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
            replaced_cidr = replaced_projectName.replace("%CIDR_BLOCK%", cidr)              # from first replace (EC2), replace the CIDR block
            replaced_ssh = replaced_cidr.replace("%SSH_PUB_KEY%", _pubkey)                  # from second replace (CIDR), replace the SSH Public Key

            final = replaced_ssh                                                            # store final and write to the new file
            
            TF_NEW.write(final)

    print_success(f"Successfully wrote Terraform file \"./{projectName}-main.tf\"")

def argparser():

    # Print ASCII cos its cool :)
    print(printAscii())

    parser = argparse.ArgumentParser(description='redreaper - A terraform script builder for cloud deployement of red team and phishing environments')

    parser.add_argument("-c",
            "--cidr",
            help="CIDR block for the subnet (Example: 192.168.100.0/24",
            #action="store_true",
            required=True
            )

    parser.add_argument("-p",
            "--projectname",
            help="Name of the project to use (Example: Project_Carnivore)",
            #action="store_true",
            required=True
            )

    parser.add_argument("-s",
            "--sshkey",
            help="Name of the SSH key that will be used for the EC2 instance",
            #action="store_true",
            required=True
            )

    parser.add_argument("-t",
            "--template",
            help="Path to the terraform template file. This should be a file in ./AWS/ folder (Example: ./AWS/aws_terraform_redirectors.tf)",
            #action="store_true",
            required=True
            )

    # Show help menu if no arguments provided
    args = parser.parse_args(args=None if sys.argv[1:] else ['-h'])

    print_info("==== INFO ====")
    print(f"\t- Project Name: {args.projectname}")
    print(f"\t- CIDR: {args.cidr}")
    print(f"\t- SSH Key Name: {args.sshkey}")
    print(f"\t- Template file: {args.template}")

    verify = input("\nIs everything correct [N/y]: ")
    if verify == "" or verify == "N" or verify == 'No' or verify == "n" or verify == "no":
        sys.exit(-3)
    elif verify == "Y" or verify == "Yes" or verify == "y" or verify == "yes":
        pass
    else:
        print_error("Input was invalid")
        sys.exit(-4) 

    build_tf(
        args.cidr, 
        args.projectname,
        args.sshkey,
        args.template
        )


if __name__ == "__main__":
    
    try:
        argparser()
    except KeyboardInterrupt as e:
        print_error("User Interrupted Operation")
        sys.exit(-2)
