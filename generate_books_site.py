import pandas as pd

EXCEL_FILE = "books.xlsx"
OUTPUT_HTML = "index.html"

df = pd.read_excel(EXCEL_FILE)
df = df.fillna("")

rows_html = ""
for _, row in df.iterrows():
    rows_html += f"""
    <tr>
        <td>{row['Name']}</td>
        <td>{row['Author']}</td>
        <td>{row['Year']}</td>
        <td>{row['Location']}</td>
        <td>{row['Pictures']}</td>
        <td>{row['Duplicate']}</td>
    </tr>
    """

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Book Library</title>

<style>
body {{
    font-family: Arial;
    margin: 40px;
}}

#search {{
    padding: 10px;
    width: 400px;
    margin-bottom: 20px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
}}

th {{
    background: #f2f2f2;
    cursor: pointer;
}}

tr:hover {{
    background: #f5f5f5;
}}
</style>

</head>

<body>

<h1>Book Library</h1>

<input type="text" id="search" placeholder="Search books...">

<table id="books">
<thead>
<tr>
<th onclick="sortTable(0)">Name</th>
<th onclick="sortTable(1)">Author</th>
<th onclick="sortTable(2)">Year</th>
<th onclick="sortTable(3)">Location</th>
<th onclick="sortTable(4)">Pictures</th>
<th onclick="sortTable(5)">Duplicate</th>
</tr>
</thead>

<tbody>
{rows_html}
</tbody>
</table>

<script>

document.getElementById("search").addEventListener("keyup", function() {{
    let filter = this.value.toLowerCase();
    let rows = document.querySelectorAll("#books tbody tr");

    rows.forEach(row => {{
        let text = row.innerText.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    }});
}});


function sortTable(n) {{
  let table = document.getElementById("books");
  let rows = Array.from(table.rows).slice(1);
  let asc = table.getAttribute("data-sort") !== "asc";

  rows.sort((a, b) => {{
    let x = a.cells[n].innerText.toLowerCase();
    let y = b.cells[n].innerText.toLowerCase();

    if(!isNaN(x) && !isNaN(y)) {{
        return asc ? x - y : y - x;
    }}

    return asc ? x.localeCompare(y) : y.localeCompare(x);
  }});

  rows.forEach(row => table.tBodies[0].appendChild(row));
  table.setAttribute("data-sort", asc ? "asc" : "desc");
}}

</script>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("Website created:", OUTPUT_HTML)