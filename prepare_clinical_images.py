#!/usr/bin/env python3
import os
import shutil
from PIL import Image, ImageOps, ImageFilter

SRC_DIR = "/Users/kotsuka/Documents/systemDev/csd-website/base_files"
DEST_DIR = "/Users/kotsuka/Documents/systemDev/csd-website/images/clinical"
os.makedirs(DEST_DIR, exist_ok=True)

# 1. Copy raw screenshots with clean descriptive names
mapping = {
    "Screenshot 2026-09-07 at 19.19.14.png": "clinical_dashboard_overview.png",
    "Screenshot 2026-09-07 at 19.19.20.png": "clinical_student_list.png",
    "Screenshot 2026-09-07 at 19.20.09.png": "clinical_student_report.png",
    "Screenshot 2026-09-07 at 19.20.55.png": "clinical_facility_info_sheet.png",
    "Screenshot 2026-09-07 at 19.23.51.png": "clinical_student_profile_photo.png",
    "Screenshot 2026-09-07 at 19.24.41.png": "clinical_consent_management.png",
    "Screenshot 2026-09-07 at 19.26.14.png": "clinical_placement_facility_slots.png",
    "Screenshot 2026-09-07 at 19.26.22.png": "clinical_placement_matrix_students.png",
    "Screenshot 2026-09-07 at 19.27.43.png": "clinical_checklist_management.png",
    "Screenshot 2026-09-07 at 19.28.05.png": "clinical_facility_database_170k.png",
    "Screenshot 2026-09-07 at 19.29.12.png": "clinical_student_pre_entry.png",
    "Screenshot 2026-09-07 at 19.34.51.png": "clinical_request_documents.png",
    "Screenshot 2026-09-07 at 19.39.44.png": "clinical_booking_hotel_search.png",
    "Screenshot 2026-09-07 at 19.44.01.png": "clinical_navitime_route_search.png",
    "Screenshot 2026-09-07 at 19.45.47.png": "clinical_navitime_web_map.png",
}

for src_name, dest_name in mapping.items():
    src_file = os.path.join(SRC_DIR, src_name)
    dest_file = os.path.join(DEST_DIR, dest_name)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied: {dest_name}")

print("\nProcessing and generating composite assets...")

def add_card_styling(img, border_color=(203, 213, 225), border_width=2):
    return ImageOps.expand(img, border=border_width, fill=border_color)

# --- STEP 01 Composite ---
img_s1_base = Image.open(os.path.join(DEST_DIR, "clinical_student_pre_entry.png")).convert("RGBA")
img_s1_inset = Image.open(os.path.join(DEST_DIR, "clinical_facility_database_170k.png")).convert("RGBA")

w_base, h_base = img_s1_base.size
w_in, h_in = img_s1_inset.size
inset_target_w = int(w_base * 0.48)
inset_target_h = int(h_in * (inset_target_w / w_in))
img_s1_inset_resized = img_s1_inset.resize((inset_target_w, inset_target_h), Image.Resampling.LANCZOS)
img_s1_inset_styled = add_card_styling(img_s1_inset_resized, border_color=(13, 148, 136), border_width=4)

s1_composite = img_s1_base.copy()
paste_x = w_base - img_s1_inset_styled.width - 40
paste_y = h_base - img_s1_inset_styled.height - 40
s1_composite.paste(img_s1_inset_styled, (paste_x, paste_y), img_s1_inset_styled.convert("RGBA"))
s1_composite.convert("RGB").save(os.path.join(DEST_DIR, "clinical_step01_composite.png"), quality=95)
print("Created: clinical_step01_composite.png")

# --- STEP 02 Composite ---
img_s2_base = Image.open(os.path.join(DEST_DIR, "clinical_placement_matrix_students.png")).convert("RGBA")
img_s2_inset = Image.open(os.path.join(DEST_DIR, "clinical_placement_facility_slots.png")).convert("RGBA")

w_base, h_base = img_s2_base.size
w_in, h_in = img_s2_inset.size
inset_target_w = int(w_base * 0.46)
inset_target_h = int(h_in * (inset_target_w / w_in))
img_s2_inset_resized = img_s2_inset.resize((inset_target_w, inset_target_h), Image.Resampling.LANCZOS)
img_s2_inset_styled = add_card_styling(img_s2_inset_resized, border_color=(2, 132, 199), border_width=4)

