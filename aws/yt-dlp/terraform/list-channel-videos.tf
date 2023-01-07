data "archive_file" "list-channel-videos" {
  type             = "zip"
  source_dir = "../list-channel-videos"
  output_file_mode = "0666"
  output_path      = "${path.module}/files/list-channel-videos.zip"
}

# aws_iam_role.list-channel-videos:
resource "aws_iam_role" "list-channel-videos" {
    assume_role_policy    = jsonencode(
        {
            Statement = [
                {
                    Action    = "sts:AssumeRole"
                    Effect    = "Allow"
                    Principal = {
                        Service = "lambda.amazonaws.com"
                    }
                },
            ]
            Version   = "2012-10-17"
        }
    )

    managed_policy_arns   = [
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    ]

    name                  = "nextjs13-yt-dlp-ListChannelVideos-tf"
    path                  = "/"

    inline_policy {
        name   = "DynamoDB"
        policy = jsonencode(
            {
                Statement = [
                    {
                        Action   = [
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
            }
        )
    }
    inline_policy {
        name   = "SQS"
        policy = jsonencode(
            {
                Statement = [
                    {
                        Action   = [
                            "sqs:SendMessage*",
                        ]
                        Effect   = "Allow"
                        Resource = aws_sqs_queue.videos.arn
                    },
                ]
            }
        )
    }
}


# aws_lambda_function.list-channel-videos:
resource "aws_lambda_function" "list-channel-videos" {
    architectures                  = [
        "x86_64",
    ]
    function_name                  = "nextjs13-yt-dlp-ListChannelsVideos-tf"
    handler                        = "index.handler"

    layers                         = [
        "arn:aws:lambda:us-east-1:195663387853:layer:yt-dlp:8",
    ]

    memory_size                    = 256
    package_type                   = "Zip"
    reserved_concurrent_executions = -1
    role                           = aws_iam_role.list-channel-videos.arn
    runtime                        = "python3.9"
    filename                       = data.archive_file.list-channel-videos.output_path
    source_code_hash               = filebase64sha256(data.archive_file.list-channel-videos.output_path)

    timeout                        = 900

    environment {
        variables = {
            "QueueUrl"  = aws_sqs_queue.videos.url
            "TableName" = aws_dynamodb_table.channels.id
        }
    }

    ephemeral_storage {
        size = 512
    }

    timeouts {}

    tracing_config {
        mode = "PassThrough"
    }
}