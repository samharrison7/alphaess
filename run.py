import os
from datetime import datetime
from dotenv import load_dotenv
from alphaess.alphaess import alphaess
import gspread
from google.oauth2.service_account import Credentials


async def log_current_power():
    # Get the AlphaESS app ID and secret from the .env file
    load_dotenv('.env')
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')

    # Get the Google API credentials
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", 'https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                                  scopes=SCOPES)
    gclient = gspread.authorize(creds)
    # Connect to Alpha and Google
    aclient = alphaess(APP_ID, APP_SECRET)
    sheet = gclient.open('AlphaESS-log').sheet1
    ess_list = await aclient.getESSList()

    # We presume there is only one installation and get the serial number
    # for that
    serial = ess_list[0]['sysSn']

    # Get the most recent power data and construct an array for the spreadsheet
    power = await aclient.getLastPowerData(serial)
    row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           power['ppv'],
           power['pload'],
           power['pgrid'],
           power['pbat'],
           'discharging' if power['pbat'] > 0.0 else 'idle' if power['pbat'] == 0.0 else 'charging',
           'consuming' if power['pgrid'] > 0.0 else 'idle' if power['pgrid'] == 0.0 else 'feeding']
    # Add to the spreadsheet and close the AlphaESS client
    sheet.append_row(row)
    await aclient.close()
    return row
