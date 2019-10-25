"""
Tests for 'monitoring'
"""
import json

from django.contrib.gis.geos import Point
from django.test import TestCase, Client

from monitoring.models import Contact, Sex
from monitoring.updates import update_contact


class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(first_name="Trey Polk", last_name="Polk")
        Contact.objects.create(first_name="Gilberto", last_name="Gilsdorf")
        Sex.objects.create(name='Man', varname='man', id='M')
        Sex.objects.create(name='Woman', varname='woman', id='F')

    def test_name_generation(self):
        """name is created from first and last name"""
        Contact.objects.create(first_name="Maranda", last_name="Pedro")
        contact = Contact.objects.get(first_name="Maranda", last_name="Pedro")
        self.assertEqual(contact.name, "Maranda Pedro")
        Contact.objects.create(name="Bruce Lehr")
        contact = Contact.objects.get(name="Bruce Lehr")
        self.assertEqual(contact.name, "Bruce Lehr")

    def test_snake_names(self):
        """changes snake_name to Snake Name"""
        Contact.objects.create(first_name="Audry", last_name="Glassford", community='snake_name')
        contact = Contact.objects.get(first_name="Audry", last_name="Glassford")
        self.assertEqual(contact.community, "Snake Name")

    def test_remove_spaces(self):
        """trims name"""
        contact = Contact.objects.create(first_name=" Willena  ", last_name="   Vanalstyne ")
        self.assertEqual(contact.name, "Willena Vanalstyne")
        self.assertEqual(contact.first_name, "Willena")
        self.assertEqual(contact.last_name, "Vanalstyne")

    def test_no_name(self):
        """tries to add a contact with no name"""
        with self.assertRaisesMessage(ValueError, 'We need a name! name, first_name and last_name seem to be empty.'):
            Contact.objects.create(document='555')

    def test_update_contact(self):
        """add a contact looking up FK using names """
        row = {}
        row['first_name'] = 'Diana'
        row['last_name'] = 'Lacey'
        row['sex'] = 'Woman'
        contact = Contact()
        request = None
        update_contact(request, contact, row)
        self.assertEqual(contact.name, "Diana Lacey")
        self.assertEqual(contact.sex.id, "F")

    def test_update_varname(self):
        """add a contact looking up FK using varnames """
        row = {}
        row['name'] = 'Amado Oberholtzer'
        row['sex'] = 'man'
        contact = Contact()
        request = None
        update_contact(request, contact, row)
        self.assertEqual(contact.name, "Amado Oberholtzer")
        self.assertEqual(contact.sex.id, "M")

    def test_find_dupes(self):
        """find duplicates using names"""
        name = "Leigha Parnell"
        Contact.objects.create(name=name, location=Point(1, 1))
        Contact.objects.create(name=name, location=Point(2, 2))
        c = Client()
        response = c.get('/opt/api-name/{}/'.format(name.upper()))
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(name, response_content['models'][0]['name'])

    def test_api_contact(self):
        """get contact json data"""
        name = "Ophelia Oshiro"
        document = "555"
        contact = Contact.objects.create(name=name, document=document, location=Point(1, 1))
        contact = Contact.objects.create(name=name, document=document, location=Point(1, 1))
        c = Client()
        response = c.get('/opt/api-contact/{}/'.format(contact.id))
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(name, response_content['models'][0]['name'])


    def test_api_contact(self):
        """get contact json data"""
        name = "Akiko Rolfe"
        document = "555"
        Contact.objects.create(name=name, document=document, location=Point(1, 1))
        Contact.objects.create(name=name, document=document, location=Point(1, 1))
        c = Client()
        response = c.get('/opt/api-doc/{}/'.format(document))
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(name, response_content['models'][0]['name'])
