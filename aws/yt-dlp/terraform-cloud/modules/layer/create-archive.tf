resource "null_resource" "directory" {
    provisioner "local-exec" {
        command = "mkdir -p layers/${var.package-name}"
    }
}

resource "local_file" "file" {
    content  = var.package-name
    filename = "layers/${var.package-name}/requirements.txt"
    depends_on = [null_resource.directory]
}

resource "null_resource" "pip" {
    provisioner "local-exec" {
        command = "cd layers/${var.package-name} && pip3 install -r requirements.txt -t ./python"
    }
    depends_on = [local_file.file]
}

data "archive_file" "archive" {
  type        = "zip"
  source_dir = "./layers/${var.package-name}"
  output_path = "./files/${var.package-name}.zip"
  depends_on = [null_resource.pip]
}