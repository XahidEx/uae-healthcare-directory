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
  <title>{title} | UAE Healthcare Directory</title>

  <!-- SEO Meta Tags -->
  <meta name="description" content="Directory of clinics and hospitals in UAE by emirate, including services and contact details." />
  <meta name="robots" content="index, follow" />
  
  <!-- Open Graph -->
  <meta property="og:title" content="{title} | UAE Healthcare Directory" />
  <meta property="og:description" content="Find clinics and hospitals across UAE emirates with services and links." />
  <meta property="og:url" content="https://xahidex.github.io/uae-healthcare-directory/" />
  <meta property="og:type" content="website" />

  <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
</head>
<body class="bg-gray-50 text-gray-900 font-sans min-h-screen flex flex-col">
  <header class="fixed top-0 w-full bg-white shadow z-30">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <a href="index.html" class="text-xl font-bold text-blue-700 hover:underline">🏥 UAE Healthcare Directory</a>
    </div>
  </header>
  <main class="flex-grow max-w-6xl mx-auto p-6 pt-24">
    <h1 class="text-3xl font-bold mb-6 text-blue-700">{title}</h1>
    <div class="overflow-x-auto prose prose-indigo max-w-full">{content}</div>
    <a href="index.html" class="inline-block mt-8 text-blue-600 hover:underline">← Back to Directory</a>
  </main>
  <footer class="bg-white shadow-inner mt-12 py-6 text-center text-sm text-gray-600">
    Built by <a href="https://xahidex.com" target="_blank" rel="noopener" class="text-blue-600 hover:underline">Jahidul Islam</a>. Contributed by open-source community.
  </footer>
</body>
</html>
"""

def style_tables(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        table['class'] = table.get('class', []) + ["min-w-full", "divide-y", "divide-gray-200", "border", "border-gray-300", "rounded-md", "table-auto"]
        
        thead = table.find("thead")
        if thead:
            thead['class'] = thead.get('class', []) + ["bg-gray-50"]
            for th in thead.find_all("th"):
                th['class'] = th.get('class', []) + ["px-6", "py-3", "text-left", "text-xs", "font-medium", "text-gray-500", "uppercase", "tracking-wider"]

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

    html_content = markdown.markdown(md_content, extensions=["tables", "fenced_code", "nl2br"])
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
