# -*- coding: utf-8 -*-
from datetime import datetime, time
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from report_forms.c9.forms import C9_patient_Form, FileUploadForm, C9_operation_Form
from report_forms.c9.models import c9_patient, c9_operation, c9_patientCSV, c9_operationCSV
from report_forms.tools import csvDump, DateException, parseInt, getMinSec, median, csvExport
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
        patients=operations=False
        first = True
        try:
            patients = request.FILES['patients']
            pimported_csv = c9_patientCSV.import_data(data=patients)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Patients template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        except MultiValueDictKeyError:
            pass
        try:
            operations = request.FILES['operation_room']
            oimported_csv = c9_operationCSV.import_data(data=operations)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Operation template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        except MultiValueDictKeyError:
            pass
        if patients:
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
        if operations:
            for line in oimported_csv:
                if first:
                    first = False
                    continue
                try: saot = datetime.strptime(line.saturday_open_time, "%H:%M")
                except: saot = None
                try: sact = datetime.strptime(line.saturday_close_time, "%H:%M")
                except: sact = None
                try: suot = datetime.strptime(line.sunday_open_time, "%H:%M")
                except: suot = None
                try: suct = datetime.strptime(line.sunday_close_time, "%H:%M")
                except: suct = None
                try:
                    new_c9o = c9_operation.objects.create(
                        central_operating_unit = line.central_operating_unit,
                        operating_unit = line.operating_unit,
                        type_of_or = parseInt(line.type_of_or),
                        weekday_open_time = datetime.strptime(line.weekday_open_time, "%H:%M"),
                        weekday_close_time = datetime.strptime(line.weekday_close_time, "%H:%M"),
                        weekday_staffed_days = parseInt(line.weekday_staffed_days),
                        saturday_open_time = saot,
                        saturday_close_time = sact,
                        saturday_staffed_days = parseInt(line.saturday_staffed_days),
                        sunday_open_time = suot,
                        sunday_close_time = suct,
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
                    exists += (line.central_operating_unit+" "+line.operating_unit,)
                except DateException, (instance):
                    date_errors += ((line.central_operating_unit+" "+line.operating_unit,instance.parameter),)
                except:
                    errors += (line.central_operating_unit+" "+line.operating_unit,)
        if (date_errors or exists or errors) and (operations or patients):
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
        pdateerrors=ordateerrors=missing_fields=()
        tn=ame_ami_noc=number_of_cases=aa2=at1=0
        mk1=aa1=ami1=mka1=ame1=()
        #operating rooms
        patient_cases = c9_patient.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, central_operating_unit=ocase.central_operating_unit, operating_unit=ocase.operating_unit)
        try: mk2_sat = (datetime.combine(datetime.today(), ocase.saturday_close_time) - datetime.combine(datetime.today(), ocase.saturday_open_time)).seconds * ocase.saturday_staffed_days / 60
        except: mk2_sat = 0
        try: mk2_sun = (datetime.combine(datetime.today(), ocase.sunday_close_time) - datetime.combine(datetime.today(), ocase.sunday_open_time)).seconds * ocase.sunday_staffed_days / 60
        except: mk2_sun = 0
        try: mk2_week = (datetime.combine(datetime.today(), ocase.weekday_close_time) - datetime.combine(datetime.today(), ocase.weekday_open_time)).seconds * ocase.weekday_staffed_days / 60
        except: mk2_week = 0
        mk2 = mk2_sat + mk2_sun + mk2_week

        if not ocase.saturday_staffed_days:
            ocase.saturday_staffed_days = 0
        if not ocase.sunday_staffed_days:
            ocase.sunday_staffed_days = 0
        at2 = ocase.sunday_staffed_days + ocase.saturday_staffed_days + ocase.weekday_staffed_days
        limit = (ocase.observation_ends - ocase.observation_begins).days
        if ocase.observation_ends < ocase.observation_begins or ocase.saturday_open_time > ocase.saturday_close_time or ocase.sunday_open_time > ocase.sunday_close_time or ocase.weekday_open_time > ocase.weekday_close_time:
            ordateerrors = (ocase.central_operating_unit+" "+ocase.operating_unit,)
        for pcase in patient_cases:
            current_error = False
            if not (pcase.surgery_end and pcase.surgery_start) or pcase.patient_arrive_time > pcase.surgery_start or pcase.surgery_start > pcase.surgery_end or pcase.surgery_end > pcase.patient_leave_time:
                pdateerrors += (pcase.patient_identifier,)
                current_error = True
            #operations in the same operating room
            if ocase.observation_begins <= pcase.date <= ocase.observation_ends:
                #operations in the same operating room under observation
                if pcase.type_of_day == 1:
                    current_close_time = ocase.saturday_close_time
                    current_open_time  = ocase.saturday_open_time
                    if not current_close_time and not current_open_time:
                        missing_fields = (pcase.patient_identifier,)
                    break
                elif pcase.type_of_day == 2:
                    current_close_time = ocase.sunday_close_time
                    current_open_time  = ocase.sunday_open_time
                    if not current_close_time and not current_open_time:
                        missing_fields = (pcase.patient_identifier,)
                    break
                else:
                    current_close_time = ocase.weekday_close_time
                    current_open_time = ocase.weekday_open_time
                if current_close_time < pcase.patient_leave_time:
                    #overtime
                    tn += 1
                    patient_leave_time = current_close_time
                    at1 = (datetime.combine(datetime.today(), pcase.patient_leave_time) - datetime.combine(datetime.today(), current_close_time)).seconds / 60
                else:
                    patient_leave_time = pcase.patient_leave_time
                try:
                    if pcase.surgery_end > current_close_time:
                        mka_surgery_end = current_close_time
                    else:
                        mka_surgery_end = pcase.surgery_end
                except: mka_surgery_end = pcase.surgery_end
                if pcase.patient_arrive_time < current_close_time:
                    try: mk1 += ( (datetime.combine(datetime.today(), patient_leave_time) - datetime.combine(datetime.today(), pcase.patient_arrive_time)).seconds / 60,)
                    except: mk1 += (0,)
                    try: mka1 += ( (datetime.combine(datetime.today(), mka_surgery_end) - datetime.combine(datetime.today(), pcase.surgery_start)).seconds / 60,)
                    except: mka1 += (0,)

                try:
                    aa1 += ((datetime.combine(datetime.today(), pcase.anesthesia_end) - datetime.combine(datetime.today(), pcase.anesthesia_start)).seconds / 60,)
                    aa2 += 1
                except: aa1 += (0,)
                if not current_error:
                    try: ame1 += ((datetime.combine(datetime.today(), pcase.surgery_start) - datetime.combine(datetime.today(), pcase.patient_arrive_time)).seconds / 60,)
                    except: ame1 += (0,)
                    try: ami1 += ( (datetime.combine(datetime.today(), mka_surgery_end) - datetime.combine(datetime.today(), pcase.surgery_start)).seconds / 60,)
                    except: ami1 += (0,)
                    ame_ami_noc += 1
                number_of_cases += 1
        raw_surgery_data += ({
            "name":ocase.central_operating_unit+" "+ocase.operating_unit,
            'ordateerrors': ordateerrors,
            'pdateerrors': pdateerrors,
            "tn": tn,
            'mk1': mk1,
            "mk2": mk2,
            'mka1': mka1,
            'number_of_cases': number_of_cases,
            'ame_ami_noc': ame_ami_noc,
            'ami1': ami1,
            'limit': limit,
            'aa1': aa1,
            'aa2': aa2,
            'ame1': ame1,
            'at1': at1,
            'at2': at2,
            'missing_fields' : missing_fields,
        },)
        i += 1

    ''' Working & Counting '''
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
        try: ami = getMinSec( float(sum(operating_room['ami1'])) / operating_room['ame_ami_noc'] )
        except: ami = 0
        try: mmi = getMinSec( float(median(operating_room['ami1'])) )
        except: mmi = 0
        try: ame = getMinSec( float(sum(operating_room['ame1'])) / operating_room['ame_ami_noc'] )
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
            'cases': operating_room['limit'],
            'test': operating_room['number_of_cases'],
            'test1': operating_room['mk1'],
            'ordateerrors': operating_room['ordateerrors'],
            'pdateerrors': operating_room['pdateerrors'],
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
            'missing_fields' : operating_room['missing_fields'],
            },)
        i += 1
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

