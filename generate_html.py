
import pandas as pd

# Load Excel file
df = pd.read_excel("Sommelier_Selection_Garibaldi_Optimized.xlsx")

# Mapping section names for anchor links
section_anchors = {
    "Sparkling Wines": "SPARKLING_WINES",
    "White Wines": "WHITE_WINES",
    "Rosé & Orange Wine": "ROSÉ_&amp;_ORANGE_WINE",
    "Red Wines": "RED_WINES",
    "Sweet Wines": "SWEET_WINES"
}

# Start building HTML
html = """<html>
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
<button aria-label="Search" onclick="toggleSearch()" style="background: none; border: none; font-size: 1.5em; cursor: pointer;">🔍</button>
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
<nav>""" + "".join(f'<a href="#{anchor}">{name}</a>' for name, anchor in section_anchors.items()) + "</nav>"

# Append sections and entries
for section, anchor in section_anchors.items():
    html += f'<section id="{anchor}">
<h2>{section}</h2>
'
    wines = df[df['Sezione'] == section]
    for _, row in wines.iterrows():
        price = f"${int(row['Prezzo'])}"
        entry = f"{row['Nazione']}, {row['Regione']}, {row['Annata']} {row['Nome']}"
        html += f'<div class="entry">{price}  {entry}</div>
'
    html += "</section>
"

html += "</body></html>"

# Write to file
with open("/mnt/data/generate_html.py", "w") as f:
    f.write(html)
