FROM python:3.6

RUN pip install \
  lxml==4.2.1 \
  selenium==3.11.0 \
  python-dateutil==2.7.2 \
  pymongo==3.6.1
