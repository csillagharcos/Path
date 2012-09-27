# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c31.forms import C31Form, FileUploadForm
from report_forms.c31.models import c31, c31CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import calculate_age, csvDump, parseInt

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
        try:
            csv_file = request.FILES['file']
            imported_csv = c31CSV.import_data(data=csv_file)
        except UnicodeDecodeError:
            return render_to_response('error.html', {"message": _("You probably forgot to delete the first row of the csv file, please recheck.") }, context_instance=RequestContext(request))
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
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
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c31_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c31.objects.all()
    for case in cases:
        if calculate_age(case.date_of_birth, case.date_of_admission) < 18:
            uncountable_case += (case,)
        else:
            countable_case += (case,)

    ''' Working '''
    indicator_one_numerator = subindicator_one_30 = subindicator_two_2 = subindicator_one = 0
    for case in countable_case:
        if case.patient_discharge_status == 2:
            indicator_one_numerator += 1
            if (case.date_of_discharge - case.date_of_admission).days <= 2:
                subindicator_two_2 += 1
            if not case.patient_admission_status:
                subindicator_one += 1
                if (case.date_of_discharge - case.date_of_admission).days > 30:
                    subindicator_one_30 += 1

    ''' Counting '''
    try: indicator_one = float( indicator_one_numerator / len(cases) ) * 100
    except ZeroDivisionError: indicator_one = 0
    try: subindicator_one = float( subindicator_one / subindicator_one_30 ) * 100
    except ZeroDivisionError: subindicator_one = 0
    try: subindicator_two = float( subindicator_two_2 / len(cases) ) * 100
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
    return render_to_response('c31_statistics.html', context, context_instance=RequestContext(request))

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
