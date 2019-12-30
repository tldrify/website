FROM python:3-alpine

ADD requirements.txt /

RUN apk add --no-cache --update \
      mariadb-connector-c \
      python3 \
      py3-pip \
      nginx \
    && apk add --no-cache --virtual .build-deps \
      build-base \
      linux-headers \
      mariadb-connector-c-dev \
      mariadb-dev \
      pcre-dev \
    && pip3 --no-cache-dir install --ignore-installed -r /requirements.txt \
    && pip3 --no-cache-dir install uwsgi \
    && apk del .build-deps \
    && mkdir -p /run/nginx

ADD tldr /tldr
ADD *.py /
ADD docker/nginx.conf /etc/nginx/conf.d/default.conf
ADD docker/wsgi.ini /
ADD docker/entrypoint.sh /

ENV MARIADB_PLUGIN_DIR=/usr/lib/mariadb/plugin

EXPOSE 80
WORKDIR /
ENTRYPOINT ["/entrypoint.sh"]
