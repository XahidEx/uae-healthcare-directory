import os
import markdown
from bs4 import BeautifulSoup

DATA_DIR = "data"
DOCS_DIR = "docs"

os.makedirs(DOCS_DIR, exist_ok=True)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-gray-900 font-sans min-h-screen">
  <main class="max-w-6xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6 text-blue-700">🏥 Clinics and Hospitals in {title}</h1>
    <div class="overflow-x-auto prose prose-indigo max-w-full">{content}</div>
    <a href="index.html" class="inline-block mt-8 text-blue-600 hover:underline">← Back to Directory</a>
  </main>
</body>
</html>
"""

def style_tables(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        # Add classes to table
        table['class'] = table.get('class', []) + ["min-w-full", "divide-y", "divide-gray-200", "border", "border-gray-300", "rounded-md", "table-auto"]
        
        # Style thead
        thead = table.find("thead")
        if thead:
            thead['class'] = thead.get('class', []) + ["bg-gray-50"]
            for th in thead.find_all("th"):
                th['class'] = th.get('class', []) + ["px-6", "py-3", "text-left", "text-xs", "font-medium", "text-gray-500", "uppercase", "tracking-wider"]

        # Style tbody rows
        tbody = table.find("tbody")
        if tbody:
            for tr in tbody.find_all("tr"):
                tr['class'] = tr.get('class', []) + ["bg-white", "even:bg-gray-50"]
                for td in tr.find_all("td"):
                    td['class'] = td.get('class', []) + ["px-6", "py-4", "whitespace-nowrap", "text-sm", "text-gray-900"]
    return str(soup)

def convert_md_to_html(md_path, html_path):
    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Convert markdown to HTML (tables, fenced_code, nl2br enabled)
    html_content = markdown.markdown(md_content, extensions=["tables", "fenced_code", "nl2br"])

    # Add Tailwind classes to tables and their elements
    html_content = style_tables(html_content)

    title = os.path.splitext(os.path.basename(md_path))[0].replace("-", " ").title()
    full_html = html_template.format(title=title, content=html_content)

    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(full_html)
    print(f"Converted {md_path} -> {html_path}")

def main():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".md"):
            md_path = os.path.join(DATA_DIR, filename)
            html_filename = filename.replace(".md", ".html")
            html_path = os.path.join(DOCS_DIR, html_filename)
            convert_md_to_html(md_path, html_path)

if __name__ == "__main__":
    main()
