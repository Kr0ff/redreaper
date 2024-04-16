# redreaper
A terraform based project to automatically create a cloud environment for red team or phishing engagements

# Description
This project was created to understand better the usage of terraform and the various different modules for cloud environments such as Digital Ocean, AWS and Azure. The project aims to automate the creation of red team and/or phishing infrastructure in various cloud providers such as those aforementioned.

Redreaper uses python3 to take some information regarding the infrastructure that will be deployed and uses terraform templates stored in each provider's folder. After the generation of the final terraform files the user can then run terraform and deploy the environment.

# Credits
This tool was insipired by the various other tools that already exist out there. Some of which are mentioned below:
- https://github.com/SecuraBV/RedWizard
