from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from django.utils import translation

class LoginHomeViewsTest(TestCase):
	fixtures = ['user.json']

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_basic_login(self):
		'''
			Test if the login function is working properly
		'''

		resp = self.client.post(reverse('login'),{'username': 'bss3', 'password' : '123'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp.status_code, 200)
		
