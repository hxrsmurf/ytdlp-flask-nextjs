data "terraform_remote_state" "outputs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "outputs"
    }
  }
}

module "notify-new-upload" {
    source = "../../modules/lambda"
    name = "notify-new-upload"
    layers = [
        data.terraform_remote_state.outputs.outputs.layers.yt-dlp
    ]
    memory = "256"
    timeout = "30"
    environment = {
        ses_arn = data.terraform_remote_state.outputs.outputs.ses.arn
        email = data.terraform_remote_state.outputs.outputs.ses.email
    }
    policy-arn = [
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
        data.terraform_remote_state.outputs.outputs.arn-default-lambda-execution,
        data.terraform_remote_state.outputs.outputs.policy.ses,
        aws_iam_policy.sns.arn
    ]
}

resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn = data.terraform_remote_state.outputs.outputs.sqs.new-video.arn
  function_name    = module.notify-new-upload.arn
}