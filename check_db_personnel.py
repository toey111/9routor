import urllib.request
import json

try:
    req = urllib.request.urlopen("http://localhost:8000/api/v1/personnel?page=1&limit=50")
    data = json.loads(req.read().decode('utf-8'))
    print(f"Total in DB: {data.get('total')}")
    for p in data.get('items', []):
        print(f"ID {p['id']}: {p['personnel_code']} - {p['full_name_th']} ({p.get('position_name')}, {p.get('branch_name')})")
except Exception as e:
    print("Error:", e)
