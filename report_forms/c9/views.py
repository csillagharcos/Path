# -*- coding: utf-8 -*-
from datetime import datetime
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from report_forms.c9.forms import C9_patient_Form, FileUploadForm, C9_operation_Form
from report_forms.c9.models import c9_patient, c9_operation, c9_patientCSV, c9_operationCSV
from report_forms.tools import csvDump, DateException, parseInt
from django.utils.translation import ugettext_lazy as _

@login_required
def Display_patient(request):
    if request.method == "POST":
        form = C9_patient_Form(request.POST)
        if form.is_valid():
            new_c9 = c9_patient.objects.create(
                operating_unit = form.cleaned_data['operating_unit'],
                date = form.cleaned_data['date'],
                case_number = form.cleaned_data['case_number'],
                patient_identifier = form.cleaned_data['patient_identifier'],
                patient_arrive_time = form.cleaned_data['patient_arrive_time'],
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
                new_c9p = c9_patient.objects.create(
                    operating_unit = line.operating_unit,
                    date = datetime.strptime(line.date, "%Y-%m-%d"),
                    case_number = parseInt(line.case_number),
                    patient_identifier = line.patient_identifier,
                    patient_arrive_time = datetime.strptime(line.patient_arrive_time, "%H:%M"),
                    patient_leave_time = datetime.strptime(line.patient_leave_time, "%H:%M"),
                    added_by = request.user,
                )
                new_c9p.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)

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
                    weekday_staffed_days = datetime.strptime(line.weekday_staffed_days, "%H:%M"),
                    saturday_open_time = datetime.strptime(line.saturday_open_time, "%H:%M"),
                    saturday_close_time = datetime.strptime(line.saturday_close_time, "%H:%M"),
                    saturday_staffed_days = datetime.strptime(line.saturday_staffed_days, "%H:%M"),
                    sunday_open_time = datetime.strptime(line.sunday_open_time, "%H:%M"),
                    sunday_close_time = datetime.strptime(line.sunday_close_time, "%H:%M"),
                    sunday_staffed_days = datetime.strptime(line.sunday_staffed_days, "%H:%M"),
                    hygiene_category = parseInt(line.hygiene_category),
                    professional_field = line.professional_field,
                    preparatory_room = parseInt(line.preparatory_room),
                    postoperative_room = parseInt(line.postoperative_room),
                    added_by = request.user,
                )
                new_c9o.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c9_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c1_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c9_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    patient_cases = c9_patient.objects.all()
    operation_cases = c9_operation.objects.all()

    ''' Working '''

    ''' Counting '''

    ''' Displaying '''
    context = {
        "removed": len(uncountable_case),
        "counted": len(countable_case),
    }
    return render_to_response('c9_statistics.html', context, context_instance=RequestContext(request))

def patients_Template(request):
    model = (
        _('Identifier of operating unit or operating rooms'),
        _('Date'),
        _('Case number'),
        _('Patient identifier'),
        _('Time patient arrives to OR'),
        _('Time patient leaves OR'),
    )
    return csvDump(model, "c9_patients")

def operation_Template(request):
    model = (
        _('Identifier of central operating unit'),
        _('Identifier of OR'),
        _('Type of OR'),
        _('Weekday normal time of opening'),
        _('Weekday normal time of closing'),
        _('Weekday number of staffed days in the observed period'),
        _('Saturday normal time of opening'),
        _('Saturday normal time of closing'),
        _('Saturday number of staffed days in the observed period'),
        _('Sunday/Holiday normal time of opening'),
        _('Sunday/Holiday normal time of closing'),
        _('Sunday/Holiday number of staffed days in the observed period'),
        _('Hygiene category of OR'),
        _('Professional field'),
        _('Preparatory room'),
        _('Post-operative observatory room'),
    )
    return csvDump(model, "c9_operation")