from nose.plugins.attrib import attr

from django.test import TestCase

from authentication.forms import UoftEmailForm


@attr('unit')
class UofTEmailFormTestCase(TestCase):
    def test_not_an_email(self):
        form = UoftEmailForm({'email': 'red leader'})
        self.assertFalse(form.is_valid())

    def test_a_non_uoft_email(self):
        form = UoftEmailForm({'email': 'josephbkahn@gmail.com'})
        self.assertFalse(form.is_valid())

    def test_not_an_almost_uoft_email(self):
        form = UoftEmailForm({'email': 'jkahn@mail.utoronto.com'})
        self.assertFalse(form.is_valid())

    def test_uoft_email(self):
        form = UoftEmailForm({'email': 'jkahn@mail.utoronto.ca'})
        self.assertTrue(form.is_valid())
