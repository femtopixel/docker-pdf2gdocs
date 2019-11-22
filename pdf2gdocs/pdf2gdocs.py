#!/usr/bin/env python
# coding: utf-8

import logging
import os
import glob
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

DIRECTORY = '/upload'
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
PORT = int(os.environ.get('PORT', 0))


def get_credentials(port: int = 0):
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/credentials/token.pickle'):
        with open('/credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('/credentials/credentials.json'):
                raise FileNotFoundError(
                    'credentials.json does not exist. ' +
                    'Please follow README instruction ' +
                    '(and go to https://developers.google.com/docs/api/quickstart/python)'
                )
            flow = InstalledAppFlow.from_client_secrets_file('/credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=port)
        # Save the credentials for the next run
        with open('/credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def upload_images(files, logger):
    drive = build('drive', 'v3', credentials=get_credentials(PORT))
    uploaded_files = []
    file_metadata = {'name': 'photo.png'}
    batch = drive.new_batch_http_request()
    user_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    logger.info('Uploading images')
    for file in files:
        logger.info('Uploading %s' % file)
        media = MediaFileUpload(file, mimetype='image/png')
        file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
        batch.add(
            drive.permissions().create(
                fileId=file.get('id'),
                body=user_permission,
                fields='id',
            )
        )
        uploaded_files.append(file.get('id'))
    logger.info('Allowing images access')
    batch.execute()
    return uploaded_files


def delete_uploaded_files(uploaded_files, logger):
    drive = build('drive', 'v3', credentials=get_credentials(PORT))
    logger.info('Deleting uploaded images')
    for file_id in uploaded_files:
        logger.info('Deleting %s' % file_id)
        drive.files().delete(fileId=file_id).execute()


def create_document(title, files, logger):
    docs = build('docs', 'v1', credentials=get_credentials(PORT))
    uploaded_files = upload_images(files, logger)
    doc = docs.documents().create(body={'title': title}).execute()

    # raise ValueError(doc)
    requests_list = [{
        'updateDocumentStyle': {
            'documentStyle': {
                'marginTop': {
                    'magnitude': 0,
                    'unit': 'PT',
                },
                'marginBottom': {
                    'magnitude': 0,
                    'unit': 'PT',
                },
                'marginRight': {
                    'magnitude': 0,
                    'unit': 'PT',
                },
                'marginLeft': {
                    'magnitude': 0,
                    'unit': 'PT',
                },
            },
            'fields': 'marginTop,marginBottom,marginRight,marginLeft',
        },
    }]
    for file_id in uploaded_files:
        requests_list.append({
            'insertInlineImage': {
                'location': {
                    'index': 1
                },
                'uri':
                    'https://docs.google.com/uc?id=' + file_id,
                'objectSize': {
                    'height': {
                        'magnitude': 848,
                        'unit': 'PT'
                    },
                    'width': {
                        'magnitude': 595,
                        'unit': 'PT'
                    }
                }
            }
        })
    logger.info('Creating document')
    docs.documents().batchUpdate(documentId=doc.get('documentId'), body={'requests': requests_list}).execute()
    delete_uploaded_files(uploaded_files, logger)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    files = [file for file in glob.glob(glob.escape(DIRECTORY) + '/**/*', recursive=True)]
    for file_path in files:
        logger.info("Converting %s" % file_path)
        bashCommand = 'convert -quality 100 -density 150 ' + file_path + ' /app/tmp/%04d.png'
        os.system(bashCommand)
        files_images = sorted(
            [file_image for file_image in glob.glob(glob.escape('/app/tmp') + '/**/*', recursive=True)],
            reverse=True
        )
        create_document(title=os.path.basename(file_path), files=files_images, logger=logger)
        logger.info("Removing %s" % file_path)
        os.remove(file_path)
        for file in files_images:
            logger.info('Removing %s' % file)
            os.remove(file)
        logger.info("Done %s" % file_path)
