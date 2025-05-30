import pandas as pd

df = pd.read_excel("Sommelier_Selection_Garibaldi_Optimized .xlsx")

html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sommelier Selection $198 – Garibaldi</title>
  <style>
    body {
      background-color: #f0eee4;
      font-family: 'EB Garamond', serif;
      color: #17110c;
      padding: 2em;
      max-width: 900px;
      margin: auto;
    }
    h1 {
      font-size: 2em;
      text-align: center;
      margin-bottom: 0.5em;
    }
    h2 {
      border-top: 1px solid #17110c;
      padding-top: 1em;
      font-size: 1.4em;
      font-weight: bold;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      padding: 0.4em 0;
    }
    .search-container {
      text-align: right;
      margin-bottom: 1em;
    }
    input[type="text"] {
      padding: 0.3em;
      font-size: 1em;
      border: 1px solid #ccc;
    }
  </style>
</head>
<body>
  <h1>Sommelier Selection Under $198</h1>
  <div class="search-container">
    <input type="text" id="searchInput" placeholder="Search a wine..." onkeyup="searchFunction()">
  </div>
'''

for section in df['Sezione'].dropna().unique():
    html += f"<h2>{section}</h2><ul>"
    filtered = df[df['Sezione'] == section]
    for _, row in filtered.iterrows():
        label = f"${row['Prezzo']} {row['Nazione']} {row['Regione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}"
        html += f"<li>{label}</li>"
    html += "</ul>"

html += '''
<script>
function searchFunction() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let lis = document.getElementsByTagName("li");
  for (let i = 0; i < lis.length; i++) {
    let txt = lis[i].innerText.toLowerCase();
    lis[i].style.display = txt.includes(input) ? "" : "none";
  }
}
</script>
</body>
</html>
'''

with open("index.html", "w") as f:
    f.write(html)