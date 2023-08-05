# VPC ----------------------------------------------
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_vpc" "main" {
    count = var.vpc.cidr_block == "" ? 0 : 1
    cidr_block           = var.vpc.cidr_block
    enable_dns_hostnames = true
    tags = {
        Name = var.cluster_name
    }
}

resource "aws_subnet" "public" {
    count = var.vpc.cidr_block == "" ? 0 : var.az_count
    vpc_id                  = aws_vpc.main[0].id
    cidr_block              = cidrsubnet (aws_vpc.main[0].cidr_block, 8, var.vpc.octet3s [count.index])
    availability_zone       = data.aws_availability_zones.available.names [count.index]
    map_public_ip_on_launch = true
    tags = {
        Name = "${var.cluster_name}-net-public-${count.index}"
    }
}

resource "random_shuffle" "subnets" {
  input        = var.vpc.cidr_block == "" ? toset(data.aws_subnets.default.ids) : [ for each in aws_subnet.public: each.id ]
  result_count = 1
}

# gateways ----------------------------------------------
resource "aws_internet_gateway" "external" {
  count = var.vpc.cidr_block == "" ? 0 : 1
  vpc_id = aws_vpc.main[0].id
}

resource "aws_route_table" "main" {
    count = var.vpc.cidr_block != "" && var.template_version == "1.0" ? 1:0
    vpc_id = aws_vpc.main[0].id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.external [0].id
    }
}

resource "aws_default_route_table" "main" {
  count = var.vpc.cidr_block != "" && var.template_version != "1.0" ? 1:0
  default_route_table_id = aws_vpc.main[0].default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.external [0].id
  }
}

resource "aws_route_table_association" "external-pub" {
    count = var.vpc.cidr_block == "" ? 0 : var.az_count
    subnet_id      = aws_subnet.public [count.index].id
    route_table_id = var.template_version == "1.0" ? aws_route_table.main [0].id : aws_default_route_table.main [0].id
}
