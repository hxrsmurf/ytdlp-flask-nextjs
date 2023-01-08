resource "aws_apigatewayv2_api" "parse-url" {
  name          = "yt-dlp-ParseUrl-tf"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_route" "parse-url" {
  api_id    = aws_apigatewayv2_api.parse-url.id
  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.parse-url.id}"
}

resource "aws_apigatewayv2_integration" "parse-url" {
  api_id           = aws_apigatewayv2_api.parse-url.id
  integration_type = "AWS_PROXY"

  connection_type           = "INTERNET"
  description               = "API for ParseURL - Managed by Terraform"
  integration_method        = "POST"
  integration_uri           = module.parse-url.invoke_arn
  passthrough_behavior      = "WHEN_NO_MATCH"
  payload_format_version    = "2.0"
}

resource "aws_apigatewayv2_stage" "parse-url" {
  api_id = aws_apigatewayv2_api.parse-url.id
  name   = "$default"
  auto_deploy = true
}