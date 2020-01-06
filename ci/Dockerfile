FROM alpine:3.11

RUN apk add --no-cache --update curl

ADD ci/entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
