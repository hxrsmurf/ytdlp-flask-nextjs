import base64

def convert(video_id):
    data = f'\
    #!/bin/bash\n\
    apt-get update\n\
    #apt-get install python pip ffmpeg docker.io -yf\n\
    apt-get install python pip ffmpeg -yf\n\
    pip install yt-dlp\n\
    cd /root/\n\
    yt-dlp --format bestvideo*+bestaudio/best --merge-output-format mp4 --output \'%(id)s/%(id)s.%(ext)s\' https://youtu.be/{video_id}\
    '
    return(data)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.run_instances
    # This value will be base64 encoded automatically. Do not base64 encode this value prior to performing the operation.

    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    print(encodedStr)