# -*- coding: utf-8 -*-
from csvImporter.fields import CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel
from report_forms.choices import PRINCIPAL_DIAG_CODE_S, YES_NO_CHOICES, PENICILIN_ALLERGY_CHOICES, ROUTE_OF_ADMIN_CHOICES_FOUR
from settings import LANGUAGES

class Medicine(models.Model):
    name                   = models.CharField(_('Name'),max_length=255)
    dose                   = models.FloatField(_('Dosage'))
    doseUnder              = models.FloatField(_('Dosage under 60kg'))
    doseAbove              = models.FloatField(_('Dosage above 100kg'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Medicine')
        verbose_name_plural = _('Medicines')

class diagCode(models.Model):
    code        = models.CharField(_('Code'), max_length=10)
    language    = models.CharField(_('Language'), max_length=10, choices=LANGUAGES)

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = _('Diagnosis Code')
        verbose_name_plural = _('Diagnosis Codes')

class c23(models.Model):
    case_id                         = models.IntegerField(_('Case ID'), unique=True)
    hospital_registration_number    = models.CharField(_('Hospital registration number'), max_length=50)
    date_of_birth                   = models.DateField(_('Date of birth'))
    weight_of_patient               = models.IntegerField(_('Weight of patient (kg)'))
    principal_diagnoses_code        = models.CharField(_('Principal diagnosis code (ICD-10)'), max_length=5, choices=PRINCIPAL_DIAG_CODE_S, default='')
    principal_procedure_code        = models.CharField(_('Principal procedure code'), max_length=10)
    procedure_planned               = models.IntegerField(_('Is the surgical procedure planned?'), max_length=1, choices=YES_NO_CHOICES, default=1)
    patient_allergy                 = models.IntegerField(_('Is patient allergic to any antibiotics suggested in the protocol?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    generic_name_of_drug            = models.CharField(_('Generic name of antibiotic drug'), max_length=255, null=True, blank=True)
    penicilin_allergy               = models.IntegerField(_('In case of allergy to penicillin, scale of severity?'), choices=PENICILIN_ALLERGY_CHOICES, default=1)
    preoperative_infection          = models.IntegerField(_('Has patient preoperative infection?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    type_of_infection               = models.CharField(_('Type of infection'), max_length=255, null=True, blank=True)
    surgical_incision               = models.DateTimeField(_('Date and time of surgical incision'))
    antibiotic_given                = models.IntegerField(_('Prophylactic antibiotic given?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    name_of_first_dose              = models.CharField(_('Generic name first used antibiotic drug'), max_length=255, null=True, blank=True)
    first_dose                      = models.FloatField(_('First dose of first antibiotic drug'), max_length=10, null=True, blank=True)
    name_of_second_dose             = models.CharField(_('Generic name second used antibiotic drug'), max_length=255, null=True, blank=True)
    second_dose                     = models.FloatField(_('First dose of second antibiotic drug'), max_length=10, null=True, blank=True)
    route_of_admin                  = models.IntegerField(_('Route of administration of first dose'), max_length=1, choices=ROUTE_OF_ADMIN_CHOICES_FOUR, null=True, blank=True, default=1)
    date_of_first_dose              = models.DateTimeField(_('Date and time of first dose'), null=True, blank=True)
    total_dose_in_24h               = models.FloatField(_('Total doses in 24 hours'), max_length=10, null=True, blank=True)
    date_of_last_dose               = models.DateTimeField(_('Date and time of last dose'), null=True, blank=True)
    date_of_wound_close             = models.DateTimeField(_('Date and time of surgical wound closure'))
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.case_id)

    class Meta:
        verbose_name = _('Planned surgery for hip replacement')
        verbose_name_plural = _('Planned surgery for hip replacement')

class c23CSV(CsvModel):
    case_id                         = CharField()
    hospital_registration_number    = CharField()
    date_of_birth                   = CharField()
    weight_of_patient               = CharField()
    principal_diagnoses_code        = CharField()
    principal_procedure_code        = CharField()
    procedure_planned               = CharField()
    patient_allergy                 = CharField()
    generic_name_of_drug            = CharField()
    penicilin_allergy               = CharField()
    preoperative_infection          = CharField()
    type_of_infection               = CharField()
    surgical_incision               = CharField()
    surgical_incision_time          = CharField()
    antibiotic_given                = CharField()
    name_of_first_dose              = CharField()
    name_of_second_dose             = CharField()
    first_dose                      = CharField()
    second_dose                     = CharField()
    route_of_admin                  = CharField()
    date_of_first_dose              = CharField()
    time_of_first_dose              = CharField()
    total_dose_in_24h               = CharField()
    date_of_last_dose               = CharField()
    time_of_last_dose               = CharField()
    date_of_wound_close             = CharField()
    time_of_wound_close             = CharField()
    comments                        = CharField()

    class Meta:
        delimiter = ";"

admin.site.register(Medicine)