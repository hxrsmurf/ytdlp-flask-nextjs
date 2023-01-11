data "terraform_remote_state" "sqs" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "sqs"
    }
  }
}

output "sqs" {
    value = data.terraform_remote_state.sqs.outputs
}