# resource "aws_subnet" "private" {
#     count = var.vpc.cidr_block == "" ? 0 : var.az_count
#     vpc_id                  = aws_vpc.main[0].id
#     cidr_block              = cidrsubnet (aws_vpc.main[0].cidr_block, 8, var.vpc.octet3s [count.index] + 100)
#     availability_zone       = data.aws_availability_zones.available.names [count.index]
#     map_public_ip_on_launch = true
#     tags = {
#         Name = "${var.cluster_name}-net-private-${count.index}"
#     }
# }

# resource "aws_eip" "gw" {
#   vpc        = true
#   depends_on = [aws_internet_gateway.external]
#   tags = {
#     Name =  "${var.cluster_name}-eip"
#   }
# }

# resource "aws_nat_gateway" "gw" {
#   count = var.vpc.cidr_block == "" ? 0 : 1
#   subnet_id     = aws_subnet.public [0].id
#   allocation_id = aws_eip.gw.id

#   tags = {
#     Name =  "${var.cluster_name}-nat"
#   }
# }

# resource "aws_route_table" "private" {
#   count = var.vpc.cidr_block == "" ? 0 : 1
#   vpc_id = aws_vpc.main [0].id
#   route {
#     cidr_block     = "0.0.0.0/0"
#     nat_gateway_id = aws_nat_gateway.gw [0].id
#   }

#   tags = {
#     Name =  "${var.cluster_name}-private"
#   }
# }

# resource "aws_route_table_association" "private" {
#   count = var.vpc.cidr_block == "" ? 0 : var.az_count
#   subnet_id      = aws_subnet.private[count.index].id
#   route_table_id = aws_route_table.private [0].id
# }

# resource "aws_route" "self-private" {
#   count = length (var.vpc.peering_vpc_ids)
#   route_table_id = aws_route_table.private[0].id
#   destination_cidr_block = data.aws_vpc.targets [count.index].cidr_block
#   vpc_peering_connection_id = aws_vpc_peering_connection.connection [count.index].id
# }
