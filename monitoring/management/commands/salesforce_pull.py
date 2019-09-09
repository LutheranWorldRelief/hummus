from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project, SubProject

class Command(BaseCommand):
    help = 'Imports Salesforce products into Hummus'

    def add_arguments(self, parser):
        parser.add_argument('project_ids', nargs='*', type=int)

    def handle(self, *args, **options):
        username = settings.SALESFORCE_USERNAME
        password = settings.SALESFORCE_PASSWORD
        token = settings.SALESFORCE_TOKEN
        sf = Salesforce(username=username, password=password, security_token=token)


        # Get Projects

        qs = Project.objects.all()
        sf_fields = "Id, Name, Project_Type__c, LWR_Region__c, Search_Strings__c, Start_Date__c, End_Date__c, CreatedBy.Name, Project_Identifier__c"
        if options['project_ids']:
            projects = sf.query_all("SELECT %s FROM Project__c WHERE Id IN %s" % (sf_fields, options['project_ids']))
        else:
            projects = sf.query_all("SELECT %s FROM Project__c WHERE RecordType.Name <> 'Non-Project' AND Status__c <> 'Terminated'" % (sf_fields,))
        for project in projects['records']:
            if qs.filter(salesforce=project['Id']).exists():
                # project exists already, update fields
                pass
            else:
                # new project
                """
                new_project = Project()
                new_project.salesforce = project['Id']
                new_project.name = project['name']
                new_project.save()
                """
                self.stdout.write(self.style.SUCCESS('Successfully created project "%s: %s"' % (project['Id'], project['Name'])))

        # Get Sub Projects

        qs = SubProject.objects.all()
        sf_fields = "Id, Name, Country__r.Name, CreatedBy.Name, Sub_Project_Identifier__c"
        if options['project_ids']:
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.Id IN %s" % (sf_fields, options['project_ids']))
        else:
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.RecordType.Name <> 'Non-Project' AND Project__r.Status__c <> 'Terminated'" % (sf_fields,))
        for subproject in subprojects['records']:
            if qs.filter(salesforce=subproject['Id']).exists():
                # subproject exists already, update fields
                pass
            else:
                # new subproject
                """
                new_subproject = SubProject()
                new_subproject.salesforce = subproject['Id']
                new_subproject.name = subproject['name']
                new_subproject.project = project
                new_project.save()
                """
                self.stdout.write(self.style.SUCCESS('Successfully created subproject "%s: %s"' % (subproject['Id'], subproject['Name'])))
