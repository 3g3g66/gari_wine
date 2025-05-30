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

# Raggruppa per sezione
grouped = df.groupby("Sezione")

# HTML layout
html_start = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Sommelier Selection $198 - Garibaldi</title>
  <style>
    body {
      font-family: 'EB Garamond', serif;
      background-color: #f0eee4;
      color: #17110c;
      padding: 30px;
      font-size: 18px;
    }
    h1 {
      text-align: center;
      font-size: 28px;
      margin-bottom: 10px;
    }
    h2 {
      margin-top: 40px;
      font-weight: bold;
      font-size: 22px;
      border-bottom: 1px solid #17110c;
      padding-bottom: 6px;
    }
    .wine-entry {
      margin: 4px 0;
      padding-left: 40px;
    }
    .price {
      font-weight: bold;
      display: inline-block;
      width: 70px;
    }
    .section {
      margin-bottom: 30px;
    }
    .search {
      position: absolute;
      top: 30px;
      right: 30px;
    }
    #searchInput {
      padding: 6px;
      font-size: 16px;
    }
  </style>
</head>
<body>
<div class='search'>
  <input type='text' id='searchInput' placeholder='Search a wine...' onkeyup='filterWines()'>
</div>
<h1>Sommelier Selection<br>Garibaldi Restaurant<br>Under $198</h1>
<script>
function filterWines() {
  var input, filter, entries, entry, i, txtValue;
  input = document.getElementById('searchInput');
  filter = input.value.toUpperCase();
  entries = document.getElementsByClassName('wine-entry');
  for (i = 0; i < entries.length; i++) {
    entry = entries[i];
    txtValue = entry.textContent || entry.innerText;
    entry.style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
  }
}
</script>
"""

html_body = ""
for section, group in grouped:
    html_body += f"<div class='section'><h2>{section}</h2>"
    for _, row in group.iterrows():
        html_body += f"<div class='wine-entry'><span class='price'>${row['Prezzo']}</span>{row['Nazione']} {row['Regione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}</div>"
    html_body += "</div>"

html_end = "</body></html>"

# Scrive il file HTML
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_start + html_body + html_end)
