resource "aws_iam_policy" "sns" {
  name        = "yt-dlp-sns-tf"
  path        = "/"
  description = "Allow SNS Publish"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sns:Publish"
        ]
        Effect = "Allow"
        Resource = [
          data.terraform_remote_state.outputs.outputs.sns.sns.arn
        ]
      },
    ]
  })
}