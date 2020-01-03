FROM python:3.8-alpine3.11 AS base

# builder
FROM base AS builder

ADD requirements.txt /

RUN apk add \
      build-base \
      linux-headers \
      mariadb-connector-c-dev \
      mariadb-dev \
      pcre-dev \
    && pip3 install --prefix=/install -r /requirements.txt

# prod
FROM base AS prod

RUN apk add --no-cache --update \
      mariadb-connector-c \
      nginx \
    && mkdir -p /run/nginx

COPY --from=builder /install /usr/local

ADD tldr /tldr
ADD *.py /
ADD deploy/nginx.conf /etc/nginx/conf.d/default.conf
ADD deploy/wsgi.ini /
ADD deploy/entrypoint.sh /

ENV MARIADB_PLUGIN_DIR=/usr/lib/mariadb/plugin

EXPOSE 80
WORKDIR /

ENTRYPOINT ["/entrypoint.sh"]
