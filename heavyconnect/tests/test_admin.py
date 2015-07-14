from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver

class AdminTestCase(LiveServerTestCase):
	def setUp(self):
		# setUp is where you instantiate the selenium webdriver and loads the browser.
		User.objects.create_superuser(
			username='admin',
			password='admin',
			email='admin@example.com'
		)

		self.selenium = webdriver.Chrome()
		self.selenium.maximize_window()
		super(AdminTestCase, self).setUp()

	def tearDown(self):
		# Call tearDown to close the web browser
		self.selenium.quit()
		super(AdminTestCase, self).tearDown()

	def test_admin_access_home(self):
		self.selenium.get(
			'%s%s' % (self.live_server_url, "/home/")
		)

		assert "login" in self.selenium.title