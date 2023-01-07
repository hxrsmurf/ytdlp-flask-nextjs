# aws_dynamodb_table.videos:
resource "aws_dynamodb_table" "videos" {
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "id"
    name           = "nextjs-13-yt-dlp-videos-tf"
    read_capacity  = 0
    stream_enabled = false
    tags           = {}
    tags_all       = {}
    write_capacity = 0

    attribute {
        name = "id"
        type = "S"
    }

    attribute {
        name = "upload_date"
        type = "S"
    }

    global_secondary_index {
        hash_key           = "id"
        name               = "id-upload_date-index"
        non_key_attributes = []
        projection_type    = "ALL"
        range_key          = "upload_date"
        read_capacity      = 0
        write_capacity     = 0
    }

    point_in_time_recovery {
        enabled = false
    }

    timeouts {}
}

# aws_dynamodb_table.channels:
resource "aws_dynamodb_table" "channels" {
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "id"
    name           = "nextjs-13-yt-dlp-channels-tf"
    read_capacity  = 0
    stream_enabled = false
    tags           = {}
    tags_all       = {}
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

    point_in_time_recovery {
        enabled = false
    }

    timeouts {}
}