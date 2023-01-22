resource "aws_sns_topic" "topic" {
  name = "yt-dlp-new-video-tf"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.topic.arn
  protocol  = "email"
  endpoint  = "yt-dlp@homelabwithkevin.com"
}

output "sns" {
  value = {
    arn  = aws_sns_topic.topic.arn,
    name = aws_sns_topic.topic.name,
    url  = "https://us-east-1.console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/${aws_sns_topic.topic.arn}"
  }
}