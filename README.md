![logo](logo.png)

PDF to Google Docs - Docker Image
======================

[![Docker Pulls](https://img.shields.io/docker/pulls/femtopixel/pdf2gdocs.svg)](https://hub.docker.com/r/femtopixel/pdf2gdocs/)
[![Docker Stars](https://img.shields.io/docker/stars/femtopixel/pdf2gdocs.svg)](https://hub.docker.com/r/femtopixel/pdf2gdocs/)
[![PayPal donation](https://github.com/jaymoulin/jaymoulin.github.io/raw/master/ppl.png "PayPal donation")](https://www.paypal.me/jaymoulin)
[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png "Buy me a coffee")](https://www.buymeacoffee.com/jaymoulin)
[![Buy me a coffee](https://storage.ko-fi.com/cdn/kofi2.png "Buy me a coffee")](https://www.ko-fi.com/jaymoulin)

DISCLAIMER: As-of 2021, this product does not have a free support team anymore. If you want this product to be maintained, please support.

(This product is available under a free and permissive license, but needs financial support to sustain its continued improvements. In addition to maintenance and stability there are many desirable features yet to be added.)

Description
-----------

The purpose of this image is to convert a PDF file to a Google Doc.
With this specific method, a file can be archived without using Google Drive quota.

Installation
------------

1. Go to https://developers.google.com/docs/api/quickstart/python
1. Click the _Enable the Google Docs Api_ button 
1. Click the _Download configuration_ button
1. Go to https://console.developers.google.com/apis/library/drive.googleapis.com
1. Enable the Google Drive API service
1. Init the container `docker run --name pdf2gdocs -it -v /path/to/your/pdf/folder:/upload -v /path/to/your/credentials:/credentials --net=host femtopixel/pdf2gdocs`
1. Click the link given by the application and follow the instructions (you may be block by your browser for an unsafe URL, proceed anyway)

Each time you want to upload your pdf
```
docker start pdf2gdocs
```
