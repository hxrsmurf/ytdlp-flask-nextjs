FROM python:alpine AS builder

RUN apk add --no-cache curl mongodb-tools py3-pip
RUN pip install b2

FROM builder

ARG B2_APPLICATION_KEY_ID
ARG B2_APPLICATION_KEY
ENV B2_APPLICATION_KEY_ID=${B2_APPLICATION_KEY_ID}
ENV B2_APPLICATION_KEY=${B2_APPLICATION_KEY}

RUN b2 authorize-account $B2_APPLICATION_KEY_ID $B2_APPLICATION_KEY
COPY cronjobs /etc/crontabs/root

CMD ["crond", "-f", "-d", "8"]