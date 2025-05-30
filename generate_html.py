
import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

json_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")
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

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sommelier Selection – Garibaldi</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: "EB Garamond", serif;
      background-color: #f0eee4;
      color: #17110c;
      padding: 40px;
    }
    h1 {
      text-align: center;
      font-size: 30px;
      font-weight: bold;
    }
    h2 {
      font-size: 22px;
      margin-top: 40px;
      border-top: 1px solid #17110c;
      padding-top: 10px;
    }
    ul {
      list-style: none;
      padding-left: 0;
    }
    li {
      margin: 6px 0;
    }
    strong {
      font-weight: bold;
    }
    #searchInput {
      float: right;
      padding: 6px;
      font-size: 14px;
      margin-top: -30px;
    }
    nav {
      text-align: center;
      margin: 20px 0;
    }
    nav a {
      margin: 0 10px;
      text-decoration: none;
      font-weight: bold;
      color: #17110c;
    }
  </style>
</head>
<body>
<h1>Sommelier Selection<br>Garibaldi Restaurant<br>Under $198</h1>
<input type="text" id="searchInput" onkeyup="filterWines()" placeholder="Search a wine...">
<nav>
'''

for section in df['Sezione'].unique():
    anchor = section.replace(" ", "_")
    html += f"<a href='#{anchor}'>{section}</a>"

html += "</nav>"

for section in df['Sezione'].unique():
    anchor = section.replace(" ", "_")
    html += f"<h2 id='{anchor}'>{section}</h2><ul>"
    group = df[df['Sezione'] == section]
    for _, row in group.iterrows():
        html += f"<li><strong>${row['Prezzo']}</strong>&nbsp;&nbsp;{row['Nazione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}</li>"
    html += "</ul>"

html += '''
<script>
function filterWines() {
  let input = document.getElementById("searchInput");
  let filter = input.value.toLowerCase();
  let lis = document.querySelectorAll("li");
  lis.forEach(li => {
    let text = li.textContent.toLowerCase();
    li.style.display = text.includes(filter) ? "" : "none";
  });
}
</script>
</body></html>
'''

with open("index.html", "w") as f:
    f.write(html)
