
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H

# Live Netlify website page
data = data = "https://smartcampusqr.netlify.app/index.html"

# Save QR images in the same folder
output_dir = os.path.dirname(os.path.abspath(__file__))

qr_paths = [
    os.path.join(output_dir, "smart_campus_qr.png"),
    os.path.join(output_dir, "Qr.PNG"),
]

qr = qrcode.QRCode(
    version=None,
    error_correction=ERROR_CORRECT_H,
    box_size=15,
    border=6,
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(
    fill_color="black",
    back_color="white"
).convert("RGB")

for qr_path in qr_paths:
    img.save(qr_path)

print("QR Code created successfully!")
print("QR DATA:", data)
print("Saved at:", ", ".join(qr_paths))

img.show()
