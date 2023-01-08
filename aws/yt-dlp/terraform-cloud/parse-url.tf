module "parse-url" {
    source = "./modules/lambda"
    name = "parse-url"
    layers = [
        module.yt-dlp.arn
    ]
    memory = "128"
    timeout = "60"
    environment = {
        TableChannels = aws_dynamodb_table.channels.id,
        TableVideos = aws_dynamodb_table.videos.id,
        QueueUrl = module.sqs-videos.url
    }
    policy-arn = [
        var.default-arn,
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
        aws_iam_policy.sqs.arn
    ]
}

resource "aws_lambda_event_source_mapping" "parse-url" {
  event_source_arn = module.sqs-channels.arn
  function_name    = module.parse-url.arn
}
