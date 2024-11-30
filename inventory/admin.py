from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_type', 'country_code', 'state_abbr', 'city')
    search_fields = ('title',)

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_id', 'usd_rate', 'review_score', 'published')
    list_filter = ('published', 'country_code', 'location_id')
    search_fields = ('title', 'country_code', 'location_id__title')

class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'language', 'description')
    search_fields = ('property_id__title', 'language')

admin.site.register(Location, LocationAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
