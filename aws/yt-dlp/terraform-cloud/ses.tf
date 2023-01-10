resource "aws_ses_email_identity" "yt-dlp" {
  email = "yt-dlp@homelabwithkevin.com"
}

module "ses" {
    source = "./modules/lambda"
    name = "ses"
    layers = [
        module.yt-dlp.arn
    ]
    memory = "128"
    timeout = "30"
    environment = {
        ses_arn = aws_ses_email_identity.yt-dlp.arn
        email = aws_ses_email_identity.yt-dlp.email
    }
    policy-arn = [
        var.default-arn,
        aws_iam_policy.ses.arn,
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
    ]
}

resource "aws_lambda_event_source_mapping" "ses" {
  event_source_arn = module.sqs-new-video.arn
  function_name    = module.ses.arn
}