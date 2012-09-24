# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c8.forms import C8Form, FileUploadForm
from report_forms.c8.models import c8, c8CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import parseInt, csvDump

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
        csv_file = request.FILES['file']
        imported_csv = c8CSV.import_data(data=csv_file)
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
                #todo: testing for fail state
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c8.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c8.objects.all()
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