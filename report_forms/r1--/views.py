# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c32.forms import C32Form, FileUploadForm
from report_forms.c32.models import c32, c32CSV
from django.utils.translation import ugettext_lazy as _

@login_required
def Display(request):
    if request.method == "POST":
        form = C32Form(request.POST)
        if form.is_valid():
            new_c32 = c32.objects.create(
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
            new_c32.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C32Form(request.POST)
            return render(request, 'c32.html', { 'form': form })

    form = C32Form()
    return render(request, 'c32.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        imported_csv = c32CSV.import_data(data=csv_file)
        for line in imported_csv:
            try:
                new_c32 = c32.objects.create(
                                            patient_id                      = line.patient_id,
                                            case_id                         = line.case_id,
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_admission               = datetime.strptime(line.date_of_admission, "%Y-%m-%d"),
                                            patient_admission_status        = line.patient_admission_status,
                                            date_of_discharge               = datetime.strptime(line.date_of_discharge, "%Y-%m-%d"),
                                            patient_discharge_status        = line.patient_discharge_status,
                                            icd                             = line.icd,
                                            added_by                        = request.user,
                )
                new_c32.save()
            except IntegrityError:
                #todo: testing for fail state
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c31.html', context, context_instance=RequestContext(request))


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

def calculate_age(born, today = date.today()):
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return int(today.year - born.year - 1)
    else:
        return int(today.year - born.year)