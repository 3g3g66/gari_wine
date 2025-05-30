import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Carica il secret JSON da GitHub Actions
json_creds = os.getenv('GOOGLE_CREDENTIALS_JSON')
if not json_creds:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON environment variable")

creds_dict = json.loads(json_creds)

# Autenticazione Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Apri il foglio
spreadsheet = client.open("Sommelier_Selection_Garibaldi_Optimized")
sheet = spreadsheet.sheet1
data = sheet.get_all_records()

df = pd.DataFrame(data)
grouped = df.groupby("Sezione")

# HTML Template con stile elegante + search
html_template = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Sommelier Selection Under $198</title>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Libre Baskerville', serif;
      background-color: #fdfaf6;
      color: #2e2e2e;
      margin: 0;
      padding: 2rem;
    }}
    h1 {{
      text-align: center;
      font-size: 1.8rem;
      font-weight: bold;
      margin-bottom: 1.5rem;
    }}
    nav {{
      text-align: center;
      margin-bottom: 2rem;
    }}
    nav a {{
      margin: 0 1rem;
      text-decoration: none;
      color: #333;
      font-weight: 500;
    }}
    section {{
      margin-bottom: 2rem;
    }}
    h2 {{
      font-size: 1.2rem;
      font-weight: bold;
      border-bottom: 1px solid #ddd;
      margin-top: 2rem;
    }}
    ul {{
      list-style: none;
      padding: 0;
    }}
    li {{
      margin-bottom: 0.5rem;
    }}
    #search {{
      float: right;
      margin-top: -3rem;
    }}
    #search input {{
      padding: 5px;
      font-size: 0.9rem;
    }}
  </style>
</head>
<body>
  <h1>SOMMELIER SELECTION UNDER $198</h1>
  <div id="search">
    <input type="text" id="searchInput" placeholder="Search... 🔍" onkeyup="searchFunction()">
  </div>
  <nav>
    <a href="#Sparkling Wines">Sparkling Wines</a>
    <a href="#White Wines">White Wines</a>
    <a href="#Rosé & Orange Wine">Rosé & Orange Wine</a>
    <a href="#Red Wines">Red Wines</a>
    <a href="#Sweet Wines">Sweet Wines</a>
  </nav>
  {body_content}
  <script>
    function searchFunction() {{
      var input, filter, li, i;
      input = document.getElementById('searchInput');
      filter = input.value.toUpperCase();
      li = document.getElementsByTagName('li');
      for (i = 0; i < li.length; i++) {{
        txtValue = li[i].textContent || li[i].innerText;
        li[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
      }}
    }}
  </script>
</body>
</html>"""

# Generazione contenuto
body_content = ""
for name, group in grouped:
    body_content += f"<section id='{name}'><h2>{name}</h2><ul>"
    for _, row in group.iterrows():
        line = f"${row['Prezzo']} {row['Nazione']}, {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}"
        body_content += f"<li>{line}</li>"
    body_content += "</ul></section>"

html = html_template.format(body_content=body_content)

with open("index.html", "w") as f:
    f.write(html)
