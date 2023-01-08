module "hello" {
    source = "./modules/lambda"
    name = "hello"
    layers = [
        module.requests.arn,
        module.yt-dlp.arn,
        module.ffmpeg.arn
    ]
    memory = "128"
    timeout = "60"
    environment = {
        Blank = "blank"
    }
    policy-arn = [
        var.default-arn
    ]
}

module "recreate" {
    source = "./modules/lambda"
    name = "recreate"
    layers = [
    ]
    memory = "128"
    timeout = "60"
    environment = {
        QueueUrl = module.sqs-channels.url
    }
    policy-arn = [
        var.default-arn,
        aws_iam_policy.sqs.arn
    ]
}

variable "default-arn" {
    default = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}