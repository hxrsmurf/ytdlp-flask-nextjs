# Description
I'm wanting to have a Serverless method to get the latest videos from all of the YouTube Channels I like to watch.

# Flow

1. Hourly EventBridge triggers `ListChannels` Lambda function
2. `ListChannels` function queries DynamoDB for all Channels and sends to SQS
3. SQS triggers `SQSParser` Lambda function
4. `SQSParser` function uses `yt-dlp` to download the channel's information and gets the latest uploaded video (entry)
5. `SQSParser` function compares the new info with DynamoDB's info, if different, update database else pass