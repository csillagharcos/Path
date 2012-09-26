# -*- coding: utf-8 -*-
from datetime import datetime, date
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c8.forms import C8Form, FileUploadForm
from report_forms.c8.models import c8, c8CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import parseInt, csvDump, calculate_age, median

@login_required
def Display(request):
    if request.method == "POST":
        form = C8Form(request.POST)
        if form.is_valid():
            new_c8 = c8.objects.create(
                patient_id                      = form.cleaned_data['patient_id'],
                case_id                         = form.cleaned_data['case_id'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],
                date_of_admission               = form.cleaned_data['date_of_admission'],
                patient_admission_status        = form.cleaned_data['patient_admission_status'],
                type_of_admission               = form.cleaned_data['type_of_admission'],
                was_surgical_procedure          = form.cleaned_data['was_surgical_procedure'],
                date_of_surgical_procedure      = form.cleaned_data['date_of_surgical_procedure'],
                date_of_discharge               = form.cleaned_data['date_of_discharge'],
                patient_discharge_status        = form.cleaned_data['patient_discharge_status'],
                diagnosis_group                 = form.cleaned_data['diagnosis_group'],
                icd                             = form.cleaned_data['icd'],
                drg                             = form.cleaned_data['drg'],
                added_by                        = request.user,
            )
            new_c8.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C8Form(request.POST)
            return render(request, 'c8.html', { 'form': form })

    form = C8Form()
    return render(request, 'c8.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        try:
            csv_file = request.FILES['file']
            imported_csv = c8CSV.import_data(data=csv_file)
        except UnicodeDecodeError:
            return render_to_response('error.html', {"message": _("You probably forgot to delete the first row of the csv file, please recheck.") }, context_instance=RequestContext(request))
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            try:
                new_c8 = c8.objects.create(
                                            patient_id                      = parseInt(line.patient_id),
                                            case_id                         = parseInt(line.case_id),
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_admission               = datetime.strptime(line.date_of_admission, "%Y-%m-%d"),
                                            patient_admission_status        = parseInt(line.patient_admission_status),
                                            type_of_admission               = parseInt(line.type_of_admission),
                                            was_surgical_procedure          = parseInt(line.was_surgical_procedure),
                                            date_of_surgical_procedure      = datetime.strptime(line.date_of_surgical_procedure, "%Y-%m-%d"),
                                            date_of_discharge               = datetime.strptime(line.date_of_discharge, "%Y-%m-%d"),
                                            patient_discharge_status        = parseInt(line.patient_discharge_status),
                                            diagnosis_group                 = parseInt(line.diagnosis_group),
                                            icd                             = line.icd,
                                            drg                             = line.drg,
                                            added_by                        = request.user,
                )
                new_c8.save()
            except IntegrityError:
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c8_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c8.objects.all()
    for case in cases:
        if calculate_age(case.date_of_birth, case.date_of_admission) <= 18 or case.patient_admission_status == 1 or case.type_of_admission == 1 or case.type_of_admission == 2 or case.patient_discharge_status == 1 or case.patient_discharge_status == 3:
            uncountable_case += (case,)
        else:
            countable_case += (case,)



    ''' Working '''
    s_days = hap_days = hf_days = cabg_days = ka_days = ih_days = taa_days = c_days = v_days = ()
    sd_days = hapd_days = hfd_days = cabgd_days = kad_days = ihd_days = taad_days = cd_days = vd_days = ()
    sde_days = hapde_days = hfde_days = cabgde_days = kade_days = ihde_days = taade_days = cde_days = vde_days = ()
    s_dates = hap_dates = hf_dates = cabg_dates = ka_dates = ih_dates = taa_dates = c_dates = v_dates = ()
    for case in countable_case:
        if not case.diagnosis_group:         #Stroke
            s_days += ((case.date_of_discharge - case.date_of_admission).days,)
            s_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                sd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                sde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 1: #Hospital acquired pneumonia
            hap_days += ((case.date_of_discharge - case.date_of_admission).days,)
            hap_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                hapd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                hapde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 2: #Hip fracture
            hf_days += ((case.date_of_discharge - case.date_of_admission).days,)
            hf_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                hfd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                hfde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 3: #CABG
            cabg_days += ((case.date_of_discharge - case.date_of_admission).days,)
            cabg_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                cabgd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                cabgde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 4: #Knee arthroscopy
            ka_days += ((case.date_of_discharge - case.date_of_admission).days,)
            ka_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                kad_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                kade_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 5: #Inguinal hernia
            ih_days += ((case.date_of_discharge - case.date_of_admission).days,)
            ih_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                ihd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                ihde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 6: #Tonsillectomy and/or adenoidectomy
            taa_days += ((case.date_of_discharge - case.date_of_admission).days,)
            taa_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                taad_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                taade_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 7: #Cholecystectomy
            c_days += ((case.date_of_discharge - case.date_of_admission).days,)
            c_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                cd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                cde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)
        elif case.case.diagnosis_group == 8: #Varicose veins - stripping and ligation
            v_days += ((case.date_of_discharge - case.date_of_admission).days,)
            v_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                vd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days,)
                vde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days,)

    ''' Stroke '''
    try: s_first_date = sorted(s_dates)[0]
    except: s_first_date = 0
    try: s_last_date = sorted(s_dates, reverse=True)[0]
    except: s_last_date = 0
    try: s_avg = sum(s_days) / len(s_days)
    except: s_avg = 0
    try: s_med = median(s_days)
    except: s_med = 0
    try: sd_avg = sum(sd_days) / len(sd_days)
    except: sd_avg = 0
    try: sd_med = median(sd_days)
    except: sd_med = 0
    try: sde_avg = sum(sde_days) / len(sde_days)
    except: sde_avg = 0
    try: sde_med = median(sde_days)
    except: sde_med = 0

    ''' Hospital acquired pneumonia '''
    try: hap_first_date = sorted(hap_dates)[0]
    except: hap_first_date = 0
    try: hap_last_date = sorted(hap_dates, reverse=True)[0]
    except: hap_last_date = 0
    try: hap_avg = sum(hap_days) / len(hap_days)
    except: hap_avg = 0
    try: hap_med = median(hap_days)
    except: hap_med = 0
    try: hapd_avg = sum(hapd_days) / len(hapd_days)
    except: hapd_avg = 0
    try: hapd_med = median(hapd_days)
    except: hapd_med = 0
    try: hapde_avg = sum(hapde_days) / len(hapde_days)
    except: hapde_avg = 0
    try: hapde_med = median(hapde_days)
    except: hapde_med = 0

    ''' Hip fracture '''
    try: hf_first_date = sorted(hf_dates)[0]
    except: hf_first_date = 0
    try: hf_last_date = sorted(hf_dates, reverse=True)[0]
    except: hf_last_date = 0
    try: hf_avg = sum(hf_days) / len(hf_days)
    except: hf_avg = 0
    try: hf_med = median(hf_days)
    except: hf_med = 0
    try: hfd_avg = sum(hfd_days) / len(hfd_days)
    except: hfd_avg = 0
    try: hfd_med = median(hfd_days)
    except: hfd_med = 0
    try: hfde_avg = sum(hfde_days) / len(hfde_days)
    except: hfde_avg = 0
    try: hfde_med = median(hfde_days)
    except: hfde_med = 0
    
    ''' CABG '''
    try: cabg_first_date = sorted(cabg_dates)[0]
    except: cabg_first_date = 0
    try: cabg_last_date = sorted(cabg_dates, reverse=True)[0]
    except: cabg_last_date = 0
    try: cabg_avg = sum(cabg_days) / len(cabg_days)
    except: cabg_avg = 0
    try: cabg_med = median(cabg_days)
    except: cabg_med = 0
    try: cabgd_avg = sum(cabgd_days) / len(cabgd_days)
    except: cabgd_avg = 0
    try: cabgd_med = median(cabgd_days)
    except: cabgd_med = 0
    try: cabgde_avg = sum(cabgde_days) / len(cabgde_days)
    except: cabgde_avg = 0
    try: cabgde_med = median(cabgde_days)
    except: cabgde_med = 0
    
    ''' Knee arthroscopy '''
    try: ka_first_date = sorted(ka_dates)[0]
    except: ka_first_date = 0
    try: ka_last_date = sorted(ka_dates, reverse=True)[0]
    except: ka_last_date = 0
    try: ka_avg = sum(ka_days) / len(ka_days)
    except: ka_avg = 0
    try: ka_med = median(ka_days)
    except: ka_med = 0
    try: kad_avg = sum(kad_days) / len(kad_days)
    except: kad_avg = 0
    try: kad_med = median(kad_days)
    except: kad_med = 0
    try: kade_avg = sum(kade_days) / len(kade_days)
    except: kade_avg = 0
    try: kade_med = median(kade_days)
    except: kade_med = 0

    ''' Inguinal hernia '''
    try: ih_first_date = sorted(ih_dates)[0]
    except: ih_first_date = 0
    try: ih_last_date = sorted(ih_dates, reverse=True)[0]
    except: ih_last_date = 0
    try: ih_avg = sum(ih_days) / len(ih_days)
    except: ih_avg = 0
    try: ih_med = median(ih_days)
    except: ih_med = 0
    try: ihd_avg = sum(ihd_days) / len(ihd_days)
    except: ihd_avg = 0
    try: ihd_med = median(ihd_days)
    except: ihd_med = 0
    try: ihde_avg = sum(ihde_days) / len(ihde_days)
    except: ihde_avg = 0
    try: ihde_med = median(ihde_days)
    except: ihde_med = 0
    
    ''' Tonsillectomy and/or adenoidectomy '''
    try: taa_first_date = sorted(taa_dates)[0]
    except: taa_first_date = 0
    try: taa_last_date = sorted(taa_dates, reverse=True)[0]
    except: taa_last_date = 0
    try: taa_avg = sum(taa_days) / len(taa_days)
    except: taa_avg = 0
    try: taa_med = median(taa_days)
    except: taa_med = 0
    try: taad_avg = sum(taad_days) / len(taad_days)
    except: taad_avg = 0
    try: taad_med = median(taad_days)
    except: taad_med = 0
    try: taade_avg = sum(taade_days) / len(taade_days)
    except: taade_avg = 0
    try: taade_med = median(taade_days)
    except: taade_med = 0

    ''' Cholecystectomy '''
    try: c_first_date = sorted(c_dates)[0]
    except: c_first_date = 0
    try: c_last_date = sorted(c_dates, reverse=True)[0]
    except: c_last_date = 0
    try: c_avg = sum(c_days) / len(c_days)
    except: c_avg = 0
    try: c_med = median(c_days)
    except: c_med = 0
    try: cd_avg = sum(cd_days) / len(cd_days)
    except: cd_avg = 0
    try: cd_med = median(cd_days)
    except: cd_med = 0
    try: cde_avg = sum(cde_days) / len(cde_days)
    except: cde_avg = 0
    try: cde_med = median(cde_days)
    except: cde_med = 0

    ''' Varicose veins - stripping and ligation '''
    try: v_first_date = sorted(v_dates)[0]
    except: v_first_date = 0
    try: v_last_date = sorted(v_dates, reverse=True)[0]
    except: v_last_date = 0
    try: v_avg = sum(v_days) / len(v_days)
    except: v_avg = 0
    try: v_med = median(v_days)
    except: v_med = 0
    try: vd_avg = sum(vd_days) / len(vd_days)
    except: vd_avg = 0
    try: vd_med = median(vd_days)
    except: vd_med = 0
    try: vde_avg = sum(vde_days) / len(vde_days)
    except: vde_avg = 0
    try: vde_med = median(vde_days)
    except: vde_med = 0


    ''' Counting '''
    diagnosis = (
        (_('Stroke'), s_first_date, s_last_date, s_avg, s_med, sd_avg, sd_med, sde_avg, sde_med, len(s_days) ),
        (_('Hospital acquired pneumonia'), hap_first_date, hap_last_date, hap_avg, hap_med, hapd_avg, hapd_med, hapde_avg, hapde_med, len(hap_days)),
        (_('Hip fracture'), hf_first_date, hf_last_date, hf_avg, hf_med, hfd_avg, hfd_med, hfde_avg, hfde_med, len(hf_days)),
        (_('CABG'), cabg_first_date, cabg_last_date, cabg_avg, cabg_med, cabgd_avg, cabgd_med, cabgde_avg, cabgde_med, len(cabg_days)),
        (_('Knee arthroscopy'), ka_first_date, ka_last_date, ka_avg, ka_med, kad_avg, kad_med, kade_avg, kade_med, len(ka_days)),
        (_('Inguinal hernia'), ih_first_date, ih_last_date, ih_avg, ih_med, ihd_avg, ihd_med, ihde_avg, ihde_med, len(ih_days)),
        (_('Tonsillectomy and/or adenoidectomy'), taa_first_date, taa_last_date, taa_avg, taa_med, taad_avg, taad_med, taade_avg, taade_med, len(taa_days)),
        (_('Cholecystectomy'), c_first_date, c_last_date, c_avg, c_med, cd_avg, cd_med, cde_avg, cde_med, len(c_days)),
        (_('Varicose veins - stripping and ligation'), v_first_date, v_last_date, v_avg, v_med, vd_avg, vd_med, vde_avg, vde_med, len(v_days)),
        )
    quantity = (2,0,0,0,0,0,0,0,0)
    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "diagnosis": diagnosis
    }
    return render_to_response('c8_statistics.html', context, context_instance=RequestContext(request))

def Template(request):
    model = (
        _('Patients ID'),
        _('Case ID'),
        _('Date of birth'),
        _('Date of hospital admission'),
        _('Patient admission status'),
        _('Type of admission'),
        _('Was surgical procedure?'),
        _('Date of first surgical procedure'),
        _('Date of hospital discharge'),
        _('Patient discharge status'),
        _('Diagnosis group'),
        _('Diagnosis code: ICD-10'),
        _('Diagnosis code: DRG'),
        )
    return csvDump(model, "c8")