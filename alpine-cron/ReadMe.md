# Welcome

This is a basic docker container to run `cron` in alpine.

I've got it doing a few things every 4-hours:

- Query my `latest` API to get the latest YouTube videos
- Backup the MongoDB with [mongodump](https://www.mongodb.com/docs/database-tools/mongodump/) and upload to [Backblaze B2](https://www.backblaze.com/b2/docs/quick_command_line.html)
