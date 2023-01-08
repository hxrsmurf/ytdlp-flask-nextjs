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
        role_arn = module.role-eventbridge-list-channels.arn

        retry_policy {
            maximum_event_age_in_seconds = 86400
            maximum_retry_attempts       = 0
        }
    }
}

module "role-eventbridge-list-channels" {
    source = "./modules/eventbridge-role"
    name = "ListChannels-tf"
    lambda-arn = module.list-channel-videos.arn
}