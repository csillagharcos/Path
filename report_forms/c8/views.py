# -*- coding: utf-8 -*-
from datetime import datetime
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from report_forms.c8.forms import C8Form, FileUploadForm, TrendForm
from report_forms.c8.models import c8, c8CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import parseInt, csvDump, calculate_age, median, DateException, csvExport

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
            return render_to_response('c8_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C8Form(request.POST)
            return render(request, 'c8.html', { 'form': form })

    form = C8Form()
    return render(request, 'c8.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        first = True
        try:
            csv_file = request.FILES['file']
            imported_csv = c8CSV.import_data(data=csv_file)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            try:
                try: dob = datetime.strptime(line.date_of_birth, "%Y-%m-%d")
                except: raise DateException(_("Date field is empty!"))
                try: doa = datetime.strptime(line.date_of_admission, "%Y-%m-%d")
                except: raise DateException(_("Date field is empty!"))
                try: dosp = datetime.strptime(line.date_of_surgical_procedure, "%Y-%m-%d")
                except: raise DateException(_("Date field is empty!"))
                try: dod = datetime.strptime(line.date_of_discharge, "%Y-%m-%d")
                except: raise DateException(_("Date field is empty!"))
                if dob > doa:
                    raise DateException(_("Can't be born after admission!"))
                if dosp < doa:
                    raise DateException(_("Can't be operated before admission!"))
                if dosp > dod:
                    raise DateException(_("Can't be operated after discharge!"))
                try: dg = parseInt(line.diagnosis_group)
                except: raise DateException(_("This does not contain a number"))
                if ((dg == 0 or dg == 1 or dg == 2 or dg == 5) and not line.icd) or ((dg == 3 or dg == 4 or dg == 5 or dg == 6 or dg == 7 or dg == 8) and not line.drg):
                    raise DateException(_("Diagnosis group does not match ICD or DRG code."))
                new_c8 = c8.objects.create(
                                            patient_id                      = parseInt(line.patient_id),
                                            case_id                         = parseInt(line.case_id),
                                            date_of_birth                   = dob,
                                            date_of_admission               = doa,
                                            patient_admission_status        = parseInt(line.patient_admission_status),
                                            type_of_admission               = parseInt(line.type_of_admission),
                                            was_surgical_procedure          = parseInt(line.was_surgical_procedure),
                                            date_of_surgical_procedure      = dosp,
                                            date_of_discharge               = dod,
                                            patient_discharge_status        = parseInt(line.patient_discharge_status),
                                            diagnosis_group                 = parseInt(line.diagnosis_group),
                                            icd                             = line.icd,
                                            drg                             = line.drg,
                                            added_by                        = request.user,
                )
                new_c8.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c8_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c8_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c8_file_upload.html', context, context_instance=RequestContext(request))

@login_required
def Statistics(request):
    context = CountStatistics(c8.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace))
    return render_to_response('c8_statistics.html', context, context_instance=RequestContext(request))

@login_required
def Trend(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(c8.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date1a'], date_of_admission__lte = form.cleaned_data['date1b'] ), False )
            interval_two = CountStatistics(c8.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date2a'], date_of_admission__lte = form.cleaned_data['date2b'] ), False )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(c8.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date3a'], date_of_admission__lte = form.cleaned_data['date3b'] ), False )
                context = ZipThat(interval_one, interval_two, form.cleaned_data, interval_three)
            else:
                interval_three = False
                context = ZipThat(interval_one, interval_two,form.cleaned_data)
            return render_to_response('c8_trend_diagram.html', context, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'c8_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'c8_trend.html', { 'form': form })

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

@login_required
def Export(request):
    model = ((
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
                 ),)
    cases = c8.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.patient_id),
                      str(case.case_id),
                      str(case.date_of_birth),
                      str(case.date_of_admission),
                      str(case.patient_admission_status),
                      str(case.type_of_admission),
                      str(case.was_surgical_procedure),
                      str(case.date_of_surgical_procedure),
                      str(case.date_of_discharge),
                      str(case.patient_discharge_status),
                      str(case.diagnosis_group),
                      str(case.icd),
                      str(case.drg),
                      ),)
    return csvExport(model, 'c8_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

def CountStatistics(cases, notView=True):
    ''' Query '''
    countable_case=uncountable_case=()
    for case in cases:
        if calculate_age(case.date_of_birth, case.date_of_admission) <= 18 or case.patient_admission_status == 1 or case.type_of_admission == 1 or case.type_of_admission == 2 or case.patient_discharge_status == 1 or case.patient_discharge_status == 3:
            uncountable_case += (case,)
        else:
            if (case.diagnosis_group == 0 and (case.icd == "I61" or case.icd == "I62" or case.icd == "I63" or case.icd == "I64")) or (case.diagnosis_group == 1 and (case.icd == "J13" or case.icd == "J14" or case.icd == "J15" or case.icd == "J18" or case.icd == "A48.1")) or (case.diagnosis_group == 2 and (case.icd == "S72.0" or case.icd == "S72.1" or case.icd == "S72.2")) or (case.diagnosis_group == 3 and (case.drg == "177A" or case.drg == "177B" or case.drg == "177C" or case.drg == "177D" or case.drg == "190A" or case.drg == "192A" or case.drg == "192B")) or (case.diagnosis_group == 4 and (case.drg == "398A" or case.drg == "398B")) or (case.diagnosis_group == 5 and (case.icd == "K40" or case.drg == "281B" or case.drg == "282A" or case.drg == "282B")) or (case.diagnosis_group == 6 and case.drg == "097A") or (case.diagnosis_group == 7 and (case.drg == "344" or case.drg == "345" or case.drg == "369Z")) or (case.diagnosis_group == 8 and case.drg == "2030"):
                countable_case += (case,)
            else:
                print case.diagnosis_group
                print case.icd
                print case.drg
                print "----------------------------"
                uncountable_case += (case,)

#    if len(countable_case) < 60 and notView:
#        return render_to_response('c8_statistics.html', { "not_enough": True })

    ''' Working '''
    s_days = hap_days = hf_days = cabg_days = ka_days = ih_days = taa_days = c_days = v_days = ()
    sd_days = hapd_days = hfd_days = cabgd_days = kad_days = ihd_days = taad_days = cd_days = vd_days = ()
    sde_days = hapde_days = hfde_days = cabgde_days = kade_days = ihde_days = taade_days = cde_days = vde_days = ()
    s_dates = hap_dates = hf_dates = cabg_dates = ka_dates = ih_dates = taa_dates = c_dates = v_dates = ()
    for case in countable_case:
        if not case.diagnosis_group: #Stroke
            s_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            s_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                sd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                sde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 1: #Hospital acquired pneumonia
            hap_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            hap_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                hapd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                hapde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 2: #Hip fracture
            hf_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            hf_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                hfd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                hfde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 3: #CABG
            cabg_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            cabg_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                cabgd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                cabgde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 4: #Knee arthroscopy
            ka_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            ka_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                kad_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                kade_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 5: #Inguinal hernia
            ih_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            ih_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                ihd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                ihde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 6: #Tonsillectomy and/or adenoidectomy
            taa_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            taa_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                taad_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                taade_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 7: #Cholecystectomy
            c_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            c_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                cd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                cde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)
        elif case.diagnosis_group == 8: #Varicose veins - stripping and ligation
            v_days += ((case.date_of_discharge - case.date_of_admission).days+1,)
            v_dates += (case.date_of_admission,)
            if case.was_surgical_procedure == 1:
                vd_days += ((case.date_of_surgical_procedure - case.date_of_admission).days+1,)
                vde_days += ((case.date_of_discharge - case.date_of_surgical_procedure).days+1,)

    ''' Stroke '''
    try: s_first_date = sorted(s_dates)[0]
    except: s_first_date = 0
    try: s_last_date = sorted(s_dates, reverse=True)[0]
    except: s_last_date = 0
    try: s_avg = float(sum(s_days)) / len(s_days)
    except: s_avg = 0
    try: s_med = median(s_days)
    except: s_med = 0
    try: sd_avg = float(sum(sd_days)) / len(sd_days)
    except: sd_avg = 0
    try: sd_med = median(sd_days)
    except: sd_med = 0
    try: sde_avg = float(sum(sde_days)) / len(sde_days)
    except: sde_avg = 0
    try: sde_med = median(sde_days)
    except: sde_med = 0

    ''' Hospital acquired pneumonia '''
    try: hap_first_date = sorted(hap_dates)[0]
    except: hap_first_date = 0
    try: hap_last_date = sorted(hap_dates, reverse=True)[0]
    except: hap_last_date = 0
    try: hap_avg = float(sum(hap_days)) / len(hap_days)
    except: hap_avg = 0
    try: hap_med = median(hap_days)
    except: hap_med = 0
    try: hapd_avg = float(sum(hapd_days)) / len(hapd_days)
    except: hapd_avg = 0
    try: hapd_med = median(hapd_days)
    except: hapd_med = 0
    try: hapde_avg = float(sum(hapde_days)) / len(hapde_days)
    except: hapde_avg = 0
    try: hapde_med = median(hapde_days)
    except: hapde_med = 0

    ''' Hip fracture '''
    try: hf_first_date = sorted(hf_dates)[0]
    except: hf_first_date = 0
    try: hf_last_date = sorted(hf_dates, reverse=True)[0]
    except: hf_last_date = 0
    try: hf_avg = float(sum(hf_days)) / len(hf_days)
    except: hf_avg = 0
    try: hf_med = median(hf_days)
    except: hf_med = 0
    try: hfd_avg = float(sum(hfd_days)) / len(hfd_days)
    except: hfd_avg = 0
    try: hfd_med = median(hfd_days)
    except: hfd_med = 0
    try: hfde_avg = float(sum(hfde_days)) / len(hfde_days)
    except: hfde_avg = 0
    try: hfde_med = median(hfde_days)
    except: hfde_med = 0

    ''' CABG '''
    try: cabg_first_date = sorted(cabg_dates)[0]
    except: cabg_first_date = 0
    try: cabg_last_date = sorted(cabg_dates, reverse=True)[0]
    except: cabg_last_date = 0
    try: cabg_avg = float(sum(cabg_days)) / len(cabg_days)
    except: cabg_avg = 0
    try: cabg_med = median(cabg_days)
    except: cabg_med = 0
    try: cabgd_avg = float(sum(cabgd_days)) / len(cabgd_days)
    except: cabgd_avg = 0
    try: cabgd_med = median(cabgd_days)
    except: cabgd_med = 0
    try: cabgde_avg = float(sum(cabgde_days)) / len(cabgde_days)
    except: cabgde_avg = 0
    try: cabgde_med = median(cabgde_days)
    except: cabgde_med = 0

    ''' Knee arthroscopy '''
    try: ka_first_date = sorted(ka_dates)[0]
    except: ka_first_date = 0
    try: ka_last_date = sorted(ka_dates, reverse=True)[0]
    except: ka_last_date = 0
    try: ka_avg = float(sum(ka_days)) / len(ka_days)
    except: ka_avg = 0
    try: ka_med = median(ka_days)
    except: ka_med = 0
    try: kad_avg = float(sum(kad_days)) / len(kad_days)
    except: kad_avg = 0
    try: kad_med = median(kad_days)
    except: kad_med = 0
    try: kade_avg = float(sum(kade_days)) / len(kade_days)
    except: kade_avg = 0
    try: kade_med = median(kade_days)
    except: kade_med = 0

    ''' Inguinal hernia '''
    try: ih_first_date = sorted(ih_dates)[0]
    except: ih_first_date = 0
    try: ih_last_date = sorted(ih_dates, reverse=True)[0]
    except: ih_last_date = 0
    try: ih_avg = float(sum(ih_days)) / len(ih_days)
    except: ih_avg = 0
    try: ih_med = median(ih_days)
    except: ih_med = 0
    try: ihd_avg = float(sum(ihd_days)) / len(ihd_days)
    except: ihd_avg = 0
    try: ihd_med = median(ihd_days)
    except: ihd_med = 0
    try: ihde_avg = float(sum(ihde_days)) / len(ihde_days)
    except: ihde_avg = 0
    try: ihde_med = median(ihde_days)
    except: ihde_med = 0

    ''' Tonsillectomy and/or adenoidectomy '''
    try: taa_first_date = sorted(taa_dates)[0]
    except: taa_first_date = 0
    try: taa_last_date = sorted(taa_dates, reverse=True)[0]
    except: taa_last_date = 0
    try: taa_avg = float(sum(taa_days)) / len(taa_days)
    except: taa_avg = 0
    try: taa_med = median(taa_days)
    except: taa_med = 0
    try: taad_avg = float(sum(taad_days)) / len(taad_days)
    except: taad_avg = 0
    try: taad_med = median(taad_days)
    except: taad_med = 0
    try: taade_avg = float(sum(taade_days)) / len(taade_days)
    except: taade_avg = 0
    try: taade_med = median(taade_days)
    except: taade_med = 0

    ''' Cholecystectomy '''
    try: c_first_date = sorted(c_dates)[0]
    except: c_first_date = 0
    try: c_last_date = sorted(c_dates, reverse=True)[0]
    except: c_last_date = 0
    try: c_avg = float(sum(c_days)) / len(c_days)
    except: c_avg = 0
    try: c_med = median(c_days)
    except: c_med = 0
    try: cd_avg = float(sum(cd_days)) / len(cd_days)
    except: cd_avg = 0
    try: cd_med = median(cd_days)
    except: cd_med = 0
    try: cde_avg = float(sum(cde_days)) / len(cde_days)
    except: cde_avg = 0
    try: cde_med = median(cde_days)
    except: cde_med = 0

    ''' Varicose veins - stripping and ligation '''
    try: v_first_date = sorted(v_dates)[0]
    except: v_first_date = 0
    try: v_last_date = sorted(v_dates, reverse=True)[0]
    except: v_last_date = 0
    try: v_avg = float(sum(v_days)) / len(v_days)
    except: v_avg = 0
    try: v_med = median(v_days)
    except: v_med = 0
    try: vd_avg = float(sum(vd_days)) / len(vd_days)
    except: vd_avg = 0
    try: vd_med = median(vd_days)
    except: vd_med = 0
    try: vde_avg = float(sum(vde_days)) / len(vde_days)
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
    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "diagnosis": diagnosis
    }
    return context

