import pandas as pd

# Carica il file Excel
df = pd.read_excel("Sommelier_Selection_Garibaldi_Optimized.xlsx", engine="openpyxl")
grouped = df.groupby("Sezione")

html = """<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Sommelier Selection</title>
<style>
  body { background: #f0eee4; font-family: 'EB Garamond', serif; color: #17110c; margin: 40px; }
  h1 { text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 4px; }
  h2 { text-align: center; font-size: 20px; font-weight: normal; margin-top: 0; }
  .search-container { text-align: right; margin-bottom: 20px; }
  .search-container input { padding: 4px; font-size: 14px; }
  h3 { font-size: 18px; border-bottom: 1px solid #17110c; padding-top: 30px; }
  table { width: 100%; border-collapse: collapse; margin-top: 6px; }
  td { padding: 4px 0; vertical-align: top; }
  td.price { width: 50px; font-weight: bold; }
</style>
</head>
<body>
<h1>Sommelier Selection<br>Garibaldi Restaurant<br>Under $198</h1>
<div class='search-container'>
  <input type='text' id='searchBox' placeholder='Search a wine...' onkeyup='filterWines()'>
</div>
"""

for section, group in grouped:
    html += f"<h3 id='{section.replace(' ', '')}'>{section}</h3><table>"
    for _, row in group.iterrows():
        html += f"<tr><td class='price'>${int(row['Prezzo'])}</td><td>{row['Nazione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}</td></tr>"
    html += "</table>"

html += """
<script>
function filterWines() {
  const input = document.getElementById('searchBox');
  const filter = input.value.toLowerCase();
  const rows = document.querySelectorAll('table tr');
  rows.forEach(row => {
    const text = row.innerText.toLowerCase();
    row.style.display = text.includes(filter) ? '' : 'none';
  });
}
</script>
</body></html>
"""

# Salva il file HTML
with open("index.html", "w") as f:
    f.write(html)