from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import requests

from monitoring.models import Country

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
            print("%s : %s : %s : %s" % (country.name, region, subregion, phonecode))
            country.continent = region
            country.subregion = subregion
            country.phonecode = phonecode
            country.save()
            #self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
