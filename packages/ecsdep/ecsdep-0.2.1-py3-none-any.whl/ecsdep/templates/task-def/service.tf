
# task definition ----------------------------------------
resource "aws_ecs_task_definition" "ecsdep" {
    network_mode       = var.requires_compatibilities[0] == "EC2" ? null : "awsvpc"
    family             = var.stages [terraform.workspace].task_definition_name
    execution_role_arn = data.aws_iam_role.ecs_tasks_execution_role.arn
    container_definitions = file ("tasks.json")
    requires_compatibilities = var.requires_compatibilities
    cpu = var.service_resources.cpu > 0 ? var.service_resources.cpu : null
    memory = var.service_resources.memory > 0 ? var.service_resources.memory : null
}

# service -------------------------------------------------------
resource "aws_ecs_service" "ecsdep" {
    name            = var.stages [terraform.workspace].service_name
    cluster         = data.aws_ecs_cluster.main.id
    task_definition = aws_ecs_task_definition.ecsdep.arn
    iam_role        = var.requires_compatibilities[0] == "EC2" && length (var.exposed_container) == 1 ? data.aws_iam_role.ecs_service_role.arn : null
    desired_count   = var.service_auto_scaling.desired
    launch_type     = var.requires_compatibilities[0]

    dynamic "network_configuration" {
      for_each = var.requires_compatibilities[0] == "FARGATE" ? [""] : []
      content {
        security_groups  = [data.aws_security_group.host.id]
        subnets          = data.aws_subnets.subnets.ids
        assign_public_ip = true
      }
    }

    dynamic "load_balancer" {
      for_each = length (var.exposed_container) == 1 ? [""] : []
      content {
        target_group_arn = aws_alb_target_group.ecsdep [0].id
        container_name   = var.exposed_container [0].name
        container_port   = var.exposed_container [0].port
      }
    }
}

# alb target gorup and routing rule -----------------------
resource "aws_alb_target_group" "ecsdep" {
  count       = length (var.exposed_container)
  name        = "${var.cluster_name}-${var.stages [terraform.workspace].service_name}"
  port        = var.exposed_container [count.index].port
  protocol    = var.target_group.protocol
  vpc_id      = data.aws_security_group.host.vpc_id
  target_type = var.requires_compatibilities[0] == "EC2" ? "instance" : "ip"

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
  }

  health_check {
    path                = var.target_group.healthcheck.path
    healthy_threshold   = var.target_group.healthcheck.healthy_threshold
    unhealthy_threshold = var.target_group.healthcheck.unhealthy_threshold
    timeout             = var.target_group.healthcheck.timeout
    interval            = var.target_group.healthcheck.interval
    matcher             = var.target_group.healthcheck.matcher
  }
}

resource "aws_lb_listener_rule" "default" {
  count = length (var.exposed_container)
  listener_arn = data.aws_alb_listener.front_end.arn
  priority     = var.stages [terraform.workspace].listener_priority

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.ecsdep [count.index].arn
  }

  condition {
    path_pattern {
      values = var.loadbalancing_pathes
    }
  }

  condition {
    host_header {
      values = var.stages [terraform.workspace].hosts
    }
  }
}

# service auto scaling -------------------------------------------
resource "aws_appautoscaling_target" "ecs_target" {
  count = var.service_auto_scaling.cpu > 0 || var.service_auto_scaling.memory > 0 ? 1 : 0
  max_capacity       = var.service_auto_scaling.max
  min_capacity       = var.service_auto_scaling.min
  resource_id        = "service/${var.cluster_name}/${var.stages [terraform.workspace].service_name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  role_arn           = data.aws_iam_role.ecs_service_autoscale_role.arn
}

resource "aws_appautoscaling_policy" "ecs_target_cpu" {
  count = var.service_auto_scaling.cpu > 0 ? 1 : 0
  name               = "application-scaling-policy-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target [count.index].resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target [count.index].scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target [count.index].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = var.service_auto_scaling.cpu
  }
  depends_on = [aws_appautoscaling_target.ecs_target]
}

resource "aws_appautoscaling_policy" "ecs_target_memory" {
  count = var.service_auto_scaling.memory > 0 ? 1 : 0
  name               = "application-scaling-policy-memory"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target [count.index].resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target [count.index].scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target [count.index].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    target_value = var.service_auto_scaling.memory
  }
  depends_on = [aws_appautoscaling_target.ecs_target]
}

# logging ----------------------------------------------
resource "aws_cloudwatch_log_group" "log_group" {
  count             = length (var.loggings)
  name              = "/ecs/${var.cluster_name}/${var.stages [terraform.workspace].service_name}/${var.loggings [count.index]}"
  retention_in_days = 30
  tags = {
    Name = "${var.stages [terraform.workspace].service_name}-${var.loggings [count.index]}"
  }
}

resource "aws_cloudwatch_log_stream" "log_stream" {
  count          = length (var.loggings)
  name           = "${var.stages [terraform.workspace].service_name}-${var.loggings [count.index]}"
  log_group_name = aws_cloudwatch_log_group.log_group [count.index].name
}

