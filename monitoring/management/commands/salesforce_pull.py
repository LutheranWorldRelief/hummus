from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Project, SubProject, Country, LWRRegion, Organization


def getByName(model, string):
    result = model.objects.filter(name=string).first()
    return result


def getCountries(string):
    countries = string.split(', ')
    for country in countries:
        if " and " in country:
            countries.remove(country)
            countries.extend(country.split(' and '))
    countries.sort()
    real_countries = []
    for country in countries:
        real_country = Country.objects.filter(name=country).first()
        if real_country:
            real_countries.append(real_country)
    return real_countries


def updateOrganization(hummus_record, salesforce_record, options):
    if options['verbose']:
        print(salesforce_record['Name'])
    fields_map = {'status': 'Organization_Status__c', 'name': 'Name', 'varname': 'Acronym__c',
                  'country': 'BillingCountry', 'salesforce': 'Id'}
    # 'country': ['BillingCountry', 'Name'],}
    update = False
    for field in fields_map:
        if isinstance(fields_map[field], list):
            salesforce_value = salesforce_record[fields_map[field][0]][fields_map[field][1]]
        else:
            salesforce_value = salesforce_record[fields_map[field]]
        if field == 'country':
            salesforce_value = getByName(Country, salesforce_value)
        if str(getattr(hummus_record, field)) != str(salesforce_value):
            if options['verbose']:
                print("field {} : {} != {}".format(
                    field, getattr(hummus_record, field), salesforce_value))
            setattr(hummus_record, field, salesforce_value)
            update = True
    if update:
        hummus_record.save()
    return update


def updateProject(hummus_record, salesforce_record, options):
    if options['verbose']:
        print(salesforce_record['Name'])
    fields_map = {'status': 'Status__c', 'start': 'Start_Date__c', 'end': 'End_Date__c',
                  'recordtype': ['RecordType', 'Name'], 'lwrregion': 'LWR_Region__c',
                  'owner': ['Owner', 'Name'], 'atype': 'Project_Type__c', 'countries': 'Search_Strings__c',
                  'actualmen': 'Men_Direct_Rollup__c', 'actualwomen': 'Women_Direct_Rollup__c',
                  'targetmen': 'Target_Men_Direct_Rollup__c', 'targetwomen': 'Target_Women_Direct_Rollup__c',
                  'actualimen': 'Men_Indirect_Rollup__c', 'actualiwomen': 'Women_Indirect_Rollup__c',
                  'targetimen': 'Target_Men_Indirect_Rollup__c',
                  'targetiwomen': 'Target_Women_Indirect_Rollup__c', }
    update = False
    for field in fields_map:
        if isinstance(fields_map[field], list):
            salesforce_value = salesforce_record[fields_map[field][0]][fields_map[field][1]]
        else:
            salesforce_value = salesforce_record[fields_map[field]]
        if hasattr(salesforce_value, 'is_integer') and salesforce_value.is_integer():
            salesforce_value = int(salesforce_value)
        if field == 'lwrregion':
            salesforce_value = getByName(LWRRegion, salesforce_value)
        if field == 'countries':
            countries = getCountries(salesforce_record['Search_Strings__c'])
            if countries != list(hummus_record.countries.all()):
                if options['verbose']:
                    print('Update countries {} with {}'.format(
                        countries, hummus_record.countries.all()))
                update = True
                hummus_record.countries.set(countries)
            continue
        if str(getattr(hummus_record, field)) != str(salesforce_value):
            if options['verbose']:
                print("field {} : {} != {}".format(
                    field, getattr(hummus_record, field), salesforce_value))
            setattr(hummus_record, field, salesforce_value)
            update = True
    if update:
        hummus_record.save()
    return update


