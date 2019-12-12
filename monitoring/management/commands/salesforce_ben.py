from django.core.management.base import BaseCommand
from django.conf import settings

from simple_salesforce import Salesforce

from monitoring.models import Beneficiaries, SubProject


def updateEntry(hummus_record, salesforce_record, options):
    fields_map = {
        'fiscalyear': 'Fiscal_Year__c', 'quarter': 'Quarter__c',
        'actualmen': 'Men_Direct_Actual__c', 'actualwomen': 'Women_Direct_Actual__c',
        'targetmen': 'Men_Direct_Target__c', 'targetwomen': 'Women_Direct_Target__c',
        'actualimen': 'Men_Indirect_Actual__c', 'actualiwomen': 'Women_Direct_Actual__c',
        'targetimen': 'Men_Indirect_Target__c',
        'targetiwomen': 'Women_Indirect_Target__c',
    }
    update = False
    for field in fields_map:
        if salesforce_record[fields_map['quarter']] is None:
            salesforce_record[fields_map['quarter']] = 0
        salesforce_value = salesforce_record[fields_map[field]]
        if hasattr(salesforce_value, 'is_integer') and salesforce_value.is_integer():
            salesforce_value = int(salesforce_value)
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
    help = 'Imports Salesforce beneficiaries into Hummus'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('subproject_ids', nargs='*', type=int)

        # Named (optional) arguments
        parser.add_argument('--verbose', action='store_true', help='Be verbose about changes',)

    def handle(self, *args, **options):
        username = settings.SALESFORCE_USERNAME
        password = settings.SALESFORCE_PASSWORD
        token = settings.SALESFORCE_TOKEN
        sf = Salesforce(username=username, password=password, security_token=token)

        # Get Beneficiaries

        hummus_bens = Beneficiaries.objects.all()
        sf_fields = "Id, Fiscal_Year__c, Quarter__c, Sub_Project__r.Id, Men_Direct_Target__c,\
                     Men_Indirect_Target__c, Women_Direct_Target__c, Women_Indirect_Target__c,\
                     Men_Direct_Actual__c, Men_Indirect_Actual__c, Women_Direct_Actual__c,\
                     Women_Indirect_Actual__c".replace(' ', '')
        if options['subproject_ids']:
            beneficiaries = sf.query_all(
                "SELECT %s FROM Beneficiaries__c WHERE Sub_Project__r.Id IN %s" % (
                    sf_fields, options['project_ids']))
        else:
            beneficiaries = sf.query_all(
                "SELECT %s FROM Beneficiaries__c"
                % (sf_fields,))
        for ben in beneficiaries['records']:
            hummus_ben = hummus_bens.filter(salesforce=ben['Id']).first()
            if hummus_ben:
                if updateEntry(hummus_ben, ben, options):
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully updated beneficiaries entry %s: "%s%s"' %
                        (ben['Id'], ben['Fiscal_Year__c'], ben['Quarter__c'])))
            else:
                new_ben = Beneficiaries()
                new_ben.salesforce = ben['Id']
                subproject = SubProject.objects.filter(
                    salesforce=ben['Sub_Project__r']['Id']).first()
                if not subproject:
                    self.stdout.write(self.style.WARNING('{} not found. Import SubProjects first'.
                                                         format(ben['Sub_Project__r']['Id'])))
                    continue
                new_ben.subproject = subproject
                updateEntry(new_ben, ben, options)
                self.stdout.write(self.style.SUCCESS('Successfully created ben %s: "%s%s"' %
                                                     (ben['Id'], ben['Fiscal_Year__c'], ben['Quarter__c'])))
