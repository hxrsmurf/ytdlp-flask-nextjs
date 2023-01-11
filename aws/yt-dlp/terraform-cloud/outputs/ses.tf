data "terraform_remote_state" "ses" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "ses"
    }
  }
}

output "ses" {
    value = data.terraform_remote_state.ses.outputs
}