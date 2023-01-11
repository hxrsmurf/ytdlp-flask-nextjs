data "terraform_remote_state" "layers" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "layers"
    }
  }
}

output "layers" {
    value = data.terraform_remote_state.layers.outputs
}