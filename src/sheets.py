import csv
import gspread

def load_csv(csv_path: str) -> list[list[str]]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)
    
def clear_and_write(client: gspread.Client, spreadsheet_id: str, data: list[list[str]]) -> None:
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.sheet1
    
    sheet.clear()
    sheet.update(data, "A1")