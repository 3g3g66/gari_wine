
import pandas as pd

# URL pubblico del tuo Google Sheet in formato CSV esportabile
sheet_url = "https://docs.google.com/spreadsheets/d/1lTsDTvDzCI-D6fciiWdXBaHvtubxj7Gy/export?format=csv"

# Legge i dati
df = pd.read_csv(sheet_url)

# Rimuove etichette OUT OF STOCK
df = df[df["Stato"].str.upper() != "OUT"]

# Ordina per categoria e prezzo
df["Prezzo (SGD)"] = df["Prezzo (SGD)"].replace("[\$,]", "", regex=True).astype(float)
df = df.sort_values(by=["Categoria", "Prezzo (SGD)"])

# Inizia l’HTML
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sommelier Selection $198 – Garibaldi Restaurant</title>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap" rel="stylesheet">
<style>
    body { font-family: 'EB Garamond', serif; background: #f0eee4; color: #17110c; padding: 2em; }
    h1, h2 { text-align: center; margin: 0.2em 0; }
    .section { font-weight: bold; font-size: 1.2em; margin-top: 2em; }
    .wine { margin-left: 2em; margin-bottom: 0.5em; white-space: nowrap; }
    .price { display: inline-block; width: 60px; }
    .country { display: inline-block; width: 90px; }
    .region { display: inline-block; width: 110px; }
    .vintage { display: inline-block; width: 50px; }
    .name { display: inline-block; width: 220px; }
    .producer { display: inline-block; width: 160px; }
    .search-bar {
        position: fixed; top: 1em; right: 1em;
    }
    input[type="text"] {
        padding: 6px; font-size: 16px; border-radius: 8px;
        border: 1px solid #ccc;
    }
</style>
<script>
function searchWine() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let wines = document.getElementsByClassName("wine");
  for (let wine of wines) {
    wine.style.display = wine.textContent.toLowerCase().includes(input) ? "block" : "none";
  }
}
</script>
</head>
<body>
<div class="search-bar">
  <input type="text" id="searchInput" onkeyup="searchWine()" placeholder="Search a wine...">
</div>
<h1>Sommelier Selection</h1>
<h2>Under $198 – Garibaldi Restaurant</h2>
"""

# Genera le sezioni
for section in df["Categoria"].unique():
    html += f'<div class="section">{section}</div>\n'
    for _, row in df[df["Categoria"] == section].iterrows():
        html += (
            f'<div class="wine">'
            f'<span class="price">${int(row["Prezzo (SGD)"])}</span>'
            f'<span class="country">{row["Nazione"]}</span>'
            f'<span class="region">{row["Regione"]}</span>'
            f'<span class="vintage">{row["Annata"]}</span>'
            f'<span class="name">{row["Nome Vino"]}</span>'
            f'<span class="producer">{row["Produttore"]}</span>'
            f'</div>\n'
        )

html += "</body></html>"

# Salva
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
