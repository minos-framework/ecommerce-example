FROM ghcr.io/clariteia/minos:0.1.0 as build
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry export --without-hashes > req.txt && pip wheel -r req.txt --wheel-dir ./dist
COPY . .
RUN poetry build --format wheel

FROM python:slim as production
COPY --from=build /microservice/dist/ ./dist
RUN pip install --no-deps ./dist/*
COPY ./config.yml ./config.yml
CMD ["microservice", "start"]