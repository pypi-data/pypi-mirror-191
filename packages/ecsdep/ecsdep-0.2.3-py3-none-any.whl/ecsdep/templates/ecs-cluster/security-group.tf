
resource "aws_security_group" "host" {
    name        = "${var.cluster_name}-member"
    description = "allows host service ports"
    vpc_id      = var.vpc.cidr_block == "" ? data.aws_vpc.default.id : aws_vpc.main[0].id

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        security_groups = [
            aws_security_group.load_balancer.id
        ]
    }

    ingress {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        security_groups = [
            aws_security_group.load_balancer.id
        ]
    }

    ingress {
        from_port   = 32768
        to_port     = 65535
        protocol    = "tcp"
        description = "Access from ALB"
        security_groups = [
            aws_security_group.load_balancer.id
        ]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "${var.cluster_name}-member"
    }
}
