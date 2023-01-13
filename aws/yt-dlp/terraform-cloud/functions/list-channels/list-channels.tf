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

module "role-eventbridge" {
    source = "../../modules/eventbridge-role"
    name = "list-channels-eventbridge-tf"
    lambda-arn = module.list-channels.arn
}

resource "aws_scheduler_schedule" "list-channels" {
    group_name                   = "default"
    name                         = "list-channels-tf"
    schedule_expression          = "rate(1 hours)"
    schedule_expression_timezone = "America/Detroit"
    state                        = "ENABLED"

    flexible_time_window {
        mode                      = "OFF"
    }

    target {
        arn      = module.list-channels.arn
        input    = jsonencode({})
        role_arn = module.role-eventbridge.arn

        retry_policy {
            maximum_event_age_in_seconds = 86400
            maximum_retry_attempts       = 0
        }
    }
}