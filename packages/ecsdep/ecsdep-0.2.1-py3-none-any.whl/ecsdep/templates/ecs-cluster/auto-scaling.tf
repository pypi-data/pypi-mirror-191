# cluster auto scaling --------------------------------
resource "aws_autoscaling_group" "ecs_cluster" {
    count = var.autoscale.cpu > 0 || var.autoscale.memory > 0 ? 1 : 0
    vpc_zone_identifier  = var.vpc.cidr_block == "" ? toset(data.aws_subnets.default.ids) : [ for each in aws_subnet.public: each.id ]
    name                 = "ecs-${var.cluster_name}"
    min_size             = var.autoscale ["min"]
    max_size             = var.autoscale ["max"]
    desired_capacity     = var.autoscale ["desired"]
    health_check_type    = "EC2"
    # launch_configuration = aws_launch_configuration.host.name

    launch_template {
      id      = aws_launch_template.host.id
      version = "$Latest"
    }

    tag {
      key                 = "Name"
      value               = var.cluster_name
      propagate_at_launch = true
    }
    tag {
      key                 = "system"
      value               = var.cluster_name
      propagate_at_launch = true
    }
}

resource "aws_autoscaling_policy" "memory-reservation" {
  count = var.autoscale.memory > 0 ? 1 : 0
  name                   = "${var.cluster_name}-memory-reservation"
  policy_type            = "TargetTrackingScaling"
  adjustment_type        = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.ecs_cluster [count.index].name

  target_tracking_configuration {
    customized_metric_specification {
      metric_dimension {
        name  = "ClusterName"
        value = var.cluster_name
      }

      metric_name = "MemoryReservation"
      namespace   = "AWS/ECS"
      statistic   = "Average"
    }
    target_value = var.autoscale.memory
  }
}

# policy for service addition ---------------------------
resource "aws_autoscaling_policy" "cpu-tracking" {
  count = var.autoscale.cpu > 0 ? 1 : 0
  name                      = "${var.cluster_name}-cpu-tracking"
  policy_type               = "TargetTrackingScaling"
  adjustment_type           = "ChangeInCapacity"
  autoscaling_group_name    = aws_autoscaling_group.ecs_cluster [count.index].name

  target_tracking_configuration {
    customized_metric_specification {
      metric_dimension {
        name  = "ClusterName"
        value = var.cluster_name
      }

      metric_name = "CPUReservation"
      namespace   = "AWS/ECS"
      statistic   = "Average"
    }
    target_value = var.autoscale.cpu
  }
}