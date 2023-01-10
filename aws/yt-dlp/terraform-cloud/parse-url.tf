module "parse-url" {
    source = "./modules/lambda"
    name = "parse-url"
    layers = [
        module.yt-dlp.arn
    ]
    memory = "256"
    timeout = "30"
    environment = {
        TableChannels = aws_dynamodb_table.channels.id,
        TableVideos = aws_dynamodb_table.videos.id,
        QueueVideos = module.sqs-videos.url
        QueueChannels = module.sqs-channels.url,
        QueueNewVideo = module.sqs-new-video.url
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

resource "aws_lambda_event_source_mapping" "parse-url" {
  event_source_arn = module.sqs-channels.arn
  function_name    = module.parse-url.arn
}