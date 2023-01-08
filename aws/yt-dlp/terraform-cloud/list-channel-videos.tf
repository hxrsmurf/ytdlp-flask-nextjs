module "list-channel-videos" {
    source = "./modules/lambda"
    name = "list-channel-videos"
    layers = [
        module.yt-dlp.arn
    ]
    memory = "1024"
    timeout = "900"
    environment = {
        TableChannels = aws_dynamodb_table.channels.id,
        TableVideos = aws_dynamodb_table.videos.id,
        QueueVideos = module.sqs-videos.url
        QueueChannels = module.sqs-channels.url
        SourceIp = var.source_ip
    }
    policy-arn = [
        var.default-arn,
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
        aws_iam_policy.sqs.arn,
        aws_iam_policy.dynamodb-channels.arn,
        aws_iam_policy.dynamodb-videos.arn
    ]
}

resource "aws_scheduler_schedule" "list-channel-videos" {
    group_name                   = "default"
    name                         = "yt-dlp-ListChannels-EventBridge-tf"
    schedule_expression          = "rate(1 hours)"
    schedule_expression_timezone = "America/Detroit"
    state                        = "DISABLED"

    flexible_time_window {
        mode                      = "OFF"
    }

    target {
        arn      = module.list-channel-videos.arn
        input    = jsonencode({})
        role_arn = module.role-eventbridge-list-channel-videos.arn

        retry_policy {
            maximum_event_age_in_seconds = 86400
            maximum_retry_attempts       = 0
        }
    }
}

module "role-eventbridge-list-channel-videos" {
    source = "./modules/eventbridge-role"
    name = "ListChannelVideos-tf"
    lambda-arn = module.list-channel-videos.arn
}