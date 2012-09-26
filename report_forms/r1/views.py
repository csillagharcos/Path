# -*- coding: utf-8 -*-
from datetime import datetime
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.r1.forms import r1Form, FileUploadForm
from report_forms.r1.models import r1, r1CSV
from report_forms.tools import parseFloat, parseInt, csvDump
from django.utils.translation import ugettext_lazy as _

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
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = r1Form(request.POST)
            return render(request, 'r1.html', { 'form': form })

    form = r1Form()
    return render(request, 'r1.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        try:
            csv_file = request.FILES['file']
            imported_csv = r1CSV.import_data(data=csv_file)
        except UnicodeDecodeError:
            return render_to_response('error.html', {"message": _("You probably forgot to delete the first row of the csv file, please recheck.") }, context_instance=RequestContext(request))
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            try:
                new_r1 = r1.objects.create(
                                            patient_id                      = line.patient_id,
                                            case_id                         = line.case_id,
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            field_of_rehab                  = parseInt(line.field_of_rehab),
                                            field_of_rehab_other            = line.field_of_rehab_other,
                                            date_of_admission               = datetime.strptime(line.date_of_admission, "%Y-%m-%d"),
                                            FIM_applied                     = parseInt(line.FIM_applied),
                                            FIM_date_of_assess              = datetime.strptime(line.FIM_date_of_assess, "%Y-%m-%d"),
                                            FIM_score                       = parseFloat(line.FIM_score),
                                            BI_applied                      = parseInt(line.BI_applied),
                                            BI_date_of_assess               = datetime.strptime(line.BI_date_of_assess, "%Y-%m-%d"),
                                            BI_score                        = parseFloat(line.BI_score),
                                            SMWT_applied                    = parseInt(line.SMWT_applied),
                                            SMWT_date_of_assess             = datetime.strptime(line.SMWT_date_of_assess, "%Y-%m-%d"),
                                            SMWT_score                      = parseFloat(line.SMWT_score),
                                            SF_applied                      = parseInt(line.SF_applied),
                                            SF_date_of_assess               = datetime.strptime(line.SF_date_of_assess, "%Y-%m-%d"),
                                            SF_score                        = parseFloat(line.SF_score),
                                            SAT_applied                     = parseInt(line.SAT_applied),
                                            SAT_date_of_assess              = datetime.strptime(line.SAT_date_of_assess, "%Y-%m-%d"),
                                            SAT_score                       = parseFloat(line.SAT_score),
                                            FEV_applied                     = parseInt(line.FEV_applied),
                                            FEV_date_of_assess              = datetime.strptime(line.FEV_date_of_assess, "%Y-%m-%d"),
                                            FEV_score                       = parseFloat(line.FEV_score),
                                            AI_applied                      = parseInt(line.AI_applied),
                                            AI_date_of_assess               = datetime.strptime(line.AI_date_of_assess, "%Y-%m-%d"),
                                            AI_score                        = parseFloat(line.AI_score),
                                            SNC_applied                     = parseInt(line.SNC_applied),
                                            SNC_date_of_assess              = datetime.strptime(line.SNC_date_of_assess, "%Y-%m-%d"),
                                            SNC_score                       = parseFloat(line.SNC_score),
                                            SCI_applied                     = parseInt(line.SCI_applied),
                                            SCI_date_of_assess              = datetime.strptime(line.SCI_date_of_assess, "%Y-%m-%d"),
                                            SCI_score                       = parseFloat(line.SCI_score),
                                            Other_applied                   = parseInt(line.Other_applied),
                                            Other_name_of                   = line.other_name_of,
                                            Other_date_of_assess            = datetime.strptime(line.Other_date_of_assess, "%Y-%m-%d"),
                                            Other_score                     = parseFloat(line.Other_score),
                                            patient_discharge_status        = parseInt(line.patient_discharge_status),
                                            discharge                       = parseInt(line.discharge),
                                            if_unplanned                    = parseInt(line.if_unplanned),
                                            date_of_discharge               = datetime.strptime(line.date_of_discharge, "%Y-%m-%d"),
                                            FIM_applied_discharge           = parseInt(line.FIM_applied_discharge),
                                            FIM_date_of_assess_discharge    = datetime.strptime(line.FIM_date_of_assess_discharge, "%Y-%m-%d"),
                                            FIM_score_discharge             = parseFloat(line.FIM_score_discharge),
                                            BI_applied_discharge            = parseInt(line.BI_applied_discharge),
                                            BI_date_of_assess_discharge     = datetime.strptime(line.BI_date_of_assess_discharge, "%Y-%m-%d"),
                                            BI_score_discharge              = parseFloat(line.BI_score_discharge),
                                            SMWT_applied_discharge          = parseInt(line.SMWT_applied_discharge),
                                            SMWT_date_of_assess_discharge   = datetime.strptime(line.SMWT_date_of_assess_discharge, "%Y-%m-%d"),
                                            SMWT_score_discharge            = parseFloat(line.SMWT_score_discharge),
                                            SF_applied_discharge            = parseInt(line.SF_applied_discharge),
                                            SF_date_of_assess_discharge     = datetime.strptime(line.SF_date_of_assess_discharge, "%Y-%m-%d"),
                                            SF_score_discharge              = parseFloat(line.SF_score_discharge),
                                            SAT_applied_discharge           = parseInt(line.SAT_applied_discharge),
                                            SAT_date_of_assess_discharge    = datetime.strptime(line.SAT_date_of_assess_discharge, "%Y-%m-%d"),
                                            SAT_score_discharge             = parseFloat(line.SAT_score_discharge),
                                            FEV_applied_discharge           = parseInt(line.FEV_applied_discharge),
                                            FEV_date_of_assess_discharge    = datetime.strptime(line.FEV_date_of_assess_discharge, "%Y-%m-%d"),
                                            FEV_score_discharge             = parseFloat(line.FEV_score_discharge),
                                            AI_applied_discharge            = parseInt(line.AI_applied_discharge),
                                            AI_date_of_assess_discharge     = datetime.strptime(line.AI_date_of_assess_discharge, "%Y-%m-%d"),
                                            AI_score_discharge              = parseFloat(line.AI_score_discharge),
                                            SNC_applied_discharge           = parseInt(line.SNC_applied_discharge),
                                            SNC_date_of_assess_discharge    = datetime.strptime(line.SNC_date_of_assess_discharge, "%Y-%m-%d"),
                                            SNC_score_discharge             = parseFloat(line.SNC_score_discharge),
                                            SCI_applied_discharge           = parseInt(line.SCI_applied_discharge),
                                            SCI_date_of_assess_discharge    = datetime.strptime(line.SCI_date_of_assess_discharge, "%Y-%m-%d"),
                                            SCI_score_discharge             = parseFloat(line.SCI_score_discharge),
                                            Other_applied_discharge         = parseInt(line.Other_applied_discharge),
                                            Other_name_of_discharge         = line.Other_name_of_discharge,
                                            Other_date_of_assess_discharge  = datetime.strptime(line.Other_date_of_assess_discharge, "%Y-%m-%d"),
                                            Other_score_discharge           = parseFloat(line.Other_score_discharge),
                                            added_by                        = request.user,
                )
                new_r1.save()
            except IntegrityError:
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('r1_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    r1a_countable_case=r1a_uncountable_case=r1b_countable_case=r1b_uncountable_case=r2_countable_case=r2_uncountable_case=()
    cases = r1.objects.all()
    for case in cases:
        if case.patient_discharge_status == 1 and case.discharge == 0:
            r2_countable_case += (case,)
        else:
            r2_uncountable_case += (case,)
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
        if (case.FIM_date_of_assess - case.date_of_admission).days < 7 or (case.BI_date_of_assess - case.date_of_admission).days < 7 or (case.SMWT_date_of_assess - case.date_of_admission).days < 7 or (case.SF_date_of_assess - case.date_of_admission).days < 7 or (case.SAT_date_of_assess - case.date_of_admission).days < 7 or (case.FEV_date_of_assess - case.date_of_admission).days < 7 or (case.AI_date_of_assess - case.date_of_admission).days < 7 or (case.SNC_date_of_assess - case.date_of_admission).days < 7 or (case.SCI_date_of_assess - case.date_of_admission).days < 7 or (case.Other_date_of_assess - case.date_of_admission).days < 7:
            r1a_first_indicator += 1
        if (case.FIM_date_of_assess - case.date_of_admission).days < 2 or (case.BI_date_of_assess - case.date_of_admission).days < 2 or (case.SMWT_date_of_assess - case.date_of_admission).days < 2 or (case.SF_date_of_assess - case.date_of_admission).days < 2 or (case.SAT_date_of_assess - case.date_of_admission).days < 2 or (case.FEV_date_of_assess - case.date_of_admission).days < 2 or (case.AI_date_of_assess - case.date_of_admission).days < 2 or (case.SNC_date_of_assess - case.date_of_admission).days < 2 or (case.SCI_date_of_assess - case.date_of_admission).days < 2 or (case.Other_date_of_assess - case.date_of_admission).days < 2:
            r1a_second_indicator += 1
        if (case.FIM_date_of_assess - case.date_of_admission).days < 3 or (case.BI_date_of_assess - case.date_of_admission).days < 3 or (case.SMWT_date_of_assess - case.date_of_admission).days < 3 or (case.SF_date_of_assess - case.date_of_admission).days < 3 or (case.SAT_date_of_assess - case.date_of_admission).days < 3 or (case.FEV_date_of_assess - case.date_of_admission).days < 3 or (case.AI_date_of_assess - case.date_of_admission).days < 3 or (case.SNC_date_of_assess - case.date_of_admission).days < 3 or (case.SCI_date_of_assess - case.date_of_admission).days < 3 or (case.Other_date_of_assess - case.date_of_admission).days < 3:
            r1a_second_indicator += 1

    for case in r1b_countable_case:
        if (case.FIM_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.BI_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.SMWT_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.SF_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.SAT_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.FEV_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.AI_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.SNC_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.SCI_date_of_assess_discharge - case.date_of_admission).days < 4 or (case.Other_date_of_assess_discharge - case.date_of_admission).days < 4:
            r1a_first_indicator += 1
        if (case.FIM_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.BI_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.SMWT_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.SF_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.SAT_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.FEV_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.AI_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.SNC_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.SCI_date_of_assess_discharge - case.date_of_admission).days < 2 or (case.Other_date_of_assess_discharge - case.date_of_admission).days < 2:
            r1a_second_indicator += 1
        if (case.FIM_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.BI_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.SMWT_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.SF_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.SAT_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.FEV_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.AI_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.SNC_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.SCI_date_of_assess_discharge - case.date_of_admission).days < 3 or (case.Other_date_of_assess_discharge - case.date_of_admission).days < 3:
            r1a_second_indicator += 1

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

    try: r1a_first = r1a_first_indicator / len(r1a_countable_case) * 100
    except: r1a_first = 0
    try: r1a_second = r1a_second_indicator / len(r1a_countable_case) * 100
    except: r1a_second = 0
    try: r1a_third = r1a_third_indicator / len(r1a_countable_case) * 100
    except: r1a_third = 0

    try: r1b_first = r1b_first_indicator / len(r1b_countable_case) * 100
    except: r1b_first = 0
    try: r1b_second = r1b_second_indicator / len(r1b_countable_case) * 100
    except: r1b_second = 0
    try: r1b_third = r1b_third_indicator / len(r1b_countable_case) * 100
    except: r1b_third = 0

    try: r2_first = r2_first_indicator / len(r2_countable_case) * 100
    except: r2_first = 0
    try: r2_second = r2_second_indicator / len(r2_countable_case) * 100
    except: r2_second = 0
    try: r2_third = r2_third_indicator / len(r2_countable_case) * 100
    except: r2_third = 0
    try: r2_fourth = r2_fourth_indicator / len(r2_countable_case) * 100
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
    return render_to_response('r1_statistics.html', context, context_instance=RequestContext(request))

def Template(request):
    model = (
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