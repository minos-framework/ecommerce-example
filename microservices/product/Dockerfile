FROM ghcr.io/clariteia/minos:1.0 as build

RUN poetry build

FROM debian:buster as production

COPY --from=build /microservice/dist/ ./dist
