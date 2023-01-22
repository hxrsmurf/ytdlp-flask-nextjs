data "terraform_remote_state" "sns" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "sns"
    }
  }
}

output "sns" {
    value = data.terraform_remote_state.sns.outputs
}