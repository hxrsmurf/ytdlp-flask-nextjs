data "terraform_remote_state" "outputs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "outputs"
    }
  }
}

module "list-channels" {
    source = "../../modules/lambda"
    name = "list-channels"
    layers = [
        data.terraform_remote_state.outputs.outputs.layers.yt-dlp
    ]
    memory = "256"
    timeout = "30"
    environment = {
        TableChannels = data.terraform_remote_state.outputs.outputs.databases.channels.name,
        QueueChannels = data.terraform_remote_state.outputs.outputs.sqs.channels.url
    }
    policy-arn = [
        data.terraform_remote_state.outputs.outputs.arn-default-lambda-execution,
        data.terraform_remote_state.outputs.outputs.policy.channels,
        data.terraform_remote_state.outputs.outputs.policy.sqs
    ]
}