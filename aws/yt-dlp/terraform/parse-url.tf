data "archive_file" "parse-url" {
  type             = "zip"
  source_dir = "../parse-url"
  output_file_mode = "0666"
  output_path      = "${path.module}/files/parse-url.zip"
}

# aws_iam_role.parse-url:
resource "aws_iam_role" "parse-url" {
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
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
    ]

    name                  = "nextjs13-yt-dlp-ParseUrlRole-tf"
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
                            aws_dynamodb_table.channels.arn,
                            "${aws_dynamodb_table.channels.arn}/index/*",
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
                        Resource = aws_sqs_queue.sqs.arn
                    },
                ]
            }
        )
    }
}

# aws_lambda_function.parse-url:
resource "aws_lambda_function" "parse-url" {
    architectures                  = [
        "x86_64",
    ]
    function_name                  = "nextjs13-yt-dlp-ParseUrl-tf"
    handler                        = "index.handler"

    layers                         = [
        "arn:aws:lambda:us-east-1:195663387853:layer:ffmpeg:9",
        "arn:aws:lambda:us-east-1:195663387853:layer:requests:6",
        "arn:aws:lambda:us-east-1:195663387853:layer:yt-dlp:8",
    ]

    memory_size                    = 256
    package_type                   = "Zip"
    reserved_concurrent_executions = -1
    role                           = aws_iam_role.parse-url.arn
    runtime                        = "python3.9"
    timeout                        = 60
    filename                       = data.archive_file.parse-url.output_path

    environment {
        variables = {
            "QueueUrl"      = aws_sqs_queue.sqs.url
            "TableChannels" = aws_dynamodb_table.channels.id
            "TableVideos" = aws_dynamodb_table.videos.id
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