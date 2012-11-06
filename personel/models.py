from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from university.models import School
from countries.models import Country

class Personel(models.Model):
    user           = models.OneToOneField(User, verbose_name=_('User'))
    workplace      = models.ForeignKey(School, verbose_name=_('University'))
    country        = models.ForeignKey(Country, verbose_name=_('Country'))

    def __unicode__(self):
        if self.user.get_full_name():
            name = self.user.get_full_name()
        else:
            name = self.user.username
        return name + " ("+self.workplace.university_name + ")"

admin.site.register(Personel)