FROM python:alpine AS builder

RUN apk add --no-cache mongodb-tools py3-pip
RUN pip install b2
RUN mkdir /tmp/backups

FROM builder

ARG B2_APPLICATION_KEY_ID
ARG B2_APPLICATION_KEY
ENV B2_APPLICATION_KEY_ID=${B2_APPLICATION_KEY_ID}
ENV B2_APPLICATION_KEY=${B2_APPLICATION_KEY}

COPY cronjobs /etc/crontabs/root
COPY backup.sh /root/backup.sh

RUN b2 authorize-account $B2_APPLICATION_KEY_ID $B2_APPLICATION_KEY
RUN chmod +x /root/backup.sh

CMD ["crond", "-f", "-d", "8"]