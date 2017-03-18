from django.test import TestCase, Client

from .models import Person
import persons.errors

class PersonListViewTests(TestCase):

	def setUp(self):
		self.client = Client()

		# Create one person to start
		self.person = Person.objects.create(first_name='Alberto',
											last_name='Carrillo',
											date_of_birth='2011-02-19', 
							   				zip_code='33186')

	def test_index_view(self):    	
		response = self.client.get('/')        
		self.assertEqual(response.status_code, 200)

	def test_person_delete(self):
		test_person = Person.objects.create(first_name='Alberto',
											last_name='Carrillo',
											date_of_birth='2011-02-19', 
							   				zip_code='33186')

		response = self.client.get("/delete/%s" % (test_person.pk), follow=True)
		self.assertRedirects(response, '/')

	def test_person_delete_non_existent(self):
		response = self.client.get('/delete/1000', follow=True)
		self.assertRedirects(response, '/')
		self.assertContains(response, persons.errors.PERSON_DOES_NOT_EXIST_ERR_MSG)		

	def test_edit_not_existent(self):
		response = self.client.get("/edit/1000", follow=True)
		self.assertRedirects(response, '/')
		self.assertContains(response, persons.errors.PERSON_UPDATE_NOT_EXISt_ERR_MSG)

class PersonFormViewTests(TestCase):

	def setUp(self):
		self.client = Client()

		# Create one person to start
		self.person = Person.objects.create(first_name='Alberto',
											last_name='Carrillo',
											date_of_birth='1990-02-19', 
							   				zip_code='33186')

	def test_create_view_available(self):
		response = self.client.get('/create')
		self.assertEqual(response.status_code, 200)

	def test_edit_view_available(self):
		response = self.client.get("/edit/%s" % (self.person.pk))
		self.assertEqual(response.status_code, 200)

	def test_create_person(self):
		first_name = 'John'
		last_name  = 'Smith'
		date_of_birth = '2011-02-19'
		zip_code = '33186'

		self.client.post('/create', {'first_name': first_name,
									'last_name': last_name,
									'date_of_birth': date_of_birth,
									'zip_code': zip_code})

		person = Person.objects.get(first_name=first_name, 
									last_name=last_name, 
									date_of_birth=date_of_birth, 
									zip_code=zip_code)

		self.assertEqual(person.first_name, first_name)
		self.assertEqual(person.last_name, last_name)
		self.assertEqual(str(person.date_of_birth), date_of_birth)
		self.assertEqual(person.zip_code, zip_code)

	def test_edit_person(self):
		first_name = 'Ben'
		last_name  = 'Seager'
		date_of_birth = '2011-02-19'
		zip_code = '33176'

		self.client.post("/edit/%s" % (self.person.pk), {'first_name': first_name,
		    											'last_name': last_name,
		    											'date_of_birth': date_of_birth,
		    											'zip_code': zip_code})

		person = Person.objects.get(first_name=first_name, 
									last_name=last_name, 
									date_of_birth=date_of_birth, 
									zip_code=zip_code)

		self.assertEqual(person.first_name, first_name)
		self.assertEqual(person.last_name, last_name)
		self.assertEqual(str(person.date_of_birth), date_of_birth)
		self.assertEqual(person.zip_code, zip_code)



