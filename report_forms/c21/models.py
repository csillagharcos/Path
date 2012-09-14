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

PRINCIPAL_DIAG_CODE = (
    ('', _('-- Select --')),
    ('C18', 'C18'),
    ('C19', 'C19'),
    ('C20', 'C20'),
    ('C20.0', 'C21.0'),
    ('C20.1', 'C21.1'),
    ('C20.2', 'C21.2'),
    ('C20.8', 'C21.8'),
)

PENICILIN_ALLERGY_CHOICES = (
    ('1', _('Immediate')),
    ('2', _('Other')),
    ('3', _('No Information'))
)

ROUTE_OF_ADMIN_CHOICES = (
    (1, _('IV')),
    (2, _('IM')),
    (3, _('SC')),
    (4, _('Other')),
    (5, _('PO')),
)

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

class c21(models.Model):
    case_id                         = models.IntegerField(_('Case ID'))
    hospital_registration_number    = models.CharField(_('Hospital registration number'), max_length=50)
    date_of_birth                   = models.DateField(_('Date of birth'))
    weight_of_patient               = models.IntegerField(_('Weight of patient'))
    principal_diagnoses_code        = models.CharField(_('Principal diagnosis code (ICD-10 or DRG)'), max_length=5, choices=PRINCIPAL_DIAG_CODE, default='')
    principal_procedure_code        = models.CharField(_('Principal procedure code'), max_length=10)
    procedure_planned               = models.IntegerField(_('Is the surgical procedure planned?'), max_length=1, choices=YES_NO_CHOICES, default=1)
    patient_allergy                 = models.IntegerField(_('Is patient allergic to any antibiotics suggested in the protocol?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    generic_name_of_drug            = models.CharField(_('Generic name of antibiotic drug'), max_length=255, null=True, blank=True)
    penicilin_allergy               = models.IntegerField(_('In case of allergy to penicillin, scale of severity?'), choices=PENICILIN_ALLERGY_CHOICES, default=1)
    preoperative_infection          = models.IntegerField(_('Has patient preoperative infection?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    surgical_incision               = models.DateTimeField(_('Date of surgical incision'))
    antibiotic_given                = models.IntegerField(_('Prophylactic antibiotic given?'), max_length=1, choices=YES_NO_CHOICES, default=0)
    name_of_first_dose              = models.ForeignKey(Medicine, verbose_name=_('Name of first dose'), related_name="First Dose", null=True, blank=True)
    first_dose                      = models.FloatField(_('First dose'), max_length=10, null=True, blank=True)
    name_of_second_dose             = models.ForeignKey(Medicine, verbose_name=_('Name of second dose'), related_name="Second Dose", null=True, blank=True)
    second_dose                     = models.FloatField(_('Second dose'), max_length=10, null=True, blank=True)
    name_of_other_dose              = models.CharField(_("Name of other dose"), max_length=255, null=True, blank=True)
    other_dose                      = models.FloatField(_('Other dose'), max_length=10, null=True, blank=True)
    route_of_admin                  = models.IntegerField(_('Route of administration of first dose'), max_length=1, choices=ROUTE_OF_ADMIN_CHOICES, null=True, blank=True, default=1)
    date_of_first_dose              = models.DateTimeField(_('Date of first dose'), null=True, blank=True)
    total_dose_in_24h               = models.FloatField(_('Total doses in 24 hours'), max_length=10, null=True, blank=True)
    date_of_last_dose               = models.DateTimeField(_('Date of last dose'), null=True, blank=True)
    date_of_wound_close             = models.DateTimeField(_('Date of surgical wound closure'))
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.patient_id)

    class Meta:
        verbose_name = _('Planned surgery for colorectal cancer')
        verbose_name_plural = _('Planned surgery for colorectal cancers')

class c21CSV(CsvModel):
    case_id                         = IntegerField()
    hospital_registration_number    = IntegerField()
    date_of_birth                   = CharField()
    weight_of_patient               = IntegerField()
    principal_diagnoses_code        = CharField()
    principal_procedure_code        = CharField()
    procedure_planned               = IntegerField()
    patient_allergy                 = IntegerField()
    generic_name_of_drug            = CharField()
    penicilin_allergy               = IntegerField()
    preoperative_infection          = IntegerField()
    surgical_incision               = CharField()
    surgical_incision_time          = CharField()
    antibiotic_given                = IntegerField()
    name_of_first_dose              = CharField()
    first_dose                      = FloatField()
    name_of_second_dose             = CharField()
    second_dose                     = FloatField()
    name_of_other_dose              = CharField()
    other_dose                      = FloatField()
    route_of_admin                  = IntegerField()
    date_of_first_dose              = CharField()
    time_of_first_dose              = CharField()
    total_dose_in_24h               = FloatField
    date_of_last_dose               = CharField()
    time_of_last_dose               = CharField()
    date_of_wound_close             = CharField()
    time_of_wound_close             = CharField()

    class Meta:
        delimiter = ";"
        has_header = True

admin.site.register(c21)
admin.site.register(Medicine)