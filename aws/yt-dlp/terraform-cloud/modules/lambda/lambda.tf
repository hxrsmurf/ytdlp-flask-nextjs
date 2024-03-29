data "archive_file" "archive" {
  type             = "zip"
  source_dir = "./code"
  output_file_mode = "0666"
  output_path      = "./${var.name}.zip"
}

# aws_iam_role.list-channel-videos:
resource "aws_iam_role" "role" {
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

    managed_policy_arns   = var.policy-arn

    name                  = "yt-dlp-${var.name}-tf"
    path                  = "/"
}

resource "aws_lambda_function" "function" {
    architectures                  = [
        "x86_64",
    ]
    function_name                  = "yt-dlp-${var.name}-tf"
    handler                        = "index.handler"

    layers                         = var.layers

    memory_size                    = var.memory
    package_type                   = "Zip"
    reserved_concurrent_executions = -1
    role                           = aws_iam_role.role.arn
    runtime                        = var.runtime
    filename                       = data.archive_file.archive.output_path
    source_code_hash               = filebase64sha256(data.archive_file.archive.output_path)

    timeout                        = var.timeout

    environment {
        variables = var.environment
    }

    ephemeral_storage {
        size = 512
    }

    timeouts {}

    tracing_config {
        mode = "PassThrough"
    }
}

output "arn" {
    value = aws_lambda_function.function.arn
}

output "invoke_arn" {
    value = aws_lambda_function.function.invoke_arn
}

output "url" {
    value = "https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/${aws_lambda_function.function.id}"
}