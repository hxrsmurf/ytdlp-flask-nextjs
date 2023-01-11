data "terraform_remote_state" "policy" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "policy"
    }
  }
}

output "policy" {
    value = data.terraform_remote_state.policy.outputs
}