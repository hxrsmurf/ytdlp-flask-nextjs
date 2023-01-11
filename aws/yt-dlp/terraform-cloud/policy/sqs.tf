data "terraform_remote_state" "sqs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "sqs"
    }
  }
}

resource "aws_iam_policy" "sqs" {
  name        = "yt-dlp-sqs-tf1"
  path        = "/"
  description = "Allow SQS"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sqs:SendMessage*"
        ]
        Effect   = "Allow"
        Resource = [
            data.terraform_remote_state.sqs.outputs.sqs.videos.arn,
            data.terraform_remote_state.sqs.outputs.sqs.channels.arn,
            data.terraform_remote_state.sqs.outputs.sqs.new-video.arn
        ]
      },
    ]
  })
}

output "sqs" {
    value = aws_iam_policy.sqs.arn
}