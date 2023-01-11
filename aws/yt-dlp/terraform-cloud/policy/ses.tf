data "terraform_remote_state" "ses" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "ses"
    }
  }
}

resource "aws_iam_policy" "ses" {
  name        = "yt-dlp-ses-tf1"
  path        = "/"
  description = "Allow SES"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendEmail"
        ]
        Effect   = "Allow"
        Resource = [
            data.terraform_remote_state.ses.outputs.ses.arn
        ]
      },
    ]
  })
}

output "ses" {
    value = aws_iam_policy.ses.arn
}