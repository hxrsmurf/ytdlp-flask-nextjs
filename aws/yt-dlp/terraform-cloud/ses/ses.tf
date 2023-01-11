resource "aws_ses_email_identity" "yt-dlp" {
  email = "yt-dlp@homelabwithkevin.com"
}

output "ses" {
  value = aws_ses_email_identity.yt-dlp
}