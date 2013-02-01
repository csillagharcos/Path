from csvImporter.fields import IntegerField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel
from report_forms.choices import ADMISSION_STATUS_CHOICES, TYPE_OF_ADMISSION, YES_NO_CHOICES, DISCHARGE_STATUS_CHOICES, DIAGNOSES_GROUP_CHOICES, ICD10_CHOICES, DRG_CHOICES
from settings import LANGUAGES

DGC_CHOICES = (
    (0, _("ICD-10")),
    (1, _("DRG")),
)

class diagCodes(models.Model):
    code = models.CharField(_('Code fields'), max_length=20)
    group = models.IntegerField(_('Diagnosis group'), choices=DIAGNOSES_GROUP_CHOICES, default=0)
    group_category = models.IntegerField(_('Diagnosis group category'), choices=DGC_CHOICES, default=0)
    language = models.CharField(_('Language'), max_length=5, choices=LANGUAGES)

    class Meta:
        verbose_name = _('Diagnosis Code')
        verbose_name_plural = _('Diagnosis Codes')

    def __unicode__(self):
        return self.code

class c8(models.Model):
    patient_id                      = models.IntegerField(_('Patients ID'), unique=True)
    case_id                         = models.IntegerField(_('Case ID'))
    date_of_birth                   = models.DateField(_('Date of birth'))
    date_of_admission               = models.DateField(_('Date of hospital admission'))
    patient_admission_status        = models.IntegerField(_('Patient admission status'), max_length=1, choices=ADMISSION_STATUS_CHOICES, default=0 )
    type_of_admission               = models.IntegerField(_('Type of admission'), max_length=1, choices=TYPE_OF_ADMISSION, default=0 )
    was_surgical_procedure          = models.IntegerField(_('Was surgical procedure?'), max_length=1, choices=YES_NO_CHOICES, default=0 )
    date_of_surgical_procedure      = models.DateField(_('Date of first surgical procedure'), null=True, blank=True)
    date_of_discharge               = models.DateField(_('Date of hospital discharge'))
    patient_discharge_status        = models.IntegerField(_('Patient discharge status'), max_length=1, choices=DISCHARGE_STATUS_CHOICES, default=0 )
    diagnosis_group                 = models.IntegerField(_('Diagnosis group'), max_length=1, choices=DIAGNOSES_GROUP_CHOICES, default=0 )
    icd                             = models.CharField(_('Diagnosis code: ICD-10'), max_length=5, choices=ICD10_CHOICES, default='', null=True, blank=True )
    drg                             = models.CharField(_('Diagnosis code: DRG'), max_length=5, choices=DRG_CHOICES, default='', null=True, blank=True )
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.patient_id)

    class Meta:
        verbose_name = _('Length of Stay')
        verbose_name_plural = _('Length of Stays')

class c8CSV(CsvModel):
    patient_id                      = CharField()
    case_id                         = CharField()
    date_of_birth                   = CharField()
    date_of_admission               = CharField()
    patient_admission_status        = CharField()
    type_of_admission               = CharField()
    was_surgical_procedure          = CharField()
    date_of_surgical_procedure      = CharField()
    date_of_discharge               = CharField()
    patient_discharge_status        = CharField()
    diagnosis_group                 = CharField()
    icd                             = CharField()
    drg                             = CharField()
    class Meta:
        delimiter = ";"
