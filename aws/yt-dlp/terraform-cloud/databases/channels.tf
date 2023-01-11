resource "aws_dynamodb_table" "channels" {
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "id"
    name           = "yt-dlp-channels-tf"
    read_capacity  = 0
    stream_enabled = false
    write_capacity = 0

    attribute {
        name = "id"
        type = "S"
    }

    attribute {
        name = "channel"
        type = "S"
    }

    global_secondary_index {
        hash_key           = "id"
        name               = "id-channel-index"
        non_key_attributes = []
        projection_type    = "ALL"
        range_key          = "channel"
        read_capacity      = 0
        write_capacity     = 0
    }
}

output "channels" {
    value = aws_dynamodb_table.channels.arn
}