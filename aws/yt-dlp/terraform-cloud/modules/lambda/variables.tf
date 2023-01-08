variable "name" {}
variable "layers" {}
variable "memory" {}
variable "timeout" {}
variable "runtime" {
    default = "python3.9"
}
variable "environment" {}