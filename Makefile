VERSION ?= 1.0.0
CACHE ?= --no-cache=1
FULLVERSION ?= 1.0.0
archs ?= amd64 arm32v6 arm64v8 i386
.PHONY: all build publish latest version
all: build publish
build:
	cp -R /usr/bin/qemu-*-static .
	$(foreach arch,$(archs), \
		cat Dockerfile | sed "s/FROM python:alpine/FROM $(arch)\/python:alpine/g" > .build; \
		docker build -t femtopixel/pdf2gdocs:${VERSION}-$(arch) -f .build --build-arg VERSION=${VERSION}-$(arch) ${CACHE} .;\
	)
publish:
	docker push femtopixel/pdf2gdocs -a
	cat manifest.yml | sed "s/\$$VERSION/${VERSION}/g" > manifest2.yaml
	cat manifest2.yaml | sed "s/\$$FULLVERSION/${FULLVERSION}/g" > manifest.yaml
	manifest-tool push from-spec manifest.yaml
latest: build
	cat manifest.yml | sed "s/\$$VERSION/${VERSION}/g" > manifest2.yaml
	cat manifest2.yaml | sed "s/\$$FULLVERSION/latest/g" > manifest.yaml
	manifest-tool push from-spec manifest.yaml
