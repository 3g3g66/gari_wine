import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from collections import defaultdict

# Autenticazione con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if not creds_json:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON environment variable")

creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Apri il file Google Sheet
sheet = client.open("Sommelier_Selection_Garibaldi_Optimized")
worksheet = sheet.sheet1
data = worksheet.get_all_values()[1:]  # salta intestazione

# Inizializza HTML
html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'/>
  <title>Wine List</title>
  <style>
    body { font-family: 'EB Garamond', serif; background-color: #f0eee4; color: #17110c; margin: 0; padding: 0; }
    h1 { text-align: center; padding: 1em; font-size: 1.6em; background-color: #e5e0d3; margin: 0; }
    nav { position: sticky; top: 0; background: #f0eee4; border-bottom: 1px solid #ccc; padding: 10px; text-align: center; z-index: 10; }
    nav a { margin: 0 8px; text-decoration: none; font-weight: bold; font-size: 1.05em; color: #17110c; }
    .wine-entry {
  font-size: 1em;
  padding: 0.3em 0;
  border-bottom: 1px solid #ddd5c8;
  margin-left: 110px;
}
    .label { max-width: 70%; }
    .price { font-weight: bold; white-space: nowrap; }
    h2 { margin-left: 110px; font-size: 1.2em; margin-top: 2em; padding-top: 1em; border-top: 1px solid #ccc; font-weight: bold; }
    #searchInput { display: none; margin: 10px auto; padding: 10px; width: 80%; font-size: 1em; font-family: 'EB Garamond', serif; border: 1px solid #ccc; border-radius: 5px; display: block; }
  </style>
  <link href='https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap' rel='stylesheet'/>
</head>
<body>
  <h1>SOMMELIER SELECTION UNDER $198</h1>
  <div style="margin-top: 10px; margin-bottom: 20px; text-align: center;">
    <a href="https://garibaldi-wine-library.netlify.app" style="font-size: 16px; text-decoration: underline; color: #17110c;">
      ← Back to Full Wine List
    </a>
  </div>
  <div style="text-align: right; padding: 0.3em 1em 0.1em 1em;">
    <button aria-label="Search" onclick="toggleSearch()" style="background: none; border: none; font-size: 1.5em; cursor: pointer;">🔍</button>
    <input id="searchInput" style="display:none !important; margin-top: 10px; padding: 10px; width: 80%; font-size: 1em; font-family: 'EB Garamond', serif; border: 1px solid #ccc; border-radius: 5px;" type="text" />
  </div>
  <script>
    function toggleSearch() {
      var input = document.getElementById("searchInput");
      input.style.display = input.style.display === "none" ? "block" : "none";
      if (input.style.display === "block") input.focus();
    }
    document.getElementById("searchInput").addEventListener("input", function() {
      var input = this.value.toLowerCase();
      var entries = document.querySelectorAll(".wine-entry");
      var sections = document.querySelectorAll("section h2");
      entries.forEach(function(entry) {
      entry.style.display = entry.textContent.toLowerCase().includes(input) ? "block" : "none";
      });
     window.addEventListener("DOMContentLoaded", function() {
  var input = document.getElementById("searchInput");
  if (input) {
    input.style.display = "none";
    input.value = "";
  }
});
      sections.forEach(function(section) {
        section.style.display = input.length > 0 ? "none" : "block";
      });
    });
  </script>
  <nav>
    <a href="#SPARKLING_WINES">Sparkling Wines</a>
    <a href="#WHITE_WINES">White Wines</a>
    <a href="#ROSÉ_ORANGE_WINE">Rosé & Orange Wine</a>
    <a href="#RED_WINES">Red Wines</a>
    <a href="#SWEET_WINES">Sweet Wines</a>
  </nav>
'''

sections = defaultdict(list)
for row in data:
    if len(row) < 7: continue
    section = re.sub(r'\W+', '_', row[0].strip().upper())
    price = row[1].strip()
    nation = row[2].strip()
    region = row[3].strip()
    year = row[4].strip()
    wine = row[5].strip()
    producer = row[6].strip()
    entry_html = f"<div class='wine-entry'><strong>${price}</strong>&nbsp;&nbsp;{nation}  {region} – {year}  {wine}  {producer}</div>"
 
    sections[section].append(entry_html)

for section_id, wines in sections.items():
    html += f'<section id="{section_id}">'
    html += f'<h2>{section_id.replace("_", " ").title()}</h2>'
    html += "\n".join(wines)
    html += "</section>"

html += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
