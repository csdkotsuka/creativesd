#!/usr/bin/env python3
import os
import subprocess
import re

PROJECT_ROOT = "/Users/kotsuka/Documents/systemDev/csd-website"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "leaflet_output/nyushi")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_PATH = os.path.join(PROJECT_ROOT, "nyushi_leaflet_2p.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    full_html = f.read()

# Replace relative image paths with absolute file:// URLs
abs_images_path = f"file://{PROJECT_ROOT}/images/"
full_html_abs = re.sub(r'src=["\']images/', f'src="{abs_images_path}', full_html)
full_html_abs = re.sub(r'src=["\']assets/images/', f'src="file://{PROJECT_ROOT}/assets/images/', full_html_abs)

abs_html_file = "/tmp/nyushi_leaflet_2p_abs.html"
with open(abs_html_file, "w", encoding="utf-8") as f:
    f.write(full_html_abs)

print("1. Generating High-Res A4 2-Page PDF...")
pdf_path = os.path.join(OUTPUT_DIR, "NYUSHI_Leaflet_A4.pdf")
cmd_pdf = [
    CHROME_BIN,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--virtual-time-budget=5000",
    f"--print-to-pdf={pdf_path}",
    f"file://{abs_html_file}"
]
subprocess.run(cmd_pdf, check=True)
print(f"Generated: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

sections = re.findall(r'(<section class="leaflet-page.*?<\/section>)', full_html_abs, re.DOTALL)
print(f"Found {len(sections)} sections in HTML")

head_match = re.search(r'(<head>.*?<\/head>)', full_html_abs, re.DOTALL)
head_content = head_match.group(1) if head_match else ""

pages = [
    ("page_1_front.jpg", 1),
    ("page_2_back.jpg", 2),
]

print("\n2. Capturing high-resolution screenshots for each page (1200 x 1697)...")
for idx, (filename, page_num) in enumerate(pages):
    if idx < len(sections):
        page_html_content = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<style>
.leaflet-page {{
    width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    max-height: 100% !important;
    border: none !important;
    box-shadow: none !important;
}}
</style>
<body class="bg-white text-slate-800 p-0 m-0 overflow-hidden flex justify-center items-center font-sans">
    <div style="width: 1200px; height: 1697px; box-sizing: border-box; overflow: hidden;">
        {sections[idx].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}
    </div>
</body>
</html>"""
        temp_html_path = f"/tmp/nyushi_page_{page_num}_abs.html"
        with open(temp_html_path, "w", encoding="utf-8") as tf:
            tf.write(page_html_content)

        temp_png = f"/tmp/nyushi_page_{page_num}.png"
        cmd_shot = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--virtual-time-budget=5000",
            f"--screenshot={temp_png}",
            "--window-size=1200,1697",
            f"file://{temp_html_path}"
        ]
        subprocess.run(cmd_shot, check=True)

        out_jpg = os.path.join(OUTPUT_DIR, filename)
        subprocess.run(["sips", "-s", "format", "jpeg", temp_png, "--out", out_jpg, "-s", "formatOptions", "96"], check=True)
        print(f"Generated: {out_jpg}")

print("\n3. Generating Side-by-Side Spread Preview (2400 x 1697)...")
if len(sections) >= 2:
    spread_html = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<style>
.leaflet-page {{
    width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    max-height: 100% !important;
    border: none !important;
    box-shadow: none !important;
}}
</style>
<body class="bg-white text-slate-800 p-0 m-0 overflow-hidden flex justify-center items-center font-sans">
    <div style="width: 2400px; height: 1697px; display: flex; flex-direction: row; box-sizing: border-box; overflow: hidden;">
        <div style="width: 1200px; height: 1697px;">{sections[0].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
        <div style="width: 1200px; height: 1697px;">{sections[1].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
    </div>
</body>
</html>"""
    temp_spread_html = "/tmp/nyushi_spread_abs.html"
    with open(temp_spread_html, "w", encoding="utf-8") as tf:
        tf.write(spread_html)

    temp_spread_png = "/tmp/nyushi_spread.png"
    subprocess.run([
        CHROME_BIN, "--headless", "--disable-gpu", "--virtual-time-budget=5000",
        f"--screenshot={temp_spread_png}", "--window-size=2400,1697", f"file://{temp_spread_html}"
    ], check=True)
    out_spread_jpg = os.path.join(OUTPUT_DIR, "spread_1_front_back.jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", temp_spread_png, "--out", out_spread_jpg, "-s", "formatOptions", "96"], check=True)
    print(f"Generated: {out_spread_jpg}")

    spread_pdf_path = os.path.join(OUTPUT_DIR, "NYUSHI_Leaflet_Spread.pdf")
    spread_pdf_html = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<style>
@page {{ size: A3 landscape; margin: 0; }}
@media print {{
    html, body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; height: auto !important; }}
    .spread-sheet {{ width: 420mm !important; height: 296.5mm !important; display: flex !important; flex-direction: row !important; }}
    .spread-half {{ width: 210mm !important; height: 296.5mm !important; }}
}}
</style>
<body class="bg-white text-slate-800 p-0 m-0">
    <div class="spread-sheet" style="width: 420mm; height: 296.5mm; display: flex;">
        <div class="spread-half" style="width: 210mm; height: 296.5mm;">{sections[0].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
        <div class="spread-half" style="width: 210mm; height: 296.5mm;">{sections[1].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
    </div>
</body>
</html>"""
    temp_spread_pdf_html = "/tmp/nyushi_spread_pdf_abs.html"
    with open(temp_spread_pdf_html, "w", encoding="utf-8") as tf:
        tf.write(spread_pdf_html)

    subprocess.run([
        CHROME_BIN, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        "--virtual-time-budget=5000", f"--print-to-pdf={spread_pdf_path}", f"file://{temp_spread_pdf_html}"
    ], check=True)
    print(f"Generated: {spread_pdf_path}")

print("\nSUCCESS: All Admissions (Nyushi) leaflet assets generated successfully!")
