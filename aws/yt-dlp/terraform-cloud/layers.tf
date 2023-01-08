module "requests" {
    source = "./modules/layer"
    name = "requests-tf"
    package-name = "requests"
}

module "yt-dlp" {
    source = "./modules/layer"
    name = "yt-dlp-tf"
    package-name = "yt-dlp"
}

module "ffmpeg" {
    source = "./modules/layer"
    name = "ffmpeg-tf"
    package-name = "ffmpeg"
}