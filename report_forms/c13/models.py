# -*- coding: utf-8 -*-
from datetime import datetime
from csvImporter.fields import IntegerField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel
from report_forms.choices import JOB_CHOICES

class joblist(models.Model):
    job_english                     = models.CharField(_('Job name in english'), max_length=255, default="")
    job_hungarian                   = models.CharField(_('Job name in hungarian'), max_length=255, default="")

    def __unicode__(self):
        return self.job_english + " (" + self.job_hungarian + ")"

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

class c13(models.Model):
    job                             = models.ForeignKey(joblist, verbose_name=_('Job'))
    year                            = models.IntegerField(_('Observed year'), default=2012)
    needlestick_injuries            = models.IntegerField(_('Number of needle stick injuries in the observed year'), default=0)
    staff_beginning                 = models.IntegerField(_('Total number of hospital staff at the beginning of the year (1st January)'), default=0)
    staff_end                       = models.IntegerField(_('Total number of hospital staff at the end of the year (31st December)'), default=0)
    working_hours_beginning         = models.IntegerField(_('Total number of contracted working hours for the data at the beginning of the year/day (employee+ entrepreneur)'), default=0)
    working_hours_end               = models.IntegerField(_('Total number of contracted working hours for the data at the end of the year /day(employee+ entrepreneur)'), default=0)
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return self.job.job_english +" ("+ self.job.job_hungarian +") - " + str(self.year)

    class Meta:
        verbose_name = _('Needle stick injury')
        verbose_name_plural = _('Needle stick injuries')

admin.site.register(joblist)
