FROM python

RUN apt install git
RUN pip install git+git://github.com/Clariteia/discovery.git@e8597f5f0925d3de113ea8182fead1ec82134b80

COPY config.yml ./config.yml
CMD ["discovery", "start", "config.yml"]
