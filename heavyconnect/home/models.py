from django.db import models
from django.contrib.auth.models import User

class HeavyUser(models.Model):
	user = models.OneToOneField(User)
	dob = models.DateTimeField()