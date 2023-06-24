# Author: Kr0ff
# Version: 1.0

terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
    token = var.do_token
}

variable "do_token" {
    description = "Digital Ocean API Token"
    nullable = false
}

# Project Name = %PROJECT_NAME%
# Droplet Instance = %INSTANCE_NAME%
# SSH pubkey = %SSH_PUBKEY%
resource "digitalocean_ssh_key" "sshkey_%PROJECT_NAME%" {
  name       = "ssh-%PROJECT_NAME%"
  public_key = "%SSH_PUB_KEY%"
}

# s-1vcpu-2gb
# lon1
# ubuntu-22-04-x64
# Create a new Web Droplet in the nyc2 region
resource "digitalocean_droplet" "dp_%PROJECT_NAME%" {
  image  = "ubuntu-22-04-x64"
  name   = "dp-smtp01-%PROJECT_NAME%"
  region = "lon1"
  size   = "s-1vcpu-2gb"
  ssh_keys = [digitalocean_ssh_key.sshkey_%PROJECT_NAME%.fingerprint]
}   

# Project Name = %PROJECT_NAME%
resource "digitalocean_project" "%PROJECT_NAME%" {
  name        = "%PROJECT_NAME%"
  description = "Created by RedReaper"
  purpose     = "Assessment_%PROJECT_NAME%"
  environment = "Production"
  resources   = [digitalocean_droplet.dp_%PROJECT_NAME%.urn]

  depends_on = [ digitalocean_droplet.dp_%PROJECT_NAME% ]
}

# Project Name = %PROJECT_NAME%
# Droplet Instance = %INSTANCE_NAME%
resource "digitalocean_firewall" "fw_%PROJECT_NAME%" {
  name = "fw-%PROJECT_NAME%"

  droplet_ids = [digitalocean_droplet.dp_%PROJECT_NAME%.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "25"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "icmp"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range = "0"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  depends_on = [ digitalocean_droplet.dp_%PROJECT_NAME% ]
}

output "Droplet_IPV4" {
    value = digitalocean_droplet.dp_%PROJECT_NAME%.ipv4_address
}