module "ffmpeg" {
    source = "../modules/layer"
    name = "ffmpeg-tf"
    package-name = "ffmpeg"
}

output "ffmpeg" {
    value = module.ffmpeg.arn
}