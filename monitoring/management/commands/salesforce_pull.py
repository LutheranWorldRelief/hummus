from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project

class Command(BaseCommand):
    help = 'Imports Salesforce products into Hummus'

    def add_arguments(self, parser):
        parser.add_argument('project_ids', nargs='*', type=int)

    def handle(self, *args, **options):
        username = settings.SALESFORCE_USERNAME
        password = settings.SALESFORCE_PASSWORD
        token = settings.SALESFORCE_TOKEN
        sf = Salesforce(username=username, password=password, security_token=token)
        sf_fields = "Id, Name, \
                    Project__r.Project_Type__c,\
                    Project__r.LWR_Region__c,\
                    Country__r.Name,\
                    Project__r.Start_Date__c,\
                    Project__r.End_Date__c,\
                    CreatedBy.Name,\
                    Project__r.Project_Identifier__c,\
                    Sub_Project_Identifier__c"
        if options['project_ids']:
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Id IN %s" % (options['project_ids']))
        else:
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Hummus_Id = NULL")
        for project in subprojects['records']:
            if qs.filter(saleforce_subproject=project['Id']).exists():
                # FIXME: Update Salesforce Hummus_Id
            else:
                project.salesforce_subproject = project['Id']
                project.name = project['name']
                project.save()
            self.stdout.write(self.style.SUCCESS('Successfully created project "%s: %s"' % (project.id, project.name))
