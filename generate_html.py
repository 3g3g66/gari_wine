import pandas as pd

df = pd.read_excel("Sommelier_Selection_Garibaldi_Optimized.xlsx")
df = df[df["Nome del Vino"].notnull()]

sections_order = [
    "Sparkling Wines", "White Wines", "Rosé & Orange Wine",
    "Red Wines", "Sweet Wines"
]

df["Sezione"] = pd.Categorical(df["Sezione"], categories=sections_order, ordered=True)
df.sort_values(["Sezione", "Prezzo"], inplace=True)

html = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Sommelier Selection Garibaldi</title>
  <style>
    body {
      background-color: #f0eee4;
      font-family: 'EB Garamond', serif;
      color: #17110c;
      margin: 40px;
    }
    h1, h2, h3 {
      text-align: center;
      margin: 0;
    }
    h1 { font-size: 32px; }
    h2 { font-size: 28px; margin-top: 50px; border-top: 1px solid #17110c; padding-top: 20px; }
    h3 { font-size: 18px; margin-bottom: 40px; }
    .wine-entry {
      display: flex;
      padding: 2px 0;
    }
    .price {
      width: 70px;
      font-weight: bold;
    }
    .text {
      flex: 1;
    }
    #search-box {
      float: right;
      margin-top: -30px;
    }
    input[type='text'] {
      padding: 6px;
      font-size: 16px;
    }
    .category-link {
      margin-right: 25px;
    }
    .nav {
      text-align: center;
      margin: 20px 0;
    }
  </style>
</head>
<body>
  <h1>Sommelier Selection<br>Garibaldi Restaurant</h1>
  <h3>Under $198</h3>

  <div id='search-box'>
    <input type='text' id='searchInput' onkeyup='searchWines()' placeholder='Search a wine...'>
  </div>

  <div class='nav'>
"""

for section in sections_order:
    anchor = section.replace(" ", "").replace("&", "").replace("é", "e")
    html += f"<a class='category-link' href='#{anchor}'>{section}</a>\n"

html += "</div>"

for section in sections_order:
    anchor = section.replace(" ", "").replace("&", "").replace("é", "e")
    wines = df[df["Sezione"] == section]
    if not wines.empty:
        html += f"<h2 id='{anchor}'>{section}</h2>"
        for _, row in wines.iterrows():
            html += f"<div class='wine-entry'><div class='price'>${int(row['Prezzo'])}</div><div class='text'>{row['Nazione']} {row['Annata']} {row['Nome del Vino']} – {row['Produttore']}</div></div>"

html += """
<script>
function searchWines() {
  var input = document.getElementById("searchInput");
  var filter = input.value.toLowerCase();
  var wines = document.getElementsByClassName("wine-entry");
  for (var i = 0; i < wines.length; i++) {
    var txt = wines[i].innerText;
    wines[i].style.display = txt.toLowerCase().includes(filter) ? "" : "none";
  }
}
</script>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html)