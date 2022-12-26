FROM python:alpine

COPY qemu-* /usr/bin/
COPY . /app
WORKDIR /app
ARG VERSION=v1.0.0
LABEL maintainer="Jay MOULIN <https://twitter.com/MoulinJay>"
LABEL version=${VERSION}
RUN apk add imagemagick --no-cache --update && pip install -e .
CMD /app/pdf2gdocs/pdf2gdocs.py
