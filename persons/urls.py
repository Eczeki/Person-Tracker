from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PersonListView.as_view(), name='person-list'),
    url(r'create', views.create, name='create'),
    url(r'edit/(?P<pk>[0-9]+)', views.edit, name='edit'),
    url(r'delete/(?P<pk>[0-9]+)', views.delete, name='delete'),
]