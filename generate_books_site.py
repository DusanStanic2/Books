import pandas as pd

EXCEL_FILE = "books.xlsx"
OUTPUT_HTML = "index.html"

# Load data
try:
    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna("")
except FileNotFoundError:
    print(f"Error: {EXCEL_FILE} not found.")
    exit()

# Generate table rows
rows_html = ""
for _, row in df.iterrows():
    rows_html += f"""
    <tr>
        <td class="font-bold">{row['Name']}</td>
        <td class="text-secondary">{row['Author']}</td>
        <td><span class="year-pill">{row['Year']}</span></td>
        <td>{row['Location']}</td>
        <td class="text-center">{row['Pictures']}</td>
        <td class="text-center">{row['Duplicate']}</td>
    </tr>
    """

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aesthetic Library</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">

    <style>
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.8);
            --glass-border: rgba(255, 255, 255, 0.4);
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --text-main: #1e293b;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            background-color: #0f172a;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            display: flex;
            justify-content: center;
        }}

        .container {{
            width: 100%;
            max-width: 1200px;
            z-index: 1;
        }}

        header {{
            text-align: center;
            margin-bottom: 50px;
            color: white;
        }}

        h1 {{
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.02em;
            text-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }}

        /* Floating Glass Search */
        .search-wrapper {{
            max-width: 600px;
            margin: 0 auto 40px auto;
        }}

        #search {{
            width: 100%;
            padding: 18px 25px;
            border-radius: 50px;
            border: 1px solid var(--glass-border);
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            font-size: 1.1rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        #search:focus {{
            transform: translateY(-2px);
            background: white;
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        }}

        /* Glass Table Card */
        .glass-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
        }}

        /* --- STYLED TABLE HEADERS --- */
        th {{
            padding: 20px;
            text-align: left;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: #64748b;
            border-bottom: 2px solid rgba(0,0,0,0.05);
            transition: all 0.2s ease;
            cursor: pointer; /* Basic pointer but reinforced by hover effects */
            position: relative;
        }}

        th:hover {{
            background: rgba(255, 255, 255, 0.5);
            color: var(--primary);
            border-bottom: 2px solid var(--primary);
        }}

        /* Custom "Sorting" indicator on hover */
        th:hover::after {{
            content: ' ↓↑';
            font-size: 0.7rem;
            opacity: 0.6;
            position: absolute;
            right: 10px;
        }}

        td {{
            padding: 20px;
            border-bottom: 1px solid rgba(0,0,0,0.05);
            transition: background 0.2s ease;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.4);
        }}

        .font-bold {{ font-weight: 600; color: #000; }}
        .text-secondary {{ color: #475569; }}
        .text-center {{ text-align: center; }}

        .year-pill {{
            background: var(--primary);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
        }}

    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>Archive & Library</h1>
        <p style="opacity: 0.7; color: white;">Refined Digital Collection</p>
    </header>

    <div class="search-wrapper">
        <input type="text" id="search" placeholder="Search your collection...">
    </div>

    <div class="glass-card">
        <table id="books">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Title</th>
                    <th onclick="sortTable(1)">Author</th>
                    <th onclick="sortTable(2)">Year</th>
                    <th onclick="sortTable(3)">Location</th>
                    <th onclick="sortTable(4)" class="text-center">Pics</th>
                    <th onclick="sortTable(5)" class="text-center">Dup</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</div>

<script>
    document.getElementById("search").addEventListener("keyup", function() {{
        let filter = this.value.toLowerCase();
        let rows = document.querySelectorAll("#books tbody tr");
        rows.forEach(row => {{
            row.style.display = row.innerText.toLowerCase().includes(filter) ? "" : "none";
        }});
    }});

    function sortTable(n) {{
        const table = document.getElementById("books");
        const tbody = table.tBodies[0];
        const rows = Array.from(tbody.rows);
        const dir = table.getAttribute("data-dir") === "asc" ? "desc" : "asc";

        rows.sort((a, b) => {{
            let x = a.cells[n].innerText.toLowerCase();
            let y = b.cells[n].innerText.toLowerCase();
            return dir === "asc" ? x.localeCompare(y, undefined, {{numeric: true}}) : y.localeCompare(x, undefined, {{numeric: true}});
        }});

        rows.forEach(row => tbody.appendChild(row));
        table.setAttribute("data-dir", dir);
    }}
</script>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅🚀✨ High-end design generated: {OUTPUT_HTML}")