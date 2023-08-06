data "aws_caller_identity" "current" { }

data "aws_route_table" "targets" {
  count = length (var.vpc.peering_vpc_ids)
  vpc_id = var.vpc.peering_vpc_ids [count.index] == "default" ? data.aws_vpc.default.id : var.vpc.peering_vpc_ids [count.index]
}

data "aws_vpc" "targets" {
  count = length (var.vpc.peering_vpc_ids)
  id = var.vpc.peering_vpc_ids [count.index] == "default" ? data.aws_vpc.default.id : var.vpc.peering_vpc_ids [count.index]
}

resource "aws_vpc_peering_connection" "connection" {
  count = length (var.vpc.peering_vpc_ids)
  vpc_id = aws_vpc.main [0].id
  peer_owner_id = data.aws_caller_identity.current.account_id
  peer_vpc_id = var.vpc.peering_vpc_ids [count.index] == "default" ? data.aws_vpc.default.id : var.vpc.peering_vpc_ids [count.index]
  auto_accept = true

  accepter {
    allow_remote_vpc_dns_resolution = true
  }

  requester {
    allow_remote_vpc_dns_resolution = true
  }
}

resource "aws_route" "target" {
  count = length (var.vpc.peering_vpc_ids)
  route_table_id = data.aws_route_table.targets [count.index].id
  destination_cidr_block = aws_vpc.main [0].cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.connection [count.index].id
}

resource "aws_route" "self" {
  count = length (var.vpc.peering_vpc_ids)
  route_table_id = aws_vpc.main[0].default_route_table_id
  destination_cidr_block = data.aws_vpc.targets [count.index].cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.connection [count.index].id
}
