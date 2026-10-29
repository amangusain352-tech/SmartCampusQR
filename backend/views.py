import os
from io import BytesIO
import webbrowser
from PIL import Image
from pyzbar.pyzbar import decode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
import qrcode
from .models import TeacherProfile

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

    # Render the homepage with QR diagnostics.
    context = {'logs': output_logs}
    return render(request, 'index.html', context)

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
    base_url = os.environ.get("SMARTCAMPUS_BASE_URL", "").rstrip("/")
    landing_path = "/select-services.html"
    landing_url = (
        f"{base_url}{landing_path}"
        if base_url
        else request.build_absolute_uri(landing_path)
    )
    image = qrcode.make(landing_url)
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")

    response = HttpResponse(image_buffer.getvalue(), content_type="image/png")
    response["Cache-Control"] = "no-store"
    return response

def page_render_view(request, page_name):
    if not page_name.endswith('.html'):
        page_name += '.html'
    try:
        return render(request, page_name)
    except Exception:
        return HttpResponse(f"<h2>Page '{page_name}' not found</h2>", status=404)


def teacher_portal_view(request):
    return render(request, "teacherportal.html")


def teacher_register_view(request):
    if request.method != "POST":
        return redirect("teacher_portal")

    full_name = request.POST.get("full_name", "").strip()
    faculty_id = request.POST.get("faculty_id", "").strip().upper()
    department = request.POST.get("department", "").strip()
    designation = request.POST.get("designation", "").strip()
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip().lower()
    cabin = request.POST.get("cabin", "").strip()
    call_hours = request.POST.get("call_hours", "").strip()
    subjects = request.POST.get("subjects", "").strip()
    password = request.POST.get("password", "")
    confirm_password = request.POST.get("confirm_password", "")

    if password != confirm_password:
        messages.error(request, "Passwords do not match.")
        return redirect("teacher_portal")

    if User.objects.filter(email__iexact=email).exists():
        messages.error(request, "An account with this email already exists. Please sign in.")
        return redirect("teacher_portal")

    if TeacherProfile.objects.filter(faculty_id__iexact=faculty_id).exists():
        messages.error(request, "This faculty ID is already registered.")
        return redirect("teacher_portal")

    user = User(username=email, email=email)
    try:
        validate_password(password, user=user)
    except ValidationError as error:
        for message in error.messages:
            messages.error(request, message)
        return redirect("teacher_portal")

    try:
        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=password)
            TeacherProfile.objects.create(
                user=user,
                full_name=full_name,
                faculty_id=faculty_id,
                department=department,
                designation=designation,
                phone=phone,
                cabin=cabin,
                call_hours=call_hours,
                subjects=subjects,
            )
    except IntegrityError:
        messages.error(request, "An account with those details already exists. Please sign in.")
        return redirect("teacher_portal")

    login(request, user)
    return redirect("teacher_dashboard")


def teacher_login_view(request):
    if request.method != "POST":
        return redirect("teacher_portal")

    identifier = request.POST.get("identifier", "").strip()
    password = request.POST.get("password", "")
    user = None

    if "@" in identifier:
        user = User.objects.filter(email__iexact=identifier).first()
    else:
        profile = TeacherProfile.objects.select_related("user").filter(
            faculty_id__iexact=identifier
        ).first()
        user = profile.user if profile else None

    authenticated_user = authenticate(
        request,
        username=user.username if user else identifier,
        password=password,
    )
    if authenticated_user is None or not hasattr(authenticated_user, "teacher_profile"):
        messages.error(request, "Invalid faculty email/ID or password.")
        return redirect("teacher_portal")

    login(request, authenticated_user)
    return redirect("teacher_dashboard")


@login_required(login_url="teacher_portal")
def teacher_dashboard_view(request):
    try:
        teacher = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        logout(request)
        messages.error(request, "No teacher profile is linked to this account. Please register.")
        return redirect("teacher_portal")

    initials = "".join(part[0] for part in teacher.full_name.split()[:2]).upper()
    return render(
        request,
        "teacherdashboard.html",
        {"teacher": teacher, "teacher_initials": initials or "T"},
    )


def teacher_logout_view(request):
    logout(request)
    return redirect("teacher_portal")
