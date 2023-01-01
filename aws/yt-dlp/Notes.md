# Lambda Runtimes

| Memory | Duration | Warm  | Notes  |
| ------ | -------- | ----- |------- |
| 128 MB | 6968 MS  | TRUE  |        |
| 128 MB | 7534 MS  | FALSE |        |
| 256 MB | 6677 MS  | ?     |        |
| 256 MB | 4709 MS  | ?     |        |
| 128 MB | 22989 MS |       |        |
| 10240 MB | 22989 MS |       |        |

# ThreadPool Run Times

| Location | Start | Stop | Total |
| -------- | ----- | ---- | ----- |
| Local | 9494.2582166 | 9527.8418547 | 33.583638100000826 |
| AWS | 9545.0321265 | 9568.7539713 | 23.721844800000326 |

# MultiProcessing Run Times

| Location | Start | Stop | Total |
| -------- | ----- | ---- | ----- |
| Local | 10316.5120111 | 10327.9452126 | 11.433201499999996 |
| Local | 10710.226 | 10721.9291217 | 11.703121700000338 |
| AWS | 10814.1933493 | 10844.9377323 | 30.744383000001108 |

# yt-dlp MP4 Encoding Run Times

| Location | Memory | Duration |
| - | - | - |
| AWS | 256 MB | 28504 MS |
| AWS | 128 MB | 58515 MS |


# Docs
- https://aws.amazon.com/blogs/media/processing-user-generated-content-using-aws-lambda-and-ffmpeg/