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
            module.sqs-channels.arn,
            module.sqs-new-video.arn
        ]
      },
    ]
  })
}

resource "aws_iam_policy" "dynamodb-channels" {
  name        = "yt-dlp-dynamodb-channels-tf"
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
          aws_dynamodb_table.channels.arn,
          "${aws_dynamodb_table.channels.arn}/index/*"
        ]
      },
    ]
  })
}

resource "aws_iam_policy" "dynamodb-videos" {
  name        = "yt-dlp-dynamodb-videos-tf"
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
          aws_dynamodb_table.videos.arn,
          "${aws_dynamodb_table.videos.arn}/index/*",
        ]
      },
    ]
  })
}

resource "aws_iam_policy" "ses" {
  name        = "yt-dlp-ses-tf"
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
          aws_ses_email_identity.yt-dlp.arn
        ]
      },
    ]
  })
}