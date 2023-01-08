module "sqs-tf" {
    source = "./modules/sqs/"
    name = "sqs-tf"
    delay_seconds = "30"
    visibility_timeout_seconds = "900"
}

module "sqs-videos" {
    source = "./modules/sqs/"
    name = "yt-dlp-videos-tf"
    delay_seconds = "30"
    visibility_timeout_seconds = "900"
}

module "sqs-channels" {
    source = "./modules/sqs/"
    name = "yt-dlp-channels-tf"
    delay_seconds = "30"
    visibility_timeout_seconds = "900"
}