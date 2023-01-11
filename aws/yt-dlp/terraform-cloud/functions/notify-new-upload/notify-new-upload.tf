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
        data.terraform_remote_state.outputs.outputs.arn-default-lambda-execution,
        data.terraform_remote_state.outputs.outputs.policy.ses,
        "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
    ]
}