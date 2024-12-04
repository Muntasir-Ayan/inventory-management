from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        # Optional: you can specify which fields to import/export here
        fields = ('id', 'title', 'center', 'parent', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')

class LocationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type',)
    resource_class = LocationResource

admin.site.register(Location, LocationAdmin)

class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'user__username')
    list_filter = ('published', 'country_code', 'bedroom_count')
    list_editable = ('published',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            queryset = queryset.filter(user=request.user)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:  # If creating a new object
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].disabled = True  # Disable editing the 'user' field
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # When creating a new instance
            obj.user = request.user  # Ensure the user is set to the logged-in user

            # Automatically set the country_code based on the associated Location
            if obj.location:  # Ensure the 'location' is provided
                obj.country_code = obj.location.country_code

        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = request.user.__class__.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Accommodation, AccommodationAdmin)

class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language', 'description', 'policy')  # Display key fields in the list
    search_fields = ('property__title', 'language')  # Searching by accommodation title and language
    list_filter = ('language',)

admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
