#!/usr/bin/env python3
import os
from PIL import Image, ImageOps, ImageDraw, ImageFilter

DEST_DIR = "/Users/kotsuka/Documents/systemDev/csd-website/images/clinical"
os.makedirs(DEST_DIR, exist_ok=True)

def add_clean_shadow_border(img, border_color=(226, 232, 240), border_width=2):
    # Add border
    bordered = ImageOps.expand(img, border=border_width, fill=border_color)
    return bordered

# --- 1. STEP 01: 学生事前入力 + 17.5万件施設DB ---
base_s1 = Image.open(os.path.join(DEST_DIR, "clinical_student_pre_entry.png")).convert("RGBA")
# Crop base to focus on student input table
w, h = base_s1.size
base_s1_cropped = base_s1.crop((0, int(h * 0.12), w, h))

inset_s1 = Image.open(os.path.join(DEST_DIR, "clinical_facility_database_170k.png")).convert("RGBA")
# Crop inset to focus on 175,409 facilities header and departments
wi, hi = inset_s1.size
inset_s1_crop = inset_s1.crop((int(wi * 0.22), int(hi * 0.12), wi, int(hi * 0.75)))
# resize inset
target_w = int(base_s1_cropped.width * 0.46)
target_h = int(inset_s1_crop.height * (target_w / inset_s1_crop.width))
inset_s1_res = inset_s1_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
inset_s1_styled = add_clean_shadow_border(inset_s1_res, border_color=(13, 148, 136), border_width=4)

s1_comp = base_s1_cropped.copy()
paste_x = s1_comp.width - inset_s1_styled.width - 30
paste_y = s1_comp.height - inset_s1_styled.height - 30
s1_comp.paste(inset_s1_styled, (paste_x, paste_y), inset_s1_styled)
s1_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_step01_composite.png"), quality=96)
print("Updated: clinical_step01_composite.png")

# --- 2. STEP 02: 学生視点マトリクス + 施設視点スロット & 距離 ---
base_s2 = Image.open(os.path.join(DEST_DIR, "clinical_placement_matrix_students.png")).convert("RGBA")
w, h = base_s2.size
base_s2_cropped = base_s2.crop((0, int(h * 0.14), w, h))

inset_s2 = Image.open(os.path.join(DEST_DIR, "clinical_placement_facility_slots.png")).convert("RGBA")
wi, hi = inset_s2.size
# Crop to show facility slot and distance in km
inset_s2_crop = inset_s2.crop((int(wi * 0.15), int(hi * 0.14), wi, int(hi * 0.85)))
target_w = int(base_s2_cropped.width * 0.46)
target_h = int(inset_s2_crop.height * (target_w / inset_s2_crop.width))
inset_s2_res = inset_s2_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
inset_s2_styled = add_clean_shadow_border(inset_s2_res, border_color=(2, 132, 199), border_width=4)

s2_comp = base_s2_cropped.copy()
paste_x = s2_comp.width - inset_s2_styled.width - 30
paste_y = s2_comp.height - inset_s2_styled.height - 30
s2_comp.paste(inset_s2_styled, (paste_x, paste_y), inset_s2_styled)
s2_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_step02_composite.png"), quality=96)
print("Updated: clinical_step02_composite.png")

# --- 3. STEP 03: NAVITIME API モーダル + Web地図 ---
base_s3 = Image.open(os.path.join(DEST_DIR, "clinical_navitime_route_search.png")).convert("RGBA")
map_s3 = Image.open(os.path.join(DEST_DIR, "clinical_navitime_web_map.png")).convert("RGBA")
# Crop map to route between Niihama and Shikokuchuo
wm, hm = map_s3.size
map_crop = map_s3.crop((int(wm * 0.28), int(hm * 0.30), int(wm * 0.82), int(hm * 0.80)))
target_w = int(base_s3.width * 0.45)
target_h = int(map_crop.height * (target_w / map_crop.width))
map_res = map_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
map_styled = add_clean_shadow_border(map_res, border_color=(16, 185, 129), border_width=4)

s3_comp = base_s3.copy()
paste_x = s3_comp.width - map_styled.width - 25
paste_y = s3_comp.height - map_styled.height - 25
s3_comp.paste(map_styled, (paste_x, paste_y), map_styled)
s3_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_step03_composite.png"), quality=96)
print("Updated: clinical_step03_composite.png")

# --- 4. STEP 04: Booking.com 宿泊施設検索 ---
# Base modal cropped slightly to focus cleanly on hotel list and rates
base_s4 = Image.open(os.path.join(DEST_DIR, "clinical_booking_hotel_search.png")).convert("RGB")
base_s4.save(os.path.join(DEST_DIR, "clinical_step04_composite.png"), quality=96)
print("Updated: clinical_step04_composite.png")