s2_composite = img_s2_base.copy()
paste_x = w_base - img_s2_inset_styled.width - 40
paste_y = h_base - img_s2_inset_styled.height - 40
s2_composite.paste(img_s2_inset_styled, (paste_x, paste_y), img_s2_inset_styled.convert("RGBA"))
s2_composite.convert("RGB").save(os.path.join(DEST_DIR, "clinical_step02_composite.png"), quality=95)
print("Created: clinical_step02_composite.png")

# --- STEP 03 Composite ---
img_s3_base = Image.open(os.path.join(DEST_DIR, "clinical_navitime_route_search.png")).convert("RGBA")
img_s3_map = Image.open(os.path.join(DEST_DIR, "clinical_navitime_web_map.png")).convert("RGBA")

w_map, h_map = img_s3_map.size
map_crop = img_s3_map.crop((int(w_map * 0.25), int(h_map * 0.25), int(w_map * 0.85), int(h_map * 0.85)))

w_base, h_base = img_s3_base.size
inset_target_w = int(w_base * 0.46)
inset_target_h = int(map_crop.height * (inset_target_w / map_crop.width))
map_resized = map_crop.resize((inset_target_w, inset_target_h), Image.Resampling.LANCZOS)
map_styled = add_card_styling(map_resized, border_color=(16, 185, 129), border_width=4)

s3_composite = img_s3_base.copy()
paste_x = w_base - map_styled.width - 30
paste_y = h_base - map_styled.height - 30
s3_composite.paste(map_styled, (paste_x, paste_y), map_styled.convert("RGBA"))
s3_composite.convert("RGB").save(os.path.join(DEST_DIR, "clinical_step03_composite.png"), quality=95)
print("Created: clinical_step03_composite.png")

# --- STEP 04 Composite ---
img_s4 = Image.open(os.path.join(DEST_DIR, "clinical_booking_hotel_search.png")).convert("RGB")
img_s4.save(os.path.join(DEST_DIR, "clinical_step04_composite.png"), quality=95)
print("Created: clinical_step04_composite.png")

# --- KEY 01 Profile Image ---
img_k1 = Image.open(os.path.join(DEST_DIR, "clinical_student_profile_photo.png")).convert("RGB")
img_k1.save(os.path.join(DEST_DIR, "clinical_key01_profile_zoom.png"), quality=95)
print("Created: clinical_key01_profile_zoom.png")

# --- KEY 02 Facility Info Sheet Composite ---
img_k2_sheet = Image.open(os.path.join(DEST_DIR, "clinical_facility_info_sheet.png")).convert("RGBA")
img_k2_report = Image.open(os.path.join(DEST_DIR, "clinical_student_report.png")).convert("RGBA")

k2_canvas = Image.new("RGBA", (1800, 1600), (248, 250, 252, 255))
target_h = 1500
k2_rep_w = int(img_k2_report.width * (target_h / img_k2_report.height))
k2_rep_res = img_k2_report.resize((k2_rep_w, target_h), Image.Resampling.LANCZOS)
k2_rep_styled = add_card_styling(k2_rep_res, border_color=(203, 213, 225), border_width=2)

k2_sht_w = int(img_k2_sheet.width * (target_h / img_k2_sheet.height))
k2_sht_res = img_k2_sheet.resize((k2_sht_w, target_h), Image.Resampling.LANCZOS)
k2_sht_styled = add_card_styling(k2_sht_res, border_color=(13, 148, 136), border_width=3)

k2_canvas.paste(k2_rep_styled, (40, 50), k2_rep_styled.convert("RGBA"))
k2_canvas.paste(k2_sht_styled, (1800 - k2_sht_styled.width - 40, 50), k2_sht_styled.convert("RGBA"))
k2_canvas.convert("RGB").save(os.path.join(DEST_DIR, "clinical_key02_facility_sheet_composite.png"), quality=95)
print("Created: clinical_key02_facility_sheet_composite.png")

# --- KEY 03 Request and Consent Composite ---
img_k3_req = Image.open(os.path.join(DEST_DIR, "clinical_request_documents.png")).convert("RGBA")
img_k3_con = Image.open(os.path.join(DEST_DIR, "clinical_consent_management.png")).convert("RGBA")

