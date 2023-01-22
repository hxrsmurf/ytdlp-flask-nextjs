data "terraform_remote_state" "google-spaces" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "google-spaces"
    }
  }
}

resource "aws_sns_topic_subscription" "google-spaces" {
  topic_arn = aws_sns_topic.topic.arn
  protocol  = "lambda"
  endpoint  = data.terraform_remote_state.google-spaces.outputs.google-spaces.arn
}