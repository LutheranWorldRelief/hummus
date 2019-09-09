from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project

def soql_escape(string):
    # Escape backslashes and single-quotes, in that order.
    return string.replace("\\", "\\\\").replace("'", "\\'")

class Command(BaseCommand):
    help = 'Gets Salesforce IDs for projects created in Hummus'

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
                    Project__r.Id,\
                    Sub_Project_Identifier__c"
        qs = Project.objects.all()
        if options['project_ids']:
            qs = qs.filter(id__in=project_ids)
        for project in qs:
            qs = qs.filter(salesforce__isnull=True)
            # FIXME add list of ids to exclude
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.Name = '%s'" % (
                sf_fields, soql_escape(project.name))
            )
            if len(subprojects['records']):
                found = subprojects['records'][0]
                status = 'FOUND: %s' % (found['Project__r']['Id'])
                project.salesforce = found['Project__r']['Id']
                project.save()
            else:
                status = 'N/A'

            print("%s, %s, %s" % (project.id, status, soql_escape(project.name)))
