import re
import datetime
from django import forms

from .models import Person
from django.core.exceptions import ValidationError

class PersonForm(forms.Form):
    first_name 		= forms.CharField(max_length=30)
    last_name 		= forms.CharField(max_length=30)
    date_of_birth 	= forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    zip_code 		= forms.CharField(max_length=9)

    def is_valid(self):
		valid = super(PersonForm, self).is_valid()

		if not valid:
			return valid

		if self.cleaned_data['date_of_birth'] > datetime.date.today():
			self.add_error('date_of_birth', 'Date of birth is invalid because it is set in the future')
			return False

		if re.match('^(\d{5}(-\d{4})?|[A-Z]\d[A-Z] ?\d[A-Z]\d)$', self.cleaned_data['zip_code']) == None:
			self.add_error('zip_code', 'Zipcode is not valid')
			return False

		return True 

    def create_person(self):
    	"""
		Create a new person record
    	"""
        person = Person()
        self.__update_person(person, self.cleaned_data)        
        
    def edit_person(self, pk):
    	"""
    	Updates an existing person record
    	"""        
        person = Person.objects.get(pk=pk) 
        self.__update_person(person, self.cleaned_data)

    def __update_person(self, person, person_data):
    	person.first_name 		= person_data['first_name']
        person.last_name 		= person_data['last_name']
        person.date_of_birth 	= person_data['date_of_birth']
        person.zip_code 		= person_data['zip_code']
        person.save()      