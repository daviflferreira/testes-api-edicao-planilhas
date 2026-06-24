import json

def load_json(json_path: str) -> list[list[str]]:
    with open(json_path, encoding="utf-8") as f:
        payload = json.load(f)
        
    rows = payload["rows"]
    if not rows:
        return []
    
    headers = list(rows[0].keys())
    data = [headers]
    for row in rows:
        data.append([str(row[key]) for key in headers])
        
    return data