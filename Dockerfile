FROM python:2

MAINTAINER fanwei.zeng

ENV PYTHONUNBUFFERED 1

ADD . /site/
WORKDIR /site/
COPY etc/pip.conf /etc/pip.conf
RUN pip install -r requirements.txt

ENV PYTHONPATH $PYTHONPATH:/site
CMD ["gunicorn", "-k", "eventlet", "-w", "4", "-b", "0.0.0.0:8080", "redis_funnel.mgmt.app:app"]

EXPOSE 8080
