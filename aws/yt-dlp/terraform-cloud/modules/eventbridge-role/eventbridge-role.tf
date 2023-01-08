
variable "name" {}
variable "lambda-arn" {}

output "arn" {
  value = aws_iam_role.role.arn
}

resource "aws_iam_role" "role" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "scheduler.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )
  managed_policy_arns  = []
  max_session_duration = 3600
  name                 = var.name
  path                 = "/"

  inline_policy {
    name = "EventBridge"
    policy = jsonencode(
      {
        Statement = [
          {
            Action   = "lambda:InvokeFunction"
            Effect   = "Allow"
            Resource = var.lambda-arn
          },
        ]
      }
    )
  }
}
