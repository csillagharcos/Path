# -*- coding: utf-8 -*-
from csvImporter.fields import CharField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel
from report_forms.choices import TYPE_OF_OR, HYGIENE_CATEGORY, YES_NO_CHOICES

class c9_patient(models.Model):
    operating_unit                  = models.CharField(_('Identifier of operating unit or operating rooms'), max_length=255)
    date                            = models.DateField(_('Date'))
    case_number                     = models.IntegerField(_('Case number'))
    patient_identifier              = models.CharField(_('Patient identifier'), max_length=255)
    patient_arrive_time             = models.TimeField(_('Time patient arrives to OR'))
    patient_leave_time              = models.TimeField(_('Time patient leaves OR'))
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.case_number)

    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')

class c9_operation(models.Model):
    central_operating_unit          = models.CharField(_('Identifier of central operating unit'), max_length=255)
    operating_unit                  = models.CharField(_('Identifier of OR'), max_length=255)
    type_of_or                      = models.IntegerField(_('Type of OR'), max_length=1, default=1, choices=TYPE_OF_OR)
    weekday_open_time               = models.TimeField(_('Weekday normal time of opening'))
    weekday_close_time              = models.TimeField(_('Weekday normal time of closing'))
    weekday_staffed_days            = models.TimeField(_('Weekday number of staffed days in the observed period'))
    saturday_open_time              = models.TimeField(_('Saturday normal time of opening'))
    saturday_close_time             = models.TimeField(_('Saturday normal time of closing'))
    saturday_staffed_days           = models.TimeField(_('Saturday number of staffed days in the observed period'))
    sunday_open_time                = models.TimeField(_('Sunday/Holiday normal time of opening'))
    sunday_close_time               = models.TimeField(_('Sunday/Holiday normal time of closing'))
    sunday_staffed_days             = models.TimeField(_('Sunday/Holiday number of staffed days in the observed period'))
    hygiene_category                = models.IntegerField(_('Hygiene category of OR'), max_length=1, default=1, choices=HYGIENE_CATEGORY)
    professional_field              = models.CharField(_('Professional field'), max_length=255)
    preparatory_room                = models.IntegerField(_('Preparatory room'), max_length=1, choices=YES_NO_CHOICES, default=0)
    postoperative_room              = models.IntegerField(_('Post-operative observatory room'), max_length=1, choices=YES_NO_CHOICES, default=0)
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.case_number)

    class Meta:
        verbose_name = _('Operation room')
        verbose_name_plural = _('Operation rooms')


class c9_patientCSV(CsvModel):
    operating_unit                  = CharField()
    operating_room                  = CharField()
    date                            = CharField()
    case_number                     = CharField()
    patient_identifier              = CharField()
    patient_arrive_time             = CharField()
    patient_leave_time              = CharField()

    class Meta:
        delimiter = ";"

class c9_operationCSV(CsvModel):
    central_operating_unit          = CharField()
    operating_unit                  = CharField()
    type_of_or                      = CharField()
    weekday_open_time               = CharField()
    weekday_close_time              = CharField()
    weekday_staffed_days            = CharField()
    saturday_open_time              = CharField()
    saturday_close_time             = CharField()
    saturday_staffed_days           = CharField()
    sunday_open_time                = CharField()
    sunday_close_time               = CharField()
    sunday_staffed_days             = CharField()
    hygiene_category                = CharField()
    professional_field              = CharField()
    preparatory_room                = CharField()
    postoperative_room              = CharField()

    class Meta:
        delimiter = ";"
