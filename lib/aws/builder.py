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

        # Check if the output folder exists for AWS module
        if Helpers.check_folder_exists(f"{SCRIPT_RELPATH}/AWS/output") == False:

            # Make the output folder if it doesn't exist
            os.mkdir(f"{SCRIPT_RELPATH}/AWS/output")

            # Check if the project specific folder exists for AWS module
            if Helpers.check_folder_exists(f"{SCRIPT_RELPATH}/AWS/output/{projectName}") == False:
                
                # Make the project specific folder if it doesn't exist
                os.mkdir(f"{SCRIPT_RELPATH}/AWS/output/{projectName}")
        else:
            pass

        # if Helpers.check_file_exists(f"{tf_file}") == False:
        #     print_error(f"Terraform file \"{tf_file}\" does not exist")
        #     sys.exit(-1)

        #print_info(f"Using \"{tf_file}\" to create environment")
        
        # Prepare the EC2 redirector instance Terraform
        def gen_ec2(cidr, projectName, ssh_pubkey):
            
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/ec2_redirectors.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/ec2_redirectors.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    replaced_cidr = replaced_projectName.replace("%CIDR_BLOCK%", cidr)              # from first replace (EC2), replace the CIDR block
                    replaced_ssh = replaced_cidr.replace("%SSH_PUB_KEY%", ssh_pubkey)               # from second replace (CIDR), replace the SSH Public Key

                    final = replaced_ssh                                                            # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False

                    TF_ORIG.close()
                TF_NEW.close()


        # Prepare the EC2 networking Terraform
        def gen_network(projectName):

            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/network.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/network.tf", "r") as TF_ORIG:

                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    final = replaced_projectName                                                    # store final and write to the new file

                    if TF_NEW.write(final):
                        return True
                    else:
                        return False
                    
                    TF_ORIG.close()
                TF_NEW.close()

        # Prepare the EC2 security groups Terraform
        def gen_secgroups(projectName):
            
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/security_groups.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/security_groups.tf", "r") as TF_ORIG:

                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    # replaced_cidr = replaced_projectName.replace("%CIDR_BLOCK%", cidr)              # from first replace (EC2), replace the CIDR block
                    final = replaced_projectName                                                           # store final and write to the new file

                    if TF_NEW.write(final):
                        return True
                    else:
                        return False
                    
                    TF_ORIG.close()
                TF_NEW.close()

        # Prepare the variable information Terraform
        def gen_vars(cidr, projectName):

            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/vars.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/vars.tf", "r") as TF_ORIG:

                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    replaced_cidr = replaced_projectName.replace("%CIDR_BLOCK%", cidr)              # from first replace (EC2), replace the CIDR block
                    final = replaced_cidr                                                           # store final and write to the new file

                    if TF_NEW.write(final):
                        return True
                    else:
                        return False
                    
                    TF_ORIG.close()
                TF_NEW.close()

        # Prepare the output information Terraform
        def gen_outputs(projectName):

            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/outputs.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/outputs.tf", "r") as TF_ORIG:

                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    final = replaced_projectName                                                    # store final and write to the new file

                    if TF_NEW.write(final):
                        return True
                    else:
                        return False
                    
                    TF_ORIG.close()
                TF_NEW.close()
        
        # Prepare the CDN Terraform instance for the project
        def gen_cdn(c2domain, projectName):
        
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/cloudfront.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/cloudfront.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%PROJECT_NAME%", projectName)   # replace EC2 name with project name
                    replaced_c2domain = replaced_projectName.replace("%C2DOMAIN%", c2domain)       # from first replace (project name), replace the C2 domain

                    final = replaced_c2domain                                                      # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 

                    TF_ORIG.close()
                TF_NEW.close()            
                    
        # Prepare the Route53 Terraform hosted zone for the project
        def gen_r53(c2domain, projectName):
        
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/route53.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/AWS/route53.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%PROJECT_NAME%", projectName)   # replace project name
                    replaced_c2domain = replaced_projectName.replace("%C2DOMAIN%", c2domain)       # from first replace (project name), replace the C2 domain
                    
                    final = replaced_c2domain                                                      # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 

                    TF_ORIG.close()
                TF_NEW.close()                    

        try:
            if gen_ec2(cidr, projectName, ssh_pubkey) == True:
                print_success(f"Successfully wrote the EC2 Redirector Terraform file \"./AWS/output/{projectName}/ec2_redirectors.tf\"")
            
            if gen_network(projectName) == True:
                print_success(f"Successfully wrote the network Terraform file \"./AWS/output/{projectName}/network.tf\"")
            
            if gen_secgroups(projectName) == True:
                print_success(f"Successfully wrote the security groups Terraform file \"./AWS/output/{projectName}/security_groups.tf\"")
            
            if gen_vars(cidr, projectName) == True:
                print_success(f"Successfully wrote the variables Terraform file \"./AWS/output/{projectName}/vars.tf\"")
            
            if gen_outputs(projectName) == True:
                print_success(f"Successfully wrote the outputs Terraform file \"./AWS/output/{projectName}/outputs.tf\"")
            
            if gen_cdn(c2domain, projectName) == True:
                print_success(f"Successfully wrote CDN Terraform file \"./AWS/output/{projectName}/cloudfront.tf\"")
                
            if gen_r53(c2domain, projectName) == True:
                print_success(f"Successfully wrote Route53 Terraform file \"./AWS/output/{projectName}/route53.tf\"")
                
            # Just copy the provider Terraform to the output folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}/provider.tf", "a+") as TF_PROVIDER_NEW:
                with open(f"{SCRIPT_RELPATH}/AWS/provider.tf", "r") as TF_PROVIDER_ORIG:
                    text = TF_PROVIDER_ORIG.read()

                    TF_PROVIDER_NEW.write(text)

                    TF_PROVIDER_ORIG.close()
                TF_PROVIDER_NEW.close()

            return True
        
        except Exception as e:
            raise Exception(e)