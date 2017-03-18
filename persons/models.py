from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from django.db import models

class Person(models.Model):
	"""
	There are no uniques in this model. I don't think we need any since we can have multiple people
	with the exact same name, born in the exact same day, and living in the exact same area
	"""
	first_name 		= models.CharField(max_length=30)
	last_name 		= models.CharField(max_length=30)
	date_of_birth 	= models.DateField()
	# I'm assuming this is only for US-based people. I'm setting max length to 9 in case
	# the Zip+4 format is needed    
	zip_code		= models.CharField(max_length=9)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)