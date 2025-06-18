import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Autenticazione tramite secret
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if not creds_json:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON environment variable")

creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Apri Google Sheet
sheet = client.open("Sommelier_Selection_Garibaldi_Optimized")
worksheet = sheet.sheet1
data = worksheet.get_all_values()[1:]  # Salta intestazione

# Costruzione HTML
html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Wine List</title>
  <style>
    body {
      font-family: 'EB Garamond', serif;
      background-color: #f0eee4;
      color: #17110c;
      margin: 0;
      padding: 0;
    }
    h1 {
      text-align: center;
      padding: 1em;
      font-size: 1.6em;
      background-color: #e5e0d3;
      margin: 0;
    }
    .entry {
      margin-left: 110px;
      padding: 0.5em 0;
      border-bottom: 1px solid #ddd5c8;
      font-size: 1em;
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap" rel="stylesheet"/>
</head>
<body>
  <h1>Garibaldi Wine List</h1>
"""

for row in data:
    sezione, prezzo, nazione, regione, annata, nome_vino, produttore = row[:7]
    label = f"{annata} – {nome_vino} ({produttore})"
    html += f'<div class="entry">{label} <strong>${prezzo}</strong></div>\n'

html += """
</body>
</html>
"""

# Salva il file HTML
with open("/mnt/data/generate_html_FIXED.py", "w", encoding="utf-8") as f:
    f.write(__import__("textwrap").dedent(html))

"/mnt/data/generate_html_FIXED.py"
