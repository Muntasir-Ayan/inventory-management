# yourapp/management/commands/insert_demo_data.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from inventory.models import Location, Accommodation, LocalizeAccommodation

class Command(BaseCommand):
    help = 'Inserts demo data into the database'

    def handle(self, *args, **kwargs):
        # Setup Django settings (only needed if running the script directly)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

        # 1. Create a Location (e.g., New York City)
        location = Location.objects.create(
            id="US_NY_NYC",
            title="New York City",
            center=Point(-74.0060, 40.7128),  # Longitude, Latitude
            location_type="city",
            country_code="US",
            state_abbr="NY",
            city="New York",
        )

        # 2. Create a User (e.g., John Doe)
        user = User.objects.create_user(
            username="john_doe",
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )

        # 3. Create an Accommodation (e.g., Luxury Apartment in NYC)
        accommodation = Accommodation.objects.create(
            id="ACM001",
            feed=1,
            title="Luxury Apartment in NYC",
            country_code="US",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=250.00,
            center=Point(-74.0060, 40.7128),  # Longitude, Latitude
            images=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
            location=location,
            amenities=["WiFi", "Air Conditioning", "Heater"],
            user=user,
            published=True
        )

        # 4. Create Localized Descriptions and Policies
        # English localization
        localization_en = LocalizeAccommodation.objects.create(
            property=accommodation,
            language="en",
            description="A luxurious 2-bedroom apartment in the heart of New York City, offering stunning views and modern amenities.",
            policy={
                "pet_policy": "No pets allowed",
                "check_in": "After 3 PM",
                "check_out": "Before 11 AM"
            }
        )

        # French localization
        localization_fr = LocalizeAccommodation.objects.create(
            property=accommodation,
            language="fr",
            description="Un appartement de luxe de 2 chambres au cœur de New York, offrant une vue imprenable et des équipements modernes.",
            policy={
                "pet_policy": "Animaux non admis",
                "check_in": "Après 15h",
                "check_out": "Avant 11h"
            }
        )

        # Print success message
        self.stdout.write(self.style.SUCCESS('Demo data inserted successfully!'))
