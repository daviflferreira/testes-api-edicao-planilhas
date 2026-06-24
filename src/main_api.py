import os
from dotenv import load_dotenv
from auth_api import get_sheets_service
from sheets_api import clear_and_write, load_csv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), "..", os.getenv("SERVICE_ACCOUNT_PATH"))
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "metrics.csv")

def main():
    service = get_sheets_service(SERVICE_ACCOUNT_PATH)
    data = load_csv(CSV_PATH)
    clear_and_write(service, SPREADSHEET_ID, data)
    print(f"Planilha atualiada com {len(data) - 1} linhas de dados")
    
if __name__ == "__main__":
    main()