def updateSubProject(hummus_record, salesforce_record, options):
    fields_map = {'status': 'Status__c', 'start': 'Start_Date__c', 'end': 'End_Date__c',
                  'recordtype': ['RecordType', 'Name'], 'lwrregion': 'LWR_Region__c',
                  'country': ['Country__r', 'Name'], 'atype': 'Type__c',
                  'agriculture': 'Agriculture__c',
                  'agriculture_count': 'Agriculture_Count__c',
                  'eoperations_count': 'Emergency_Operations_Count__c',
                  'climatechange_count': 'Climate_Change_Count__c',
                  'actualmen': 'Men_Direct_Actual__c', 'actualwomen': 'Women_Direct_Actual__c',
                  'targetmen': 'Men_Direct_Target__c', 'targetwomen': 'Women_Direct_Target__c',
                  'actualimen': 'Men_Indirect_Actual__c', 'actualiwomen': 'Women_Direct_Actual__c',
                  'targetimen': 'Men_Indirect_Target__c',
                  'targetiwomen': 'Women_Indirect_Target__c',
                  'organization': ['Implementer__r', 'Name']}
    update = False
    for field in fields_map:
        if isinstance(fields_map[field], list):
            if salesforce_record[fields_map[field][0]]:
                salesforce_value = salesforce_record[fields_map[field][0]][fields_map[field][1]]
        else:
            salesforce_value = salesforce_record[fields_map[field]]
        if hasattr(salesforce_value, 'is_integer') and salesforce_value.is_integer():
            salesforce_value = int(salesforce_value)
        if field == 'organization':
            salesforce_value = getByName(Organization, salesforce_value)
        if field == 'lwrregion':
            salesforce_value = getByName(LWRRegion, salesforce_value)
        if field == 'country':
            salesforce_value = getByName(Country, salesforce_value)
        if str(getattr(hummus_record, field)) != str(salesforce_value):
            if options['verbose']:
                print("field {} : {} != {}".format(
                    field, getattr(hummus_record, field), salesforce_value))
            setattr(hummus_record, field, salesforce_value)
            update = True
    if update:
        hummus_record.save()
    return update


