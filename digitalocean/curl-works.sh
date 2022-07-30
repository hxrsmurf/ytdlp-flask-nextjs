curl --request POST \
     --url https://video.bunnycdn.com/library/LIBRARYID/videos \
     --header 'Accept: application/json' \
     --header 'AccessKey: ACCESSKEY' \
     --header 'Content-Type: application/*+json' \
     --data '{"title":"python"}'

curl --location --request PUT 'https://video.bunnycdn.com/library/LIBRARYID/videos/VIDEOID' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'AccessKey: ACCESSKEY' \
--data-binary '@VIDEOID.mp4'