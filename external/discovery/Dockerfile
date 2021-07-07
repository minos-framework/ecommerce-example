FROM python

RUN apt install git
RUN pip install git+git://github.com/Clariteia/discovery.git@4e8b7b4170d9f41028421b3e810242cefd42c91a

COPY config.yml ./config.yml
CMD ["discovery", "start", "config.yml"]
