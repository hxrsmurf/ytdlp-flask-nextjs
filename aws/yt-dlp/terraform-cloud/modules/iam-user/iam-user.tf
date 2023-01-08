resource "aws_iam_user" "user" {
    name      = var.name
    path      = "/"
}

variable "name" {}