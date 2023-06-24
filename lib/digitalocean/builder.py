from lib.helpers import *

class DOBuilder:
    def __init__(self):
        projectName = self.projectName
        ssh_pubkey = self.ssh_pubkey
    
    def build_digitalocean(projectName, ssh_pubkey):
        
        # https://stackoverflow.com/a/5475224
        SCRIPT_RELPATH = sys.path[0]

        # DigitalOcean allows only the following characters in names
        # -> (a-z, A-Z, 0-9, . and -)
        if "_" in projectName:
            projectName = str(projectName).replace("_", "-")

        if Helpers.check_folder_exists(f"{SCRIPT_RELPATH}/DigitalOcean/output") == False:
            os.mkdir(f"{SCRIPT_RELPATH}/DigitalOcean/output")
        else:
            pass
        
        def gen_smtp_dp(projectName, ssh_pubkey):
            # Create a new file in root of the project folder
            with open(f"{SCRIPT_RELPATH}/DigitalOcean/output/do-terraform-dp-{projectName}-smtp.tf", "a+") as TF_NEW:

                # Open the template terraform file and replace values
                with open(f"{SCRIPT_RELPATH}/DigitalOcean/do-terraform-dp-smtp.tf", "r") as TF_ORIG:
                    
                    replaced_projectName = TF_ORIG.read().replace("%PROJECT_NAME%", projectName)    # replace DP name with project name
                    replaced_ssh = replaced_projectName.replace("%SSH_PUB_KEY%", ssh_pubkey)        # from second replace (projectName), replace the SSH Public Key

                    final = replaced_ssh                                                            # store final and write to the new file
                    
                    if TF_NEW.write(final):
                        return True
                    else:
                        return False 
        try:
            if gen_smtp_dp(projectName, ssh_pubkey) == True:
                print_success(f"Successfully wrote DigitalOcean SMTP Terraform file \"./DigitalOcean/output/do-terraform-dp-{projectName}-smtp.tf\"")

            return True
        except Exception as e:
                raise Exception(e)