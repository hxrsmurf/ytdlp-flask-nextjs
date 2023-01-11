module "yt-dlp" {
    source = "../modules/layer"
    name = "yt-dlp-tf"
    package-name = "yt-dlp"
}

output "yt-dlp" {
    value = module.yt-dlp.arn
}