output "ecs_cluster_arn" {
  description = "Reference ECS cluster ARN."
  value       = aws_ecs_cluster.this.arn
}

output "database_endpoint" {
  description = "Managed PostgreSQL endpoint; sensitive to deployment operators."
  value       = aws_db_instance.postgres.endpoint
  sensitive   = true
}

output "repository_urls" {
  description = "Immutable service image repositories."
  value       = { for name, repository in aws_ecr_repository.service : name => repository.repository_url }
}
