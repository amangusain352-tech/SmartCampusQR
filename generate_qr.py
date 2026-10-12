import os
import qrcode

# PC ka LAN IP
base_url = "http://192.168.1.12:5500"
data = f"{base_url}/service-selection.html"

output_dir = os.path.dirname(__file__)

qr_paths = [
    os.path.join(output_dir, "smart_campus_qr.png"),
    os.path.join(output_dir, "Qr.PNG"),
]

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(
    fill_color="black",
    back_color="white"
)

for qr_path in qr_paths:
    img.save(qr_path)

print("QR Code created successfully!")
print("QR DATA:", data)
print("Saved at:", ", ".join(qr_paths))

img.show()