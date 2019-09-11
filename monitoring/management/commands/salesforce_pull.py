from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project, SubProject, Country, LWRRegion


def getCountries(string):
    countries = string.split(', ')
    for country in countries:
        if " and " in country:
            countries.remove(country)
            countries.extend(country.split(' and '))
    real_countries = []
    for country in countries:
        real_country = Country.objects.filter(name=country).first()
        if real_country:
            real_countries.append(real_country)
    return real_countries


class Command(BaseCommand):
    help = 'Imports Salesforce products into Hummus'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('project_ids', nargs='*', type=int)

        # Named (optional) arguments
        parser.add_argument('--skip-projects', action='store_true', help='Skips Projects sync',)
        parser.add_argument('--skip-subprojects', action='store_true', help='Skips SubProjects sync',)

    def handle(self, *args, **options):
        username = settings.SALESFORCE_USERNAME
        password = settings.SALESFORCE_PASSWORD
        token = settings.SALESFORCE_TOKEN
        sf = Salesforce(username=username, password=password, security_token=token)

        # Get Projects

        hummus_projects = Project.objects.all()

        if not options['skip_projects']:
            sf_fields = "Id, Name, Project_Type__c, LWR_Region__c, Search_Strings__c, Start_Date__c, End_Date__c, CreatedBy.Name, Project_Identifier__c"
            if options['project_ids']:
                projects = sf.query_all("SELECT %s FROM Project__c WHERE Id IN %s" % (sf_fields, options['project_ids']))
            else:
                projects = sf.query_all("SELECT %s FROM Project__c WHERE RecordType.Name <> 'Non-Project' AND Status__c <> 'Terminated'" % (sf_fields,))
            for project in projects['records']:
                hummus_project = hummus_projects.filter(salesforce=project['Id']).first()
                if hummus_project:
                    # project exists already, update fields
                    if not hummus_project.code:
                        hummus_project.code = project['Project_Identifier__c']
                    # double check we are referring to the same subproject
                    if hummus_project.code == project['Project_Identifier__c']:
                        if project['LWR_Region__c']:
                            hummus_project.lwrregion = LWRRegion.objects.get(name=project['LWR_Region__c'])
                        hummus_project.countries.set(getCountries(project['Search_Strings__c']))
                        hummus_project.save()
                        self.stdout.write(self.style.SUCCESS('Successfully updated project %s: "%s"' % (project['Id'], project['Name'])))
                else:
                    # new project
                    real_region = LWRRegion.objects.filter(name=project['LWR_Region__c']).first()
                    new_project = Project()
                    new_project.salesforce = project['Id']
                    new_project.name = project['Name']
                    new_project.lwrregion = real_region
                    new_project.save()
                    new_project.countries.set(getCountries(project['Search_Strings__c']))
                    self.stdout.write(self.style.SUCCESS('Successfully created project %s: "%s"' % (project['Id'], project['Name'])))

        # Get Sub Projects

        if not options['skip_subprojects']:
            hummus_subprojects = SubProject.objects.all()
            sf_fields = "Id, Name, Country__r.Name, CreatedBy.Name, Sub_Project_Identifier__c, Project__r.Id, Men_Direct_Target__c, Men_Indirect_Target__c, Women_Direct_Target__c, Women_Indirect_Target__c"
            if options['project_ids']:
                subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.Id IN %s" % (sf_fields, options['project_ids']))
            else:
                subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.RecordType.Name <> 'Non-Project' AND Project__r.Status__c <> 'Terminated'" % (sf_fields,))
            for subproject in subprojects['records']:
                hummus_subproject = hummus_subprojects.filter(salesforce=subproject['Id']).first()
                if hummus_subproject:
                    # subproject exists already, update fields
                    if not hummus_subproject.code:
                        hummus_subproject.code = subproject['Sub_Project_Identifier__c']
                    # double check we are referring to the same subproject
                    if hummus_subproject.code == subproject['Sub_Project_Identifier__c']:
                        hummus_subproject.targetmen = subproject['Men_Direct_Target__c']
                        hummus_subproject.targetimen = subproject['Men_Indirect_Target__c']
                        hummus_subproject.targetwomen = subproject['Women_Direct_Target__c']
                        hummus_subproject.targetiwomen = subproject['Women_Indirect_Target__c']
                        hummus_subproject.save()
                        self.stdout.write(self.style.SUCCESS('Successfully updated subproject %s: "%s"' % (subproject['Id'], subproject['Name'])))
                else:
                    # new subproject
                    if hummus_projects.filter(salesforce=subproject['Project__r']['Id']).exists():
                        project = hummus_projects.filter(salesforce=subproject['Project__r']['Id']).first()
                        new_subproject = SubProject()
                        new_subproject.salesforce = subproject['Id']
                        new_subproject.name = subproject['Name']
                        new_subproject.project = project
                        new_subproject.save()
                        self.stdout.write(self.style.SUCCESS('Successfully created subproject %s: "%s"' % (subproject['Id'], subproject['Name'])))

