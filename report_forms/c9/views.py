# -*- coding: utf-8 -*-
from datetime import datetime, time
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from report_forms.c9.forms import C9_patient_Form, FileUploadForm, C9_operation_Form
from report_forms.c9.models import c9_patient, c9_operation, c9_patientCSV, c9_operationCSV
from report_forms.tools import csvDump, DateException, parseInt, getMinSec, median
from django.utils.translation import ugettext_lazy as _

@login_required
def Display_patient(request):
    if request.method == "POST":
        form = C9_patient_Form(request.POST)
        if form.is_valid():
            new_c9 = c9_patient.objects.create(
                central_operating_unit = form.cleaned_data['central_operating_unit'],
                operating_unit = form.cleaned_data['operating_unit'],
                date = form.cleaned_data['date'],
                type_of_day = form.cleaned_data['type_of_day'],
                case_number = form.cleaned_data['case_number'],
                patient_identifier = form.cleaned_data['patient_identifier'],
                patient_arrive_time = form.cleaned_data['patient_arrive_time'],
                anesthesia_start = form.cleaned_data['anesthesia_start'],
                surgery_start = form.cleaned_data['surgery_start'],
                surgery_end = form.cleaned_data['surgery_end'],
                anesthesia_end = form.cleaned_data['anesthesia_end'],
                patient_leave_time = form.cleaned_data['patient_leave_time'],
                added_by = request.user,
            )
            new_c9.save()
            return render_to_response('c9_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C9_patient_Form(request.POST)
            return render(request, 'c9.html', { 'form': form })

    form = C9_patient_Form()
    return render(request, 'c9.html', { 'form': form })

@login_required
def Display_operation(request):
    if request.method == "POST":
        form = C9_operation_Form(request.POST)
        if form.is_valid():
            new_c9 = c9_operation.objects.create(
                central_operating_unit = form.cleaned_data['central_operating_unit'],
                operating_unit = form.cleaned_data['operating_unit'],
                type_of_or = form.cleaned_data['type_of_or'],
                weekday_open_time = form.cleaned_data['weekday_open_time'],
                weekday_close_time = form.cleaned_data['weekday_close_time'],
                weekday_staffed_days = form.cleaned_data['weekday_staffed_days'],
                saturday_open_time = form.cleaned_data['saturday_open_time'],
                saturday_close_time = form.cleaned_data['saturday_close_time'],
                saturday_staffed_days = form.cleaned_data['saturday_staffed_days'],
                sunday_open_time = form.cleaned_data['sunday_open_time'],
                sunday_close_time = form.cleaned_data['sunday_close_time'],
                sunday_staffed_days = form.cleaned_data['sunday_staffed_days'],
                hygiene_category = form.cleaned_data['hygiene_category'],
                professional_field = form.cleaned_data['professional_field'],
                preparatory_room = form.cleaned_data['preparatory_room'],
                postoperative_room = form.cleaned_data['postoperative_room'],
                observation_begins = form.cleaned_data['observation_begins'],
                observation_ends = form.cleaned_data['observation_ends'],
                added_by = request.user,
            )
            new_c9.save()
            return render_to_response('c9_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C9_operation_Form(request.POST)
            return render(request, 'c9.html', { 'form': form })

    form = C9_operation_Form()
    return render(request, 'c9.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        first = True
        try:
            patients = request.FILES['patients']
            pimported_csv = c9_patientCSV.import_data(data=patients)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Patients template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        try:
            operations = request.FILES['operation_room']
            oimported_csv = c9_operationCSV.import_data(data=operations)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Operation template csv. The number of fields is different.") }, context_instance=RequestContext(request))

        for line in pimported_csv:
            if first:
                first = False
                continue
            try:
                try: anst = datetime.strptime(line.anesthesia_start, "%H:%M")
                except: anst = None
                try: sst = datetime.strptime(line.surgery_start, "%H:%M")
                except: sst = None
                try: sen = datetime.strptime(line.surgery_end, "%H:%M")
                except: sen = None
                try: anen = datetime.strptime(line.anesthesia_end, "%H:%M")
                except: anen = None
                new_c9p = c9_patient.objects.create(
                    central_operating_unit = line.central_operating_unit,
                    operating_unit = line.operating_unit,
                    date = datetime.strptime(line.date, "%Y-%m-%d"),
                    type_of_day = parseInt(line.type_of_day),
                    case_number = parseInt(line.case_number),
                    patient_identifier = line.patient_identifier,
                    patient_arrive_time = datetime.strptime(line.patient_arrive_time, "%H:%M"),
                    anesthesia_start = anst,
                    surgery_start = sst,
                    surgery_end = sen,
                    anesthesia_end = anen,
                    patient_leave_time = datetime.strptime(line.patient_leave_time, "%H:%M"),
                    added_by = request.user,
                )
                new_c9p.save()
            except IntegrityError:
                exists += (line.patient_identifier,)
            except DateException, (instance):
                date_errors += ((line.patient_identifier,instance.parameter),)
            except:
                errors += (line.patient_identifier,)
        first = True
        for line in oimported_csv:
            if first:
                first = False
                continue
            try:
                new_c9o = c9_operation.objects.create(
                    central_operating_unit = line.central_operating_unit,
                    operating_unit = line.operating_unit,
                    type_of_or = parseInt(line.type_of_or),
                    weekday_open_time = datetime.strptime(line.weekday_open_time, "%H:%M"),
                    weekday_close_time = datetime.strptime(line.weekday_close_time, "%H:%M"),
                    weekday_staffed_days = parseInt(line.weekday_staffed_days),
                    saturday_open_time = datetime.strptime(line.saturday_open_time, "%H:%M"),
                    saturday_close_time = datetime.strptime(line.saturday_close_time, "%H:%M"),
                    saturday_staffed_days = parseInt(line.saturday_staffed_days),
                    sunday_open_time = datetime.strptime(line.sunday_open_time, "%H:%M"),
                    sunday_close_time = datetime.strptime(line.sunday_close_time, "%H:%M"),
                    sunday_staffed_days = parseInt(line.sunday_staffed_days),
                    hygiene_category = parseInt(line.hygiene_category),
                    professional_field = line.professional_field,
                    preparatory_room = parseInt(line.preparatory_room),
                    postoperative_room = parseInt(line.postoperative_room),
                    observation_begins = datetime.strptime(line.observation_begins, "%Y-%m-%d"),
                    observation_ends = datetime.strptime(line.observation_ends, "%Y-%m-%d"),

                    added_by = request.user,
                )
                new_c9o.save()
            except IntegrityError:
                exists += (line.central_operating_unit,)
            except DateException, (instance):
                date_errors += ((line.central_operating_unit,instance.parameter),)
            except:
                errors += (line.central_operating_unit,)
        if exists or errors:
            return render_to_response('c9_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c9_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c9_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    raw_surgery_data=display_stats=()
    i=0
    operation_cases = c9_operation.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for ocase in operation_cases:
        tn=mk2=number_of_cases=aa2=at1=at2=0
        mk1=aa1=mka1=ame1=()
        #operating rooms
        patient_cases = c9_patient.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, central_operating_unit=ocase.central_operating_unit, operating_unit=ocase.operating_unit)
        for pcase in patient_cases:
            #operations in the same operating room
            if ocase.observation_begins <= pcase.date <= ocase.observation_ends:
                #operations in the same operating room under observation
                if pcase.type_of_day == 1:
                    current_close_time = ocase.saturday_close_time
                    current_open_time  = ocase.saturday_open_time
                elif pcase.type_of_day == 2:
                    current_close_time = ocase.sunday_close_time
                    current_open_time  = ocase.sunday_open_time
                else:
                    current_close_time = ocase.weekday_close_time
                    current_open_time  = ocase.weekday_open_time
                if current_close_time < pcase.patient_leave_time:
                    #overtime
                    tn += 1
                    patient_leave_time = current_close_time
                    at1 = (datetime.combine(datetime.today(), pcase.patient_leave_time) - datetime.combine(datetime.today(), current_close_time)).seconds / 60
                    at2 = (ocase.observation_ends - ocase.observation_begins).days
                else:
                    patient_leave_time = pcase.patient_leave_time

                try: mk1 += ( (datetime.combine(datetime.today(), patient_leave_time) - datetime.combine(datetime.today(), pcase.patient_arrive_time)).seconds / 60,)
                except: mk1 += (0,)
                try: mka1 += ( (datetime.combine(datetime.today(), pcase.surgery_end) - datetime.combine(datetime.today(), pcase.surgery_start)).seconds / 60,)
                except: mka1 += (0,)
                try: mk2 += (datetime.combine(datetime.today(), current_close_time) - datetime.combine(datetime.today(), current_open_time)).seconds / 60
                except: mk2 += 0
                try:
                    aa1 += ((datetime.combine(datetime.today(), pcase.anesthesia_end) - datetime.combine(datetime.today(), pcase.anesthesia_start)).seconds / 60,)
                    aa2 += 1
                except: aa1 += (0,)
                try: ame1 += ((datetime.combine(datetime.today(), pcase.surgery_start) - datetime.combine(datetime.today(), pcase.patient_arrive_time)).seconds / 60,)
                except: ame1 += (0,)
                number_of_cases += 1
        raw_surgery_data += ({
            "name":ocase.central_operating_unit+" "+ocase.operating_unit,
            "tn": tn,
            'mk1': mk1,
            "mk2": mk2,
            'mka1': mka1,
            'number_of_cases': number_of_cases,
            'aa1': aa1,
            'aa2': aa2,
            'ame1': ame1,
            'at1': at1,
            'at2': at2,
        },)
        i += 1

    ''' Working '''
    for operating_room in raw_surgery_data:
        try: mk  = float(sum(operating_room['mk1'])) / operating_room['mk2'] * 100
        except: mk = 0
        try: mka = float(sum(operating_room['mka1'])) / operating_room['mk2'] * 100
        except: mka = 0
        try: amt = getMinSec( float(sum(operating_room['mk1'])) / operating_room['number_of_cases'] )
        except: amt = 0
        try: mmt = getMinSec( float(median(operating_room['mk1'])) )
        except: mmt = 0
        try: aa  = getMinSec( float(sum(operating_room['aa1'])) / operating_room['aa2'] )
        except: aa = 0
        try: ma = getMinSec( float(median(operating_room['aa1'])) )
        except: ma = 0
        try: ami = getMinSec( float(sum(operating_room['mka1'])) / operating_room['number_of_cases'] )
        except: ami = 0
        try: mmi = getMinSec( float(median(operating_room['mka1'])) )
        except: mmi = 0
        try: ame = getMinSec( float(sum(operating_room['ame1'])) / operating_room['number_of_cases'] )
        except: ame = 0
        try: mme = getMinSec( float(median(operating_room['ame1'])) )
        except: mme = 0
        try: at = getMinSec( float(operating_room['at1']) / operating_room['at2'] )
        except: at = 0
        try: attn = getMinSec( float(operating_room['at1']) / operating_room['tn'] )
        except: attn = 0
        display_stats += ({
            'name': operating_room['name'],
            'tn'  : operating_room['tn'],
            'mk'  : mk,
            'mka' : mka,
            'amt' : amt,
            'mmt' : mmt,
            'aa'  : aa,
            'ma'  : ma,
            'ami' : ami,
            'mmi' : mmi,
            'ame' : ame,
            'mme' : mme,
            'at'  : at,
            'attn'  : attn,
            },)
        i += 1

    ''' Counting '''
    mk1=0
    mk2=0
    mka1=0
    mka2=0
    amt1=0
    aa1=0
    ami1=0
    ame1=0
    esetszam=0
    tn1=0
    tn2=0
    at1=0
    at2=0
    attn1=0
    attn2=0
    try: mk = float(mk1) / mk2
    except: mk=0
    try: mka = float(mka1) / mka2
    except: mka=0
    try: amt = float(amt1) / esetszam
    except: amt=0
    try: aa = float(aa1) / esetszam
    except: aa=0
    try: ami = float(ami1) / esetszam
    except: ami=0
    try: ame = float(ame1) / esetszam
    except: ame=0
    try: tn = float(tn1) / tn2
    except: tn=0
    try: at = float(at1) / at2
    except: at=0
    try: attn = float(attn1) / attn2
    except: attn=0

    ''' Displaying '''
    context = {
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "display_stats": display_stats,

    }
    return render_to_response('c9_statistics.html', context, context_instance=RequestContext(request))

def patients_Template(request):
    model = (
        _('Identifier of central operating unit'),
        _('Identifier of OR'),
        _('Date'),
        _('Type of day'),
        _('Case number'),
        _('Patient identifier'),
        _('Time patient arrives to OR'),
        _('Anesthesia start'),
        _('Surgery start'),
        _('Surgery end'),
        _('Anesthesia end'),
        _('Time patient leaves OR'),
    )
    return csvDump(model, "c9_patients")

def operation_Template(request):
    model = (
        _('Identifier of central operating unit'),
        _('Identifier of OR'),
        _('Type of OR'),
        _('Normal time of opening on weekdays'),
        _('Normal time of closing on weekdays'),
        _('Weekday number of staffed days in the observed period'),
        _('Normal time of opening on saturdays'),
        _('Normal time of closing on saturdays'),
        _('Saturday number of staffed days in the observed period'),
        _('Normal time of opening on sundays and holidays'),
        _('Normal time of closing on sundays and holidays'),
        _('Sunday/Holiday number of staffed days in the observed period'),
        _('Hygiene category of OR'),
        _('Professional field'),
        _('Preparatory room'),
        _('Post-operative observatory room'),
        _('Beginning of observational period'),
        _('End of observational period'),
    )
    return csvDump(model, "c9_operation")