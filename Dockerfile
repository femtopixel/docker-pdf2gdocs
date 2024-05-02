FROM python:alpine

COPY . /app
WORKDIR /app
ARG VERSION=v1.0.0
ARG TARGETPLATFORM
LABEL maintainer="Jay MOULIN <https://twitter.com/MoulinJay>"
LABEL version=${VERSION}-${TARGETPLATFORM}
RUN apk add imagemagick --no-cache --update && pip install -e .
CMD /app/pdf2gdocs/pdf2gdocs.py
