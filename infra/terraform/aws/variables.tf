variable "aws_region" {
  description = "AWS region for the reference topology."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Non-production reference environment name."
  type        = string
  default     = "demo"
}

variable "vpc_cidr" {
  description = "CIDR for the isolated reference VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "database_username" {
  description = "Database administrator name; password must come from managed secrets."
  type        = string
  default     = "tradeops_admin"
}
