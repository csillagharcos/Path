from django import forms
from django.forms.models import ModelForm
from report_forms.c8.models import c8, diagCodes
from django.utils.translation import ugettext_lazy as _
from report_forms.choices import DIAGNOSES_GROUP_CHOICES

class C8Form(ModelForm):
    icd                         = forms.ChoiceField(label=_('Diagnosis code: ICD-10'), choices=())
    drg                         = forms.ChoiceField(label=_('Diagnosis code: DRG'), choices=())
    date_of_birth               = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_admission           = forms.DateTimeField(label=_('Date of hospital admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge           = forms.DateTimeField(label=_('Date of hospital discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_surgical_procedure  = forms.DateTimeField(label=_('Date of first surgical procedure'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

    def __init__(self, language_code="hu", *args, **kwargs):
        super(C8Form, self).__init__(*args, **kwargs)
        #SETUP ICD-10 VERSION
        stroke = CAP = HF = IH = CABG = KA = TAOA = CHOL = VVSAL = ()
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=0):
            stroke += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=1):
            CAP += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=2):
            HF += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=3):
            IH += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=4):
            CABG += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=5):
            KA += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=6):
            TAOA += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=7):
            CHOL += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=0, group=8):
            VVSAL += ((str(DC.code), str(DC.code)),)
        icd = (
            ('', _('-- Select --')),
        )
        if stroke:
            icd += ((_("Stroke"),  (stroke)),)
        if CAP:
            icd += ((_("Community acquired pneumonia"),  (CAP)),)
        if HF:
            icd += ((_("Hip fracture"),  (HF)),)
        if IH:
            icd += ((_("Inguinal hernia"),  (IH)),)
        if CABG:
            icd += ((_("CABG"),  (CABG)),)
        if KA:
            icd += ((_("Knee arthroscopy"),  (KA)),)
        if TAOA:
            icd += ((_("Tonsillectomy and/or adenoidectomy"),  (TAOA)),)
        if CHOL:
            icd += ((_("Cholecystectomy"),  (CHOL)),)
        if VVSAL:
            icd += ((_("Varicose veins - stripping and ligation"),  (VVSAL)),)
        self.fields['icd'].choices=icd
        #SETUP DRG VERSION
        stroke = CAP = HF = IH = CABG = KA = TAOA = CHOL = VVSAL = ()
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=0):
            stroke += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=1):
            CAP += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=2):
            HF += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=3):
            IH += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=4):
            CABG += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=5):
            KA += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=6):
            TAOA += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=7):
            CHOL += ((str(DC.code), str(DC.code)),)
        for DC in diagCodes.objects.filter(language=language_code, group_category=1, group=8):
            VVSAL += ((str(DC.code), str(DC.code)),)
        drg = (
            ('', _('-- Select --')),
            )
        if stroke:
            drg += ((_("Stroke"),  (stroke)),)
        if CAP:
            drg += ((_("Community acquired pneumonia"),  (CAP)),)
        if HF:
            drg += ((_("Hip fracture"),  (HF)),)
        if IH:
            drg += ((_("Inguinal hernia"),  (IH)),)
        if CABG:
            drg += ((_("CABG"),  (CABG)),)
        if KA:
            drg += ((_("Knee arthroscopy"),  (KA)),)
        if TAOA:
            drg += ((_("Tonsillectomy and/or adenoidectomy"),  (TAOA)),)
        if CHOL:
            drg += ((_("Cholecystectomy"),  (CHOL)),)
        if VVSAL:
            drg += ((_("Varicose veins - stripping and ligation"),  (VVSAL)),)
        self.fields['drg'].choices=drg

    def clean(self):
        cleaned_data = super(C8Form, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        dg = cleaned_data.get("diagnosis_group")
        drg = cleaned_data.get("drg")
        icd = cleaned_data.get("icd")
        date_of_admission = cleaned_data.get("date_of_admission")
        date_of_discharge = cleaned_data.get("date_of_discharge")
        date_of_surgical_procedure = cleaned_data.get("date_of_surgical_procedure")

        if (dg == 3 or dg == 4 or dg == 5 or dg == 6 or dg == 7 or dg == 8) and not drg:
            self._errors["drg"] = self.error_class([_("Diagnosis group is not for DRG!")])
            del cleaned_data["drg"]

        if (dg == 0 or dg == 1 or dg == 2 or dg == 5) and not icd:
            self._errors["icd"] = self.error_class([_("Diagnosis group is not for ICD!")])
            del cleaned_data["icd"]

        if date_of_birth > date_of_admission:
            self._errors["date_of_birth"] = self.error_class([_("Can't be born after admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be born after admission!")])
            del cleaned_data["date_of_birth"]
            del cleaned_data["date_of_admission"]


        if date_of_surgical_procedure < date_of_admission:
            self._errors["date_of_surgical_procedure"] = self.error_class([_("Can't be operated before admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be operated before admission!")])
            del cleaned_data["date_of_surgical_procedure"]
            del cleaned_data["date_of_admission"]

        if date_of_surgical_procedure > date_of_discharge:
            self._errors["date_of_surgical_procedure"] = self.error_class([_("Can't be operated after discharge!")])
            self._errors["date_of_discharge"] = self.error_class([_("Can't be operated after discharge!")])
            del cleaned_data["date_of_surgical_procedure"]
            del cleaned_data["date_of_discharge"]

        return cleaned_data

    class Meta:
        model = c8
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()

class TrendForm(forms.Form):
    date1a = forms.DateTimeField(label=_('First date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date1b = forms.DateTimeField(label=_('First date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date2a = forms.DateTimeField(label=_('Second date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date2b = forms.DateTimeField(label=_('Second date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date3a = forms.DateTimeField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date3b = forms.DateTimeField(required=False,label=_('Third date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

class AnonymStatForm(forms.Form):
    endDate = forms.DateTimeField(label=_('Date'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))