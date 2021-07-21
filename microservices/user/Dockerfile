FROM ghcr.io/clariteia/minos:0.1.0 as development

# Install dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root
COPY . .
CMD ["python", "-m", "src", "start"]

FROM development as build
RUN poetry export --without-hashes > req.txt && pip wheel -r req.txt --wheel-dir ./dist
RUN poetry build --format wheel

FROM python:slim as production
COPY --from=build /microservice/dist/ ./dist
RUN pip install --no-deps ./dist/*
COPY ./config.yml ./config.yml
ENTRYPOINT ["microservice"]
CMD ["start"]