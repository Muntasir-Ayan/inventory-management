from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation

class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type',)

admin.site.register(Location, LocationAdmin)

# Registering Accommodation Model with admin

class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'user__username')
    list_filter = ('published', 'country_code', 'bedroom_count')
    list_editable = ('published',)

    # Override the get_queryset method to filter by the logged-in user
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            queryset = queryset.filter(user=request.user)
        return queryset

    # Override the get_form method to customize the form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Set the 'user' field to the logged-in user and disable it
        if obj is None:  # If creating a new object
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].disabled = True  # Disable editing the 'user' field

        return form

    # Prevent modification of the 'user' field in the form
    def save_model(self, request, obj, form, change):
        if not change:  # When creating a new instance
            obj.user = request.user  # Ensure the user is set to the logged-in user
        super().save_model(request, obj, form, change)

    # Ensure the 'user' field is never shown as a dropdown (for new objects)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = request.user.__class__.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Register the admin
admin.site.register(Accommodation, AccommodationAdmin)


# Registering LocalizeAccommodation Model with admin
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language', 'description', 'policy')  # Display key fields in the list
    search_fields = ('property__title', 'language')  # Searching by accommodation title and language
    list_filter = ('language',)

admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
