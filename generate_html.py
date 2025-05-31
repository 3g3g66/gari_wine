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
data = worksheet.get_all_values()

# Inizializza l'HTML
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
    nav {
      position: sticky;
      top: 0;
      background: #f0eee4;
      border-bottom: 1px solid #ccc;
      padding: 10px;
      text-align: center;
      z-index: 10;
    }
    nav a {
      margin: 0 8px;
      text-decoration: none;
      font-weight: bold;
      font-size: 1.05em;
      color: #17110c;
    }
    section {
      padding: 1em;
    }
    .entry {
      margin-left: 110px;
      padding: 0.5em 0;
      border-bottom: 1px solid #ddd5c8;
      font-size: 1em;
    }
    h2 {
      margin-left: 110px;
      font-size: 1.2em;
      margin-top: 1em;
      padding-top: 1em;
      border-top: 1px solid #ccc;
      font-weight: bold;
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap" rel="stylesheet"/>
</head>
<body>
  <h1 style="text-align: center; padding: 0.3em 0; font-size: 1.6em; background-color: #e5e0d3; margin: 0;">
    SOMMELIER SELECTION UNDER $198
  </h1>
  <div style="text-align: right; padding: 0.3em 1em 0.1em 1em;">
    <button aria-label="Search" onclick="toggleSearch()" style="background: none; border: none; font-size: 1.5em; cursor: pointer;">
      🔍
    </button>
    <input id="searchInput" placeholder="Search a wine..." style="display:none; margin-top: 10px; padding: 10px; width: 80%; font-size: 1em; font-family: 'EB Garamond', serif; border: 1px solid #ccc; border-radius: 5px;" type="text"/>
  </div>
  <script>
    function toggleSearch() {
      var input = document.getElementById("searchInput");
      input.style.display = input.style.display === "none" ? "block" : "none";
      if (input.style.display === "block") input.focus();
    }
    document.getElementById("searchInput").addEventListener("input", function() {
      var input = this.value.toLowerCase();
      var entries = document.querySelectorAll(".entry");
      var sections = document.querySelectorAll("section h2");
      entries.forEach(function(entry) {
        if (entry.textContent.toLowerCase().includes(input)) {
          entry.style.display = "block";
        } else {
          entry.style.display = "none";
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
"""

# Sezioni
sections = defaultdict(list)
for row in data[1:]:  # salta intestazione
    if len(row) < 4:
        continue
    category = row[0].strip().upper().replace(" ", "_").replace("&", "AND")
    price = row[1].strip()
    wine = row[2].strip()
    producer = row[3].strip()
    sections[category].append(f"<div class='entry'>${price} {wine} – {producer}</div>")

for section_id, entries in sections.items():
    html += f'<section id="{section_id}">\n'
    html += f'<h2>{section_id.replace("_", " ").title()}</h2>\n'
    html += "\n".join(entries)
    html += "\n</section>\n"

html += "</body>\n</html>"

# Scrivi file index.html
with open("index.html", "w") as f:
    f.write(html)