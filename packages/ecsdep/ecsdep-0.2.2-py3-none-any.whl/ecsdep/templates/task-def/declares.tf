terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data.sycbas"
    key     = "terraform/ecs-cluster/sycbas-ai/task-def/backend/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    acl     = "bucket-owner-full-control"
  }
}

provider "aws" {
  region  = "ap-northeast-2"
}

variable "template_version" {
  default = "1.1"
}

variable "cluster_name" {
  default = "sycbas-ai"
}

# variables -----------------------------------------------
variable "awslog_region" {
  default = "ap-northeast-2"
}

variable "stages" {
  default = {
    default = {
        env_service_stage = "production"
        hosts = ["ai.sycbas.com"]
        listener_priority = 10
        service_name = "backend"
        task_definition_name = "backend"
    }
  }
}

variable "service_auto_scaling" {
  default = {
    desired = 1
    min = 1
    max = 2
    cpu = 100
    memory = 80
  }
}

variable "exposed_container" {
  default = [{
    name = "sycbas-nginx"
    port = 80
  }]
}

variable "target_group" {
  default = {
    protocol = "HTTP"
    healthcheck = {
        path = "/ping"
        matcher = "200,301,302,404"
        timeout = 10
        interval = 60
        healthy_threshold = 2
        unhealthy_threshold = 10
    }
  }
}

variable "loggings" {
  default = ["sycbas-app", "sycbas-nginx"]
}

variable "loadbalancing_pathes" {
  default = ["/*"]
}

variable "requires_compatibilities" {
  default = ["EC2"]
}

variable "service_resources" {
  default = {
    memory = 486
    cpu = 486
  }
}

variable "vpc_name" {
  default = ""
}