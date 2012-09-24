from django import forms
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    username        = forms.CharField(label=_(u'Username'), widget=forms.TextInput(attrs={'placeholder': _('Username')}))
    password        = forms.CharField(label=_(u'Password'), widget=forms.PasswordInput(render_value=False,attrs={'placeholder': _('Password')}))