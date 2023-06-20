import os, sys
from lib.colours import *

class Helpers():

    def __init__(self):
        folder = self.folder
        file = self.file

    def check_folder_exists(folder):
        if not isinstance(folder, str):
            sys.exit(-1)

        if os.path.exists(folder):
            return True
        else:
            return False

    def check_file_exists(file):
        if not isinstance(file, str):
            sys.exit(-1)

        try:
            with open(file, "r") as f: 
                f.close()
                return True
        except FileNotFoundError:
            return False

#print(Helpers.check_file_exists("colours.py")) # == True
#print(Helpers.check_folder_exists("misc")) # == False