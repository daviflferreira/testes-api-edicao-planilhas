import os
from dotenv import load_dotenv
from auth_api_oauth import get_sheets_service
from sheets_api import load_csv, clear_and_write

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "metrics.csv")


def main():
    service = get_sheets_service(CREDENTIALS_PATH)
    data = load_csv(CSV_PATH)
    clear_and_write(service, SPREADSHEET_ID, data)
    print(f"Planilha atualizada com {len(data) - 1} linhas de dados.")


if __name__ == "__main__":
    main()