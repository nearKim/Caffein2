FROM ubuntu:16.04

MAINTAINER garfield@snu.ac.kr

ENV PYTHONUNBUFFERED 1

# Local directory for source codes
ENV CAFFEIN_SRC=/src
ENV CAFFEIN_SEED_SRC=/seeds
ENV CAFFEIN_CONFIG_SRC=/config

# Directory in container for source codes
ENV DOCKYARD_SRVHOME=/data
ENV DOCKYARD_SRVPROJ=$DOCKYARD_SRVHOME/$CAFFEIN_SRC

# Install dependencies
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip
RUN alias python='python3'
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nginx

# Install requirements and set initial settings
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media logs
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Copy application source code and seeds to SRC DIR
COPY $CAFFEIN_SRC $DOCKYARD_SRVPROJ
COPY $CAFFEIN_SEED_SRC $DOCKYARD_SRVHOME/seeds/

# Install dependencies
RUN pip3 install -r $DOCKYARD_SRVPROJ/requirements.txt

EXPOSE 8000

# Copy entrypoint to image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./entrypoint.sh /
COPY ./config/nginx/caffein.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/caffein.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

ENTRYPOINT ["/entrypoint.sh"]