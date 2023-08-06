# coding=utf-8

from google.oauth2.credentials import Credentials as OAuth2Credential
import google.auth
from os import environ
import json


def get_google_api_oauth2_connection(client_config, scopes):
    return OAuth2Credential.from_authorized_user_info(client_config, scopes)


def get_google_api_adc_connection(scopes):
    return google.auth.default(scopes=scopes)


# Aliasing get_google_api_adc_connection function
get_google_api_service_account_connection = get_google_api_adc_connection


def create_google_adc_config_json(file, client_id, client_secret, quota_project_id, refresh_token):
    conf = {
        'client_id': client_id,
        'client_secret': client_secret,
        'quota_project_id': quota_project_id,
        'refresh_token': refresh_token,
        'type': 'authorized_user'
    }

    create_credential_file(file, conf)


def create_google_service_account_config_json(file, client_id, project_id, private_key_id, private_key, client_email,
                                              client_x509_cert_url):
    conf = {
        'client_id': client_id,
        'project_id': project_id,
        'private_key_id': private_key_id,
        'private_key': private_key,
        'client_email': client_email,
        'type': 'service_account',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
        'client_x509_cert_url': client_x509_cert_url
    }

    create_credential_file(file, conf)


def create_credential_file(file, conf):
    with open(file, 'w') as conf_json_file:
        dumped_json = json.dumps(conf)
        print(dumped_json.replace('\\\\', '\\'), file=conf_json_file)
    environ['GOOGLE_APPLICATION_CREDENTIALS'] = file
