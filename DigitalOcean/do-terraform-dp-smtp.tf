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
resource "digitalocean_ssh_key" "sshkey_project1" {
  name       = "Project1"
  public_key = ""
}

# s-1vcpu-2gb
# lon1
# ubuntu-22-04-x64
# Create a new Web Droplet in the nyc2 region
resource "digitalocean_droplet" "dp_project1" {
  image  = "ubuntu-22-04-x64"
  name   = "smtp-01"
  region = "lon1"
  size   = "s-1vcpu-2gb"
  ssh_keys = [digitalocean_ssh_key.sshkey_project1.fingerprint]
}   

# Project Name = %PROJECT_NAME%
resource "digitalocean_project" "project1" {
  name        = "Project1"
  description = "Created by RedReaper"
  purpose     = "Project1"
  environment = "Production"
  resources   = [digitalocean_droplet.dp_project1.urn]

  depends_on = [ digitalocean_droplet.dp_project1 ]
}

# Project Name = %PROJECT_NAME%
# Droplet Instance = %INSTANCE_NAME%
resource "digitalocean_firewall" "fw_project1" {
  name = "fw-project1"

  droplet_ids = [digitalocean_droplet.dp_project1.id]

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
    protocol              = "tcp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  depends_on = [ digitalocean_droplet.dp_project1 ]
}



output "Droplet_IPV4" {
    value = digitalocean_droplet.dp_project1.ipv4_address
}
