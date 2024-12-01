from django.core.management.base import BaseCommand
from inventory.models import Location
import json

class Command(BaseCommand):
    help = 'Generate sitemap.json'

    def handle(self, *args, **kwargs):
        sitemap = []
        for country in Location.objects.filter(location_type="country"):
            data = {
                country.title: country.country_code.lower(),
                "locations": [
                    {loc.title: f"{country.country_code.lower()}/{loc.title.lower()}"}
                    for loc in Location.objects.filter(parent_id=country.id)
                ]
            }
            sitemap.append(data)

        with open('sitemap.json', 'w') as f:
            json.dump(sitemap, f, indent=2)
        self.stdout.write("sitemap.json generated!")
