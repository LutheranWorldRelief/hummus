"""
Tests for 'monitoring'
"""
from django.test import TestCase

from monitoring.models import Contact


class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(first_name="Trey Polk", last_name="Polk")
        #Contact.objects.create(first_name="Willena", last_name="Vanalstyne")
        #Contact.objects.create(first_name="Gilberto", last_name="Gilsdorf")
        #Contact.objects.create(first_name="Maranda", last_name="Pedro")

    def test_name_generation(self):
        """name is created from first and last name"""
        Contact.objects.create(first_name="Maranda", last_name="Pedro")
        contact = Contact.objects.get(first_name="Maranda", last_name="Pedro")
        self.assertEqual(contact.name, "Maranda Pedro")

    def test_remove_spaces(self):
        """name trims spaces"""
        contact = Contact.objects.create(first_name=" Willena  ", last_name="   Vanalstyne ")
        self.assertEqual(contact.name, "Willena Vanalstyne")
        self.assertEqual(contact.first_name, "Willena")
        self.assertEqual(contact.last_name, "Vanalstyne")
