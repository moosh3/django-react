from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Book(models.Model):
	
	title = models.CharField(max_length=50, blank=True)	
	description = models.CharField(max_length=1024, blank=True)


class Author(models.Model):

	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
