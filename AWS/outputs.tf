###  Show some results that would be useful after creation of resources  ###
############################################################################

# Show instance name
output "InstanceName" {
  description = "EC2 Instance name"
  value = var.ec2_instance_name

  depends_on = [ aws_instance.ec2_%INSTANCE_NAME% ]
}

# Show instance public IP address
output "InstanceIPAddress" {
  value       = aws_instance.ec2_%INSTANCE_NAME%.private_ip
  description = "The public IP address of the main server instance."

  depends_on = [
    # Security group rule must be created before this IP address could
    # actually be used, otherwise the services will be unreachable.
    aws_instance.ec2_%INSTANCE_NAME%
  ]
}

output "CDN_DomainName_%INSTANCE_NAME%" {
  description = "The domain of the CDN %INSTANCE_NAME%"
  value = "${aws_cloudfront_distribution.cdn_%INSTANCE_NAME%.domain_name}"
  depends_on = [ aws_cloudfront_distribution.cdn_%INSTANCE_NAME% ]
}

output "R53Zone_NS_%INSTANCE_NAME%" {
  description = "The Route 53 Zone Primary Name Server %INSTANCE_NAME%"
  value = "${aws_route53_zone.r53hzone_%INSTANCE_NAME%.name_servers}"  
  depends_on = [ aws_route53_zone.r53hzone_%INSTANCE_NAME% ]
}

