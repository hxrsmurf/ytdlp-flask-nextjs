curl --request POST \
     --url https://video.bunnycdn.com/library/VIDEOLIBRARYID/videos \
     --header 'Accept: application/json' \
     --header 'AccessKey: ACCESSKEY' \
     --header 'Content-Type: application/*+json' \
     --data '{"title":"555555555555555"}'

curl -vv --request PUT \
     --url 'https://video.bunnycdn.com/library/VIDEOLIBRARYID/videos/VIDEOID?enabledResolutions=1080' \
     --header 'Accept: application/json' \
     --header 'AccessKey: ACCESSKEY' \
     --data-binary '@VIDEOID.mp4'

curl --request GET \
     --url 'https://video.bunnycdn.com/library/VIDEOLIBRARYID/videos/VIDEOID' \
     --header 'Accept: application/json' \
     --header 'AccessKey: ACCESSKEY' \

$headers=@{}
$headers.Add("Accept", "application/json")
$headers.Add("AccessKey", "ACCESSKEY")
$response = Invoke-WebRequest -Uri 'https://video.bunnycdn.com/library/VIDEOLIBRARYID/videos/VIDEOID?enabledResolutions=1080' -Method PUT -Headers $headers -InFile 'IlF3oFqVt1c.mp4'


curl --request PUT --url 'https://video.bunnycdn.com/library/VIDEOLIBRARYID/videos/VIDEOID?enabledResolutions=1080' --header 'Accept: application/json' --header 'AccessKey: ACCESSKEY' --data-binary 'VIDEOID.mp4'