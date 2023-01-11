data "terraform_remote_state" "outputs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "outputs"
    }
  }
}

module "recreate" {
    source = "../../modules/lambda"
    name = "recreate"
    layers = [
        data.terraform_remote_state.outputs.outputs.layers.yt-dlp
    ]
    memory = "256"
    timeout = "30"
    environment = {
        QueueChannels = data.terraform_remote_state.outputs.outputs.sqs.channels.url
    }
    policy-arn = [
        data.terraform_remote_state.outputs.outputs.arn-default-lambda-execution,
        data.terraform_remote_state.outputs.outputs.policy.sqs
    ]
}