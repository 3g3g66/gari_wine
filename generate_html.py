import pandas as pd

df = pd.read_excel("Sommelier_Selection_Garibaldi_Optimized.xlsx")

grouped = df.groupby("Sezione")

html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Sommelier Selection</title>
  <style>
    body {
      background-color: #f0eee4;
      font-family: 'EB Garamond', serif;
      color: #17110c;
      padding: 20px;
      font-size: 18px;
    }
    h1 {
      text-align: center;
      font-size: 32px;
      margin-bottom: 10px;
    }
    h2 {
      border-bottom: 1px solid #17110c;
      padding-top: 40px;
    }
    .wine-line {
      display: flex;
      justify-content: flex-start;
      margin-bottom: 6px;
    }
    .price {
      width: 60px;
      font-weight: bold;
    }
    input[type='text'] {
      float: right;
      margin-top: -50px;
      padding: 6px;
      font-size: 16px;
      width: 200px;
    }
    nav {
      text-align: center;
      margin: 20px 0;
    }
    nav a {
      margin: 0 12px;
      text-decoration: none;
      color: #17110c;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h1>
    Sommelier Selection<br>
    Garibaldi Restaurant<br>
    Under $198
  </h1>

  <input type='text' id='searchBar' placeholder='Search a wine...' onkeyup='searchWines()'>

  <nav>
    <a href='#Sparkling Wines'>Sparkling Wines</a>
    <a href='#White Wines'>White Wines</a>
    <a href='#Rosé & Orange Wine'>Rosé & Orange Wine</a>
    <a href='#Red Wines'>Red Wines</a>
    <a href='#Sweet Wines'>Sweet Wines</a>
  </nav>

  <div id='wineList'>
"""

for name, group in grouped:
    html += f"<h2 id='{name}'>{name}</h2>"
    for _, row in group.iterrows():
        html += f"<div class='wine-line'><div class='price'>${row['Prezzo']}</div> {row['Nazione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}</div>"

html += """
  </div>
  <script>
    function searchWines() {
      let input = document.getElementById('searchBar').value.toLowerCase();
      let wines = document.querySelectorAll('.wine-line');
      wines.forEach(wine => {
        wine.style.display = wine.textContent.toLowerCase().includes(input) ? '' : 'none';
      });
    }
  </script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
