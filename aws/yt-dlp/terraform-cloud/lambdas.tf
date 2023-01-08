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
}