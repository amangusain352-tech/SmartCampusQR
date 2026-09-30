import os
import webbrowser
from PIL import Image
from pyzbar.pyzbar import decode
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

def welcome_view(request):
    image_path = os.path.join(settings.BASE_DIR, "Qr.png")
    output_logs = []
    
    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            decoded_objects = decode(img)

            if decoded_objects:
                for obj in decoded_objects:
                    qr_data = obj.data.decode("utf-8")
                    output_logs.append("QR WORKING ✅")
                    output_logs.append(f"QR DATA: {qr_data}")
            else:
                output_logs.append("QR NOT DETECTED ❌")
        else:
            output_logs.append(f"Error: Image nahi mili path par -> {image_path}")
            
    except Exception as e:
        output_logs.append(f"Error: {e}")

    # welcome.html template ko logs ke sath render karne ke liye
    context = {'logs': output_logs}
    return render(request, 'welcome.html', context)

def service_selection_view(request):
    try:
        return render(request, "service-selection.html")
    except Exception:
        return HttpResponse("<h2>Smart Campus Service Selection</h2>")

def python_scanner_view(request):
    try:
        return render(request, "scanner.html")
    except Exception:
        return HttpResponse("<h2>Python QR Scanner</h2>")

def generate_qr_view(request):
    return HttpResponse("<h2>QR Code Generator</h2><p>QR code generated successfully.</p>")

def page_render_view(request, page_name):
    if not page_name.endswith('.html'):
        page_name += '.html'
    try:
        return render(request, page_name)
    except Exception:
        return HttpResponse(f"<h2>Page '{page_name}' not found</h2>", status=404)
