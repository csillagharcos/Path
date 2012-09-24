# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c20.forms import C20Form, FileUploadForm
from report_forms.c20.models import c20, c20CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import parseInt, csvDump

@login_required
def Display(request):
    if request.method == "POST":
        form = C20Form(request.POST)
        if form.is_valid():
            new_c20 = c20.objects.create(
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
            new_c20.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C20Form(request.POST)
            return render(request, 'c20.html', { 'form': form })

    form = C20Form()
    return render(request, 'c20.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        imported_csv = c20CSV.import_data(data=csv_file)
        for line in imported_csv:
            try:
                new_c20 = c20.objects.create(
                                            patient_id                      = parseInt(line.patient_id),
                                            case_id                         = parseInt(line.case_id),
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            diagnosis_code                  = line.diagnosis_code,
                                            type_of_unit                    = parseInt(line.type_of_unit),
                                            patient_allergic_aspirin        = parseInt(line.patient_allergic_aspirin),
                                            aspirin_intolerance             = parseInt(line.aspirin_intolerance),
                                            type_of_discharge               = parseInt(line.type_of_discharge),
                                            type_of_discharge_empty         = line.type_of_discharge_empty,
                                            aspirin_refusal                 = parseInt(line.aspirin_refusal),
                                            aspirin_at_discharge            = parseInt(line.aspirin_at_discharge),
                                            non_aspirin_platelet            = parseInt(line.non_aspirin_platelet),
                                            date_of_discharge               = datetime.strptime(line.date_of_discharge, "%Y-%m-%d"),
                                            added_by                        = request.user,
                )
                new_c20.save()
            except IntegrityError:
                #todo: testing for fail state
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c20.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c20.objects.all()
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
    return render_to_response('c20_statistics.html', context, context_instance=RequestContext(request))

def Template(request):
    model = (
        _('Case ID'),
        _('Hospital registration number'),
        _('Date of birth'),
        _('Principal diagnosis code (ICD-10)'),
        _('Type of unit'),
        _('Patient allergic to aspirin?'),
        _('Is there a known contraindication or intolerance of aspirin?'),
        _('Type of discharge'),
        _('If other'),
        _('Is there a known objection/refusal to take aspirin-containing medication?'),
        _('Was patient prescribed at discharge to take aspirin?'),
        _('Was patient prescribed to take other (non-aspirin-containing) platelet aggregation inhibitor therapy?'),
        _('Date of discharge'),
        )
    return csvDump(model, "c20")