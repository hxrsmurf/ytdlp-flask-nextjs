resource "aws_iam_policy" "sqs" {
  name        = "yt-dlp-sqs-tf"
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
            module.sqs-videos.arn,
            module.sqs-channels.arn
        ]
      },
    ]
  })
}