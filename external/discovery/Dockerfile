FROM python:slim

RUN pip install minos-discovery

COPY config.yml ./config.yml
CMD ["discovery", "start", "config.yml"]
