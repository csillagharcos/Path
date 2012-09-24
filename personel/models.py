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
        return self.workplace.university_name + " worker: " + self.user.get_full_name()

admin.site.register(Personel)