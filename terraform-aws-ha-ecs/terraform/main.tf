# Create a VPC.
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = var.vpc_dns_support
  enable_dns_hostnames = var.vpc_dns_hostnames
  tags = {
    Name = "terraform"
  }
}

# Create an Internet Gateway.
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

######################## Public Subnets ##################################

# Create the first public subnet in the VPC for external traffic.
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_cidr_1
  availability_zone       = var.availability_zone[0]
  map_public_ip_on_launch = var.map_public_ip
}

# Create the second public subnet in the VPC for external traffic.
resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_cidr_2
  availability_zone       = var.availability_zone[1]
  map_public_ip_on_launch = var.map_public_ip
}

######################## Private Subnets ##################################

# Create the first private subnet in the VPC for internal traffic.
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_cidr_1
  availability_zone = var.availability_zone[0]
}

# Create the second private subnet in the VPC for internal traffic.
resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_cidr_2
  availability_zone = var.availability_zone[1]
}

######################## EIP's ##################################

# Configure EIP for the first NAT Gateway.
resource "aws_eip" "nat_1" {
  vpc = true
}

# configure EIP for the second NAT gateway.
resource "aws_eip" "nat_2" {
  vpc = true
}

######################## NAT Gateways ##################################

# Create the first NAT gateway.
resource "aws_nat_gateway" "ngw_1" {
  subnet_id     = aws_subnet.public_1.id
  allocation_id = aws_eip.nat_1.id
  # Requires a resource dependency.
  depends_on = [aws_internet_gateway.igw]
}

# Create the second NAT gateway.
resource "aws_nat_gateway" "ngw_2" {
  subnet_id     = aws_subnet.public_2.id
  allocation_id = aws_eip.nat_2.id
  # Requires a resource dependency.
  depends_on = [aws_internet_gateway.igw]
}

######################## Private Route Tables ##################################

# Create the first private subnet route table.
resource "aws_route_table" "private_1" {
  vpc_id = aws_vpc.main.id
}

# Create the second private subnet route table.
resource "aws_route_table" "private_2" {
  vpc_id = aws_vpc.main.id
}


######################## Private Route Table to NAT Gateway ##################################

# Create the first private subnet route.
resource "aws_route" "private_1" {
  route_table_id         = aws_route_table.private_1.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngw_1.id
}

# create the second perivate subnet route.
resource "aws_route" "private_2" {
  route_table_id         = aws_route_table.private_2.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngw_2.id
}

######################## Private Subnet to Route Table ##################################

# Associate the private subnet route table to the first private subnet.
resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private_1.id
}

# Associate the private subnet route table to the second private subnet.
resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private_2.id
}

######################## Public Route Table ##################################

# Create the public subnet route table.
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
}

######################## Public Route Table to Internet Gateway ##################################

# Create the public subnet route.
resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

######################## Public Subnet to Route Table ##################################

# Associate the public subnet route table to the first public subnet.
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

# Associate the public subnet route table to the second public subnet.
resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}