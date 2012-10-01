# -*- coding: utf-8 -*-
from csvImporter.fields import IntegerField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel
from report_forms.choices import DISCHARGE_STATUS_CHOICES, STROKE_CHOICES, ADMISSION_STATUS_CHOICES

class c32(models.Model):
    patient_id                      = models.IntegerField(_('Patients ID'), unique=True)
    case_id                         = models.IntegerField(_('Case ID'))
    date_of_birth                   = models.DateField(_('Date of birth'))
    date_of_admission               = models.DateField(_('Date of hospital admission'))
    patient_admission_status        = models.IntegerField(_('Patient admission status'), max_length=1, choices=ADMISSION_STATUS_CHOICES, default=0 )
    date_of_discharge               = models.DateField(_('Date of hospital discharge'))
    patient_discharge_status        = models.IntegerField(_('Patient discharge status'), max_length=1, choices=DISCHARGE_STATUS_CHOICES, default=0 )
    icd                             = models.CharField(_('ICD-10 at that departmental admission'), max_length=3, choices=STROKE_CHOICES, default="" )
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.patient_id)

    class Meta:
        verbose_name = _('30-day in-hospital mortality of patient admitted with Stroke')
        verbose_name_plural = _('30-day in-hospital mortality of patients admitted with Stroke')

class c32CSV(CsvModel):
    patient_id                      = IntegerField()
    case_id                         = IntegerField()
    date_of_birth                   = CharField()
    date_of_admission               = CharField()
    patient_admission_status        = CharField()
    date_of_discharge               = CharField()
    patient_discharge_status        = CharField()
    icd                             = CharField()

    class Meta:
        delimiter = ";"
