FROM alpine:latest

RUN apk add --no-cache curl
COPY cronjobs /etc/crontabs/root

CMD ["crond", "-f", "-d", "8"]