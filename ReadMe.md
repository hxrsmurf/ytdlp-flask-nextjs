# Welcome

This is just a pet project to learn more about [Python Flask](https://flask.palletsprojects.com/en/2.1.x/) and [NextJS](https://nextjs.org/).

The backend is Python Flask and the frontend is NextJS. The database is [Firestore](https://cloud.google.com/firestore/).

For now...
- This just links the YouTube Video's URL which you can click on.
- I just run `python backend\python.py` and `npm run build && npm run start`


## Inspiration / Based On
This is heavily based on / inspired by the below GitHub Repos.
- https://github.com/Tzahi12345/YoutubeDL-Material
- https://github.com/yt-dlp/yt-dlp
- https://github.com/ytdl-org/youtube-dl
- https://gitlab.com/osp-group/flask-nginx-rtmp-manager
- https://github.com/tubearchivist/tubearchivist

## Why?

I click "subscribe" on a lot of channels I enjoy watching. I even click that bell icon! A few months (or was it years) ago YouTube stopped sending e-mail notifications for when new videos were uploaded. I (try to) practice inbox zero and used that to tune-in. Since that, I've had to use the notification bell on the mobile app or website, which is very cumbersome.

I also want to learn more about Python Flask and NextJS!

While YouTubeDL-Material & TubeArchivist are great projects, I wanted something more lightweight and geared towards "serverless".


## To Do

- [X] [Using Mongo](https://github.com/hxrsmurf/ytdlp-flask-nextjs/pull/13) ~~[Using Firebase](https://github.com/hxrsmurf/ytdlp-flask-nextjs/pull/5)~~ ~~Migrate from SQLite to Serverless Database (DynamoDB, Firestore)~~
- [ ] Add download functionality to local storage and s3-compatible (BackBlaze B2)
- [ ] Add CDN functionality via CloudFlare or NGINX to cache videos
- [X] Added basic docker support ~~Dockerize~~
- [ ] CI/CD (?)
- [ ] Add badge metrics for issues, license, etc.
- [ ] Twilio integration (text the API to add channel)
- [ ] Web Browser extension like TubeArchivst
