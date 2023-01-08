resource "aws_lambda_layer_version" "layer" {
  filename   = data.archive_file.archive.output_path
  # source_code_hash = data.archive_file.archive.output_path
  layer_name = var.name
  description = "${var.name} (python) - Created by Terraform"
  compatible_runtimes = ["python3.9"]
  depends_on = [
    data.archive_file.archive
  ]
}

output "arn" {
  value = aws_lambda_layer_version.layer.arn
}