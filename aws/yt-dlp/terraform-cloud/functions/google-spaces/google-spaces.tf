data "terraform_remote_state" "outputs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "outputs"
    }
  }
}

module "google-spaces" {
    source = "../../modules/lambda"
    name = "google-spaces"
    layers = [
        data.terraform_remote_state.outputs.outputs.layers.requests
    ]
    memory = "128"
    timeout = "30"
    environment = {
      Space = var.environment.Space
      Key = var.environment.Key
      Token = var.environment.Token
    }
    policy-arn = [
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
        data.terraform_remote_state.outputs.outputs.arn-default-lambda-execution
    ]
}

resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn = data.terraform_remote_state.outputs.outputs.sqs.new-video.arn
  function_name    = module.google-spaces.arn
}