output "list-channels" {
  value = module.list-channels
}

output "eventbridge" {
  value = "https://us-east-1.console.aws.amazon.com/scheduler/home?region=us-east-1#schedules/default/${aws_scheduler_schedule.list-channels.name}"
}