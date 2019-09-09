from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project, SubProject, Country, LWRRegion

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

        hummus_projects = Project.objects.all()
        sf_fields = "Id, Name, Project_Type__c, LWR_Region__c, Search_Strings__c, Start_Date__c, End_Date__c, CreatedBy.Name, Project_Identifier__c"
        if options['project_ids']:
            projects = sf.query_all("SELECT %s FROM Project__c WHERE Id IN %s" % (sf_fields, options['project_ids']))
        else:
            projects = sf.query_all("SELECT %s FROM Project__c WHERE RecordType.Name <> 'Non-Project' AND Status__c <> 'Terminated'" % (sf_fields,))
        for project in projects['records']:
            if hummus_projects.filter(salesforce=project['Id']).exists():
                # project exists already, update fields
                pass
            else:
                # new project
                countries = project['Search_Strings__c'].split(', ')
                for country in countries:
                    if " and " in country:
                        countries.remove(country)
                        countries.extend(country.split(' and '))
                real_countries = []
                for country in countries:
                    real_country = Country.objects.filter(name=country).first()
                    if real_country:
                        real_countries.append(real_country)

                real_region = LWRRegion.objects.filter(name=project['LWR_Region__c']).first()
                new_project = Project()
                new_project.salesforce = project['Id']
                new_project.name = project['Name']
                new_project.lwrregion = real_region
                new_project.save()
                new_project.countries.set(real_countries)
                self.stdout.write(self.style.SUCCESS('Successfully created project "%s: %s"' % (project['Id'], project['Name'])))

        # Get Sub Projects

        hummus_subprojects = SubProject.objects.all()
        sf_fields = "Id, Name, Country__r.Name, CreatedBy.Name, Sub_Project_Identifier__c, Project__r.Id"
        if options['project_ids']:
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.Id IN %s" % (sf_fields, options['project_ids']))
        else:
            subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.RecordType.Name <> 'Non-Project' AND Project__r.Status__c <> 'Terminated'" % (sf_fields,))
        for subproject in subprojects['records']:
            if hummus_subprojects.filter(salesforce=subproject['Id']).exists():
                # subproject exists already, update fields
                pass
            else:
                # new subproject
                if hummus_projects.filter(salesforce=subproject['Project__r']['Id']).exists():
                    project = hummus_projects.filter(salesforce=subproject['Project__r']['Id']).first()
                    new_subproject = SubProject()
                    new_subproject.salesforce = subproject['Id']
                    new_subproject.name = subproject['Name']
                    new_subproject.project = project
                    new_subproject.save()
                    self.stdout.write(self.style.SUCCESS('Successfully created subproject "%s: %s"' % (subproject['Id'], subproject['Name'])))