@login_required
def Exporto(request):
    model = ((
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
                 ),)
    cases = c9_operation.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.central_operating_unit),
                      str(case.operating_unit),
                      str(case.type_of_or),
                      str(case.weekday_open_time)[:-3],
                      str(case.weekday_close_time)[:-3],
                      str(case.weekday_staffed_days),
                      str(case.saturday_open_time)[:-3],
                      str(case.saturday_close_time)[:-3],
                      str(case.saturday_staffed_days),
                      str(case.sunday_open_time)[:-3],
                      str(case.sunday_close_time)[:-3],
                      str(case.sunday_staffed_days),
                      str(case.hygiene_category),
                      str(case.professional_field),
                      str(case.preparatory_room),
                      str(case.postoperative_room),
                      str(case.observation_begins),
                      str(case.observation_ends),
                      ),)
    return csvExport(model, 'c9_operation_room_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

@login_required
def Exportp(request):
    model = ((
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
                 ),)
    cases = c9_patient.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.central_operating_unit),
                      str(case.operating_unit),
                      str(case.date),
                      str(case.type_of_day),
                      str(case.case_number),
                      str(case.patient_identifier),
                      str(case.patient_arrive_time)[:-3],
                      str(case.anesthesia_start)[:-3],
                      str(case.surgery_start)[:-3],
                      str(case.surgery_end)[:-3],
                      str(case.anesthesia_end)[:-3],
                      str(case.patient_leave_time)[:-3],
                      ),)
    return csvExport(model, 'c9_patient_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))
