# coding=utf-8

from googleapiclient.discovery import build
from greenformatics_ds2_utils.connector.google.sheets.repository import read_spreadsheet

def get_spreadsheet_service(creds):
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()

    return sheet
