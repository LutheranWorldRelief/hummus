from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import requests

from monitoring.models import Country, LWRRegion

class Command(BaseCommand):
    help = 'Gets countries regions using restcountries.eu'

    url = 'https://restcountries.eu/rest/v2/alpha/'

    def handle(self, *args, **options):
        qs = Country.objects.all()
        if args:
            qs.filter(id__in=args)
        for country in qs:
            r = requests.get("%s%s" % (self.url, country.id))
            data = r.json()
            region = data['region']
            subregion = data['subregion']
            phonecode = data['callingCodes'][0]
            lwrregion = LWRRegion.objects.filter(subregions__icontains=subregion)
            if lwrregion:
                country.lwrregion = lwrregion[0]
                self.stdout.write(self.style.SUCCESS('Successfully added country "%s" region "%s"' % (country.name, country.lwrregion) ))
            country.region = region
            country.subregion = subregion
            country.phonecode = phonecode
            country.save()
