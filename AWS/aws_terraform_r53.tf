provider "aws" {
  region = "us-east-1"
}

resource "aws_route53_zone" "r53hzone" {
  name = "${var.c2domain}"
  comment = "Created with RedReaper"
}

resource "aws_route53_record" "root" {
  # for_each = {
  #   for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
  #     name   = dvo.resource_record_name
  #     record = dvo.resource_record_value
  #     type   = dvo.resource_record_type
  #   }
  # }

  zone_id = aws_route53_zone.r53hzone.zone_id
  allow_overwrite = true
  name    = "${var.c2domain}"
  type    = "A"
  ttl     = 300
  records = ["${var.c2ip}"]

  depends_on = [ aws_route53_zone.r53hzone ]
}