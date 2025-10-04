
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.main.id
}

output "instance_public_ip" {
  description = "Public IP address"
  value       = aws_instance.main.public_ip
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = try(aws_db_instance.main.endpoint, "N/A")
}
