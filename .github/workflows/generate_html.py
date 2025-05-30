import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Carica il secret JSON da GitHub Actions
json_creds = os.getenv('GOOGLE_CREDENTIALS_JSON')
if not json_creds:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON environment variable")

# Decodifica il JSON dalle variabili d'ambiente
creds_dict = json.loads(json_creds)

# Autenticazione Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Apri il foglio Google Sheet
spreadsheet = client.open("Sommelier_Selection_Garibaldi_Optimized")
sheet = spreadsheet.sheet1
data = sheet.get_all_records()

# Converti in DataFrame
df = pd.DataFrame(data)

# Raggruppa per sezione
grouped = df.groupby("Sezione")

# Genera l'HTML
html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Sommelier Selection</title>
</head>
<body>
<h1>Sommelier Selection Under $198</h1>
"""

for name, group in grouped:
    html += f"<h2>{name}</h2><ul>"
    for _, row in group.iterrows():
        html += f"<li>${row['Prezzo']} {row['Nazione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}</li>"
    html += "</ul>"

html += "</body></html>"

# Salva il file HTML
with open("index.html", "w") as f:
    f.write(html)
