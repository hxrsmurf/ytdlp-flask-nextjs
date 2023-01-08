resource "cloudflare_record" "api-yt" {
  zone_id = var.cloudflare-zone-id
  name    = "api-yt"
  value   = trim("${aws_apigatewayv2_api.parse-url.api_endpoint}", "https://")
  type    = "CNAME"
}