# -*- coding: utf-8 -*-
from csvImporter.fields import IntegerField, FloatField, CharField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from csvImporter.model import CsvModel

C_SECTION_CHOICES = (
    (0, _('Planned')),
    (1, _('Acute')),
)

MOTHER_ILLNESS_CHOICES = (
    (0, _('No')),
    (1, _('If yes, specify here')),
)

DRG_CODES_CHOICES = (
    ('', '-- Select --'),
    ('671', '671'),
    ('671A', '671A'),
    ('671B', '671B'),
    ('672', '672'),
    ('673', '673'),
    ('674', '674'),
)

class c1OtherDiagnose(models.Model):
    name                            = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Other Diagnose')
        verbose_name_plural = _('Other Diagnoses')

class c1(models.Model):
    patient_id                      = models.IntegerField(_('Patients ID'), unique=True)
    case_id                         = models.IntegerField(_('Case ID'))
    date_of_birth                   = models.DateField(_('Date of Birth'))
    date_of_delivery                = models.DateTimeField(_('Date of Delivery'))
    number_of_prev_deliveries       = models.IntegerField(_('Number of previous deliveries'))
    number_of_prev_deliveries_by_c  = models.IntegerField(_('Number of earlier deliveries by c-section'), default=0)
    the_c_section                   = models.IntegerField(_('The c-section'), max_length=1, choices=C_SECTION_CHOICES, default=0)
    weight_of_the_newborn           = models.FloatField(_('Weight of newborn'))
    mother_illness                  = models.IntegerField(_('Mother illnes or risk'), max_length=1, choices=MOTHER_ILLNESS_CHOICES, default=0)
    specify_mother_illness          = models.CharField(_('Specify'), max_length=255, null=True, blank=True)
    drg_code                        = models.CharField(_('DRG Code'), max_length=4,choices=DRG_CODES_CHOICES, default='')
    other_diagnoses                 = models.ManyToManyField(c1OtherDiagnose, verbose_name=_('Other Diagnoses'), null=True, blank=True)
    added_on                        = models.DateTimeField(auto_now_add=True)
    added_by                        = models.ForeignKey(User, verbose_name=_('User'))

    def __unicode__(self):
        return str(self.patient_id)

    class Meta:
        verbose_name = _('C-Section Rate')
        verbose_name_plural = _('C-Section Rates')

class c1CSV(CsvModel):
    patient_id                      = IntegerField()        #A
    case_id                         = IntegerField()        #B
    date_of_birth                   = CharField()           #C
    date_of_delivery                = CharField()           #D
    time_of_delivery                = CharField()           #E
    number_of_prev_deliveries       = IntegerField()        #F
    number_of_prev_deliveries_by_c  = IntegerField()        #G
    the_c_section                   = IntegerField()        #H
    weight_of_the_newborn           = FloatField()          #I
    mother_illness                  = IntegerField()        #J
    specify_mother_illness          = CharField()           #K
    drg_code                        = CharField()           #L
    other_diagnoses                 = CharField()           #M

    class Meta:
        delimiter = ";"

admin.site.register(c1)
#admin.site.register(c1OtherDiagnose)
