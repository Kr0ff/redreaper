from lib.helpers import *

class AWSBuilder:
    
    def __init__(self):
        cidr = self.cidr
        projectName = self.projectName
        ssh_pubkey = self.ssh_pubkey
        #tf_file = self.tf_file
        c2domain = self.c2domain
        c2ipaddress = self.c2ipaddress

    # AWS environment builder 
    def build_aws(
        cidr, 
        projectName, 
        ssh_pubkey, 
        c2domain, 
        #tf_file
        ):

        # https://stackoverflow.com/a/5475224
        SCRIPT_RELPATH = sys.path[0]

        if Helpers.check_folder_exists(f"{SCRIPT_RELPATH}/AWS/output") == False:
            os.mkdir(f"{SCRIPT_RELPATH}/AWS/output")
        else:
            pass

        # if Helpers.check_file_exists(f"{tf_file}") == False:
        #     print_error(f"Terraform file \"{tf_file}\" does not exist")
        #     sys.exit(-1)

        #print_info(f"Using \"{tf_file}\" to create environment")
        
        # Prepare the EC2 redirector instance Terraform
        def gen_ec2(cidr, projectName, ssh_pubkey):
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}-ec2redirector.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/aws_terraform_ec2redirectors.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    replaced_cidr = replaced_projectName.replace("%CIDR_BLOCK%", cidr)              # from first replace (EC2), replace the CIDR block
                    replaced_ssh = replaced_cidr.replace("%SSH_PUB_KEY%", ssh_pubkey)               # from second replace (CIDR), replace the SSH Public Key

                    final = replaced_ssh                                                            # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 

        # Prepare the CDN Terraform instance for the project
        def gen_cdn(c2domain, projectName):
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}-cdn.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/aws_terraform_cdn.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%PROJECT_NAME%", projectName)   # replace EC2 name with project name
                    replaced_c2domain = replaced_projectName.replace("%C2DOMAIN%", c2domain)       # from first replace (project name), replace the C2 domain

                    final = replaced_c2domain                                                      # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 
                    
        # Prepare the Route53 Terraform hosted zone for the project
        def gen_r53(c2domain, projectName):
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}-r53.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/aws_terraform_r53.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%PROJECT_NAME%", projectName)   # replace project name
                    replaced_c2domain = replaced_projectName.replace("%C2DOMAIN%", c2domain)       # from first replace (project name), replace the C2 domain
                    
                    final = replaced_c2domain                                                      # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 
                        
        try:
            if gen_ec2(cidr, projectName, ssh_pubkey) == True:
                print_success(f"Successfully wrote EC2 Redirector Terraform file \"./AWS/output/{projectName}-ec2redirector.tf\"")
            
            if gen_cdn(c2domain, projectName) == True:
                print_success(f"Successfully wrote CDN Terraform file \"./AWS/output/{projectName}-cdn.tf\"")
                
            if gen_r53(c2domain, projectName) == True:
                print_success(f"Successfully wrote Route53 Terraform file \"./AWS/output/{projectName}-r53.tf\"")
                
            return True
        
        except Exception as e:
            raise Exception(e)