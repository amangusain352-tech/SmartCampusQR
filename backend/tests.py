from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import TeacherProfile


class CampusNavigationTests(TestCase):
    def test_homepage_loads_and_links_to_service_selection(self):
        response = self.client.get(reverse("welcome"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "service-selection.html")

    def test_service_selection_page_loads(self):
        response = self.client.get(reverse("service_selection"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What service do")

    def test_static_service_selection_path_loads(self):
        response = self.client.get("/service-selection.html")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What service do")

    def test_generated_qr_returns_a_png_image(self):
        response = self.client.get(reverse("generate_qr"), HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")


class TeacherAuthenticationTests(TestCase):
    def test_registration_saves_profile_and_opens_dashboard(self):
        response = self.client.post(
            reverse("teacher_register"),
            {
                "full_name": "Test Teacher Profile",
                "faculty_id": "FAC-TEST-204",
                "department": "Applied Sciences",
                "designation": "Assistant Professor",
                "phone": "+91 90000 12345",
                "email": "teacher@example.edu",
                "cabin": "Room A-12",
                "call_hours": "10 AM - 12 PM",
                "subjects": "Physics, Chemistry",
                "password": "StrongTeacherPass_927!",
                "confirm_password": "StrongTeacherPass_927!",
            },
        )

        self.assertRedirects(
            response,
            reverse("teacher_dashboard"),
            fetch_redirect_response=False,
        )
        profile = TeacherProfile.objects.get(faculty_id="FAC-TEST-204")
        self.assertTrue(profile.user.check_password("StrongTeacherPass_927!"))

        dashboard = self.client.get(reverse("teacher_dashboard"))
        self.assertContains(dashboard, "Test Teacher Profile")
        self.assertContains(dashboard, "Applied Sciences")
        self.assertContains(dashboard, "teacher@example.edu")
        self.assertContains(dashboard, "Room A-12")
        self.assertContains(dashboard, "Physics, Chemistry")
        self.assertNotContains(dashboard, "Prof. Aman Gusain")
        self.assertNotContains(dashboard, "Rohan Sharma")

    def test_teacher_can_sign_in_with_faculty_id(self):
        user = User.objects.create_user(
            username="faculty@example.edu",
            email="faculty@example.edu",
            password="StrongTeacherPass_927!",
        )
        TeacherProfile.objects.create(
            user=user,
            full_name="Faculty Member",
            faculty_id="FAC-LOGIN-205",
            department="Computer Science",
            designation="Assistant Professor",
            phone="9000012345",
            cabin="Room B-20",
            call_hours="1 PM - 3 PM",
            subjects="Algorithms",
        )

        response = self.client.post(
            reverse("teacher_login"),
            {
                "identifier": "FAC-LOGIN-205",
                "password": "StrongTeacherPass_927!",
            },
        )

        self.assertRedirects(
            response,
            reverse("teacher_dashboard"),
            fetch_redirect_response=False,
        )
        self.assertContains(self.client.get(reverse("teacher_dashboard")), "Faculty Member")

    def test_dashboard_requires_teacher_login(self):
        response = self.client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("teacher_portal")))