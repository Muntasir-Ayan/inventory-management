from django.core.management.base import BaseCommand
from inventory.models import Location, Accommodation, LocalizeAccommodation
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(username='tester', password='password123')
        
        continent = Location.objects.create(
            id="LOC0012",
            title="Europe",
            center=Point(13.41, 52.52),
            location_type="continent",
            country_code=""
        )
        
        country = Location.objects.create(
            id="LOC0021",
            title="Germany",
            center=Point(13.41, 52.52),
            parent=continent,
            location_type="country",
            country_code="DE"
        )
        
        city = Location.objects.create(
            id="LOC0031",
            title="Berlin",
            center=Point(13.41, 52.52),
            parent=country,
            location_type="city",
            country_code="DE"
        )
        
        accommodation = Accommodation.objects.create(
            id="ACM0012",
            title="Berlin Central Apartment",
            feed=1,
            country_code="DE",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=120.00,
            center=Point(13.41, 52.52),
            images={"image_urls": ["image1.jpg", "image2.jpg"]},
            location=city,
            amenities=["WiFi", "Parking", "Breakfast"],
            user=user,
            published=True
        )
        
        LocalizeAccommodation.objects.create(
            property=accommodation,
            language="en",
            description="Beautiful central apartment in Berlin with all amenities.",
            policy={"check_in": "after 2 PM", "check_out": "before 11 AM"}
        )
        LocalizeAccommodation.objects.create(
            property=accommodation,
            language="de",
            description="Schöne zentrale Wohnung in Berlin mit allen Annehmlichkeiten.",
            policy={"check_in": "nach 14 Uhr", "check_out": "vor 11 Uhr"}
        )
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
