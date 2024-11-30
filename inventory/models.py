from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = models.PointField()  # Geospatial point
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    location_type = models.CharField(max_length=20)  # e.g., continent, country, state, city
    country_code = models.CharField(max_length=2)  # ISO 3166-1 alpha-2
    state_abbr = models.CharField(max_length=3, null=True, blank=True)  # State abbreviation
    city = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = models.PointField()  # Geospatial point
    images = models.JSONField()  # Array of image URLs
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField()  # JSONB array of amenities
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)  # Language code (e.g., 'en')
    description = models.TextField()
    policy = models.JSONField()  # e.g., {"pet_policy": "value"}

    def __str__(self):
        return f"{self.property_id.title} ({self.language})"
