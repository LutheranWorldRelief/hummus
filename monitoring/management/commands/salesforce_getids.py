from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project

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
                    Sub_Project_Identifier__c"
        qs = Project.objects.all()
        if options['project_ids']:
            qs.filter(id__in=project_ids)
        for project in qs:
            qs.filter(salesforce_project__isnull=True, saleforce_subproject__isnull=True)
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Sub_Project__c.Name = '%s' OR Sub_Project__c.Project__r.Name = '%s'" % (
                project.name, project.name)
            )
            if len(subprojects['records']):
                found = subprojects['records'][0]
                status = 'FOUND: %s' % (found['Id'])
                if found['Name'] == project.name:
                    project.salesforce_subproject = found['Id']
                if found['Project_r']['Name'] == project.name:
                    project.salesforce_project = found['Project_r']['Id']
                project.save()
                # FIXME: update Hummus_Id field in Salesforce Sub Project or Project
            else:
                status = 'N/A'

            #self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
            print("%s: %s: %s" % (project.id, status, project.name))
