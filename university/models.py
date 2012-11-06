from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from countries.models import Country

class School(models.Model):
    university_name = models.CharField(_("Hospital"), max_length=255)
    codename        = models.CharField(_("Codename"), max_length=255)
    country         = models.ForeignKey(Country, verbose_name=_('Country'))

    def __unicode__(self):
        return self.university_name

    class Meta:
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitals')

admin.site.register(School)