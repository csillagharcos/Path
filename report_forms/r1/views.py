# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from report_forms.r1.forms import r1Form, FileUploadForm, TrendForm, AnonymStatForm
from report_forms.r1.models import r1, r1CSV
from report_forms.tools import parseFloat, parseInt, csvDump, DateException, csvExport
from django.utils.translation import ugettext_lazy as _
from university.models import School

@login_required
def Display(request):
    if request.method == "POST":
        form = r1Form(request.POST)
        if form.is_valid():
            new_r1 = r1.objects.create(
                patient_id                      = form.cleaned_data['patient_id'],
                case_id                         = form.cleaned_data['case_id'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],
                field_of_rehab                  = form.cleaned_data['field_of_rehab'],
                field_of_rehab_other            = form.cleaned_data['field_of_rehab_other'],
                date_of_admission               = form.cleaned_data['date_of_admission'],
                FIM_applied                     = form.cleaned_data['FIM_applied'],
                FIM_date_of_assess              = form.cleaned_data['FIM_date_of_assess'],
                FIM_score                       = form.cleaned_data['FIM_score'],
                BI_applied                      = form.cleaned_data['BI_applied'],
                BI_date_of_assess               = form.cleaned_data['BI_date_of_assess'],
                BI_score                        = form.cleaned_data['BI_score'],
                SMWT_applied                    = form.cleaned_data['SMWT_applied'],
                SMWT_date_of_assess             = form.cleaned_data['SMWT_date_of_assess'],
                SMWT_score                      = form.cleaned_data['SMWT_score'],
                SF_applied                      = form.cleaned_data['SF_applied'],
                SF_date_of_assess               = form.cleaned_data['SF_date_of_assess'],
                SF_score                        = form.cleaned_data['SF_score'],
                SAT_applied                     = form.cleaned_data['SAT_applied'],
                SAT_date_of_assess              = form.cleaned_data['SAT_date_of_assess'],
                SAT_score                       = form.cleaned_data['SAT_score'],
                FEV_applied                     = form.cleaned_data['FEV_applied'],
                FEV_date_of_assess              = form.cleaned_data['FEV_date_of_assess'],
                FEV_score                       = form.cleaned_data['FEV_score'],
                AI_applied                      = form.cleaned_data['AI_applied'],
                AI_date_of_assess               = form.cleaned_data['AI_date_of_assess'],
                AI_score                        = form.cleaned_data['AI_score'],
                SNC_applied                     = form.cleaned_data['SNC_applied'],
                SNC_date_of_assess              = form.cleaned_data['SNC_date_of_assess'],
                SNC_score                       = form.cleaned_data['SNC_score'],
                SCI_applied                     = form.cleaned_data['SCI_applied'],
                SCI_date_of_assess              = form.cleaned_data['SCI_date_of_assess'],
                SCI_score                       = form.cleaned_data['SCI_score'],
                Other_applied                   = form.cleaned_data['Other_applied'],
                Other_name_of                   = form.cleaned_data['Other_name_of'],
                Other_date_of_assess            = form.cleaned_data['Other_date_of_assess'],
                Other_score                     = form.cleaned_data['Other_score'],
                patient_discharge_status        = form.cleaned_data['patient_discharge_status'],
                discharge                       = form.cleaned_data['discharge'],
                if_unplanned                    = form.cleaned_data['if_unplanned'],
                date_of_discharge               = form.cleaned_data['date_of_discharge'],
                FIM_applied_discharge           = form.cleaned_data['FIM_applied_discharge'],
                FIM_date_of_assess_discharge    = form.cleaned_data['FIM_date_of_assess_discharge'],
                FIM_score_discharge             = form.cleaned_data['FIM_score_discharge'],
                BI_applied_discharge            = form.cleaned_data['BI_applied_discharge'],
                BI_date_of_assess_discharge     = form.cleaned_data['BI_date_of_assess_discharge'],
                BI_score_discharge              = form.cleaned_data['BI_score_discharge'],
                SMWT_applied_discharge          = form.cleaned_data['SMWT_applied_discharge'],
                SMWT_date_of_assess_discharge   = form.cleaned_data['SMWT_date_of_assess_discharge'],
                SMWT_score_discharge            = form.cleaned_data['SMWT_score_discharge'],
                SF_applied_discharge            = form.cleaned_data['SF_applied_discharge'],
                SF_date_of_assess_discharge     = form.cleaned_data['SF_date_of_assess_discharge'],
                SF_score_discharge              = form.cleaned_data['SF_score_discharge'],
                SAT_applied_discharge           = form.cleaned_data['SAT_applied_discharge'],
                SAT_date_of_assess_discharge    = form.cleaned_data['SAT_date_of_assess_discharge'],
                SAT_score_discharge             = form.cleaned_data['SAT_score_discharge'],
                FEV_applied_discharge           = form.cleaned_data['FEV_applied_discharge'],
                FEV_date_of_assess_discharge    = form.cleaned_data['FEV_date_of_assess_discharge'],
                FEV_score_discharge             = form.cleaned_data['FEV_score_discharge'],
                AI_applied_discharge            = form.cleaned_data['AI_applied_discharge'],
                AI_date_of_assess_discharge     = form.cleaned_data['AI_date_of_assess_discharge'],
                AI_score_discharge              = form.cleaned_data['AI_score_discharge'],
                SNC_applied_discharge           = form.cleaned_data['SNC_applied_discharge'],
                SNC_date_of_assess_discharge    = form.cleaned_data['SNC_date_of_assess_discharge'],
                SNC_score_discharge             = form.cleaned_data['SNC_score_discharge'],
                SCI_applied_discharge           = form.cleaned_data['SCI_applied_discharge'],
                SCI_date_of_assess_discharge    = form.cleaned_data['SCI_date_of_assess_discharge'],
                SCI_score_discharge             = form.cleaned_data['SCI_score_discharge'],
                Other_applied_discharge         = form.cleaned_data['Other_applied_discharge'],
                Other_name_of_discharge         = form.cleaned_data['Other_name_of_discharge'],
                Other_date_of_assess_discharge  = form.cleaned_data['Other_date_of_assess_discharge'],
                Other_score_discharge           = form.cleaned_data['Other_score_discharge'],
                added_by                        = request.user,
            )
            new_r1.save()
            return render_to_response('r1_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = r1Form(request.POST)
            return render(request, 'r1.html', { 'form': form })

    form = r1Form()
    return render(request, 'r1.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        try:
            csv_file = request.FILES['file']
            imported_csv = r1CSV.import_data(data=csv_file)
            first = True
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            try:
                try: dob = datetime.strptime(line.date_of_birth, "%Y-%m-%d")
                except: dob = None
                try: doa = datetime.strptime(line.date_of_admission, "%Y-%m-%d")
                except: doa = None
                try: fima = datetime.strptime(line.FIM_date_of_assess, "%Y-%m-%d")
                except: fima = None
                try: bia = datetime.strptime(line.BI_date_of_assess, "%Y-%m-%d")
                except: bia = None
                try: smwta = datetime.strptime(line.SMWT_date_of_assess, "%Y-%m-%d")
                except: smwta = None
                try: sfa = datetime.strptime(line.SF_date_of_assess, "%Y-%m-%d")
                except: sfa = None
                try: sata = datetime.strptime(line.SAT_date_of_assess, "%Y-%m-%d")
                except: sata = None
                try: feva = datetime.strptime(line.FEV_date_of_assess, "%Y-%m-%d")
                except: feva = None
                try: aia = datetime.strptime(line.AI_date_of_assess, "%Y-%m-%d")
                except: aia = None
                try: snca = datetime.strptime(line.SNC_date_of_assess, "%Y-%m-%d")
                except: snca = None
                try: scia = datetime.strptime(line.SCI_date_of_assess, "%Y-%m-%d")
                except: scia = None
                try: oa = datetime.strptime(line.Other_date_of_assess, "%Y-%m-%d")
                except: oa = None
                try: dod = datetime.strptime(line.date_of_discharge, "%Y-%m-%d")
                except: dod = None
                try: fimd = datetime.strptime(line.FIM_date_of_assess_discharge, "%Y-%m-%d")
                except: fimd = None
                try: bid = datetime.strptime(line.BI_date_of_assess_discharge, "%Y-%m-%d")
                except: bid = None
                try: smwtd = datetime.strptime(line.SMWT_date_of_assess_discharge, "%Y-%m-%d")
                except: smwtd = None
                try: sfd = datetime.strptime(line.SF_date_of_assess_discharge, "%Y-%m-%d")
                except: sfd = None
                try: satd = datetime.strptime(line.SAT_date_of_assess_discharge, "%Y-%m-%d")
                except: satd = None
                try: fevd = datetime.strptime(line.FEV_date_of_assess_discharge, "%Y-%m-%d")
                except: fevd = None
                try: aid = datetime.strptime(line.AI_date_of_assess_discharge, "%Y-%m-%d")
                except: aid = None
                try: sncd = datetime.strptime(line.SNC_date_of_assess_discharge, "%Y-%m-%d")
                except: sncd = None
                try: scid = datetime.strptime(line.SCI_date_of_assess_discharge, "%Y-%m-%d")
                except: scid = None
                try: od = datetime.strptime(line.Other_date_of_assess_discharge, "%Y-%m-%d")
                except: od = None

                if dob > doa:
                    raise DateException(_("Can't be born after admission!"))
                if doa > dod:
                    raise DateException(_("Can't be born after admission!"))

                if (fima and fima > dod) or (fima and fima < doa):
                    raise DateException(_("FIM assessment can't be after discharge!"))
                if (bia and bia > dod) or (bia and bia < doa):
                    raise DateException(_("Barthel index assessment can't be after discharge!"))
                if (smwta and smwta > dod) or (smwta and smwta < doa):
                    raise DateException(_("6 minutes walk test assessment can't be after discharge!"))
                if (sfa and sfa > dod) or (sfa and sfa < doa):
                    raise DateException(_("SF-36 assessment can't be after discharge!"))
                if (sata and sata > dod) or (sata and sata < doa):
                    raise DateException(_("SAT assessment can't be after discharge!"))
                if (feva and feva > dod) or (feva and feva < doa):
                    raise DateException(_("FEV-1 assessment can't be after discharge!"))
                if (aia and aia > dod) or (aia and aia < doa):
                    raise DateException(_("ASIA impairment assessment can't be after discharge!"))
                if (snca and snca > dod) or (snca and snca < doa):
                    raise DateException(_("Standard neurological classification of spinal cord injury assessment can't be after discharge!"))
                if (scia and scia > dod) or (scia and scia < doa):
                    raise DateException(_("Spinal Cord Independence Measure assessment can't be after discharge!"))
                if (oa and oa > dod) or (oa and oa < doa):
                    raise DateException(_("Other assessment can't be after discharge!"))

                if (fimd and fimd > dod) or (fimd and fimd < doa):
                    raise DateException(_("FIM assessment at discharge can't be after discharge!"))
                if (bid and bid > dod) or (bid and bid < doa):
                    raise DateException(_("Barthel index assessment at discharge can't be after discharge!"))
                if (smwtd and smwtd > dod) or (smwtd and smwtd < doa):
                    raise DateException(_("6 minutes walk test assessment at discharge can't be after discharge!"))
                if (sfd and sfd > dod) or (sfd and sfd < doa):
                    raise DateException(_("SF-36 assessment at discharge can't be after discharge!"))
                if (satd and satd > dod) or (satd and satd < doa):
                    raise DateException(_("SAT assessment at discharge can't be after discharge!"))
                if (fevd and fevd > dod) or (fevd and fevd < doa):
                    raise DateException(_("FEV-1 assessment at discharge can't be after discharge!"))
                if (aid and aid > dod) or (aid and aid < doa):
                    raise DateException(_("ASIA impairment assessment at discharge can't be after discharge!"))
                if (sncd and sncd > dod) or (sncd and sncd < doa):
                    raise DateException(_("Standard neurological classification of spinal cord injury assessment at discharge can't be after discharge!"))
                if (scid and scid > dod) or (scid and scid < doa):
                    raise DateException(_("Spinal Cord Independence Measure assessment at discharge can't be after discharge!"))
                if (od and od > dod) or (od and od < doa):
                    raise DateException(_("Other assessment at discharge can't be after discharge!"))

                if parseInt(line.Other_applied_discharge) is None:
                    oad = 0
                else:
                    oad = parseInt(line.Other_applied_discharge)
                new_r1 = r1.objects.create(
                                            patient_id                      = parseInt(line.patient_id),
                                            case_id                         = parseInt(line.case_id),
                                            date_of_birth                   = dob,
                                            field_of_rehab                  = parseInt(line.field_of_rehab),
                                            field_of_rehab_other            = line.field_of_rehab_other,
                                            date_of_admission               = doa,
                                            FIM_applied                     = parseInt(line.FIM_applied),
                                            FIM_date_of_assess              = fima,
                                            FIM_score                       = parseFloat(line.FIM_score),
                                            BI_applied                      = parseInt(line.BI_applied),
                                            BI_date_of_assess               = bia,
                                            BI_score                        = parseFloat(line.BI_score),
                                            SMWT_applied                    = parseInt(line.SMWT_applied),
                                            SMWT_date_of_assess             = smwta,
                                            SMWT_score                      = parseFloat(line.SMWT_score),
                                            SF_applied                      = parseInt(line.SF_applied),
                                            SF_date_of_assess               = sfa,
                                            SF_score                        = parseFloat(line.SF_score),
                                            SAT_applied                     = parseInt(line.SAT_applied),
                                            SAT_date_of_assess              = sata,
                                            SAT_score                       = parseFloat(line.SAT_score),
                                            FEV_applied                     = parseInt(line.FEV_applied),
                                            FEV_date_of_assess              = feva,
                                            FEV_score                       = parseFloat(line.FEV_score),
                                            AI_applied                      = parseInt(line.AI_applied),
                                            AI_date_of_assess               = aia,
                                            AI_score                        = parseFloat(line.AI_score),
                                            SNC_applied                     = parseInt(line.SNC_applied),
                                            SNC_date_of_assess              = snca,
                                            SNC_score                       = parseFloat(line.SNC_score),
                                            SCI_applied                     = parseInt(line.SCI_applied),
                                            SCI_date_of_assess              = scia,
                                            SCI_score                       = parseFloat(line.SCI_score),
                                            Other_applied                   = parseInt(line.Other_applied),
                                            Other_name_of                   = line.Other_name_of,
                                            Other_date_of_assess            = oa,
                                            Other_score                     = parseFloat(line.Other_score),
                                            patient_discharge_status        = parseInt(line.patient_discharge_status),
                                            discharge                       = parseInt(line.discharge),
                                            if_unplanned                    = parseInt(line.if_unplanned),
                                            date_of_discharge               = dod,
                                            FIM_applied_discharge           = parseInt(line.FIM_applied_discharge),
                                            FIM_date_of_assess_discharge    = fimd,
                                            FIM_score_discharge             = parseFloat(line.FIM_score_discharge),
                                            BI_applied_discharge            = parseInt(line.BI_applied_discharge),
                                            BI_date_of_assess_discharge     = bid,
                                            BI_score_discharge              = parseFloat(line.BI_score_discharge),
                                            SMWT_applied_discharge          = parseInt(line.SMWT_applied_discharge),
                                            SMWT_date_of_assess_discharge   = smwtd,
                                            SMWT_score_discharge            = parseFloat(line.SMWT_score_discharge),
                                            SF_applied_discharge            = parseInt(line.SF_applied_discharge),
                                            SF_date_of_assess_discharge     = sfd,
                                            SF_score_discharge              = parseFloat(line.SF_score_discharge),
                                            SAT_applied_discharge           = parseInt(line.SAT_applied_discharge),
                                            SAT_date_of_assess_discharge    = satd,
                                            SAT_score_discharge             = parseFloat(line.SAT_score_discharge),
                                            FEV_applied_discharge           = parseInt(line.FEV_applied_discharge),
                                            FEV_date_of_assess_discharge    = fevd,
                                            FEV_score_discharge             = parseFloat(line.FEV_score_discharge),
                                            AI_applied_discharge            = parseInt(line.AI_applied_discharge),
                                            AI_date_of_assess_discharge     = aid,
                                            AI_score_discharge              = parseFloat(line.AI_score_discharge),
                                            SNC_applied_discharge           = parseInt(line.SNC_applied_discharge),
                                            SNC_date_of_assess_discharge    = sncd,
                                            SNC_score_discharge             = parseFloat(line.SNC_score_discharge),
                                            SCI_applied_discharge           = parseInt(line.SCI_applied_discharge),
                                            SCI_date_of_assess_discharge    = scid,
                                            SCI_score_discharge             = parseFloat(line.SCI_score_discharge),
                                            Other_applied_discharge         = oad,
                                            Other_name_of_discharge         = line.Other_name_of_discharge,
                                            Other_date_of_assess_discharge  = od,
                                            Other_score_discharge           = parseFloat(line.Other_score_discharge),
                                            added_by                        = request.user,
                )
                new_r1.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('r1_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('r1_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('r1_file_upload.html', context, context_instance=RequestContext(request))

@login_required
def Statistics(request):
    context = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace))
    return render_to_response('r1_statistics.html', context, context_instance=RequestContext(request))

@login_required
def Trendr1(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date1a'], date_of_admission__lte = form.cleaned_data['date1b'] ) )
            interval_two = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date2a'], date_of_admission__lte = form.cleaned_data['date2b'] ) )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date3a'], date_of_admission__lte = form.cleaned_data['date3b'] ) )
            else:
                interval_three = False
            return render_to_response('r1_trend_diagram.html', { 'one': interval_one, 'two': interval_two, 'three': interval_three, 'form': form.cleaned_data }, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'r1_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'r1_trend.html', { 'form': form })

def Trendr2(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_discharge__gte = form.cleaned_data['date1a'], date_of_discharge__lte = form.cleaned_data['date1b'] ) )
            interval_two = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_discharge__gte = form.cleaned_data['date2a'], date_of_discharge__lte = form.cleaned_data['date2b'] ) )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_discharge__gte = form.cleaned_data['date3a'], date_of_discharge__lte = form.cleaned_data['date3b'] ) )
            else:
                interval_three = False
            return render_to_response('r2_trend_diagram.html', { 'one': interval_one, 'two': interval_two, 'three': interval_three, 'form': form.cleaned_data }, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'r1_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'r1_trend.html', { 'form': form })

def Template(request):
    model = (
        _('Patient ID'),
        _('Case ID'),
        _('Date of birth'),
        _('Professional field of rehabilitation'),
        _('If other'),
        _('Date of admission'),
        _('FIM applied at admission'),
        _('FIM date of assessment'),
        _('FIM value/score'),
        _('Barthel index applied at admission'),
        _('Barthel index date of assessment'),
        _('Barthel index value/score'),
        _('6 minutes walk test applied at admission'),
        _('6 minutes walk test date of assessment'),
        _('6 minutes walk test value/score'),
        _('SF-36 applied at admission'),
        _('SF-36 date of assessment'),
        _('SF-36 value/score'),
        _('SAT applied at admission'),
        _('SAT date of assessment'),
        _('SAT value/score'),
        _('FEV-1 applied at admission'),
        _('FEV-1 date of assessment'),
        _('FEV-1 value/score'),
        _('ASIA impairment applied at admission'),
        _('ASIA impairment date of assessment'),
        _('ASIA impairment value/score'),
        _('Standard neurological classification of spinal cord injury applied at admission'),
        _('Standard neurological classification of spinal cord injury date of assessment'),
        _('Standard neurological classification of spinal cord injury value/score'),
        _('Spinal Cord Independence Measure applied at admission'),
        _('Spinal Cord Independence Measure date of assessment'),
        _('Spinal Cord Independence Measure value/score'),
        _('Other applied at admission'),
        _('Other name of functional assessment'),
        _('Other date of assessment'),
        _('Other value/score'),
        _('Patient discharge status'),
        _('Discharge'),
        _('If unplanned, the reason'),
        _('Date of discharge'),
        _('FIM applied at discharge'),
        _('FIM date of assessment'),
        _('FIM value/score'),
        _('Barthel index applied at discharge'),
        _('Barthel index date of assessment'),
        _('Barthel index value/score'),
        _('6 minutes walk test applied at discharge'),
        _('6 minutes walk test date of assessment'),
        _('6 minutes walk test value/score'),
        _('SF-36 applied at discharge'),
        _('SF-36 date of assessment'),
        _('SF-36 value/score'),
        _('SAT applied at discharge'),
        _('SAT date of assessment'),
        _('SAT value/score'),
        _('FEV-1 applied at discharge'),
        _('FEV-1 date of assessment'),
        _('FEV-1 value/score'),
        _('ASIA impairment applied at discharge'),
        _('ASIA impairment date of assessment'),
        _('ASIA impairment value/score'),
        _('Standard neurological classification of spinal cord injury applied at discharge'),
        _('Standard neurological classification of spinal cord injury date of assessment'),
        _('Standard neurological classification of spinal cord injury value/score'),
        _('Spinal Cord Independence Measure applied at discharge'),
        _('Spinal Cord Independence Measure date of assessment'),
        _('Spinal Cord Independence Measure value/score'),
        _('Other applied at discharge'),
        _('Other name of functional assessment'),
        _('Other date of assessment'),
        _('Other value/score'),
        )
    return csvDump(model, "r1")

@login_required
def Export(request):
    model = ((
                 _('Patients ID'),
                 _('Case ID'),
                 _('Date of birth'),
                 _('Professional field of rehabilitation'),
                 _('If other'),
                 _('Date of admission'),
                 _('FIM applied at admission'),
                 _('FIM date of assessment'),
                 _('FIM value/score'),
                 _('Barthel index applied at admission'),
                 _('Barthel index date of assessment'),
                 _('Barthel index value/score'),
                 _('6 minutes walk test applied at admission'),
                 _('6 minutes walk test date of assessment'),
                 _('6 minutes walk test value/score'),
                 _('SF-36 applied at admission'),
                 _('SF-36 date of assessment'),
                 _('SF-36 value/score'),
                 _('SAT applied at admission'),
                 _('SAT date of assessment'),
                 _('SAT value/score'),
                 _('FEV-1 applied at admission'),
                 _('FEV-1 date of assessment'),
                 _('FEV-1 value/score'),
                 _('ASIA impairment applied at admission'),
                 _('ASIA impairment date of assessment'),
                 _('ASIA impairment value/score'),
                 _('Standard neurological classification of spinal cord injury applied at admission'),
                 _('Standard neurological classification of spinal cord injury date of assessment'),
                 _('Standard neurological classification of spinal cord injury value/score'),
                 _('Spinal Cord Independence Measure applied at admission'),
                 _('Spinal Cord Independence Measure date of assessment'),
                 _('Spinal Cord Independence Measure value/score'),
                 _('Other applied at admission'),
                 _('Other name of functional assessment'),
                 _('Other date of assessment'),
                 _('Other value/score'),
                 _('Patient discharge status'),
                 _('Discharge'),
                 _('If unplanned, the reason'),
                 _('Date of discharge'),
                 _('FIM applied at discharge'),
                 _('FIM date of assessment'),
                 _('FIM value/score'),
                 _('Barthel index applied at discharge'),
                 _('Barthel index date of assessment'),
                 _('Barthel index value/score'),
                 _('6 minutes walk test applied at discharge'),
                 _('6 minutes walk test date of assessment'),
                 _('6 minutes walk test value/score'),
                 _('SF-36 applied at discharge'),
                 _('SF-36 date of assessment'),
                 _('SF-36 value/score'),
                 _('SAT applied at discharge'),
                 _('SAT date of assessment'),
                 _('SAT value/score'),
                 _('FEV-1 applied at discharge'),
                 _('FEV-1 date of assessment'),
                 _('FEV-1 value/score'),
                 _('ASIA impairment applied at discharge'),
                 _('ASIA impairment date of assessment'),
                 _('ASIA impairment value/score'),
                 _('Standard neurological classification of spinal cord injury applied at discharge'),
                 _('Standard neurological classification of spinal cord injury date of assessment'),
                 _('Standard neurological classification of spinal cord injury value/score'),
                 _('Spinal Cord Independence Measure applied at discharge'),
                 _('Spinal Cord Independence Measure date of assessment'),
                 _('Spinal Cord Independence Measure value/score'),
                 _('Other applied at discharge'),
                 _('Other name of functional assessment'),
                 _('Other date of assessment'),
                 _('Other value/score'),
                 ),)
    cases = r1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.patient_id),
                      str(case.case_id),
                      str(case.date_of_birth),
                      str(case.field_of_rehab),
                      str(case.field_of_rehab_other),
                      str(case.date_of_admission),
                      str(case.FIM_applied),
                      str(case.FIM_date_of_assess),
                      str(case.FIM_score),
                      str(case.BI_applied),
                      str(case.BI_date_of_assess),
                      str(case.BI_score),
                      str(case.SMWT_applied),
                      str(case.SMWT_date_of_assess),
                      str(case.SMWT_score),
                      str(case.SF_applied),
                      str(case.SF_date_of_assess),
                      str(case.SF_score),
                      str(case.SAT_applied),
                      str(case.SAT_date_of_assess),
                      str(case.SAT_score),
                      str(case.FEV_applied),
                      str(case.FEV_date_of_assess),
                      str(case.FEV_score),
                      str(case.AI_applied),
                      str(case.AI_date_of_assess),
                      str(case.AI_score),
                      str(case.SNC_applied),
                      str(case.SNC_date_of_assess),
                      str(case.SNC_score),
                      str(case.SCI_applied),
                      str(case.SCI_date_of_assess),
                      str(case.SCI_score),
                      str(case.Other_applied),
                      str(case.Other_name_of),
                      str(case.Other_date_of_assess),
                      str(case.Other_score),
                      str(case.patient_discharge_status),
                      str(case.discharge),
                      str(case.if_unplanned),
                      str(case.date_of_discharge),
                      str(case.FIM_applied_discharge),
                      str(case.FIM_date_of_assess_discharge),
                      str(case.FIM_score_discharge),
                      str(case.BI_applied_discharge),
                      str(case.BI_date_of_assess_discharge),
                      str(case.BI_score_discharge),
                      str(case.SMWT_applied_discharge),
                      str(case.SMWT_date_of_assess_discharge),
                      str(case.SMWT_score_discharge),
                      str(case.SF_applied_discharge),
                      str(case.SF_date_of_assess_discharge),
                      str(case.SF_score_discharge),
                      str(case.SAT_applied_discharge),
                      str(case.SAT_date_of_assess_discharge),
                      str(case.SAT_score_discharge),
                      str(case.FEV_applied_discharge),
                      str(case.FEV_date_of_assess_discharge),
                      str(case.FEV_score_discharge),
                      str(case.AI_applied_discharge),
                      str(case.AI_date_of_assess_discharge),
                      str(case.AI_score_discharge),
                      str(case.SNC_applied_discharge),
                      str(case.SNC_date_of_assess_discharge),
                      str(case.SNC_score_discharge),
                      str(case.SCI_applied_discharge),
                      str(case.SCI_date_of_assess_discharge),
                      str(case.SCI_score_discharge),
                      str(case.Other_applied_discharge),
                      str(case.Other_name_of_discharge),
                      str(case.Other_date_of_assess_discharge),
                      str(case.Other_score_discharge),
                      ),)
    return csvExport(model, 'r1_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

def CountStatistics(cases, notView=True):
    ''' Query '''
    r1a_countable_case=r1a_uncountable_case=r1b_countable_case=r1b_uncountable_case=r2_countable_case=r2_uncountable_case=()
    for case in cases:
        if case.patient_discharge_status == 1 and case.discharge == 0:
            r2_uncountable_case += (case,)
        else:
            r2_countable_case += (case,)
        if (case.date_of_discharge - case.date_of_admission).days > 7:
            r1a_countable_case += (case,)
            r1b_countable_case += (case,)
        elif case.discharge == 1:
            r1a_uncountable_case += (case,)
            r1b_countable_case += (case,)
        else:
            r1a_uncountable_case += (case,)
            r1b_uncountable_case += (case,)

    ''' Working '''
    r1a_first_indicator = r1a_second_indicator = r1a_third_indicator = 0
    r1b_first_indicator = r1b_second_indicator = r1b_third_indicator = 0
    r2_first_indicator = r2_second_indicator = r2_third_indicator = r2_fourth_indicator = 0
    for case in r1a_countable_case:
        try: fima7 = (case.FIM_date_of_assess - case.date_of_admission).days+1 <= 7
        except: fima7 = False
        try: fima2 = (case.FIM_date_of_assess - case.date_of_admission).days+1 <= 2
        except: fima2 = False
        try: fima3 = (case.FIM_date_of_assess - case.date_of_admission).days+1 <= 3
        except: fima3 = False

        try: bia7 = (case.BI_date_of_assess - case.date_of_admission).days+1 <= 7
        except: bia7 = False
        try: bia2 = (case.BI_date_of_assess - case.date_of_admission).days+1 <= 2
        except: bia2 = False
        try: bia3 = (case.BI_date_of_assess - case.date_of_admission).days+1 <= 3
        except: bia3 = False

        try: smwta7 = (case.SMWT_date_of_assess - case.date_of_admission).days+1 <= 7
        except: smwta7 = False
        try: smwta2 = (case.SMWT_date_of_assess - case.date_of_admission).days+1 <= 2
        except: smwta2 = False
        try: smwta3 = (case.SMWT_date_of_assess - case.date_of_admission).days+1 <= 3
        except: smwta3 = False

        try: sfa7 = (case.SF_date_of_assess - case.date_of_admission).days+1 <= 7
        except: sfa7 = False
        try: sfa2 = (case.SF_date_of_assess - case.date_of_admission).days+1 <= 2
        except: sfa2 = False
        try: sfa3 = (case.SF_date_of_assess - case.date_of_admission).days+1 <= 3
        except: sfa3 = False

        try: sata7 = (case.SAT_date_of_assess - case.date_of_admission).days+1 <= 7
        except: sata7 = False
        try: sata2 = (case.SAT_date_of_assess - case.date_of_admission).days+1 <= 2
        except: sata2 = False
        try: sata3 = (case.SAT_date_of_assess - case.date_of_admission).days+1 <= 3
        except: sata3 = False

        try: feva7 = (case.FEV_date_of_assess - case.date_of_admission).days+1 <= 7
        except: feva7 = False
        try: feva2 = (case.FEV_date_of_assess - case.date_of_admission).days+1 <= 2
        except: feva2 = False
        try: feva3 = (case.FEV_date_of_assess - case.date_of_admission).days+1 <= 3
        except: feva3 = False

        try: aia7 = (case.AI_date_of_assess - case.date_of_admission).days+1 <= 7
        except: aia7 = False
        try: aia2 = (case.AI_date_of_assess - case.date_of_admission).days+1 <= 2
        except: aia2 = False
        try: aia3 = (case.AI_date_of_assess - case.date_of_admission).days+1 <= 3
        except: aia3 = False

        try: snca7 = (case.SNC_date_of_assess - case.date_of_admission).days+1 <= 7
        except: snca7 = False
        try: snca2 = (case.SNC_date_of_assess - case.date_of_admission).days+1 <= 2
        except: snca2 = False
        try: snca3 = (case.SNC_date_of_assess - case.date_of_admission).days+1 <= 3
        except: snca3 = False

        try: scia7 = (case.SCI_date_of_assess - case.date_of_admission).days+1 <= 7
        except: scia7 = False
        try: scia2 = (case.SCI_date_of_assess - case.date_of_admission).days+1 <= 2
        except: scia2 = False
        try: scia3 = (case.SCI_date_of_assess - case.date_of_admission).days+1 <= 3
        except: scia3 = False

        try: oa7 = (case.Other_date_of_assess - case.date_of_admission).days+1 <= 7
        except: oa7 = False
        try: oa2 = (case.Other_date_of_assess - case.date_of_admission).days+1 <= 2
        except: oa2 = False
        try: oa3 = (case.Other_date_of_assess - case.date_of_admission).days+1 <= 3
        except: oa3 = False

        if fima7 or bia7 or smwta7 or sfa7 or sata7 or feva7 or aia7 or snca7 or scia7 or oa7:
            r1a_first_indicator += 1
        if fima2 or bia2 or smwta2 or sfa2 or sata2 or feva2 or aia2 or snca2 or scia2 or oa2:
            r1a_second_indicator += 1
        if fima3 or bia3 or smwta3 or sfa3 or sata3 or feva3 or aia3 or snca3 or scia3 or oa3:
            r1a_third_indicator += 1

    for case in r1b_countable_case:
        try: fimd4 = (case.date_of_discharge - case.FIM_date_of_assess_discharge).days+1 <= 3
        except: fimd4 = False
        try: fimd2 = (case.date_of_discharge - case.FIM_date_of_assess_discharge).days+1 <= 1
        except: fimd2 = False
        try: fimd3 = (case.date_of_discharge - case.FIM_date_of_assess_discharge).days+1 <= 2
        except: fimd3 = False

        try: bid4 = (case.date_of_discharge - case.BI_date_of_assess_discharge).days+1 <= 3
        except: bid4 = False
        try: bid2 = (case.date_of_discharge - case.BI_date_of_assess_discharge).days+1 <= 1
        except: bid2 = False
        try: bid3 = (case.date_of_discharge - case.BI_date_of_assess_discharge).days+1 <= 2
        except: bid3 = False

        try: smwtd4 = (case.date_of_discharge - case.SMWT_date_of_assess_discharge).days+1 <= 3
        except: smwtd4 = False
        try: smwtd2 = (case.date_of_discharge - case.SMWT_date_of_assess_discharge).days+1 <= 1
        except: smwtd2 = False
        try: smwtd3 = (case.date_of_discharge - case.SMWT_date_of_assess_discharge).days+1 <= 2
        except: smwtd3 = False

        try: sfd4 = (case.date_of_discharge - case.SF_date_of_assess_discharge).days+1 <= 3
        except: sfd4 = False
        try: sfd2 = (case.date_of_discharge - case.SF_date_of_assess_discharge).days+1 <= 1
        except: sfd2 = False
        try: sfd3 = (case.date_of_discharge - case.SF_date_of_assess_discharge).days+1 <= 2
        except: sfd3 = False

        try: satd4 = (case.date_of_discharge - case.SAT_date_of_assess_discharge).days+1 <= 3
        except: satd4 = False
        try: satd2 = (case.date_of_discharge - case.SAT_date_of_assess_discharge).days+1 <= 1
        except: satd2 = False
        try: satd3 = (case.date_of_discharge - case.SAT_date_of_assess_discharge).days+1 <= 2
        except: satd3 = False

        try: fevd4 = (case.date_of_discharge - case.FEV_date_of_assess_discharge).days+1 <= 3
        except: fevd4 = False
        try: fevd2 = (case.date_of_discharge - case.FEV_date_of_assess_discharge).days+1 <= 1
        except: fevd2 = False
        try: fevd3 = (case.date_of_discharge - case.FEV_date_of_assess_discharge).days+1 <= 2
        except: fevd3 = False

        try: aid4 = (case.date_of_discharge - case.AI_date_of_assess_discharge).days+1 <= 3
        except: aid4 = False
        try: aid2 = (case.date_of_discharge - case.AI_date_of_assess_discharge).days+1 <= 1
        except: aid2 = False
        try: aid3 = (case.date_of_discharge - case.AI_date_of_assess_discharge).days+1 <= 2
        except: aid3 = False

        try: sncd4 = (case.date_of_discharge - case.SNC_date_of_assess_discharge).days+1 <= 3
        except: sncd4 = False
        try: sncd2 = (case.date_of_discharge - case.SNC_date_of_assess_discharge).days+1 <= 1
        except: sncd2 = False
        try: sncd3 = (case.date_of_discharge - case.SNC_date_of_assess_discharge).days+1 <= 2
        except: sncd3 = False

        try: scid4 = (case.date_of_discharge - case.SCI_date_of_assess_discharge).days+1 <= 3
        except: scid4 = False
        try: scid2 = (case.date_of_discharge - case.SCI_date_of_assess_discharge).days+1 <= 1
        except: scid2 = False
        try: scid3 = (case.date_of_discharge - case.SCI_date_of_assess_discharge).days+1 <= 2
        except: scid3 = False

        try: od4 = (case.date_of_discharge - case.Other_date_of_assess_discharge).days+1 <= 3
        except: od4 = False
        try: od2 = (case.date_of_discharge - case.Other_date_of_assess_discharge).days+1 <= 1
        except: od2 = False
        try: od3 = (case.date_of_discharge - case.Other_date_of_assess_discharge).days+1 <= 2
        except: od3 = False

        if fimd4 or bid4 or smwtd4 or sfd4 or satd4 or fevd4 or aid4 or sncd4 or scid4 or od4:
            r1b_first_indicator += 1
        if fimd2 or bid2 or smwtd2 or sfd2 or satd2 or fevd2 or aid2 or sncd2 or scid2 or od2:
            r1b_second_indicator += 1
        if fimd3 or bid3 or smwtd3 or sfd3 or satd3 or fevd3 or aid3 or sncd3 or scid3 or od3:
            r1b_third_indicator += 1

    for case in r2_countable_case:
        if case.discharge:
            r2_first_indicator += 1
            if case.if_unplanned == 1 or case.if_unplanned == 2 or case.if_unplanned == 3:
                r2_second_indicator += 1
            elif case.if_unplanned == 4:
                r2_third_indicator += 1
            elif not case.if_unplanned:
                r2_fourth_indicator += 1

    ''' Counting '''

    try: r1a_first = float(r1a_first_indicator) / len(r1a_countable_case) * 100
    except: r1a_first = 0
    try: r1a_second = float(r1a_second_indicator) / len(r1a_countable_case) * 100
    except: r1a_second = 0
    try: r1a_third = float(r1a_third_indicator) / len(r1a_countable_case) * 100
    except: r1a_third = 0

    try: r1b_first = float(r1b_first_indicator) / len(r1b_countable_case) * 100
    except: r1b_first = 0
    try: r1b_second = float(r1b_second_indicator) / len(r1b_countable_case) * 100
    except: r1b_second = 0
    try: r1b_third = float(r1b_third_indicator) / len(r1b_countable_case) * 100
    except: r1b_third = 0

    try: r2_first = float(r2_first_indicator) / len(r2_countable_case) * 100
    except: r2_first = 0
    try: r2_second = float(r2_second_indicator) / len(r2_countable_case) * 100
    except: r2_second = 0
    try: r2_third = float(r2_third_indicator) / len(r2_countable_case) * 100
    except: r2_third = 0
    try: r2_fourth = float(r2_fourth_indicator) / len(r2_countable_case) * 100
    except: r2_fourth = 0


    ''' Displaying '''
    context = {
        "overall": len(cases),
        "r1aremoved": len(r1a_uncountable_case),
        "r1acounted": len(r1a_countable_case),
        "r1bremoved": len(r1b_uncountable_case),
        "r1bcounted": len(r1b_countable_case),
        "r2removed": len(r2_uncountable_case),
        "r2counted": len(r2_countable_case),
        "r1a1": r1a_first,
        "r1a2": r1a_second,
        "r1a3": r1a_third,
        "r1b1": r1b_first,
        "r1b2": r1b_second,
        "r1b3": r1b_third,
        "r21": r2_first,
        "r22": r2_second,
        "r23": r2_third,
        "r24": r2_fourth,
        }
    return context

@login_required
def AnonymStatistics(request):
    if request.method == "POST":
        form = AnonymStatForm(request.POST)
        statistics = []
        if form.is_valid():
            start = form.cleaned_data['endDate'] - timedelta(days=365)
            end = form.cleaned_data['endDate']
            workplaces = School.objects.filter(country__printable_name = request.user.get_profile().country)
            for workplace in workplaces:
                stat = CountStatistics(r1.objects.filter(added_by__personel__workplace = workplace, date_of_admission__gte = start, date_of_admission__lte = end ), False )
                if stat['overall'] >= 60:
                    statistics += [{
                        "name" : workplace.codename,
                        "statistics" : stat
                    }]
            statistics = SortAndAddCountryAverage(statistics, start, end, request.user)
            return render_to_response('r1_anon.html', {'statistics': statistics}, context_instance=RequestContext(request))
        else:
            form = AnonymStatForm(request.POST)
            return render(request, 'r1.html', { 'form': form,'benchmarking': True })
    form = AnonymStatForm()
    return render(request, 'r1.html', { 'form': form,'benchmarking': True })

def SortAndAddCountryAverage(statistics, start, end, user):
    statistics = sorted(statistics, key=lambda x: x['name'])
    hospitals = []
    countryStat = []
    statis = []
    overall = r1bremoved = r1bcounted = r1aremoved = r1acounted = r2removed = r2counted = r1a1 = r1a2 = r1a3 = r1b1 = r1b2 = r1b3 = r21 = r22 = r23 = r24 = 0
    for workplace in statistics:
        foundCountry = False
        hospital = School.objects.get(codename=workplace['name'])
        if not hospitals:
            hospitals += [{ 'country': hospital.country.printable_name, 'hospitals': [hospital.codename,]},]
        else:
            for hos in hospitals:
                if hos['country'] == hospital.country.printable_name:
                    hos['hospitals'] += [hospital.codename,]
                    foundCountry = True
                    break
            if not foundCountry:
                hospitals += [{ 'country': hospital.country.printable_name, 'hospitals': [hospital.codename,]},]

    for country in hospitals:
        name = country['country']
        for hospit in country['hospitals']:
            query = r1.objects.filter(added_by__personel__workplace__codename = hospit, date_of_admission__gte = start, date_of_admission__lte = end )
            statis += [CountStatistics(query, False),]
        for stat in statis:
            overall += stat['overall']
            r1aremoved += stat['r1aremoved']
            r1acounted += stat['r1acounted']
            r1bremoved += stat['r1bremoved']
            r1bcounted += stat['r1bcounted']
            r2removed += stat['r2removed']
            r2counted += stat['r2counted']
            r1a1 += stat['r1a1']
            r1a2 += stat['r1a2']
            r1a3 += stat['r1a3']
            r1b1 += stat['r1b1']
            r1b2 += stat['r1b2']
            r1b3 += stat['r1b3']
            r21 += stat['r21']
            r22 += stat['r22']
            r23 += stat['r23']
            r24 += stat['r24']
        counter = len(statis)
        stat = {
            "overall": overall,
            "r1aremoved": r1aremoved,
            "r1acounted": r1acounted,
            "r1bremoved": r1bremoved,
            "r1bcounted": r1bcounted,
            "r2removed": r2removed,
            "r2counted": r2counted,
            "r1a1": (r1a1/counter),
            "r1a2": (r1a2/counter),
            "r1a3": (r1a3/counter),
            "r1b1": (r1b1/counter),
            "r1b2": (r1b2/counter),
            "r1b3": (r1b3/counter),
            "r21": (r21/counter),
            "r22": (r22/counter),
            "r23": (r23/counter),
            "r24": (r24/counter),
        }
        countryStat += [{
            'name': name,
            'statistics': stat
        },]
    combined_results = countryStat + statistics
    ci = wi = 0
    coi = woi = None
    yourCountry = yourHospital = [{},]

    for result in combined_results:
        if user.get_profile().workplace.country.printable_name == result['name']:
            coi = ci
        ci += 1
    if coi is not None:
        yourCountry = combined_results.pop(coi)

    for result in combined_results:
        if user.get_profile().workplace.codename == result['name']:
            woi = wi
        wi += 1
    if woi is not None:
        yourHospital =  combined_results.pop(woi)

    if coi is not None and woi is not None:
        combined_results = [yourCountry,] + [yourHospital,] + combined_results
    elif coi is not None:
        combined_results = [yourCountry,] + combined_results
    elif woi is not None:
        combined_results = [yourHospital,] + combined_results

    return combined_results