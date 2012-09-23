# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.r1.forms import r1Form, FileUploadForm
from report_forms.r1.models import r1, r1CSV
from report_forms.tools import parseFloat, parseInt

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
        csv_file = request.FILES['file']
        imported_csv = r1CSV.import_data(data=csv_file)
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
                #todo: testing for fail state
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('r1.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = r1.objects.all()
    for case in cases:
        pass

    ''' Working '''

    ''' Counting '''

    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
#        "indicator_one": indicator_one,
#        "subindicator_one": subindicator_one,
#        "subindicator_two": subindicator_two,
    }
    return render_to_response('r1_statistics.html', context, context_instance=RequestContext(request))