data "terraform_remote_state" "outputs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "outputs"
    }
  }
}

module "parse-url" {
    source = "../../modules/lambda"
    name = "parse-url"
    layers = [
        data.terraform_remote_state.outputs.outputs.layers.yt-dlp
    ]
    memory = "256"
    timeout = "30"
    environment = {
        TableChannels = data.terraform_remote_state.outputs.outputs.databases.channels.name,
        TableVideos = data.terraform_remote_state.outputs.outputs.databases.videos.name,
        QueueChannels = data.terraform_remote_state.outputs.outputs.sqs.channels.url,
        QueueVideos = data.terraform_remote_state.outputs.outputs.sqs.videos.url,
        QueueNewVideo = data.terraform_remote_state.outputs.outputs.sqs.new-video.url
    }
    policy-arn = [
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
        data.terraform_remote_state.outputs.outputs.arn-default-lambda-execution,
        data.terraform_remote_state.outputs.outputs.policy.sqs,
        data.terraform_remote_state.outputs.outputs.policy.channels,
        data.terraform_remote_state.outputs.outputs.policy.videos
    ]
}

resource "aws_lambda_permission" "allow_http_api" {
    statement_id  = "d6f0ab7a-032d-5b8c-b207-08dfdd9bf3d2"
    action        = "lambda:InvokeFunction"
    function_name = module.parse-url.arn
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${data.terraform_remote_state.outputs.outputs.http-api.execution_arn}/*/*/"
}

resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn = data.terraform_remote_state.outputs.outputs.sqs.channels.arn
  function_name    = module.parse-url.arn
}

output "invoke_arn" {
  value = module.parse-url.invoke_arn
}