VERSION ?= 1.0.1
CACHE ?= --no-cache=1

all: build publish
build:
	docker buildx build --platform linux/arm/v7,linux/arm64/v8,linux/amd64,linux/386,linux/arm/v6 ${PUSH} --build-arg VERSION=${VERSION} --tag femtopixel/pdf2gdocs --tag femtopixel/pdf2gdocs:${VERSION} ${CACHE} .
publish:
	PUSH=--push CACHE= make build
