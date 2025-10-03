# Networking Module
module "networking" {
  source = "./modules/networking"

  project_name       = var.project_name
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

# ECR Module
module "ecr" {
  source = "./modules/ecr"

  project_name = var.project_name
  environment  = var.environment
}

# RDS Module
module "rds" {
  source = "./modules/rds"

  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.networking.vpc_id
  private_subnets   = module.networking.private_subnets
  db_instance_class = var.db_instance_class
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
  
  allowed_security_groups = [module.ecs_backend.security_group_id]
}

# ElastiCache Module
module "elasticache" {
  source = "./modules/elasticache"

  project_name         = var.project_name
  environment          = var.environment
  vpc_id               = module.networking.vpc_id
  private_subnets      = module.networking.private_subnets
  redis_node_type      = var.redis_node_type
  redis_num_cache_nodes = var.redis_num_cache_nodes
  
  allowed_security_groups = [module.ecs_backend.security_group_id]
}

# Application Load Balancer Module
module "alb" {
  source = "./modules/alb"

  project_name    = var.project_name
  environment     = var.environment
  vpc_id          = module.networking.vpc_id
  public_subnets  = module.networking.public_subnets
  certificate_arn = var.certificate_arn
}

# ECS Backend Module
module "ecs_backend" {
  source = "./modules/ecs"

  project_name       = var.project_name
  environment        = var.environment
  service_name       = "backend"
  vpc_id             = module.networking.vpc_id
  private_subnets    = module.networking.private_subnets
  ecr_repository_url = module.ecr.backend_repository_url
  image_tag          = var.backend_image_tag
  cpu                = var.backend_cpu
  memory             = var.backend_memory
  desired_count      = var.backend_desired_count
  container_port     = 8000
  
  alb_target_group_arn = module.alb.backend_target_group_arn
  
  environment_variables = [
    {
      name  = "DATABASE_URL"
      value = "postgresql://${var.db_username}:${var.db_password}@${module.rds.db_endpoint}/${var.db_name}"
    },
    {
      name  = "REDIS_URL"
      value = "redis://${module.elasticache.redis_endpoint}:6379"
    },
    {
      name  = "ENVIRONMENT"
      value = var.environment
    }
  ]
}

# ECS Frontend Module
module "ecs_frontend" {
  source = "./modules/ecs"

  project_name       = var.project_name
  environment        = var.environment
  service_name       = "frontend"
  vpc_id             = module.networking.vpc_id
  private_subnets    = module.networking.private_subnets
  ecr_repository_url = module.ecr.frontend_repository_url
  image_tag          = var.frontend_image_tag
  cpu                = var.frontend_cpu
  memory             = var.frontend_memory
  desired_count      = var.frontend_desired_count
  container_port     = 3000
  
  alb_target_group_arn = module.alb.frontend_target_group_arn
  
  environment_variables = [
    {
      name  = "NEXT_PUBLIC_API_URL"
      value = "http://${module.alb.alb_dns_name}/api"
    },
    {
      name  = "NODE_ENV"
      value = "production"
    }
  ]
}