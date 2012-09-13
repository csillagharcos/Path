#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def iso_flag(iso, flag_path=u''):
	from countries.utils.isoflag import iso_flag
	return iso_flag(iso, flag_path)
iso_flag = stringfilter(iso_flag)

# Syntax: register.filter(name of filter, callback)
register.filter('iso_flag', iso_flag)
