import pickle
import os.path
from urllib.parse import urlparse
from functools import lru_cache

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

@lru_cache(1)
def token_file_path():
    basename = '+'.join([urlparse(scope).path.split('/')[-1] for scope in SCOPES])
    return '{}.pickle'.format( basename )


def load_credentials():
    if os.path.exists(token_file_path()):
        with open(token_file_path(), 'rb') as token:
            return pickle.load(token)
    return None


def update_credentials(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open(token_file_path(), 'wb') as token:
        pickle.dump(creds, token)

    return creds


def get_credentials():
    creds = load_credentials()
    return creds if creds and creds.valid else update_credentials(creds)


def create_service():
    return build('gmail', 'v1', credentials=get_credentials())
