#!/usr/bin/env python3
import os
import subprocess
import time
import re
import os
import subprocess
import time
import re

PROJECT_ROOT = "/Users/kotsuka/Documents/systemDev/csd-website"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "leaflet_output/kyomu")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_PATH = os.path.join(PROJECT_ROOT, "kyomu_leaflet_4p.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    full_html = f.read()

# Replace relative image paths with absolute file:// URLs so headless Chrome in /tmp or anywhere loads them perfectly
abs_images_path = f"file://{PROJECT_ROOT}/images/"
full_html_abs = re.sub(r'src=["\']images/', f'src="{abs_images_path}', full_html)
full_html_abs = re.sub(r'src=["\']assets/images/', f'src="file://{PROJECT_ROOT}/assets/images/', full_html_abs)

# Save the absolute HTML
abs_html_file = "/tmp/kyomu_leaflet_4p_abs.html"
with open(abs_html_file, "w", encoding="utf-8") as f:
    f.write(full_html_abs)

print("1. Generating High-Res A4 4-Page PDF...")
pdf_path = os.path.join(OUTPUT_DIR, "KYOMU_Leaflet_A4.pdf")
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

# Parse sections
sections = re.findall(r'(<section class="leaflet-page.*?<\/section>)', full_html_abs, re.DOTALL)
print(f"Found {len(sections)} sections in HTML")

head_match = re.search(r'(<head>.*?<\/head>)', full_html_abs, re.DOTALL)
head_content = head_match.group(1) if head_match else ""

pages = [
    ("page_1_cover.jpg", 1),
    ("page_2_academic_flow.jpg", 2),
    ("page_3_grading_reports.jpg", 3),
    ("page_4_impact_and_contact.jpg", 4),
]

print("\n2. Capturing high-resolution screenshots for each page (1200 x 1697)...")
for idx, (filename, page_num) in enumerate(pages):
    if idx < len(sections):
        page_html_content = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<body class="bg-white text-slate-800 p-0 m-0 overflow-hidden flex justify-center items-center font-sans">
    <div style="width: 1200px; height: 1697px; box-sizing: border-box; overflow: hidden;">
        {sections[idx].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}
    </div>
</body>
</html>"""
        temp_html_path = f"/tmp/kyomu_page_{page_num}_abs.html"
        with open(temp_html_path, "w", encoding="utf-8") as tf:
            tf.write(page_html_content)

        temp_png = f"/tmp/kyomu_page_{page_num}.png"
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

print("\n3. Generating A3 Spreads (Outside & Inside)...")
if len(sections) >= 4:
    # Spread 1 (Outside: P4 Left + P1 Right)
    spread1_html = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<body class="bg-white text-slate-800 p-0 m-0 overflow-hidden flex justify-center items-center font-sans">
    <div style="width: 2400px; height: 1697px; display: flex; flex-direction: row; box-sizing: border-box; overflow: hidden;">
        <div style="width: 1200px; height: 1697px;">{sections[3].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
        <div style="width: 1200px; height: 1697px;">{sections[0].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
    </div>
</body>
</html>"""
    temp_s1_html = "/tmp/kyomu_spread_1_abs.html"
    with open(temp_s1_html, "w", encoding="utf-8") as tf:
        tf.write(spread1_html)
    temp_s1_png = "/tmp/kyomu_spread_1.png"
    subprocess.run([
        CHROME_BIN, "--headless", "--disable-gpu", "--virtual-time-budget=5000",
        f"--screenshot={temp_s1_png}", "--window-size=2400,1697", f"file://{temp_s1_html}"
    ], check=True)
    out_s1 = os.path.join(OUTPUT_DIR, "spread_1_outside_cover.jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", temp_s1_png, "--out", out_s1, "-s", "formatOptions", "96"], check=True)
    print(f"Generated: {out_s1}")

    # Spread 2 (Inside: P2 Left + P3 Right)
    spread2_html = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<body class="bg-white text-slate-800 p-0 m-0 overflow-hidden flex justify-center items-center font-sans">
    <div style="width: 2400px; height: 1697px; display: flex; flex-direction: row; box-sizing: border-box; overflow: hidden;">
        <div style="width: 1200px; height: 1697px;">{sections[1].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
        <div style="width: 1200px; height: 1697px;">{sections[2].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
    </div>
</body>
</html>"""
    temp_s2_html = "/tmp/kyomu_spread_2_abs.html"
    with open(temp_s2_html, "w", encoding="utf-8") as tf:
        tf.write(spread2_html)
    temp_s2_png = "/tmp/kyomu_spread_2.png"
    subprocess.run([
        CHROME_BIN, "--headless", "--disable-gpu", "--virtual-time-budget=5000",
        f"--screenshot={temp_s2_png}", "--window-size=2400,1697", f"file://{temp_s2_html}"
    ], check=True)
    out_s2 = os.path.join(OUTPUT_DIR, "spread_2_inside_flow.jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", temp_s2_png, "--out", out_s2, "-s", "formatOptions", "96"], check=True)
    print(f"Generated: {out_s2}")

    # A3 Spread PDF
    spread_pdf_path = os.path.join(OUTPUT_DIR, "KYOMU_Leaflet_A3_Spread.pdf")
    spread_all_html = f"""<!DOCTYPE html>
<html lang="ja">
{head_content}
<style>
@page {{ size: A3 landscape; margin: 0; }}
@media print {{
    html, body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; height: auto !important; }}
    .spread-sheet {{ width: 420mm !important; height: 296.5mm !important; page-break-after: always !important; display: flex !important; flex-direction: row !important; }}
    .spread-sheet:last-child {{ page-break-after: avoid !important; }}
    .spread-half {{ width: 210mm !important; height: 296.5mm !important; }}
}}
</style>
<body class="bg-white text-slate-800 p-0 m-0">
    <div class="spread-sheet" style="width: 420mm; height: 296.5mm; display: flex;">
        <div class="spread-half" style="width: 210mm; height: 296.5mm;">{sections[3].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
        <div class="spread-half" style="width: 210mm; height: 296.5mm;">{sections[0].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
    </div>
    <div class="spread-sheet" style="width: 420mm; height: 296.5mm; display: flex;">
        <div class="spread-half" style="width: 210mm; height: 296.5mm;">{sections[1].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
        <div class="spread-half" style="width: 210mm; height: 296.5mm;">{sections[2].replace('class="leaflet-page', 'class="leaflet-page w-full h-full shadow-none rounded-none')}</div>
    </div>
</body>
</html>"""
    temp_spread_pdf_html = "/tmp/kyomu_spread_pdf_abs.html"
    with open(temp_spread_pdf_html, "w", encoding="utf-8") as tf:
        tf.write(spread_all_html)

    subprocess.run([
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={spread_pdf_path}",
        f"file://{temp_spread_pdf_html}"
    ], check=True)
    print(f"Generated: {spread_pdf_path}")

print("\nSUCCESS: All PDF and high-res JPG files generated perfectly!")
