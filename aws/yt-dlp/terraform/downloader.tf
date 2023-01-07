data "archive_file" "downloader" {
  type             = "zip"
  source_file      = "${path.module}/functions/downloader/index.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/files/downloader.zip"
}

# aws_iam_role.downloader:
resource "aws_iam_role" "downloader" {
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

    name                  = "nextjs13-yt-dlp-DownloaderRole-tf"
    path                  = "/"
}

# aws_lambda_function.downloader:
resource "aws_lambda_function" "downloader" {
    architectures                  = [
        "x86_64",
    ]
    function_name                  = "nextjs13-yt-dlp-Downloader-tf"
    handler                        = "index.handler"
    layers                         = [
        "arn:aws:lambda:us-east-1:195663387853:layer:ffmpeg:9",
        "arn:aws:lambda:us-east-1:195663387853:layer:requests:6",
        "arn:aws:lambda:us-east-1:195663387853:layer:yt-dlp:8",
    ]
    memory_size                    = 2048
    package_type                   = "Zip"
    reserved_concurrent_executions = -1
    role                           = aws_iam_role.downloader.arn
    runtime                        = "python3.9"
    filename                       = data.archive_file.downloader.output_path
    timeout                        = 900

    environment {
        variables = {
            "ApiUrl"    = "http://placeholder.homelabwithkevin.com:8080"
            "QueueUrl"  = aws_sqs_queue.sqs.url
            "TableName" = "nextjs-13-yt-dlp-channels"
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