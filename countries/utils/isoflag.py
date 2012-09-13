#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def iso_flag(iso, flag_path=u''):
	if not settings.MEDIA_URL:
		return u''
	deafult = u'-'
	if not iso:
		iso = deafult
	else:
		iso = iso.lower().strip()
	try:
		flag_name = flag_path % iso
	except (ValueError, TypeError):
		flag_path = getattr(settings, 'COUNTRIES_FLAG_PATH', u'flags/%s.gif')
		try:
			flag_name = flag_path % iso
		except (ValueError, TypeError):
			return u''
	return u''.join((settings.MEDIA_URL, flag_name))