w_base, h_base = img_k3_req.size
w_in, h_in = img_k3_con.size
inset_w = int(w_base * 0.44)
inset_h = int(h_in * (inset_w / w_in))
con_res = img_k3_con.resize((inset_w, inset_h), Image.Resampling.LANCZOS)
con_styled = add_card_styling(con_res, border_color=(2, 132, 199), border_width=4)

k3_comp = img_k3_req.copy()
paste_x = 40
paste_y = h_base - con_styled.height - 40
k3_comp.paste(con_styled, (paste_x, paste_y), con_styled.convert("RGBA"))
k3_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_key03_request_consent_composite.png"), quality=95)
print("Created: clinical_key03_request_consent_composite.png")

# --- KEY 04 Checklist and INTEVE LINK Composite ---
img_k4_chk = Image.open(os.path.join(DEST_DIR, "clinical_checklist_management.png")).convert("RGBA")
img_k4_dash = Image.open(os.path.join(DEST_DIR, "clinical_dashboard_overview.png")).convert("RGBA")

w_base, h_base = img_k4_chk.size
w_in, h_in = img_k4_dash.size
inset_w = int(w_base * 0.45)
inset_h = int(h_in * (inset_w / w_in))
dash_res = img_k4_dash.resize((inset_w, inset_h), Image.Resampling.LANCZOS)
dash_styled = add_card_styling(dash_res, border_color=(16, 185, 129), border_width=4)

k4_comp = img_k4_chk.copy()
paste_x = w_base - dash_styled.width - 40
paste_y = h_base - dash_styled.height - 40
k4_comp.paste(dash_styled, (paste_x, paste_y), dash_styled.convert("RGBA"))
k4_comp.convert("RGB").save(os.path.join(DEST_DIR, "clinical_key04_checklist_link_composite.png"), quality=95)
print("Created: clinical_key04_checklist_link_composite.png")

# --- HERO COMPOSITE (PAGE 1) ---
hero_w = 2600
hero_h = 1500
hero_canvas = Image.new("RGBA", (hero_w, hero_h), (255, 255, 255, 0))

base_mat = Image.open(os.path.join(DEST_DIR, "clinical_placement_matrix_students.png")).convert("RGBA")
b_w = 2100
b_h = int(base_mat.height * (b_w / base_mat.width))
base_mat_res = base_mat.resize((b_w, b_h), Image.Resampling.LANCZOS)
base_mat_styled = add_card_styling(base_mat_res, border_color=(203, 213, 225), border_width=3)
hero_canvas.paste(base_mat_styled, (60, 20), base_mat_styled.convert("RGBA"))

route_im = Image.open(os.path.join(DEST_DIR, "clinical_navitime_route_search.png")).convert("RGBA")
r_w = 1000
r_h = int(route_im.height * (r_w / route_im.width))
route_res = route_im.resize((r_w, r_h), Image.Resampling.LANCZOS)
route_styled = add_card_styling(route_res, border_color=(13, 148, 136), border_width=5)
hero_canvas.paste(route_styled, (20, hero_h - r_h - 20), route_styled.convert("RGBA"))

book_im = Image.open(os.path.join(DEST_DIR, "clinical_booking_hotel_search.png")).convert("RGBA")
bk_w = 950
bk_h = int(book_im.height * (bk_w / book_im.width))
book_res = book_im.resize((bk_w, bk_h), Image.Resampling.LANCZOS)
book_styled = add_card_styling(book_res, border_color=(2, 132, 199), border_width=5)
hero_canvas.paste(book_styled, (960, hero_h - bk_h - 20), book_styled.convert("RGBA"))

prof_im = Image.open(os.path.join(DEST_DIR, "clinical_student_profile_photo.png")).convert("RGBA")
p_h = 750
p_w = int(prof_im.width * (p_h / prof_im.height))
prof_res = prof_im.resize((p_w, p_h), Image.Resampling.LANCZOS)
prof_styled = add_card_styling(prof_res, border_color=(16, 185, 129), border_width=4)
hero_canvas.paste(prof_styled, (hero_w - p_w - 20, 30), prof_styled.convert("RGBA"))

hero_canvas.convert("RGB").save(os.path.join(DEST_DIR, "clinical_hero_composite.png"), quality=95)
print("Created: clinical_hero_composite.png")

print("\nAll clinical image assets prepared successfully!")
