# -*- coding: utf-8 -*-
from csvImporter.fields import IntegerField, FloatField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel

YES_NO_CHOICES = (
    (0, _('No')),
    (1, _('Yes')),
)

class c21(models.Model):
    case_id                         = models.IntegerField(_('Case ID'))
    hospital_registration_number    = models.IntegerField(_('Hospital registration number'))
    date_of_birth                   = models.DateField(_('Date of birth'))
    weight_of_patient               = models.IntegerField(_('Weight of patient'))
    principal_diagnoses_code        = models.CharField(_('Principal diagnosis code (ICD-10 or DRG)'), max_length=10)
    principal_procedure_code        = models.CharField(_('Principal procedure code'), max_length=10)
    procedure_planned               = models.IntegerField(_('Is the surgical procedure planned?'), max_length=1, choices=YES_NO_CHOICES, default=1)
    patient_allergy                 = models.IntegerField(_('Is patient allergic to any antibiotics suggested in the protocol?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    generic_name_of_drug            = models.CharField(_('Generic name of antibiotic drug'), max_length=255, null=True, blank=True)
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.patient_id)

    class Meta:
        verbose_name = _('C-Section Rate')
        verbose_name_plural = _('C-Section Rates')

class c21CSV(CsvModel):

    class Meta:
        delimiter = ";"

admin.site.register(c21)
