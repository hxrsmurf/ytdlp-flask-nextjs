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

output "arn-default-lambda-execution" {
  value = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}