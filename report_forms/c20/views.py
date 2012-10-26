# -*- coding: utf-8 -*-
from datetime import datetime, date
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c20.forms import C20Form, FileUploadForm
from report_forms.c20.models import c20, c20CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import parseInt, csvDump, calculate_age, DateException

@login_required
def Display(request):
    if request.method == "POST":
        form = C20Form(request.POST)
        if form.is_valid():
            new_c20 = c20.objects.create(
                case_id                         = form.cleaned_data['case_id'],
                hospital_registration_number    = form.cleaned_data['hospital_registration_number'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],
                diagnosis_code                  = form.cleaned_data['diagnosis_code'],
                type_of_unit                    = form.cleaned_data['type_of_unit'],
                patient_allergic_aspirin        = form.cleaned_data['patient_allergic_aspirin'],
                aspirin_intolerance             = form.cleaned_data['aspirin_intolerance'],
                type_of_discharge               = form.cleaned_data['type_of_discharge'],
                type_of_discharge_empty         = form.cleaned_data['type_of_discharge_empty'],
                aspirin_refusal                 = form.cleaned_data['aspirin_refusal'],
                aspirin_at_discharge            = form.cleaned_data['aspirin_at_discharge'],
                non_aspirin_platelet            = form.cleaned_data['non_aspirin_platelet'],
                date_of_discharge               = form.cleaned_data['date_of_discharge'],
                added_by                        = request.user,
            )
            new_c20.save()
            return render_to_response('c20_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C20Form(request.POST)
            return render(request, 'c20.html', { 'form': form })

    form = C20Form()
    return render(request, 'c20.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        first = True
        try:
            csv_file = request.FILES['file']
            imported_csv = c20CSV.import_data(data=csv_file)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            try:
                if datetime.strptime(line.date_of_birth, "%Y-%m-%d") > datetime.strptime(line.date_of_discharge, "%Y-%m-%d"):
                    raise DateException(_("Can't born after discharge!"))
                if parseInt(line.patient_allergic_aspirin) and not parseInt(line.aspirin_intolerance):
                    raise DateException(_("Aspirin contradiction should be yes, since patient is allergic to aspirin!"))
                new_c20 = c20.objects.create(
                                            case_id                         = parseInt(line.case_id),
                                            hospital_registration_number    = parseInt(line.hospital_registration_number),
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
                exists += (line.case_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.case_id,)
        if exists or errors:
            return render_to_response('c20_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c20_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c20_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c20.objects.all()
    for case in cases:
        error = False
        if not case.diagnosis_code == "I21" and not case.diagnosis_code == "I22":
            uncountable_case += (case,)
            error = True
        if calculate_age(case.date_of_birth) < 15:
            uncountable_case += (case,)
            error = True
        if case.type_of_discharge == 1 or case.type_of_discharge == 3 or case.type_of_discharge == 4 or case.patient_allergic_aspirin == 1 or case.aspirin_intolerance == 1 or case.aspirin_refusal == 1:
            uncountable_case += (case,)
            error = True
        if not error:
            countable_case += (case,)


    cindicator_one = cindicator_two = cindicator_three = 0
    indicator_one = indicator_two = indicator_three = 0
    ''' Working '''
    for case in countable_case:
        if case.aspirin_at_discharge == 1:
            cindicator_one += 1
        elif case.non_aspirin_platelet == 1:
            cindicator_two += 1
        if case.aspirin_at_discharge or case.non_aspirin_platelet == 1:
            cindicator_three += 1

    ''' Counting '''
    try: indicator_one = cindicator_one / len(countable_case) * 100
    except: indicator_one = 0
    try: indicator_two = float(cindicator_two / len(countable_case) * 100)
    except: indicator_one = 0
    try: indicator_three = float(cindicator_three / len(countable_case) * 100)
    except: indicator_one = 0

    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "indicator_one": indicator_one,
        "indicator_two": indicator_two,
        "indicator_three": indicator_three,
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