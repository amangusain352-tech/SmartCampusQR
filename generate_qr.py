import os
import qrcode

# QR image ko isi Python file ke folder mein save karega
qr_path = os.path.join(
    os.path.dirname(__file__),
    "smart_campus_qr.png"
)

# QR scan hone ke baad ab service selection page open hoga
data = "http://127.0.0.1:5500/service-selection.html"

# QR create
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)

qr.add_data(data)

qr.make(fit=True)

# Image
img = qr.make_image(
    fill_color="black",
    back_color="white"
)

# Save
img.save(qr_path)

print("QR Code created successfully!")
print("Saved at:", qr_path)

# Screen par QR show
img.show()