# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c31.forms import C31Form, FileUploadForm, TrendForm
from report_forms.c31.models import c31, c31CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import calculate_age, csvDump, parseInt, DateException, csvExport

@login_required
def Display(request):
    if request.method == "POST":
        form = C31Form(request.POST)
        if form.is_valid():
            new_c31 = c31.objects.create(
                patient_id                      = form.cleaned_data['patient_id'],
                case_id                         = form.cleaned_data['case_id'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],
                date_of_admission               = form.cleaned_data['date_of_admission'],
                patient_admission_status        = form.cleaned_data['patient_admission_status'],
                date_of_discharge               = form.cleaned_data['date_of_discharge'],
                patient_discharge_status        = form.cleaned_data['patient_discharge_status'],
                icd                             = form.cleaned_data['icd'],
                added_by                        = request.user,
            )
            new_c31.save()
            return render_to_response('c31_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C31Form(request.POST)
            return render(request, 'c31.html', { 'form': form })

    form = C31Form()
    return render(request, 'c31.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        first = True
        try:
            csv_file = request.FILES['file']
            imported_csv = c31CSV.import_data(data=csv_file)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            if datetime.strptime(line.date_of_birth, "%Y-%m-%d") > datetime.strptime(line.date_of_admission, "%Y-%m-%d"):
                raise DateException(_("Can't be born after admission!"))
            if datetime.strptime(line.date_of_discharge, "%Y-%m-%d") < datetime.strptime(line.date_of_admission, "%Y-%m-%d"):
                raise DateException(_("Can't be discharged before admission!"))
            try:
                new_c31 = c31.objects.create(
                                            patient_id                      = parseInt(line.patient_id),
                                            case_id                         = parseInt(line.case_id),
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_admission               = datetime.strptime(line.date_of_admission, "%Y-%m-%d"),
                                            patient_admission_status        = parseInt(line.patient_admission_status),
                                            date_of_discharge               = datetime.strptime(line.date_of_discharge, "%Y-%m-%d"),
                                            patient_discharge_status        = parseInt(line.patient_discharge_status),
                                            icd                             = line.icd,
                                            added_by                        = request.user,
                )
                new_c31.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c31_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c31_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c31_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    context = CountStatistics(c31.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace))
    return render_to_response('c31_statistics.html', context, context_instance=RequestContext(request))

@login_required
def Trend(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(c31.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date1a'], date_of_admission__lte = form.cleaned_data['date1b'] ), False )
            interval_two = CountStatistics(c31.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date2a'], date_of_admission__lte = form.cleaned_data['date2b'] ), False )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(c31.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date3a'], date_of_admission__lte = form.cleaned_data['date3b'] ), False )
            else:
                interval_three = False
            return render_to_response('c31_trend_diagram.html', { 'one': interval_one, 'two': interval_two, 'three': interval_three, 'form': form.cleaned_data }, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'c31_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'c31_trend.html', { 'form': form })

def Template(request):
    model = (
        _('Patients ID'),
        _('Case ID'),
        _('Date of birth'),
        _('Date of hospital admission'),
        _('Patient admission status'),
        _('Date of hospital discharge'),
        _('Patient discharge status'),
        _('ICD-10 at that departmental admission'),
        )
    return csvDump(model, "c31")

@login_required
def Export(request):
    model = ((
                 _('Patients ID'),
                 _('Case ID'),
                 _('Date of birth'),
                 _('Date of hospital admission'),
                 _('Patient admission status'),
                 _('Date of hospital discharge'),
                 _('Patient discharge status'),
                 _('ICD-10 at that departmental admission'),
                 ),)
    cases = c31.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.patient_id),
                      str(case.case_id),
                      str(case.date_of_birth),
                      str(case.date_of_admission),
                      str(case.patient_admission_status),
                      str(case.date_of_discharge),
                      str(case.patient_discharge_status),
                      str(case.icd),
                      ),)
    return csvExport(model, 'c31_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

def CountStatistics(cases, notView=True):
    ''' Query '''
    indicator_one_numerator = subindicator_one_30 = subindicator_two_2 = subindicator_one = 0
    countable_case=uncountable_case=()
    for case in cases:
        if calculate_age(case.date_of_birth, case.date_of_admission) < 18:
            uncountable_case += (case,)
        else:
            countable_case += (case,)

    if len(countable_case) < 60 and notView:
        return render_to_response('c31_statistics.html', {"not_enough": True })

    ''' Working '''
    for case in countable_case:
        if case.patient_discharge_status == 2 and (case.date_of_discharge - case.date_of_admission).days <= 30:
            indicator_one_numerator += 1
        if case.patient_discharge_status == 2 and (case.date_of_discharge - case.date_of_admission).days <= 30 and not case.patient_admission_status:
            subindicator_one += 1
        if not case.patient_admission_status and (case.patient_discharge_status == 0 or case.patient_discharge_status == 2):
            subindicator_one_30 += 1
        if case.patient_discharge_status == 2 and (case.date_of_discharge - case.date_of_admission).days <= 2:
            subindicator_two_2 += 1

    ''' Counting '''
    try: indicator_one = float( indicator_one_numerator ) / len(countable_case) * 100
    except ZeroDivisionError: indicator_one = 0
    try: subindicator_one = float( subindicator_one ) / float(subindicator_one_30)  * 100
    except ZeroDivisionError: subindicator_one = 0
    try: subindicator_two = float( subindicator_two_2 ) / len(countable_case) * 100
    except ZeroDivisionError: subindicator_two = 0
    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "indicator_one": indicator_one,
        "subindicator_one": subindicator_one,
        "subindicator_two": subindicator_two,
        }
    return context
