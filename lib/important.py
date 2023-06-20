# Important info for user after the script generates the Terraform files

try:
    from termcolor import colored
    from colorama import Fore, Style
except ImportError:
    raise Exception("Failed to import \"termcolor\" library")

def print_important_msg():
    
    msg = '''
Don't forget to go to your domain registrar and 
fix the SOA/NS records to point to Route53. 

Some additional minor setup is required for the CDN
such as:
    - certificate, 
    - origin, 
    - alternate domain names = [<C2 DOMAIN>.com ,www.<C2 DOMAIN>.com]
    
or others. Remember to double check the setup after deployment.

May your project go smoothly <3 
    '''
    
    symb = f"\n{Fore.LIGHTYELLOW_EX}[??] Important Information{Style.RESET_ALL}"
    msg_formated = colored(msg, "light_cyan", attrs=["bold","blink"])
    
    s = f"{symb} {msg_formated}"
    
    print(s)