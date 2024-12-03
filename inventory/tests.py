from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib.gis.geos import Point
from .models import Location, Accommodation, LocalizeAccommodation
from .forms import CustomUserCreationForm


class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="LOC001",
            title="Test City",
            center=Point(12.971598, 77.594566),
            location_type="city",
            country_code="IN",
            state_abbr="KA",
            city="Bangalore"
        )

    def test_location_creation(self):
        self.assertEqual(self.location.title, "Test City")
        self.assertEqual(self.location.country_code, "IN")
        self.assertEqual(self.location.location_type, "city")

    def test_str_representation(self):
        self.assertEqual(str(self.location), "Test City")


class AccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.location = Location.objects.create(
            id="LOC002",
            title="Test Location",
            center=Point(10.0, 20.0),
            location_type="city",
            country_code="US"
        )
        self.accommodation = Accommodation.objects.create(
            id="ACM001",
            title="Test Accommodation",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=120.00,
            center=Point(10.0, 20.0),
            location=self.location,
            user=self.user,
            images=[{"url": "http://example.com/image.jpg"}]
        )

    def test_accommodation_creation(self):
        self.assertEqual(self.accommodation.title, "Test Accommodation")
        self.assertEqual(self.accommodation.bedroom_count, 2)
        self.assertEqual(self.accommodation.user.username, "testuser")
        self.assertEqual(self.accommodation.images[0]['url'], "http://example.com/image.jpg")


class LocalizeAccommodationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="LOC003",
            title="Localized Test Location",
            center=Point(15.0, 30.0),
            location_type="city",
            country_code="US"
        )
        self.accommodation = Accommodation.objects.create(
            id="ACM002",
            title="Localized Accommodation",
            bedroom_count=3,
            usd_rate=150.00,
            center=Point(15.0, 30.0),
            location=self.location,
            images=[{"url": "http://example.com/localized.jpg"}]
        )
        self.localized_accommodation = LocalizeAccommodation.objects.create(
            property=self.accommodation,
            language="en",
            description="Sample description",
            policy={"check_in": "2 PM", "check_out": "11 AM"}
        )

    def test_localized_accommodation_creation(self):
        self.assertEqual(self.localized_accommodation.language, "en")
        self.assertIn("check_in", self.localized_accommodation.policy)
        self.assertEqual(self.localized_accommodation.description, "Sample description")


class SignupViewTest(TestCase):
    def setUp(self):
        Group.objects.create(name="Property Owners")

    def test_signup_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/signup.html")

    def test_signup_view_post_success(self):
        response = self.client.post(reverse("signup"), {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Password123!",
            "password2": "Password123!"
        })
        self.assertRedirects(response, "/admin", status_code=302, target_status_code=200, fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username="testuser").exists())


    def test_signup_view_post_failure(self):
        response = self.client.post(reverse("signup"), {
            "username": "",
            "email": "test@example.com",
            "password1": "Password123!",
            "password2": "Password123!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")


class CustomUserCreationFormTest(TestCase):
    def test_form_valid(self):
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Password123!",
            "password2": "Password123!"
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Password123!",
            "password2": "Password456!"
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ["The two password fields didn’t match."])
