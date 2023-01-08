module "security_group" {
    source = "./modules/security-group"
    name = "terraform-tf"
    description = "terraform-tf"
    vpc_id = "vpc-00c669209674ae8fb"
    port = "22"
    protocol = "tcp"
    cidr_block = "8.8.8.8/32"
}