# -*- coding: utf-8 -*-
from csvImporter.fields import IntegerField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel
from report_forms.choices import AMI_CHOICES, TYPE_OF_UNIT, YES_NO_CHOICES, TYPE_OF_DISCHARGE

class c20(models.Model):
    case_id                         = models.IntegerField(_('Case ID'), unique=True)
    hospital_registration_number    = models.CharField(_('Hospital registration number'), max_length=50)
    date_of_birth                   = models.DateField(_('Date of birth'))
    diagnosis_code                  = models.CharField(_('Principal diagnosis code (ICD-10)'), max_length=3, choices=AMI_CHOICES, default="")
    type_of_unit                    = models.IntegerField(_('Type of unit'), max_length=1, choices=TYPE_OF_UNIT, default=1 )
    patient_allergic_aspirin        = models.IntegerField(_('Patient allergic to aspirin?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    aspirin_intolerance             = models.IntegerField(_('Is there a known contraindication or intolerance of aspirin?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    type_of_discharge               = models.IntegerField(_('Type of discharge'), max_length=1, choices=TYPE_OF_DISCHARGE, default=1)
    type_of_discharge_empty         = models.CharField(_('If other'), max_length=255, null=True, blank=True)
    aspirin_refusal                 = models.IntegerField(_('Is there a known objection/refusal to take aspirin-containing medication?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    aspirin_at_discharge            = models.IntegerField(_('Was patient prescribed at discharge to take aspirin?'), max_length=1, choices=YES_NO_CHOICES, default=1)
    non_aspirin_platelet            = models.IntegerField(_('Was patient prescribed to take other (non-aspirin-containing) platelet aggregation inhibitor therapy?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    date_of_discharge               = models.DateField(_('Date of discharge'))
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.case_id)

    class Meta:
        verbose_name = _('AMI patient prescribed aspirin at discharge')
        verbose_name_plural = _('AMI patients prescribed aspirin at discharge')

class c20CSV(CsvModel):
    case_id                         = CharField()
    hospital_registration_number    = CharField()
    date_of_birth                   = CharField()
    diagnosis_code                  = CharField()
    type_of_unit                    = CharField()
    patient_allergic_aspirin        = CharField()
    aspirin_intolerance             = CharField()
    type_of_discharge               = CharField()
    type_of_discharge_empty         = CharField()
    aspirin_refusal                 = CharField()
    aspirin_at_discharge            = CharField()
    non_aspirin_platelet            = CharField()
    date_of_discharge               = CharField()


    class Meta:
        delimiter = ";"