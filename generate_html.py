import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Autenticazione Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Leggi i dati dal foglio Google Sheet
spreadsheet = client.open("Sommelier_Selection_Garibaldi_Optimized")
sheet = spreadsheet.sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Raggruppa per sezione e costruisci l'HTML
html_start = """<!DOCTYPE html>
<!-- QUI INIZIA IL LAYOUT STILE IPAD ORIGINALE, DA SOSTITUIRE NEL PASSAGGIO SUCCESSIVO -->"""

html_end = "</body></html>"

# Placeholder: aggiungeremo il codice HTML originale qui
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_start + "\n<!-- Contenuto dinamico qui -->\n" + html_end)
