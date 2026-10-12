from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # views.py ko import karein

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Root URL par welcome page chalega
    path('', views.welcome_view, name='welcome'),

    # 2. Service selection page
    path('service-selection/', views.service_selection_view, name='service_selection'),

    # 3. Scanner test karne ke liye path
    path('python-scan/', views.python_scanner_view, name='python_scan'),
    # 4. QR code generate karne ke liye path
    path('generate-qr/', views.generate_qr_view, name='generate_qr'),
    path('teacherportal.html', views.teacher_portal_view, name='teacher_portal'),
    path('teacher/register/', views.teacher_register_view, name='teacher_register'),
    path('teacher/login/', views.teacher_login_view, name='teacher_login'),
    path('teacher/logout/', views.teacher_logout_view, name='teacher_logout'),
    path('teacherdashboard.html', views.teacher_dashboard_view, name='teacher_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static('/', document_root=settings.BASE_DIR)

urlpatterns += [
    # 5. Generic page renderer for static templates (e.g. login.html, register.html, etc.)
    path('<str:page_name>', views.page_render_view, name='page_render'),
]
