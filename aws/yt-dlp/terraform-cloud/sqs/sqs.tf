module "sqs-tf" {
  source                     = "../modules/sqs/"
  name                       = "sqs-tf"
  delay_seconds              = "0"
  visibility_timeout_seconds = "900"
}

module "sqs-videos" {
  source                     = "../modules/sqs/"
  name                       = "yt-dlp-videos-tf"
  delay_seconds              = "0"
  visibility_timeout_seconds = "900"
}

module "sqs-channels" {
  source                     = "../modules/sqs/"
  name                       = "yt-dlp-channels-tf"
  delay_seconds              = "0"
  visibility_timeout_seconds = "900"
}

module "sqs-new-video" {
  source                     = "../modules/sqs/"
  name                       = "yt-dlp-new-video-tf"
  delay_seconds              = "0"
  visibility_timeout_seconds = "60"
}

output "sqs" {
  value = {
    "videos" : {
      "url" : module.sqs-videos.url,
      "arn" : module.sqs-videos.arn
    },
    "channels" : {
      "url" : module.sqs-channels.url,
      "arn" : module.sqs-channels.arn
    },
    "new-video" : {
      "url" : module.sqs-new-video.url,
      "arn" : module.sqs-new-video.arn
    }
  }
}
