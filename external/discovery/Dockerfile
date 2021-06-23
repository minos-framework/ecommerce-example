FROM python

RUN apt install git
RUN pip install git+git://github.com/Clariteia/discovery.git@1f9f78dabce75b027ff266f5eb34871206a8faa4

COPY config.yml ./config.yml
CMD ["discovery", "start", "config.yml"]
