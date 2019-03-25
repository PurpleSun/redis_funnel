FROM python:2

MAINTAINER fanwei.zeng

ENV PYTHONUNBUFFERED 1

ADD . /site/
WORKDIR /site/
COPY etc/pip.conf /etc/pip.conf
RUN pip install -r requirements.txt

ENV PYTHONPATH $PYTHONPATH:/site
CMD ["python", "redis_funnel/mgmt/app.py"]

EXPOSE 8080
