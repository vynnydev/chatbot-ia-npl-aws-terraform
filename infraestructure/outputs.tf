output "vpc_id" {
  description = "VPC ID"
  value       = module.networking.vpc_id
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = module.alb.alb_dns_name
}

output "alb_url" {
  description = "Application URL"
  value       = "http://${module.alb.alb_dns_name}"
}

output "backend_ecr_repository_url" {
  description = "Backend ECR repository URL"
  value       = module.ecr.backend_repository_url
}

output "frontend_ecr_repository_url" {
  description = "Frontend ECR repository URL"
  value       = module.ecr.frontend_repository_url
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = module.elasticache.redis_endpoint
  sensitive   = true
}

output "ecs_backend_cluster_name" {
  description = "ECS Backend cluster name"
  value       = module.ecs_backend.cluster_name
}

output "ecs_frontend_cluster_name" {
  description = "ECS Frontend cluster name"
  value       = module.ecs_frontend.cluster_name
}

output "backend_service_name" {
  description = "Backend service name"
  value       = module.ecs_backend.service_name
}

output "frontend_service_name" {
  description = "Frontend service name"
  value       = module.ecs_frontend.service_name
}