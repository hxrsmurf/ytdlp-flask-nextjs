data "terraform_remote_state" "databases" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "databases"
    }
  }
}


resource "aws_iam_policy" "dynamodb-channels" {
  name        = "yt-dlp-dynamodb-channels-tf1"
  path        = "/"
  description = "Allow DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:DeleteItem",
          "dynamodb:PutItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:UpdateItem",
          "dynamodb:BatchWriteItem",
          "dynamodb:BatchGetItem",
          "dynamodb:DescribeTable",
          "dynamodb:ConditionCheckItem",
        ]
        Effect   = "Allow"
        Resource = [
          data.terraform_remote_state.databases.outputs.channels,
          "${data.terraform_remote_state.databases.outputs.channels}/index/*"
        ]
      },
    ]
  })
}

resource "aws_iam_policy" "dynamodb-videos" {
  name        = "yt-dlp-dynamodb-videos-tf1"
  path        = "/"
  description = "Allow DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:DeleteItem",
          "dynamodb:PutItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:UpdateItem",
          "dynamodb:BatchWriteItem",
          "dynamodb:BatchGetItem",
          "dynamodb:DescribeTable",
          "dynamodb:ConditionCheckItem",
        ]
        Effect   = "Allow"
        Resource = [
          data.terraform_remote_state.databases.outputs.videos,
          "${data.terraform_remote_state.databases.outputs.videos}/index/*"
        ]
      },
    ]
  })
}

output "channels" {
    value = aws_iam_policy.dynamodb-channels.arn
}

output "videos" {
    value = aws_iam_policy.dynamodb-videos.arn
}