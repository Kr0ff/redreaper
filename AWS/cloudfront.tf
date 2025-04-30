# Author: Kr0ff
# Version: 1.0

resource "aws_cloudfront_distribution" "cdn_%PROJECT_NAME%" {
  # Aliases arent required at this point.
  # If including aliases, it will break the operation of terraform. 
  # This is because an alias requires a custom certificate and this will be implemented 
  # on a later bases. For now manual editing of the CDN is required.
  # 
  # aliases = ["${var.c2domain}", "www.${var.c2domain}"] 

  retain_on_delete    = false   # When enabled, manual deletion of distribution is required
  wait_for_deployment = true    # Terraform waits for status change from "InProgress" to "Deployed"

  http_version    = "http2"
  enabled         = true
  is_ipv6_enabled = false

  origin {

    domain_name = "%C2DOMAIN%"
    origin_id = "%C2DOMAIN%"

    custom_origin_config {
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = [ "TLSv1", "TLSv1.1", "TLSv1.2" ]
      https_port             = 443
      http_port              = 80
    }
  }

  default_cache_behavior {
    allowed_methods        = [ "HEAD", "DELETE", "POST", "GET", "OPTIONS", "PUT", "PATCH" ]
    min_ttl                = 0
    max_ttl                = 31536000
    default_ttl            = 86400
    target_origin_id       = "%C2DOMAIN%"
    cached_methods         = [ "HEAD", "GET" ]
    viewer_protocol_policy = "allow-all"

    forwarded_values {
      query_string = true

      cookies {
        forward = "all"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "blacklist"
      locations        = [
        # Threat index obtained from https://www.visionofhumanity.org/maps/global-terrorism-index/#/
        # Country codes obtained from https://www.iso.org/obp/ui/#search
        "AF", # Afghanistan
        "CN", # China
        "RU", # Russia
        "IL", # Israel
        "BF", # Burkina Faso
        "ML", # Mali
        "NG", # Nigeria
        "CG", # Congo
        "SY", # Syria
        "PK", # Pakistan
        "CO", # Colombia
        ]
    }
  }

  viewer_certificate { cloudfront_default_certificate = true }

  tags = {
    project = "%PROJECT_NAME%"
    comment = "Created with RedReaper"
  }

  depends_on = [ aws_route53_record.root_%PROJECT_NAME% ]
}