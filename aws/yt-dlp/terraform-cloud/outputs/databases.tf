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

output "database-urls" {
  value = {
    channels = "https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=${data.terraform_remote_state.databases.outputs.channels.name}"
    videos   = "https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name=${data.terraform_remote_state.databases.outputs.videos.name}"
  }
}