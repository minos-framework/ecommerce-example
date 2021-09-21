FROM ghcr.io/clariteia/minos:0.1.4 as development

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root
COPY . .
CMD ["poetry", "run", "microservice", "start"]

FROM development as build
RUN poetry export --without-hashes > req.txt && pip wheel -r req.txt --wheel-dir ./dist
RUN poetry build --format wheel

FROM python:slim as production
COPY --from=build /microservice/dist/ ./dist
RUN pip install --no-deps ./dist/*
COPY ./config.yml ./config.yml
ENTRYPOINT ["microservice"]
CMD ["start"]