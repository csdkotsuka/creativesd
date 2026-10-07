import os
from PIL import Image

src_dir = "/Users/kotsuka/Documents/systemDev/inteve_website/Provided file"
out_dir = "/Users/kotsuka/Documents/systemDev/inteve_website/images"

img_4873 = Image.open(os.path.join(src_dir, "IMG_4873.jpeg"))
img_duo = Image.open(os.path.join(src_dir, "3C4C8E17-311C-4D1D-98FC-6000713CF57B.jpeg"))
img_4872 = Image.open(os.path.join(src_dir, "IMG_4872.jpeg"))

# 1. Profile portrait from IMG_4873
# Total size: 4032 x 3024
# Face center: x ≈ 1950, y ≈ 1000
# Let's crop a square 2400x2400 around x: [750, 3150], y: [50, 2450]
crop_profile = img_4873.crop((750, 50, 3150, 2450))
crop_profile = crop_profile.resize((800, 800), Image.Resampling.LANCZOS)
crop_profile.save(os.path.join(out_dir, "profile_otsuka.jpg"), quality=88, optimize=True)

# 2. Radio studio recording photo (duo with logo)
# Total size: 1448 x 1086
# Slightly crop bottom/edges if needed, or keep complete context
crop_radio = img_duo.copy()
# Let's resize to 1200x900
crop_radio.thumbnail((1200, 900), Image.Resampling.LANCZOS)
crop_radio.save(os.path.join(out_dir, "radio_studio_recording.jpg"), quality=88, optimize=True)

# 3. Radio solo talking photo (from IMG_4873 wider view 4:3)
crop_talk = img_4873.crop((500, 100, 3700, 2500))
crop_talk.thumbnail((960, 640), Image.Resampling.LANCZOS)
crop_talk.save(os.path.join(out_dir, "radio_otsuka_talking.jpg"), quality=88, optimize=True)

print("Generated profile_otsuka.jpg, radio_studio_recording.jpg, radio_otsuka_talking.jpg")
