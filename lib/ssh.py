import subprocess, shlex
from lib.helpers import *

class SSH:
    
    def __init__(self):
        key_name = self.key_name

    def gen_ssh_key(key_name):

        print_info(f"Generating SSH key - \"{key_name}\"")

        _cmd_ = f"ssh-keygen -f {key_name}"

        try:
            subprocess.run(shlex.split(_cmd_, posix=True), shell=False)
        except Exception as e:
            raise Exception(e)
        
        print_success("Successfully generated SSH key")

        if Helpers.check_file_exists(key_name) == False:
            print_error("File does not exist")
            sys.exit(-1)

        # After generation of SSH key, read the pub key
        with open(key_name+".pub", "r") as sshkey:
            content = sshkey.read()
            return content.rstrip("\n")
