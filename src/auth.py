import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

def get_gspread_client(service_account_path: str) -> gspread.Client:
    creds = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
    return gspread.authorize(creds)