FROM alpine

COPY cronjobs /etc/crontabs/root
COPY docker.sh /root/docker.sh
COPY standalone.py /root/standalone.py

RUN chmod +x /root/standalone.py
RUN chmod +x /root/docker.sh

CMD ["crond", "-f", "-d", "8"]