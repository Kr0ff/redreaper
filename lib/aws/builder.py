from lib.helpers import *

class Builder:
    
    def __init__(self):
        cidr = self.cidr
        projectName = self.projectName
        ssh_pubkey = self.ssh_pubkey
        tf_file = self.tf_file


    # AWS environment builder 
    def build_aws(cidr, projectName, ssh_pubkey, tf_file):

        # https://stackoverflow.com/a/5475224
        SCRIPT_RELPATH = sys.path[0]

        if Helpers.check_folder_exists(f"{SCRIPT_RELPATH}/AWS/output") == False:
            os.mkdir(f"{SCRIPT_RELPATH}/AWS/output");
            #print_error("AWS module folder does not exist")
            #sys.exit(-1)
        else:
            pass
            #print_info("AWS output folder already exists")

        if Helpers.check_file_exists(f"{tf_file}") == False:
            print_error(f"Terraform file \"{tf_file}\" does not exist")
            sys.exit(-1)

        print_info(f"Using \"{tf_file}\" to create environment")
        
        # Prepare the EC2 redirector instance Terraform
        def gen_ec2(cidr, projectName, ssh_pubkey, tf_file):
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/AWS/output/{projectName}-ec2redirector.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{tf_file}", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%INSTANCE_NAME%", projectName)   # replace EC2 name with project name
                    replaced_cidr = replaced_projectName.replace("%CIDR_BLOCK%", cidr)              # from first replace (EC2), replace the CIDR block
                    replaced_ssh = replaced_cidr.replace("%SSH_PUB_KEY%", ssh_pubkey)               # from second replace (CIDR), replace the SSH Public Key

                    final = replaced_ssh                                                            # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 
                        
        try:
            if gen_ec2(cidr, projectName, ssh_pubkey, tf_file) == True:
                print_success(f"Successfully wrote EC2 Redirector Terraform file \"./AWS/output/{projectName}-ec2redirector.tf\"")
        except Exception as e:
            print(e)
            sys.exit(-3)

        #print_success(f"Successfully wrote Terraform file \"./AWS/output/{projectName}-ec2redirector.tf\"")