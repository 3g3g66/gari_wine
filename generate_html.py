import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

json_creds = os.getenv('GOOGLE_CREDENTIALS_JSON')
if not json_creds:
    raise ValueError('Missing GOOGLE_CREDENTIALS_JSON environment variable')
creds_dict = json.loads(json_creds)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('Sommelier_Selection_Garibaldi_Optimized')
sheet = spreadsheet.sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)
grouped = df.groupby('Sezione')

html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Sommelier Selection</title>
  <style>
    body { background: #f0eee4; font-family: 'EB Garamond', serif; color: #17110c; padding: 20px; }
    h1 { text-align: center; font-size: 2em; font-weight: bold; margin-bottom: 0.1em; }
    h2 { text-align: center; font-size: 1.4em; font-weight: bold; margin-top: 0; margin-bottom: 1.5em; }
    h3 { font-size: 1.2em; margin-top: 2em; border-bottom: 1px solid #17110c; }
    ul { list-style-type: none; padding: 0; }
    li { margin-bottom: 0.6em; }
    .price { font-weight: bold; display: inline-block; width: 48px; }
    .nav { text-align: center; margin-bottom: 2em; }
    .nav a { margin: 0 12px; text-decoration: none; color: #17110c; font-weight: 500; }
    .search-container { position: absolute; top: 30px; right: 40px; }
    .search-container input { padding: 5px; font-size: 1em; font-family: 'EB Garamond', serif; }
  </style>
</head>
<body>
  <h1>Sommelier Selection<br>Garibaldi Restaurant</h1>
  <h2>Under $198</h2>
  <div class="search-container">
    <input type="text" id="searchInput" placeholder="Search a wine..."> 🔍
  </div>
  <div class="nav">"""

for section in grouped.groups.keys():
    anchor = section.replace(' ', '')
    html += f'<a href="#{anchor}">{section}</a>'
html += '</div>'

for name, group in grouped:
    anchor = name.replace(' ', '')
    html += f'<h3 id="{anchor}">{name}</h3><ul>'
    for _, row in group.iterrows():
        price = f"${int(row['Prezzo'])}" if pd.notnull(row['Prezzo']) else ""
        line = f"{row['Nazione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}"
        html += f'<li><span class="price">{price}</span> {line}</li>'
    html += '</ul>'

html += """<script>
  document.getElementById('searchInput').addEventListener('keyup', function() {
    var filter = this.value.toUpperCase();
    var items = document.getElementsByTagName('li');
    for (var i = 0; i < items.length; i++) {
      var txt = items[i].textContent || items[i].innerText;
      items[i].style.display = txt.toUpperCase().indexOf(filter) > -1 ? '' : 'none';
    }
  });
</script>
</body>
</html>"""

with open('index.html', 'w') as f:
    f.write(html)