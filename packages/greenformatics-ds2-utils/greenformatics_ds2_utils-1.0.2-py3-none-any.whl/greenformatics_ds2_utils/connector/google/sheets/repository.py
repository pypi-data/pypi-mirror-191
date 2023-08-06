# coding=utf-8

def read_spreadsheet(sheet, spreadsheet_id, range_name):
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return

    return values
