![GitHub issues](https://img.shields.io/github/issues-raw/hxrsmurf/ytdlp-flask-nextjs?style=for-the-badge)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/hxrsmurf/ytdlp-flask-nextjs?style=for-the-badge)


|  Folder |  Build | Last Commit |
| ------------ | ------------ | ------------ | 
| Frontend  | ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hxrsmurf/ytdlp-flask-nextjs/Node.js%20CI?style=for-the-badge) | ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/hxrsmurf/ytdlp-flask-nextjs/master?style=for-the-badge)  | |
| Backend | | |
| CodeQL  | ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hxrsmurf/ytdlp-flask-nextjs/CodeQL?style=for-the-badge)  | |

# Welcome

This is just a pet project to learn more about [Python Flask](https://flask.palletsprojects.com/en/2.1.x/) and [NextJS](https://nextjs.org/).

The backend is Python Flask and the frontend is NextJS. The database is [Firestore](https://cloud.google.com/firestore/).

For now...
- This just links the YouTube Video's URL which you can click on.
- I just run `python backend\python.py` and `npm run build && npm run start`

Read more of my [Notes](https://github.com/hxrsmurf/ytdlp-flask-nextjs/blob/master/docs/Notes.md)

## Inspiration / Based On
This is heavily based on / inspired by the below GitHub Repos.
- https://github.com/Tzahi12345/YoutubeDL-Material
- https://github.com/yt-dlp/yt-dlp
- https://github.com/ytdl-org/youtube-dl
- https://gitlab.com/osp-group/flask-nginx-rtmp-manager
- https://github.com/tubearchivist/tubearchivist
- https://github.com/ViewTube/viewtube-vue
- https://www.reddit.com/r/selfhosted/
- https://www.reddit.com/r/homelab/
- https://www.reddit.com/r/DataHoarder/

## Why?

I click "subscribe" on a lot of channels I enjoy watching. I even click that bell icon! A few months (or was it years) ago YouTube stopped sending e-mail notifications for when new videos were uploaded. I (try to) practice inbox zero and used that to tune-in. Since that, I've had to use the notification bell on the mobile app or website, which is very cumbersome.

I also want to learn more about Python Flask and NextJS!

While YouTubeDL-Material & TubeArchivist are great projects, I wanted something more lightweight and geared towards "serverless".

## Diagram
![image](https://user-images.githubusercontent.com/14148184/183228479-0798685e-d98b-465f-a514-9767c0edbfe4.png)

## To Do

Check [Project Board](https://github.com/users/hxrsmurf/projects/3/views/1)

- [X] [Using Mongo](https://github.com/hxrsmurf/ytdlp-flask-nextjs/pull/13) ~~[Using Firebase](https://github.com/hxrsmurf/ytdlp-flask-nextjs/pull/5)~~ ~~Migrate from SQLite to Serverless Database (DynamoDB, Firestore)~~