def ZipThat(one,two,formStuff,three=False):
    diagnosis = []
    if three:
        for i in range(len(one['diagnosis'][0])-1):
            diagnosis += [
                {
                    'name': one['diagnosis'][i][0],
                    'startdate': [one['diagnosis'][i][1], two['diagnosis'][i][1], three['diagnosis'][i][1]],
                    'enddate': [one['diagnosis'][i][2], two['diagnosis'][i][2], three['diagnosis'][i][2]],
                    'avg': [one['diagnosis'][i][3], two['diagnosis'][i][3], three['diagnosis'][i][3]],
                    'med': [one['diagnosis'][i][4], two['diagnosis'][i][4], three['diagnosis'][i][4]],
                    'davg': [one['diagnosis'][i][5], two['diagnosis'][i][5], three['diagnosis'][i][5]],
                    'dmed': [one['diagnosis'][i][6], two['diagnosis'][i][6], three['diagnosis'][i][6]],
                    'deavg': [one['diagnosis'][i][7], two['diagnosis'][i][7], three['diagnosis'][i][7]],
                    'demed': [one['diagnosis'][i][8], two['diagnosis'][i][8], three['diagnosis'][i][8]],
                    'len': [one['diagnosis'][i][9], two['diagnosis'][i][9], three['diagnosis'][i][9]]
                },
            ]
        ZippedThat = {
            'overall': [ one['overall'], two['overall'], three['overall'] ],
            'removed': [ one['removed'], two['removed'], three['removed'] ],
            'counted': [ one['counted'], two['counted'], three['counted'] ],
            'diagnosis': diagnosis,
            'formdata': formStuff,
            }
    else:
        for i in range(len(one['diagnosis'][0])-1):
            diagnosis += [
                    {
                    'name': one['diagnosis'][i][0],
                    'startdate': [one['diagnosis'][i][1], two['diagnosis'][i][1]],
                    'enddate': [one['diagnosis'][i][2], two['diagnosis'][i][2]],
                    'avg': [one['diagnosis'][i][3], two['diagnosis'][i][3]],
                    'med': [one['diagnosis'][i][4], two['diagnosis'][i][4]],
                    'davg': [one['diagnosis'][i][5], two['diagnosis'][i][5]],
                    'dmed': [one['diagnosis'][i][6], two['diagnosis'][i][6]],
                    'deavg': [one['diagnosis'][i][7], two['diagnosis'][i][7]],
                    'demed': [one['diagnosis'][i][8], two['diagnosis'][i][8]],
                    'len': [one['diagnosis'][i][9], two['diagnosis'][i][9]]
                },
            ]
        ZippedThat = {
            'overall': [ one['overall'], two['overall'] ],
            'removed': [ one['removed'], two['removed'] ],
            'counted': [ one['counted'], two['counted'] ],
            'diagnosis': diagnosis,
            'formdata': formStuff,
        }
    return ZippedThat