FROM python:3.9-slim
WORKDIR /tavern/
RUN pip install pytest tavern
COPY ./tests ./tests
CMD ["pytest", "--verbose", "--tavern-strict", "json"]
