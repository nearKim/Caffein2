FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /src/requirements.txt /config/
RUN pip install -r /config/requirements.txt
WORKDIR /src
