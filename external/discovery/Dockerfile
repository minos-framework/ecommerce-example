FROM python:slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN pip install minos-discovery

COPY config.yml ./config.yml
CMD ["discovery", "start", "config.yml"]
