# Use the Django shell to insert data into your models
from inventory.models import Location, Accommodation, LocalizeAccommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
import random

# Create a User (this will be used for accommodation's user)
user = User.objects.create_user(username='demo_user', password='demo_password')

# Add some Location data
locations = [
    Location(id="L001", title="North America", center=Point(-98.35, 39.5), location_type='continent', country_code='US', state_abbr='XX', city='Unknown City'),
    Location(id="L002", title="United States", center=Point(-95.7129, 37.0902), location_type='country', country_code='US', state_abbr='XX', city='Unknown City'),
    Location(id="L003", title="California", center=Point(-119.4179, 36.7783), location_type='state', country_code='US', state_abbr='CA', city='Sacramento'),
    Location(id="L004", title="San Francisco", center=Point(-122.4194, 37.7749), location_type='city', country_code='US', state_abbr='CA', city='San Francisco'),
]

# Bulk create locations
Location.objects.bulk_create(locations)

# Add some Accommodation data
accommodations = [
    Accommodation(id="A001", title="Cozy Apartment in San Francisco", feed=1, country_code="US", bedroom_count=2, review_score=4.5, usd_rate=150.00, 
                  center=Point(-122.4194, 37.7749), images=['https://example.com/image1.jpg', 'https://example.com/image2.jpg'], 
                  location=Location.objects.get(id="L004"), amenities=['WiFi', 'Kitchen'], user=user, published=True),
    
    Accommodation(id="A002", title="Luxury House in California", feed=2, country_code="US", bedroom_count=5, review_score=4.8, usd_rate=350.00, 
                  center=Point(-119.4179, 36.7783), images=['https://example.com/image3.jpg', 'https://example.com/image4.jpg'], 
                  location=Location.objects.get(id="L003"), amenities=['WiFi', 'Pool', 'Hot Tub'], user=user, published=True),
    
    Accommodation(id="A003", title="Beach House in California", feed=3, country_code="US", bedroom_count=3, review_score=4.7, usd_rate=250.00, 
                  center=Point(-122.4702, 37.7697), images=['https://example.com/image5.jpg', 'https://example.com/image6.jpg'], 
                  location=Location.objects.get(id="L003"), amenities=['WiFi', 'Pool'], user=user, published=True),
]

# Bulk create accommodations
Accommodation.objects.bulk_create(accommodations)

# Add some LocalizeAccommodation data (for localization in different languages)
localize_accommodations = [
    LocalizeAccommodation(property=Accommodation.objects.get(id="A001"), language="en", description="A cozy apartment in the heart of San Francisco.", policy={"pet_policy": "No pets allowed"}),
    LocalizeAccommodation(property=Accommodation.objects.get(id="A001"), language="es", description="Un apartamento acogedor en el corazón de San Francisco.", policy={"pet_policy": "No se permiten mascotas"}),
    LocalizeAccommodation(property=Accommodation.objects.get(id="A002"), language="en", description="Luxury house with stunning views in California.", policy={"pet_policy": "Pets allowed with a fee"}),
    LocalizeAccommodation(property=Accommodation.objects.get(id="A002"), language="fr", description="Maison de luxe avec vues imprenables en Californie.", policy={"pet_policy": "Animaux autorisés avec un supplément"}),
]

# Bulk create LocalizeAccommodations
LocalizeAccommodation.objects.bulk_create(localize_accommodations)

# Confirmation message
print("Demo data has been successfully added to the database!")
