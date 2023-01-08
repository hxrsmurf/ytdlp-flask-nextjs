module "sqs-tf" {
    source = "./modules/sqs/"
    name = "sqs-tf"
    delay_seconds = "30"
    visibility_timeout_seconds = "30"
}