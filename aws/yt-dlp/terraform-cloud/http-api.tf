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

  connection_type        = "INTERNET"
  description            = "API for ParseURL - Managed by Terraform"
  integration_method     = "POST"
  integration_uri        = module.parse-url.invoke_arn
  passthrough_behavior   = "WHEN_NO_MATCH"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_stage" "parse-url" {
  api_id      = aws_apigatewayv2_api.parse-url.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_domain_name" "api-yt" {
  domain_name = "api-yt.homelabwithkevin.com"

  domain_name_configuration {
    certificate_arn = "arn:aws:acm:us-east-1:195663387853:certificate/5df5b17a-4480-42cb-a5c3-9f7a60769530"
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  timeouts {}
}

resource "aws_apigatewayv2_api_mapping" "api-yt" {
  api_id      = aws_apigatewayv2_api.parse-url.id
  domain_name = aws_apigatewayv2_domain_name.api-yt.id
  stage       = aws_apigatewayv2_stage.parse-url.id
}

output "api-parse-url" {
  value = aws_apigatewayv2_api.parse-url.api_endpoint
}