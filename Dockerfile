FROM python:3.7-slim AS base

RUN pip install pipenv
RUN apt update && apt install -y --no-install-recommends gcc cron


FROM base AS runtime
RUN useradd --create-home appuser
WORKDIR /home/appuser
RUN echo 'su appuser -c "python /home/appuser/backend.py"' > '/root/event.sh'
RUN chmod +x /root/event.sh
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

USER appuser
RUN pip install flask feedparser requests summarizer bs4 datetime
COPY Docker/ .
CMD cron
ENTRYPOINT ["python","webapp.py"]
