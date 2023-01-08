data "archive_file" "init" {
  type        = "zip"
  source_dir = "files"
  output_path = "extension.zip"
}