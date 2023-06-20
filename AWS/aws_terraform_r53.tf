# Author: Kr0ff
# Version: 1.0

resource "aws_route53_zone" "r53hzone" {
  name = "%C2DOMAIN%"
  comment = "Created with RedReaper"
}

resource "aws_route53_record" "root" {

  zone_id = aws_route53_zone.r53hzone.zone_id
  allow_overwrite = true
  name    = "%C2DOMAIN%"
  type    = "A"
  ttl     = 300
  #records = ["%C2IPADDRESS%"]
  records = ["${aws_instance.ec2_%PROJECT_NAME%.public_ip}"]

  depends_on = [ aws_route53_zone.r53hzone ]
}