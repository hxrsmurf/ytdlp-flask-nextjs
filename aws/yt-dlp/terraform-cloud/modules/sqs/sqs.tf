resource "aws_sqs_queue" "sqs" {
    name = var.name
    delay_seconds = var.delay_seconds
    visibility_timeout_seconds = var.visibility_timeout_seconds
    tags = {
        Name = var.name
    }
}

output "url" {
    value = aws_sqs_queue.sqs.url
}

output "arn" {
    value = aws_sqs_queue.sqs.arn
}

variable "name" {}
variable "delay_seconds" {}
variable "visibility_timeout_seconds" {}