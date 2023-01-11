data "terraform_remote_state" "databases" {
  backend = "remote"

  config = {
    organization = "yt-dlp"
    workspaces = {
      name = "databases"
    }
  }
}

output "databases" {
    value = data.terraform_remote_state.databases.outputs
}