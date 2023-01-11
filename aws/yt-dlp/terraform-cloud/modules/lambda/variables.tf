variable "name" {}
variable "layers" {}
variable "memory" {}
variable "timeout" {}
variable "runtime" {
    default = "python3.9"
}
variable "environment" {}
variable "policy-arn" {
    default = [
    ]
}

variable "log-retention-days" {
    default = 3
}