class Command(BaseCommand):
    help = 'Imports Salesforce products into Hummus'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('project_ids', nargs='*', type=int)

        # Named (optional) arguments
        parser.add_argument('--verbose', action='store_true', help='Be verbose about changes',)
        parser.add_argument('--skip-organizations', action='store_true',
                            help='Skips Organizations sync',)
        parser.add_argument('--skip-projects', action='store_true', help='Skips Projects sync',)
        parser.add_argument('--skip-subprojects', action='store_true',
                            help='Skips SubProjects sync',)

    def handle(self, *args, **options):
        username = settings.SALESFORCE_USERNAME
        password = settings.SALESFORCE_PASSWORD
        token = settings.SALESFORCE_TOKEN
        sf = Salesforce(username=username, password=password, security_token=token)

        # Get Organizations

        if not options['skip_organizations']:
            hummus_organizations = Organization.objects.all()
            sf_fields = "Id, Name, Organization_Status__c, Acronym__c, BillingCountry"
            organizations = sf.query_all("SELECT %s FROM Account" % (sf_fields,))
            for organization in organizations['records']:
                hummus_organization = hummus_organizations.filter(
                    salesforce=organization['Id']).first()
                if not hummus_organization and organization['Name']:
                    hummus_organization = hummus_organizations.filter(
                        name=organization['Name']).first()
                # if not hummus_organization and organization['Acronym__c']:
                #    hummus_organization = hummus_organizations.filter(Q(name=organization['Acronym__c']) | Q(varname=organization['Acronym__c'])).first()
                if hummus_organization:
                    if updateOrganization(hummus_organization, organization, options):
                        self.stdout.write(self.style.SUCCESS(
                            'Successfully updated organization %s: "%s"' % (organization['Id'], organization['Name'])))
                else:
                    hummus_organization = Organization()
                    updateOrganization(hummus_organization, organization, options)
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully created organization %s: "%s"' % (organization['Id'], organization['Name'])))

        # Get Projects

        hummus_projects = Project.objects.all()

        if not options['skip_projects']:
            sf_fields = "Id, Name, RecordType.Name, Project_Type__c, Owner.Name, LWR_Region__c, Search_Strings__c, Status__c, Start_Date__c, End_Date__c, CreatedBy.Name, Project_Identifier__c, Men_Direct_Rollup__c, Women_Direct_Rollup__c, Target_Men_Direct_Rollup__c, Target_Women_Direct_Rollup__c, Men_Indirect_Rollup__c, Women_Indirect_Rollup__c, Target_Men_Indirect_Rollup__c, Target_Women_Indirect_Rollup__c"
            if options['project_ids']:
                projects = sf.query_all("SELECT %s FROM Project__c WHERE Id IN %s" % (sf_fields, options['project_ids']))
            else:
                projects = sf.query_all("SELECT %s FROM Project__c WHERE RecordType.Name <> 'Non-Project'" % (sf_fields,))
            for project in projects['records']:
                hummus_project = hummus_projects.filter(salesforce=project['Id']).first()
                if hummus_project:
                    # project exists already, update fields
                    if not hummus_project.code:
                        hummus_project.code = project['Project_Identifier__c']
                    # double check we are referring to the same subproject
                    if hummus_project.code == project['Project_Identifier__c']:
                        if updateProject(hummus_project, project, options):
                            self.stdout.write(self.style.SUCCESS('Successfully updated project %s: "%s"' % (project['Id'], project['Name'])))
                else:
                    # new project
                    new_project = Project()
                    new_project.salesforce = project['Id']
                    new_project.name = project['Name']
                    new_project.code = project['Project_Identifier__c']
                    new_project.save()
                    updateProject(new_project, project, options)
                    self.stdout.write(self.style.SUCCESS('Successfully created project %s: "%s"' % (project['Id'], project['Name'])))

        # Get Sub Projects

        if not options['skip_subprojects']:
            hummus_subprojects = SubProject.objects.all()
            sf_fields = "Id, Name, RecordType.Name, Type__c, LWR_Region__c, Country__r.Name, CreatedBy.Name, Sub_Project_Identifier__c, Project__r.Id, Start_Date__c, End_Date__c, Status__c, Implementer__r.Name, Men_Direct_Target__c, Men_Indirect_Target__c, Women_Direct_Target__c, Women_Indirect_Target__c, Men_Direct_Actual__c, Men_Indirect_Actual__c, Women_Direct_Actual__c, Women_Indirect_Actual__c, Agriculture__c, Agriculture_Count__c, Emergency_Operations_Count__c, Climate_Change_Count__c"
            if options['project_ids']:
                subprojects = sf.query_all("SELECT %s FROM Sub_Project__c WHERE Project__r.Id IN %s" % (
                    sf_fields, options['project_ids']))
            else:
                subprojects = sf.query_all(
                    "SELECT %s FROM Sub_Project__c WHERE Project__r.RecordType.Name <> 'Non-Project'" % (sf_fields,))
            for subproject in subprojects['records']:
                # check if organization exists
                if subproject['Implementer__r'] and not getByName(Organization, subproject['Implementer__r']['Name']):
                    Organization.objects.create(name=subproject['Implementer__r']['Name'])
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully added organization "%s"' % (subproject['Implementer__r']['Name'],)))
                hummus_subproject = hummus_subprojects.filter(salesforce=subproject['Id']).first()
                if hummus_subproject:
                    # subproject exists already, update fields
                    if not hummus_subproject.code:
                        hummus_subproject.code = subproject['Sub_Project_Identifier__c']
                    # double check we are referring to the same subproject
                    if hummus_subproject.code == subproject['Sub_Project_Identifier__c']:
                        if updateSubProject(hummus_subproject, subproject, options):
                            self.stdout.write(self.style.SUCCESS('Successfully updated subproject %s: "%s"' % (subproject['Id'], subproject['Name'])))
                else:
                    # new subproject
                    if hummus_projects.filter(salesforce=subproject['Project__r']['Id']).exists():
                        project = hummus_projects.filter(salesforce=subproject['Project__r']['Id']).first()
                        new_subproject = SubProject()
                        new_subproject.salesforce = subproject['Id']
                        new_subproject.name = subproject['Name']
                        new_subproject.code = subproject['Sub_Project_Identifier__c']
                        new_subproject.project = project
                        new_subproject.save()
                        updateSubProject(new_subproject, subproject, options)
                        self.stdout.write(self.style.SUCCESS('Successfully created subproject %s: "%s"' % (subproject['Id'], subproject['Name'])))
