terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data"
    key     = "terraform/ecs-cluster/skitai-cluster/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    acl     = "bucket-owner-full-control"
  }
}

provider "aws" {
  region  = "ap-northeast-1"
}

variable "template_version" {
  default = "1.1"
}

variable "cluster_name" {
  default = "skitai-cluster"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "ami" {
  default = "amzn2-ami-ecs-hvm-*-x86_64-*"
}

variable "cors_hosts" {
  default = []
}

variable "cert_name" {
  default = "sns.co.kr"
}

variable "public_key_file" {
  default = "/my/config/path/ecsdep.pub"
}

variable "autoscale" {
  default = {
    cpu = 50
    desired = 1
    max = 4
    memory = 50
    min = 1
  }
}

variable "az_count" {
  default = 3
}

variable "task_iam_policies" {
  default = []
}

variable "vpc" {
  default = {
    cidr_block = ""
    octet3s = [10, 20, 30]
    peering_vpc_ids = []
  }
}