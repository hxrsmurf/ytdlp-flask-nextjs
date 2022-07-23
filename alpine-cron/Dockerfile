FROM python:alpine

ARG B2_KEY_ID=
ARG B2_APPLICATION_KEY=

RUN apk add --no-cache curl mongodb-tools
RUN pip install b2
run b2 authorize-account ${B2_KEY_ID} ${B2_APPLICATION_KEY}
COPY cronjobs /etc/crontabs/root

CMD ["crond", "-f", "-d", "8"]