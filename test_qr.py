import webbrowser
from PIL import Image
from pyzbar.pyzbar import decode

# Apni QR image ka naam yaha likhein
image_path = "smart_campus_qr.png"

try:
    # Image load karke decode karein
    img = Image.open(image_path)
    decoded_objects = decode(img)

    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            print("QR WORKING ✅")
            print("QR DATA:", qr_data)
            print("-" * 40)
            
            # Terminal Service Selection Menu
            print("=== SMART CAMPUS SERVICE OPTIONS ===")
            print("1. Open Link in Browser")
            print("2. Copy QR Data to Clipboard / View Only")
            print("3. Process as Attendance/Check-in")
            print("4. Exit")
            
            choice = input("\nApni service select karein (1-4): ").strip()
            
            if choice == "1":
                print("Opening link in browser...")
                webbrowser.open(qr_data)
            elif choice == "2":
                print(f"QR Data successfully loaded: {qr_data}")
            elif choice == "3":
                print(f"Attendance recorded for data: {qr_data} (Success ✅)")
            else:
                print("Exiting service menu.")
    else:
        print("QR NOT DETECTED ❌")

except Exception as e:
    print("Error:", e)