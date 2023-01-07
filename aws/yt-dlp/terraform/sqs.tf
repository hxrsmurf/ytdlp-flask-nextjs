resource "aws_sqs_queue" "sqs" {
  name                      = "nextjs13-yt-dlp-Queue-tf"
  delay_seconds             = 90

  tags = {
    Name = "nextjs13-yt-dlp-Queue-tf"
  }
}