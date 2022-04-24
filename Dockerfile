FROM python:3.7-slim AS base

RUN pip install pipenv
RUN apt update && apt install -y --no-install-recommends gcc cron


FROM base AS runtime
RUN useradd --create-home appuser
WORKDIR /home/appuser
COPY Pipfile .
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
USER appuser
RUN pipenv install --deploy
RUN pip install flask
COPY ./src/backend.py .
COPY ./Website ./Website


ENTRYPOINT ["python","Website/webapp.py"]
CMD ["cron","-f"]
