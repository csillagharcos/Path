#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
	iso = models.CharField(max_length=2, primary_key=True)
	name = models.CharField(max_length=128)
	printable_name = models.CharField(max_length=128)
	iso3 = models.CharField(max_length=3, null=True)
	numcode = models.PositiveSmallIntegerField(null=True)
	
	class Meta:
		db_table = 'country'
		verbose_name = _('Country')
		verbose_name_plural = _('Countries')
		ordering = ('name',)
		
	class Admin:
		list_display = ('printable_name', 'iso',)
		
	def __unicode__(self):
		return self.printable_name