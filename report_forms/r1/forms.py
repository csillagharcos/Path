from django import forms
from django.forms.models import ModelForm
from report_forms.r1.models import r1
from django.utils.translation import ugettext_lazy as _

class r1Form(ModelForm):
    date_of_birth                       = forms.DateTimeField(label=_('Date of birth'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_admission                   = forms.DateTimeField(label=_('Date of admission'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FIM_date_of_assess                  = forms.DateTimeField(required=False, label=_('FIM date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    BI_date_of_assess                   = forms.DateTimeField(required=False, label=_('Barthel index date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SMWT_date_of_assess                 = forms.DateTimeField(required=False, label=_('6 minutes walk test date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SF_date_of_assess                   = forms.DateTimeField(required=False, label=_('SF-36 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SAT_date_of_assess                  = forms.DateTimeField(required=False, label=_('SAT date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FEV_date_of_assess                  = forms.DateTimeField(required=False, label=_('FEV-1 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    AI_date_of_assess                   = forms.DateTimeField(required=False, label=_('ASIA impairment date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SNC_date_of_assess                  = forms.DateTimeField(required=False, label=_('Standard neurological classification of spinal cord injury date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SCI_date_of_assess                  = forms.DateTimeField(required=False, label=_('Spinal Cord Independence Measure date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    Other_date_of_assess                = forms.DateTimeField(required=False, label=_('Other date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    date_of_discharge                   = forms.DateTimeField(label=_('Date of discharge'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FIM_date_of_assess_discharge        = forms.DateTimeField(required=False, label=_('FIM date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    BI_date_of_assess_discharge         = forms.DateTimeField(required=False, label=_('Barthel index date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SMWT_date_of_assess_discharge       = forms.DateTimeField(required=False, label=_('6 minutes walk test date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SF_date_of_assess_discharge         = forms.DateTimeField(required=False, label=_('SF-36 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SAT_date_of_assess_discharge        = forms.DateTimeField(required=False, label=_('SAT date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    FEV_date_of_assess_discharge        = forms.DateTimeField(required=False, label=_('FEV-1 date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    AI_date_of_assess_discharge         = forms.DateTimeField(required=False, label=_('ASIA impairment date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SNC_date_of_assess_discharge        = forms.DateTimeField(required=False, label=_('Standard neurological classification of spinal cord injury date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    SCI_date_of_assess_discharge        = forms.DateTimeField(required=False, label=_('Spinal Cord Independence Measure date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))
    Other_date_of_assess_discharge      = forms.DateTimeField(required=False, label=_('Other date of assessment'), widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':_('(yyyy-mm-dd)')}))

    def clean(self):
        cleaned_data = super(r1Form, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")
        date_of_admission = cleaned_data.get("date_of_admission")
        date_of_discharge = cleaned_data.get("date_of_discharge")
        FIM_date_of_assess = cleaned_data.get("FIM_date_of_assess")
        BI_date_of_assess = cleaned_data.get("BI_date_of_assess")
        SMWT_date_of_assess = cleaned_data.get("SMWT_date_of_assess")
        SF_date_of_assess = cleaned_data.get("SF_date_of_assess")
        SAT_date_of_assess = cleaned_data.get("SAT_date_of_assess")
        AI_date_of_assess = cleaned_data.get("AI_date_of_assess")
        SNC_date_of_assess = cleaned_data.get("SNC_date_of_assess")
        SCI_date_of_assess = cleaned_data.get("SCI_date_of_assess")
        Other_date_of_assess = cleaned_data.get("Other_date_of_assess")
        FIM_date_of_assess_discharge = cleaned_data.get("FIM_date_of_assess_discharge")
        BI_date_of_assess_discharge = cleaned_data.get("BI_date_of_assess_discharge")
        SMWT_date_of_assess_discharge = cleaned_data.get("SMWT_date_of_assess_discharge")
        SF_date_of_assess_discharge = cleaned_data.get("SF_date_of_assess_discharge")
        SAT_date_of_assess_discharge = cleaned_data.get("SAT_date_of_assess_discharge")
        AI_date_of_assess_discharge = cleaned_data.get("AI_date_of_assess_discharge")
        SNC_date_of_assess_discharge = cleaned_data.get("SNC_date_of_assess_discharge")
        SCI_date_of_assess_discharge = cleaned_data.get("SCI_date_of_assess_discharge")
        Other_date_of_assess_discharge = cleaned_data.get("Other_date_of_assess_discharge")

        if date_of_birth > date_of_admission:
            self._errors["date_of_birth"] = self.error_class([_("Can't be born after admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be born after admission!")])
            del cleaned_data["date_of_birth"]
            del cleaned_data["date_of_admission"]

        if date_of_admission > date_of_discharge:
            self._errors["date_of_discharge"] = self.error_class([_("Can't be discharged before admission!")])
            self._errors["date_of_admission"] = self.error_class([_("Can't be discharged before admission!")])
            del cleaned_data["date_of_discharge"]
            del cleaned_data["date_of_admission"]

        if FIM_date_of_assess and FIM_date_of_assess > date_of_discharge:
            self._errors["FIM_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["FIM_date_of_assess"]
        if FIM_date_of_assess and FIM_date_of_assess < date_of_admission:
            self._errors["FIM_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["FIM_date_of_assess"]

        if BI_date_of_assess and BI_date_of_assess > date_of_discharge:
            self._errors["BI_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["BI_date_of_assess"]
        if BI_date_of_assess and BI_date_of_assess < date_of_admission:
            self._errors["BI_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["BI_date_of_assess"]

        if SMWT_date_of_assess and SMWT_date_of_assess > date_of_discharge:
            self._errors["SMWT_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["SMWT_date_of_assess"]
        if SMWT_date_of_assess and SMWT_date_of_assess < date_of_admission:
            self._errors["SMWT_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["SMWT_date_of_assess"]

        if SF_date_of_assess and SF_date_of_assess > date_of_discharge:
            self._errors["SF_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["SF_date_of_assess"]
        if SF_date_of_assess and SF_date_of_assess < date_of_admission:
            self._errors["SF_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["SF_date_of_assess"]

        if SAT_date_of_assess and SAT_date_of_assess > date_of_discharge:
            self._errors["SAT_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["SAT_date_of_assess"]
        if SAT_date_of_assess and SAT_date_of_assess < date_of_admission:
            self._errors["SAT_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["SAT_date_of_assess"]

        if AI_date_of_assess and AI_date_of_assess > date_of_discharge:
            self._errors["AI_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["AI_date_of_assess"]
        if AI_date_of_assess and AI_date_of_assess < date_of_admission:
            self._errors["AI_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["AI_date_of_assess"]

        if SNC_date_of_assess and SNC_date_of_assess > date_of_discharge:
            self._errors["SNC_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["SNC_date_of_assess"]
        if SNC_date_of_assess and SNC_date_of_assess < date_of_admission:
            self._errors["SNC_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["SNC_date_of_assess"]

        if SCI_date_of_assess and SCI_date_of_assess > date_of_discharge:
            self._errors["SCI_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["SCI_date_of_assess"]
        if SCI_date_of_assess and SCI_date_of_assess < date_of_admission:
            self._errors["SCI_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["SCI_date_of_assess"]

        if SCI_date_of_assess and SCI_date_of_assess > date_of_discharge:
            self._errors["SCI_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["SCI_date_of_assess"]
        if SCI_date_of_assess and SCI_date_of_assess < date_of_admission:
            self._errors["SCI_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["SCI_date_of_assess"]

        if Other_date_of_assess and Other_date_of_assess > date_of_discharge:
            self._errors["Other_date_of_assess"] = self.error_class([_("Assessment can't be after discharge!")])
            del cleaned_data["Other_date_of_assess"]
        if Other_date_of_assess and Other_date_of_assess < date_of_admission:
            self._errors["Other_date_of_assess"] = self.error_class([_("Assessment can't be before admission!")])
            del cleaned_data["Other_date_of_assess"]

        if FIM_date_of_assess_discharge and FIM_date_of_assess_discharge > date_of_discharge:
            self._errors["FIM_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["FIM_date_of_assess_discharge"]
        if FIM_date_of_assess_discharge and FIM_date_of_assess_discharge < date_of_admission:
            self._errors["FIM_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["FIM_date_of_assess_discharge"]

        if BI_date_of_assess_discharge and BI_date_of_assess_discharge > date_of_discharge:
            self._errors["BI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["BI_date_of_assess_discharge"]
        if BI_date_of_assess_discharge and BI_date_of_assess_discharge < date_of_admission:
            self._errors["BI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["BI_date_of_assess_discharge"]

        if SMWT_date_of_assess_discharge and SMWT_date_of_assess_discharge > date_of_discharge:
            self._errors["SMWT_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["SMWT_date_of_assess_discharge"]
        if SMWT_date_of_assess_discharge and SMWT_date_of_assess_discharge < date_of_admission:
            self._errors["SMWT_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["SMWT_date_of_assess_discharge"]

        if SF_date_of_assess_discharge and SF_date_of_assess_discharge > date_of_discharge:
            self._errors["SF_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["SF_date_of_assess_discharge"]
        if SF_date_of_assess_discharge and SF_date_of_assess_discharge < date_of_admission:
            self._errors["SF_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["SF_date_of_assess_discharge"]

        if SAT_date_of_assess_discharge and SAT_date_of_assess_discharge > date_of_discharge:
            self._errors["SAT_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["SAT_date_of_assess_discharge"]
        if SAT_date_of_assess_discharge and SAT_date_of_assess_discharge < date_of_admission:
            self._errors["SAT_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["SAT_date_of_assess_discharge"]

        if AI_date_of_assess_discharge and AI_date_of_assess_discharge > date_of_discharge:
            self._errors["AI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["AI_date_of_assess_discharge"]
        if AI_date_of_assess_discharge and AI_date_of_assess_discharge < date_of_admission:
            self._errors["AI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["AI_date_of_assess_discharge"]

        if SNC_date_of_assess_discharge and SNC_date_of_assess_discharge > date_of_discharge:
            self._errors["SNC_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["SNC_date_of_assess_discharge"]
        if SNC_date_of_assess_discharge and SNC_date_of_assess_discharge < date_of_admission:
            self._errors["SNC_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["SNC_date_of_assess_discharge"]

        if SCI_date_of_assess_discharge and SCI_date_of_assess_discharge > date_of_discharge:
            self._errors["SCI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["SCI_date_of_assess_discharge"]
        if SCI_date_of_assess_discharge and SCI_date_of_assess_discharge < date_of_admission:
            self._errors["SCI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["SCI_date_of_assess_discharge"]

        if SCI_date_of_assess_discharge and SCI_date_of_assess_discharge > date_of_discharge:
            self._errors["SCI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["SCI_date_of_assess_discharge"]
        if SCI_date_of_assess_discharge and SCI_date_of_assess_discharge < date_of_admission:
            self._errors["SCI_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["SCI_date_of_assess_discharge"]

        if Other_date_of_assess_discharge and Other_date_of_assess_discharge > date_of_discharge:
            self._errors["Other_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be after discharge!")])
            del cleaned_data["Other_date_of_assess_discharge"]
        if Other_date_of_assess_discharge and Other_date_of_assess_discharge < date_of_admission:
            self._errors["Other_date_of_assess_discharge"] = self.error_class([_("Assessment at discharge can't be before admission!")])
            del cleaned_data["Other_date_of_assess_discharge"]
        return cleaned_data

    class Meta:
        model = r1
        exclude = ('added_by')

class FileUploadForm(forms.Form):
    file  = forms.FileField()