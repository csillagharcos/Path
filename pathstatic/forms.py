from django import forms

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'Username'), widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False,attrs={'placeholder': 'Password'}))