import base64
import re
import os

B2_KEY_ID = os.environ['B2_KEY_ID']
B2_KEY = os.environ['B2_KEY']
B2_BUCKET = os.environ['B2_BUCKET']
BUNNYCDN_LIBRARY = os.environ['BUNNYCDN_LIBRARY']
BUNNYCDN_KEY = os.environ['BUNNYCDN_KEY']

def convert(video_id, bunnycdn_guid):
    data = f'\
    #!/bin/bash\n\
    apt-get update\n\
    #apt-get install python pip ffmpeg docker.io -yf\n\
    apt-get install python pip ffmpeg curl -yf\n\
    pip install yt-dlp b2\n\
    cd /root/\n\
    yt-dlp --format bestvideo*+bestaudio/best --merge-output-format mp4 --output \'%(id)s/%(id)s.%(ext)s\' https://youtu.be/{video_id}\n\
    b2 authorize-account {B2_KEY_ID} {B2_KEY}\n\
    b2 sync {video_id} b2://{B2_BUCKET}/videos/{video_id}\n\
    cd {video_id}\n\
    curl --location --request PUT \'https://video.bunnycdn.com/library/{BUNNYCDN_LIBRARY}/videos/{bunnycdn_guid}\' \
    --header \'Accept: application/json\' \
    --header \'Content-Type: application/json\' \
    --header \'AccessKey: {BUNNYCDN_KEY}\' \
    --header \'Transfer-Encoding: chunked\' \
    --upload-file \'{video_id}.mp4\'\n\
    sudo shutdown -h now\
    '
    print(data)
    return(re.sub(r"    ", "", data))

def convert_base64(data):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.run_instances
    # This value will be base64 encoded automatically. Do not base64 encode this value prior to performing the operation.

    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    return(encodedStr)