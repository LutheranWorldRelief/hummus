from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Count, Q, Value, F

import requests

from monitoring.models import Contact, ProjectContact, Organization

class Command(BaseCommand):
    help = 'Tries to de duplicate Contacts'

    def handle(self, *args, **options):
        duplicates = Contact.objects.values('first_name', 'last_name', 'name', 'document',
                                            'country').annotate(name_count=Count('*')).\
                                            filter(name_count__gt=1)
        print('There are {} duplicates'.format(duplicates.count()))
        for duplicate in duplicates:
            subdupes = Contact.objects.filter(name=duplicate['name'],
                                              first_name=duplicate['first_name'],
                                              last_name=duplicate['last_name'],
                                              document=duplicate['document'],
                                              country=duplicate['country'])
            print('{} has {} duplicates'.format(duplicate['name'], subdupes.count()))
