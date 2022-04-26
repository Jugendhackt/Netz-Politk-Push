FROM python:3.7-slim AS base

RUN pip install pipenv
RUN apt update && apt install -y --no-install-recommends gcc

FROM base AS runtime
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
RUN pip install flask feedparser requests summarizer bs4 datetime apscheduler
COPY Docker/ .
ENTRYPOINT ["python","start.py"]
