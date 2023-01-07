# aws_iam_user.user:
resource "aws_iam_user" "user" {
    name      = "nextjs13-yt-dlp-NextJSUser-tf"
    path      = "/"
}

resource "aws_iam_user_policy" "user-policy" {
    user = aws_iam_user.user.id
    policy = jsonencode({

    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:ConditionCheckItem",
                "dynamodb:PutItem",
                "dynamodb:DescribeTable",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:UpdateItem"
            ],
            "Resource": [
                aws_dynamodb_table.videos.arn,
                "${aws_dynamodb_table.videos.arn}/index/*",
                aws_dynamodb_table.channels.arn,
                "${aws_dynamodb_table.channels.arn}/index/*"
            ]
        }
    ]
    })

}