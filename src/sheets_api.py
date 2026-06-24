import csv

def load_csv(csv_path: str) -> list[list[str]]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)
    
def clear_and_write(service, spreadsheet_id: str, data: list[list[str]]) -> None:
    sheets = service.spreadsheets()
    
    sheets.values().clear(
        spreadsheetId = spreadsheet_id,
        range = "A1:Z1000"
    ).execute()
    
    sheets.values().update(
        spreadsheetId=spreadsheet_id,
        range="A1",
        valueInputOption="RAW",
        body={"values": data}
    ).execute()