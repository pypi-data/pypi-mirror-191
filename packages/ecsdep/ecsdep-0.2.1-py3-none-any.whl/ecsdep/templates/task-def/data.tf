# infra -----------------------------------------------
data "aws_vpc" "default" {
  default = true
}

data "aws_vpc" "main" {
  count = var.vpc_name == "" ? 0:1
  tags = {
    Name = var.cluster_name
  }
}

data "aws_security_group" "host" {
  name = "${var.cluster_name}-member"
}

data "aws_alb" "load_balancer" {
  name = var.cluster_name
}

data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_security_group.host.vpc_id]
  }
}

data "aws_iam_role" "ecs_tasks_execution_role" {
  name = "ecs-task-execution-role-${var.cluster_name}"
}

data "aws_iam_instance_profile" "profile" {
  name = "${var.cluster_name}-profile"
}

data "aws_iam_role" "ecs_service_role" {
  name = "ecs-service-role-${var.cluster_name}"
}

data "aws_ecs_cluster" "main" {
  cluster_name = var.cluster_name
}

data "aws_alb_listener" "front_end" {
  load_balancer_arn = data.aws_alb.load_balancer.arn
  port              = 443
}

data "aws_launch_template" "host" {
  name = var.cluster_name
}

data "aws_iam_role" "ecs_service_autoscale_role" {
  name = "ecs-service-scale-application-${var.cluster_name}"
}
