import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAMES = {
    "pilots": "pilot_roster",
    "drones": "drone_fleet",
    "missions": "missions"
}


def connect():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        SCOPE
    )
    client = gspread.authorize(creds)
    return client


def load_sheet(sheet_name):
    client = connect()
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)


def save_sheet(sheet_name, df):
    client = connect()
    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())


# ===========================
# Public Functions
# ===========================

def load_pilots():
    return load_sheet(SHEET_NAMES["pilots"])


def load_drones():
    return load_sheet(SHEET_NAMES["drones"])


def load_missions():
    return load_sheet(SHEET_NAMES["missions"])


def save_pilots(df):
    save_sheet(SHEET_NAMES["pilots"], df)


def save_drones(df):
    save_sheet(SHEET_NAMES["drones"], df)
