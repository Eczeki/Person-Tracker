from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView

from .models import Person
from .forms import PersonForm

import persons.errors


class PersonListView(ListView):

	model = Person

	def get_context_data(self, **kwargs):
		context = super(PersonListView, self).get_context_data(**kwargs)
		return context

def delete(request, pk):
	try:
		person = Person.objects.get(pk=pk)
		person.delete()
	except Person.DoesNotExist:
		messages.error(request, persons.errors.PERSON_DOES_NOT_EXIST_ERR_MSG)    
	return HttpResponseRedirect('/')

def create(request):

	# If it is a POST request process the form data
	if request.method == 'POST':
		form = PersonForm(request.POST)
		if form.is_valid():
			try:           
				form.create_person()
			except ValueError:
				messages.error(request, persons.errors.PERSON_CREATE_ERR_MSG)
				return render(request, 'persons/person-form.html', {'form': form, 'action': '/create/'})
			return HttpResponseRedirect('/')
	else:
		# In case it is get or anything else create an empty form
		form = PersonForm()

	return render(request, 'persons/person-form.html', {'form': form, 'action': '/create/'})

def edit(request, pk):

	# If it is a POST request process the form data
	if request.method == 'POST':
		form = PersonForm(request.POST)
		if form.is_valid():
			try:           
				form.edit_person(pk)
			except ValueError:
				messages.error(request, persons.errors.PERSON_UPDATE_ERR_MSG)
				return render(request, 'persons/person-form.html', {'form': form, 'action': "/edit/%s/" % (pk)})
			return HttpResponseRedirect('/')
	else:
		
		try:
			person = Person.objects.get(pk=pk)
		except Person.DoesNotExist:
			messages.error(request, persons.errors.PERSON_UPDATE_NOT_EXISt_ERR_MSG) 
			return HttpResponseRedirect('/')

		form = PersonForm({'first_name': person.first_name, 
                           'last_name': person.last_name, 
                           'date_of_birth': person.date_of_birth,
                           'zip_code': person.zip_code})                           
		
	return render(request, 'persons/person-form.html', {'form': form, 'action': "/edit/%s/" % (pk)})
