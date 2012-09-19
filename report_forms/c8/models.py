# -*- coding: utf-8 -*-
from csvImporter.fields import IntegerField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel

YES_NO_CHOICES = (
    (0, _('No')),
    (1, _('Yes')),
)

ADMISSION_STATUS_CHOICES = (
    (0, _('From home/nursing home/community care')),
    (1, _('Transferred from another hospital')),
)

TYPE_OF_ADMISSION = (
    (0, _('Planned')),
    (1, _('Urgent surgical')),
    (2, _('Emergency care')),
)

DIAGNOSES_GROUP_CHOICES = (
    (0, _('Stroke')),
    (1, _('Hospital acquired pneumonia')),
    (2, _('Hip fracture')),
    (3, _('CABG')),
    (4, _('Knee arthroscopy')),
    (5, _('Inguinal hernia')),
    (6, _('Tonsillectomy and/or adenoidectomy')),
    (7, _('Cholecystectomy')),
    (8, _('Varicose veins - stripping and ligation')),
)

ICD10_CHOICES = (
    ('', _('-- Select --')),
    (_('Stroke'), (
        ('I61', 'I61'),
        ('I62', 'I62'),
        ('I63', 'I63'),
        ('I64', 'I64'),
    )),
    (_('Hospital acquired pneumonia'), (
        ('J13', 'J13'),
        ('J14', 'J14'),
        ('J15', 'J15'),
        ('J18', 'J18'),
        ('A481', 'A481'),
    )),
    (_('Hip fracture'), (
        ('S720', 'S720'),
        ('S721', 'S721'),
        ('S722', 'S722'),
    )),
    (_('Inguinal hernia'), (
        ('K40', 'K40'),
    )),
)

DRG_CHOICES = (
    ('', _('-- Select --')),
    (_('CABG'), (
        ('177A', '177A'),
        ('177B', '177B'),
        ('177C', '177C'),
        ('177D', '177D'),
        ('190A', '190A'),
        ('192A', '192A'),
        ('192B', '192B'),
        )),
    (_('Knee arthroscopy'), (
        ('398A', '398A'),
        ('398B', '398B'),
        )),
    (_('Inguinal hernia'), (
        ('281B', '281B'),
        ('282A', '282A'),
        ('282B', '282B'),
        )),
    (_('Tonsillectomy and/or adenoidectomy'), (
        ('097A', '097A'),
        )),
    (_('Cholecystectomy'), (
        ('344', '344'),
        ('345', '345'),
        ('369Z', '369Z'),
        )),
    (_('Varicose veins - stripping and ligation'), (
        ('2030', '2030'),
        )),
)

DISCHARGE_STATUS_CHOICES = (
    (0, _('Home/nursing home/community care')),
    (1, _('Transferred into another hospital')),
    (2, _('Death')),
    (3, _('Discharge at own request')),
)


class c8(models.Model):
    patient_id                      = models.IntegerField(_('Patients ID'), unique=True)
    case_id                         = models.IntegerField(_('Case ID'))
    date_of_birth                   = models.DateField(_('Date of birth'))
    date_of_admission               = models.DateField(_('Date of hospital admission'))
    patient_admission_status        = models.IntegerField(_('Patient admission status'), max_length=1, choices=ADMISSION_STATUS_CHOICES, default=0 )
    type_of_admission               = models.IntegerField(_('Type of admission'), max_length=1, choices=TYPE_OF_ADMISSION, default=0 )
    was_surgical_procedure          = models.IntegerField(_('Was surgical procedure?'), max_length=1, choices=YES_NO_CHOICES, default=0 )
    date_of_surgical_procedure      = models.DateField(_('Date of first surgical procedure'))
    date_of_discharge               = models.DateField(_('Date of hospital discharge'))
    patient_discharge_status        = models.IntegerField(_('Patient discharge status'), max_length=1, choices=DISCHARGE_STATUS_CHOICES, default=0 )
    diagnosis_group                 = models.IntegerField(_('Diagnosis group'), max_length=1, choices=DIAGNOSES_GROUP_CHOICES, default=0 )
    icd                             = models.CharField(_('Diagnosis code: ICD-10'), max_length=5, choices=ICD10_CHOICES, default='' )
    drg                             = models.CharField(_('Diagnosis code: DRG'), max_length=5, choices=DRG_CHOICES, default='' )
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.patient_id)

    class Meta:
        verbose_name = _('Length of Stay')
        verbose_name_plural = _('Length of Stays')

class c8CSV(CsvModel):
    patient_id                      = IntegerField()
    case_id                         = IntegerField()
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

admin.site.register(c8)
