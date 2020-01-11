FROM python:3.8-alpine3.11 AS base

# builder
FROM base AS builder

ADD requirements.txt /

RUN apk add \
      build-base \
      linux-headers \
      pcre-dev \
    && pip3 install --prefix=/install -r /requirements.txt

# prod
FROM base AS prod

ADD https://raw.githubusercontent.com/spektom/dropbox-upload/master/dropbox-upload.py /

RUN apk add --no-cache --update \
      nginx \
      sqlite \
    && sed -i 's/nginx:x:100/nginx:x:1000/' /etc/passwd \
    && chown -R nginx /var/lib/nginx \
    && chown -R nginx /var/log/nginx \
    && mkdir -p /run/nginx \
    && chown nginx /run/nginx \
    && chmod 755 /dropbox-upload.py

COPY --from=builder /install /usr/local

ADD tldr /tldr
ADD *.py /
ADD deploy/nginx.conf /etc/nginx/conf.d/default.conf
ADD deploy/wsgi.ini /
ADD deploy/entrypoint.sh /

USER 1000
EXPOSE 80
WORKDIR /

ENTRYPOINT ["/entrypoint.sh"]
