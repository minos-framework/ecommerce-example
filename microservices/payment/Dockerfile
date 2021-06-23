#FROM ghcr.io/clariteia/minos:1.0 as build
#
#RUN poetry build
#
#FROM debian:buster as production
#
#COPY --from=build /microservice/dist/ ./dist

# START FIXME: must be on the base docker image for building.
FROM python:slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install --yes postgresql-client git curl netcat

# Install and setup poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

COPY . .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
## END FIXME

CMD ["microservice", "start"]