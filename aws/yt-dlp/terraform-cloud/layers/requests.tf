module "requests" {
    source = "../modules/layer"
    name = "requests-tf"
    package-name = "requests"
}

output "requests" {
    value = module.requests.arn
}