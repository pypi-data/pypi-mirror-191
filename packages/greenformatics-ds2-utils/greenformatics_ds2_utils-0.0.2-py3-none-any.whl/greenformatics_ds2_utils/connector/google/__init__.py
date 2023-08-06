# coding=utf-8

from google.oauth2.credentials import Credentials as OAuth2Credential
import google.auth
from os import environ
import json


def get_google_api_oauth2_connection(client_config, scopes):
    return OAuth2Credential.from_authorized_user_info(client_config, scopes)


def get_google_api_adc_connection(scopes):
    return google.auth.default(scopes=scopes)


def create_google_config_json(file, client_id, client_secret, quota_project_id, refresh_token):
    conf = {
        "client_id": client_id,
        "client_secret": client_secret,
        "quota_project_id": quota_project_id,
        "refresh_token": refresh_token,
        "type": "authorized_user"
    }
    with open(file, 'w') as token:
        json.dump(conf, token)
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = file
