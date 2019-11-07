from django.core.management.base import BaseCommand
from django.db.models import Count

import requests

from monitoring.models import Contact, ProjectContact

class Command(BaseCommand):
    help = 'Tries to de duplicate Contacts'

    def handle(self, *args, **options):
        # De dupes Contact
        duplicates = Contact.objects.values('first_name', 'last_name', 'name', 'document',
                                            'country').annotate(name_count=Count('*')).\
                                            filter(name_count__gt=1)
        print('There are {} "Contact" duplicates'.format(duplicates.count()))
        for duplicate in duplicates:
            ids = []
            subdupes = Contact.objects.filter(name=duplicate['name'],
                                              first_name=duplicate['first_name'],
                                              last_name=duplicate['last_name'],
                                              document=duplicate['document'],
                                              country=duplicate['country'])
            for subdupe in subdupes:
                score = 0
                for field in Contact._meta.get_fields():
                    if hasattr(subdupe, field.name) and getattr(subdupe, field.name):
                        score += 1
                subdupe.score = score
                ids.append(subdupe.id)
            winner = max(subdupes, key=lambda x: x.score)
            looser = min(subdupes, key=lambda x: x.score)
            loosers = [x.id for x in subdupes if x.id != winner.id]

            updates = ProjectContact.objects.filter(contact_id__in=ids).update(contact_id=winner.id)
            deletes = Contact.objects.filter(id__in=loosers).delete()
            print('{}: {} has {} duplicates, winner: {} (looser: {}).  Update: {}. Deletes {}.'.\
                format(winner.id, winner.name, subdupes.count(), winner.score, looser.score,
                       updates, deletes))

        # De dupes Project Contact
        duplicates = ProjectContact.objects.values('project', 'contact').\
            annotate(name_count=Count('*')).filter(name_count__gt=1)
        print('There are {} "ProjectContact" duplicates'.format(duplicates.count()))
        for duplicate in duplicates:
            ids = []
            subdupes = ProjectContact.objects.filter(contact=duplicate['contact'],
                                              project=duplicate['project'],)
            for subdupe in subdupes:
                score = 0
                for field in ProjectContact._meta.get_fields():
                    if hasattr(subdupe, field.name) and getattr(subdupe, field.name):
                        score += 1
                if subdupe.date_entry_project and\
                    (subdupe.date_entry_project < subdupe.project.start or\
                    subdupe.date_entry_project > subdupe.project.end):
                    score -= 1
                subdupe.score = score
                ids.append(subdupe.id)
            winner = max(subdupes, key=lambda x: x.score)
            looser = min(subdupes, key=lambda x: x.score)
            loosers = [x.id for x in subdupes if x.id != winner.id]

            deletes = ProjectContact.objects.filter(id__in=loosers).delete()
            print('{}: {} in {} has {} duplicates, winner: {} (looser: {}).  Deletes {}.'.\
                format(winner.id, winner.contact, winner.project, subdupes.count(), winner.score,
                       looser.score, deletes))
