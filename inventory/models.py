from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import JSONField
class Location(models.Model):
    # Define choices for location_type
    LOCATION_TYPE_CHOICES = [
        ('continent', 'Continent'),
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = models.PointField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3, default='XX')
    city = models.CharField(max_length=30, default='Unknown City')
    created_at = models.DateTimeField(auto_now_add=True)
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
    center = models.PointField()
    images = models.JSONField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    amenities = JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accommodations', blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey('Accommodation', on_delete=models.CASCADE, related_name='localized_accommodations',default='ACM001')
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = JSONField(default=dict)  # Store the policies as a dictionary

    def __str__(self):
        return f"Localization for {self.property.title} in {self.language}"
