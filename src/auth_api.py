from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheets_service(service_account_path: str):
    creds = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)