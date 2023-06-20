try:
	from colorama import Fore, Style
except ImportError as e:
	raise Exception(e)

def print_info(string):

	s = f"{Fore.BLUE}[*]{Style.RESET_ALL} {string}"

	print(s) 

def print_success(string):
	
	s = f"{Fore.GREEN}[+]{Style.RESET_ALL} {string}"

	print(s)

def print_error(string):
	
	s = f"{Fore.RED}[-]{Style.RESET_ALL} {string}"

	print(s)

def print_warning(string):

	s = f"{Fore.YELLOW}[!]{Style.RESET_ALL} {string}"

	print(s) 