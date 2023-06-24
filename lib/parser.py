from lib.ascii import *
from lib.helpers import *
from lib.ssh import *
# Import the builders 
from lib.aws.builder import *
from lib.digitalocean.builder import *

try:
        import argparse
except ImportError:
        print("[-] Failed to import \"argparse\"")


        
        # Start the AWS builder
        AWSBuilder.build_aws(
            aws_subp.cidr, 
            aws_subp.projectName, 
            aws_subp.ssh_pubkey, 
            aws_subp.c2domain, 
            aws_subp.tf_file)