# --- 5. KEY 01: 実習生プロフィール (顔写真自動挿入) ---
k1 = Image.open(os.path.join(DEST_DIR, "clinical_student_profile_photo.png")).convert("RGB")
k1.save(os.path.join(DEST_DIR, "clinical_key01_profile_zoom.png"), quality=96)
print("Updated: clinical_key01_profile_zoom.png")

# --- 6. KEY 02: 臨床実習施設情報用紙 (学生配布用) + 実習生一覧表 ---
# We make facility info sheet prominent, with report overlapping on bottom-left
sheet_k2 = Image.open(os.path.join(DEST_DIR, "clinical_facility_info_sheet.png")).convert("RGBA")
rep_k2 = Image.open(os.path.join(DEST_DIR, "clinical_student_report.png")).convert("RGBA")

# Create a neat light background canvas: 1600 x 1300
canvas_k2 = Image.new("RGBA", (1600, 1300), (248, 250, 252, 255))
# Resize sheet to occupy right ~65%
target_h = 1220
sheet_w = int(sheet_k2.width * (target_h / sheet_k2.height))
sheet_res = sheet_k2.resize((sheet_w, target_h), Image.Resampling.LANCZOS)
sheet_styled = add_clean_shadow_border(sheet_res, border_color=(13, 148, 136), border_width=3)

# Resize report
rep_h = 950
rep_w = int(rep_k2.width * (rep_h / rep_k2.height))
rep_res = rep_k2.resize((rep_w, rep_h), Image.Resampling.LANCZOS)
rep_styled = add_clean_shadow_border(rep_res, border_color=(203, 213, 225), border_width=2)

# Paste report on left, sheet overlapping on right
canvas_k2.paste(rep_styled, (30, 180), rep_styled)
canvas_k2.paste(sheet_styled, (1600 - sheet_styled.width - 30, 40), sheet_styled)
canvas_k2.convert("RGB").save(os.path.join(DEST_DIR, "clinical_key02_facility_sheet_composite.png"), quality=96)
print("Updated: clinical_key02_facility_sheet_composite.png")

# --- 7. KEY 03: 実習指導依頼文書 + 実習承諾管理 ---
req_k3 = Image.open(os.path.join(DEST_DIR, "clinical_request_documents.png")).convert("RGBA")
con_k3 = Image.open(os.path.join(DEST_DIR, "clinical_consent_management.png")).convert("RGBA")

w, h = req_k3.size
# Crop top bar slightly
req_crop = req_k3.crop((0, int(h * 0.12), w, h))

wi, hi = con_k3.size
con_crop = con_k3.crop((int(wi * 0.12), int(hi * 0.12), wi, int(hi * 0.85)))
target_w = int(req_crop.width * 0.44)
target_h = int(con_crop.height * (target_w / con_crop.width))
con_res = con_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
con_styled = add_clean_shadow_border(con_res, border_color=(2, 132, 199), border_width=4)

k3_comp = req_crop.copy()
paste_x = 30
paste_y = k3_comp.height - con_styled.height - 30
k3_comp.paste(con_styled, (paste_x, paste_y), con_styled)
k3_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_key03_request_consent_composite.png"), quality=96)
print("Updated: clinical_key03_request_consent_composite.png")

# --- 8. KEY 04: チェックリスト管理 + INTEVE LINK連携 ---
chk_k4 = Image.open(os.path.join(DEST_DIR, "clinical_checklist_management.png")).convert("RGBA")
dash_k4 = Image.open(os.path.join(DEST_DIR, "clinical_dashboard_overview.png")).convert("RGBA")

w, h = chk_k4.size
chk_crop = chk_k4.crop((0, int(h * 0.12), w, h))

wi, hi = dash_k4.size
dash_crop = dash_k4.crop((int(wi * 0.12), int(hi * 0.12), wi, int(hi * 0.85)))
target_w = int(chk_crop.width * 0.45)
target_h = int(dash_crop.height * (target_w / dash_crop.width))
dash_res = dash_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
dash_styled = add_clean_shadow_border(dash_res, border_color=(16, 185, 129), border_width=4)

k4_comp = chk_crop.copy()
paste_x = k4_comp.width - dash_styled.width - 30
paste_y = k4_comp.height - dash_styled.height - 30
k4_comp.paste(dash_styled, (paste_x, paste_y), dash_styled)
k4_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_key04_checklist_link_composite.png"), quality=96)
print("Updated: clinical_key04_checklist_link_composite.png")

print("All v2 images created cleanly!")
