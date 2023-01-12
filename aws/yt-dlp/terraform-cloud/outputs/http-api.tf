data "terraform_remote_state" "http-api" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "http-api"
    }
  }
}

output "http-api" {
    value = data.terraform_remote_state.http-api.outputs
}