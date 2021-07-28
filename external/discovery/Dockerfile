FROM python

RUN apt install git
RUN pip install minos-discovery==0.0.3

COPY config.yml ./config.yml
CMD ["discovery", "start", "config.yml"]
