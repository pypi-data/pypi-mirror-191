# private ------------------------------------
# resource "aws_subnet" "private" {
#   count             = var.az_count
#   cidr_block        = cidrsubnet (aws_vpc.main.cidr_block, 8, count.index)
#   availability_zone = data.aws_availability_zones.available.names[count.index]
#   vpc_id            = aws_vpc.main.id
#   tags = {
#     Name =  "${var.cluster_name}-net-private-${count.index}"
#   }
# }

# resource "aws_eip" "gw" {
#   count      = var.az_count
#   vpc        = true
#   depends_on = [aws_internet_gateway.external]
#   tags = {
#     Name =  "${var.cluster_name}-EIP"
#   }
# }

# resource "aws_nat_gateway" "gw" {
#   count         = var.az_count
#   subnet_id     = element(aws_subnet.public.*.id, count.index)
#   allocation_id = element(aws_eip.gw.*.id, count.index)

#   tags = {
#     Name =  "${var.cluster_name}-NAT"
#   }
# }

# resource "aws_route_table" "private" {
#   count  = var.az_count
#   vpc_id = aws_vpc.main.id
#   route {
#     cidr_block     = "0.0.0.0/0"
#     nat_gateway_id = element(aws_nat_gateway.gw.*.id, count.index)
#   }

#   tags = {
#     Name =  "${var.cluster_name}-rt-private-${count.index}"
#   }
# }

# resource "aws_route_table_association" "private" {
#   count          = var.az_count
#   subnet_id      = element(aws_subnet.private.*.id, count.index)
#   route_table_id = element(aws_route_table.private.*.id, count.index)
# }