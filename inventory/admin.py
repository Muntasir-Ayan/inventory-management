from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type',)

admin.site.register(Location, LocationAdmin)

# Registering Accommodation Model with admin
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'user__username')  # Searching by accommodation title and user username
    list_filter = ('published', 'country_code', 'bedroom_count')
    list_editable = ('published',)  # Allow editing the 'published' field directly in the list view

    # Override the get_queryset method to filter by the logged-in user
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            # If the user is in the "Property Owners" group, filter accommodations by user
            queryset = queryset.filter(user=request.user)
        return queryset

admin.site.register(Accommodation, AccommodationAdmin)

# Registering LocalizeAccommodation Model with admin
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language', 'description', 'policy')  # Display key fields in the list
    search_fields = ('property__title', 'language')  # Searching by accommodation title and language
    list_filter = ('language',)

admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
