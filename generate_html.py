import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticazione con Google Sheets
json_creds = os.getenv('GOOGLE_CREDENTIALS_JSON')
if not json_creds:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON environment variable")

creds_dict = json.loads(json_creds)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

spreadsheet = client.open("Sommelier_Selection_Garibaldi_Optimized")
sheet = spreadsheet.sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Ordina per sezione e prezzo
df = df.sort_values(by=['Sezione', 'Prezzo'])

# Genera HTML
def generate_html(df):
    sections = ['Sparkling Wines', 'White Wines', 'Rosé & Orange Wine', 'Red Wines', 'Sweet Wines']
    html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Sommelier Selection – Garibaldi</title>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'EB Garamond', serif;
      background-color: #f0eee4;
      color: #17110c;
      padding: 20px;
    }
    h1 {
      text-align: center;
      margin-bottom: 5px;
    }
    nav {
      text-align: center;
      margin-bottom: 25px;
    }
    nav a {
      margin: 0 10px;
      text-decoration: none;
      color: #17110c;
      font-weight: bold;
    }
    h2 {
      border-bottom: 1px solid #ccc;
      padding-top: 30px;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin-bottom: 8px;
    }
    .search-container {
      text-align: right;
      margin-top: -40px;
      margin-bottom: 20px;
    }
    .search-container input {
      padding: 4px;
      font-size: 15px;
    }
  </style>
</head>
<body>
  <h1>SOMMELIER SELECTION UNDER $198</h1>
  <div class='search-container'>
    <input type='text' id='searchInput' onkeyup='searchFunction()' placeholder='Search 🔍'>
  </div>
  <nav>
    <a href='#Sparkling Wines'>Sparkling</a>
    <a href='#White Wines'>White</a>
    <a href='#Rosé & Orange Wine'>Rosé & Orange</a>
    <a href='#Red Wines'>Red</a>
    <a href='#Sweet Wines'>Sweet</a>
  </nav>
"""

    for section in sections:
        group = df[df['Sezione'] == section]
        if not group.empty:
            html += f"<h2 id='{section}'>{section}</h2><ul>"
            for _, row in group.iterrows():
                line = f"${row['Prezzo']} {row['Nazione']}, {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}"
                html += f"<li>{line}</li>"
            html += "</ul>"

    html += """
<script>
function searchFunction() {
  var input, filter, li, i;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  li = document.getElementsByTagName("li");
  for (i = 0; i < li.length; i++) {
    txtValue = li[i].textContent || li[i].innerText;
    li[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
  }
}
</script>
</body>
</html>"""
    return html

# Scrive il file HTML finale
html_code = generate_html(df)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)
