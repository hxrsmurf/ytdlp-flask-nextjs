resource "aws_sqs_queue" "sqs" {
  name                      = "nextjs13-yt-dlp-Queue-tf"
  delay_seconds             = 90

  tags = {
    Name = "nextjs13-yt-dlp-Queue-tf"
  }
}

resource "aws_sqs_queue" "videos" {
  name                          = "nextjs13-yt-dlp-Videos-tf"
  delay_seconds                 = 90
  visibility_timeout_seconds    = 90

  tags = {
    Name = "nextjs13-yt-dlp-Videos-tf"
  }
}

resource "aws_sqs_queue" "videos-dlq" {
  name = "nextjs13-yt-dlp-videos-dlq-tf"
  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue",
    sourceQueueArns   = [aws_sqs_queue.videos.arn]
  })
}