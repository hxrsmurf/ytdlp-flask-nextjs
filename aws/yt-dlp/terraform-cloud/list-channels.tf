module "list-channels" {
    source = "./modules/lambda"
    name = "list-channels"
    layers = [
        module.yt-dlp.arn
    ]
    memory = "256"
    timeout = "30"
    environment = {
        TableChannels = aws_dynamodb_table.channels.id,
        QueueChannels = module.sqs-channels.url
    }
    policy-arn = [
        var.default-arn,
        aws_iam_policy.dynamodb-channels.arn,
        aws_iam_policy.sqs.arn
    ]
}

resource "aws_scheduler_schedule" "list-channels" {
    group_name                   = "default"
    name                         = "ListChannels-tf"
    schedule_expression          = "rate(1 hours)"
    schedule_expression_timezone = "America/Detroit"
    state                        = "ENABLED"

    flexible_time_window {
        mode                      = "OFF"
    }

    target {
        arn      = module.list-channels.arn
        input    = jsonencode({})
        role_arn = aws_iam_role.list-channels.arn

        retry_policy {
            maximum_event_age_in_seconds = 86400
            maximum_retry_attempts       = 0
        }
    }
}

resource "aws_iam_role" "list-channels" {
    assume_role_policy    = jsonencode(
        {
            Statement = [
                {
                    Action    = "sts:AssumeRole"
                    Effect    = "Allow"
                    Principal = {
                        Service = "scheduler.amazonaws.com"
                    }
                },
            ]
            Version   = "2012-10-17"
        }
    )
    managed_policy_arns   = []
    max_session_duration  = 3600
    name                  = "yt-dlp-ListChannelsEventBridgeRole-tf"
    path                  = "/"

    inline_policy {
        name   = "EventBridge"
        policy = jsonencode(
            {
                Statement = [
                    {
                        Action   = "lambda:InvokeFunction"
                        Effect   = "Allow"
                        Resource = module.list-channels.arn
                    },
                ]
            }
        )
    }
}