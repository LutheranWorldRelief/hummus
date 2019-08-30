from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project

class Command(BaseCommand):
    help = 'Compares local projects with Salesforce projects'

    def add_arguments(self, parser):
        parser.add_argument('project_ids', nargs='*', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_ids']:
        #    try:
        #        poll = Poll.objects.get(pk=poll_id)
        #    except Poll.DoesNotExist:
        #        raise CommandError('Poll "%s" does not exist' % poll_id)
	#
        #    poll.opened = False
        #    poll.save()

        #    self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
        username = settings.SALESFORCE_USERNAME
        password = settings.SALESFORCE_PASSWORD
        token = settings.SALESFORCE_TOKEN
        if options['project_ids']:
            print("Let's go...")
        else:
            for project in Project.objects.all():
                sf = Salesforce(username=username, password=password, security_token=token)

                subprojects = sf.query_all("SELECT \
                    Id, \
                    Project__r.Project_Type__c,\
                    Project__r.LWR_Region__c,\
                    Country__r.Name,\
                    Project__r.Start_Date__c,\
                    Project__r.End_Date__c,\
                    CreatedBy.Name,\
                    Project__r.Project_Identifier__c,\
                    Sub_Project_Identifier__c,\
                    Name\
                    FROM Sub_Project__c WHERE Sub_Project__c.Name = '%s' OR Sub_Project__c.Project__r.Name = '%s'" % (project.name, project.name))

                if len(subprojects['records']):
                    status = 'FOUND: %s' % (subprojects['records'][0]['Id'])
                else:
                    status = 'N/A'

                print("%s: %s: %s" % (project.id, status, project.name))
