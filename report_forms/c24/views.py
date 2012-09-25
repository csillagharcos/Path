# -*- coding: utf-8 -*-
from _sqlite3 import IntegrityError
from datetime import datetime, date
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c24.forms import C24Form, FileUploadForm
from report_forms.c24.models import c24, c24CSV, Medicine
from report_forms.tools import parseInt, parseFloat, csvDump
from django.utils.translation import ugettext_lazy as _

@login_required
def Display(request):
    if request.method == "POST":
        form = C24Form(request.POST)
        if form.is_valid():
            new_c24 = c24.objects.create(
                case_id                         = form.cleaned_data['case_id'],
                hospital_registration_number    = form.cleaned_data['hospital_registration_number'],
                date_of_birth                   = datetime.strptime(form.cleaned_data['date_of_birth'], "%Y-%m-%d"),
                weight_of_patient               = form.cleaned_data['weight_of_patient'],
                principal_diagnoses_code        = form.cleaned_data['principal_diagnoses_code'],
                principal_procedure_code        = form.cleaned_data['principal_procedure_code'],
                procedure_planned               = form.cleaned_data['procedure_planned'],
                patient_allergy                 = form.cleaned_data['patient_allergy'],
                generic_name_of_drug            = form.cleaned_data['generic_name_of_drug'],
                penicilin_allergy               = form.cleaned_data['penicilin_allergy'],
                preoperative_infection          = form.cleaned_data['preoperative_infection'],
                type_of_infection               = form.cleaned_data['type_of_infection'],
                surgical_incision               = datetime.strptime(form.cleaned_data['surgical_incision'], "%Y-%m-%d %H:%M:%S"),
                antibiotic_given                = form.cleaned_data['antibiotic_given'],
                name_of_first_dose              = form.cleaned_data['name_of_first_dose'],
                first_dose                      = form.cleaned_data['first_dose'],
                name_of_second_dose             = form.cleaned_data['name_of_second_dose'],
                second_dose                     = form.cleaned_data['second_dose'],
                name_of_other_dose              = form.cleaned_data['name_of_other_dose'],
                other_dose                      = form.cleaned_data['other_dose'],
                route_of_admin                  = form.cleaned_data['route_of_admin'],
                date_of_first_dose              = datetime.strptime(form.cleaned_data['date_of_first_dose'], "%Y-%m-%d %H:%M:%S"),
                total_dose_in_24h               = form.cleaned_data['total_dose_in_24h'],
                date_of_last_dose               = datetime.strptime(form.cleaned_data['date_of_last_dose'], "%Y-%m-%d %H:%M:%S"),
                date_of_wound_close             = datetime.strptime(form.cleaned_data['date_of_wound_close'], "%Y-%m-%d %H:%M:%S"),
                added_by                        = request.user,
            )
            new_c24.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C24Form(request.POST)
            return render(request, 'c24.html', { 'form': form })

    form = C24Form()
    return render(request, 'c24.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        exists=()
        try:
            csv_file = request.FILES['file']
            imported_csv = c24CSV.import_data(data=csv_file)
        except UnicodeDecodeError:
            return render_to_response('error.html', {"message": _("You probably forgot to delete the first row of the csv file, please recheck.") }, context_instance=RequestContext(request))
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            try:
                try: first_dose_name = Medicine.objects.get(name = line.name_of_first_dose)
                except ObjectDoesNotExist: first_dose_name = None
                try: second_dose_name = Medicine.objects.get(name = line.name_of_second_dose)
                except ObjectDoesNotExist: second_dose_name = None
                try: si = datetime.strptime(line.surgical_incision+" "+line.surgical_incision_time, "%Y-%m-%d %H:%M")
                except ValueError: si = None
                try: dofd = datetime.strptime(line.date_of_first_dose+" "+line.time_of_first_dose, "%Y-%m-%d %H:%M")
                except ValueError: dofd = None
                try: dold =datetime.strptime(line.date_of_last_dose+" "+line.time_of_last_dose, "%Y-%m-%d %H:%M")
                except ValueError: dold = None
                try: dowc =datetime.strptime(line.date_of_wound_close+" "+line.time_of_wound_close, "%Y-%m-%d %H:%M")
                except ValueError: dowc = None
                if not parseInt(line.penicilin_allergy):
                    pa = 1
                else:
                    pa = parseInt(line.penicilin_allergy)

                new_c24 = c24.objects.create(
                    case_id                         = parseInt(line.case_id),
                    hospital_registration_number    = line.hospital_registration_number,
                    date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                    weight_of_patient               = parseInt(line.weight_of_patient),
                    principal_diagnoses_code        = line.principal_diagnoses_code,
                    principal_procedure_code        = line.principal_procedure_code,
                    procedure_planned               = parseInt(line.procedure_planned),
                    patient_allergy                 = parseInt(line.patient_allergy),
                    generic_name_of_drug            = line.generic_name_of_drug,
                    penicilin_allergy               = pa,
                    preoperative_infection          = parseInt(line.preoperative_infection),
                    type_of_infection               = line.type_of_infection,
                    surgical_incision               = si,
                    antibiotic_given                = parseInt(line.antibiotic_given),
                    name_of_first_dose              = first_dose_name,
                    name_of_second_dose             = second_dose_name,
                    name_of_other_dose              = line.name_of_other_dose,
                    first_dose                      = parseFloat(line.first_dose),
                    second_dose                     = parseFloat(line.second_dose),
                    other_dose                      = parseFloat(line.other_dose),
                    route_of_admin                  = parseInt(line.route_of_admin),
                    date_of_first_dose              = dofd,
                    total_dose_in_24h               = parseFloat(line.total_dose_in_24h),
                    date_of_last_dose               = dold,
                    date_of_wound_close             = dowc,
                    added_by                        = request.user,
                )
                new_c24.save()
            except IntegrityError:
                pass
#                return HttpResponse(simplejson.dumps({"value" : "Delete the first row!"}), mimetype="application/json")
        return HttpResponse(simplejson.dumps({"value" : exists}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c24_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
#    ''' Query '''
#    countable_case=uncountable_case=()
#    cases = c1.objects.all()
#    for case in cases:
#        if case.other_diagnoses.count():
#            uncountable_case += (case,)
#        else:
#            countable_case += (case,)
#
#    ''' Working '''
#    numerator = map(float,[0,0,0,0,0,0,0,0])
#    agedenominator = [0,0,0]
#    previousdenominator = [0,0]
#    for case in countable_case:
#        age = calculate_age(case.date_of_birth)
#        if age < 20:
#            agedenominator[0] += 1
#        elif 20 <= age <= 35:
#            agedenominator[1] += 1
#        elif age < 35:
#            agedenominator[2] += 1
#        if not case.number_of_prev_deliveries:
#            previousdenominator[0] += 1
#        else:
#            previousdenominator[1] += 1
#        if case.drg_code == "671A" or case.drg_code == "671B":
#            numerator[0] += 1                                               #indicator 1
#            if not case.the_c_section:
#                numerator[1] += 1                                           #subindicator 1
#            else:
#                numerator[2] += 1                                           #subindicator 2
#            ''' Subindicator 3 '''
#            if age < 20:
#                numerator[3] += 1                                           #subindicator 3.1
#            elif 20 <= age <= 35:
#                numerator[4] += 1                                           #subindicator 3.2
#            elif age > 35:
#                numerator[5] += 1                                           #subindicator 3.3
#            ''' Subindicator 4 '''
#            if not case.number_of_prev_deliveries:
#                numerator[6] += 1                                           #subindicator 4.1
#            else:
#                numerator[7] += 1                                           #subindicator 4.2
#
#    ''' Counting '''
#    indicator_one               = numerator[0] / len(countable_case)     * 100
#    subindicator_one            = numerator[1] / len(countable_case)     * 100
#    subindicator_two            = numerator[2] / len(countable_case)     * 100
#    try:
#        subindicator_three_one  = numerator[3] / agedenominator[0]   * 100
#    except ZeroDivisionError:
#        subindicator_three_one  = 0
#
#    try:
#        subindicator_three_two  = numerator[4] / agedenominator[1]   * 100
#    except ZeroDivisionError:
#        subindicator_three_two  = 0
#
#    try:
#        subindicator_three_three= numerator[5] / agedenominator[2]   * 100
#    except ZeroDivisionError:
#        subindicator_three_three= 0
#
#    try:
#        subindicator_four_one   = numerator[6] / previousdenominator[0] * 100
#    except ZeroDivisionError:
#        subindicator_four_one   = 0
#
#    try:
#        subindicator_four_two   = numerator[7] / previousdenominator[1] * 100
#    except ZeroDivisionError:
#        subindicator_four_two   = 0
#
#    ''' Displaying '''
#    context = {
#        "overall": len(cases),
#        "removed": len(uncountable_case),
#        "counted": len(countable_case),
#        "indicator_one": indicator_one,
#        "subindicator_one": subindicator_one,
#        "subindicator_two": subindicator_two,
#        "subindicator_three_one": subindicator_three_one,
#        "subindicator_three_two": subindicator_three_two,
#        "subindicator_three_three": subindicator_three_three,
#        "subindicator_four_one": subindicator_four_one,
#        "subindicator_four_two": subindicator_four_two,
#    }
    return render_to_response('c24_statistics.html', {}, context_instance=RequestContext(request))

def Template(request):
    model = (
        _('Case ID'),
        _('Hospital registration number'),
        _('Date of birth'),
        _('Weight of patient'),
        _('Principal diagnosis code (ICD-10 or DRG)'),
        _('Principal procedure code'),
        _('Is the surgical procedure planned?'),
        _('Is patient allergic to any antibiotics suggested in the protocol?'),
        _('Generic name of antibiotic drug'),
        _('In case of allergy to penicillin, scale of severity?'),
        _('Has patient preoperative infection?'),
        _('Type of infection'),
        _('Date of surgical incision'),
        _('Time of surgical incision'),
        _('Prophylactic antibiotic given?'),
        _('Name of first dose'),
        _('Name of second dose'),
        _('Name of other dose'),
        _('First dose'),
        _('Second dose'),
        _('Other dose'),
        _('Route of administration of first dose'),
        _('Date of first dose'),
        _('Time of first dose'),
        _('Total doses in 24 hours'),
        _('Date of last dose'),
        _('Time of last dose'),
        _('Date of surgical wound closure'),
        _('Time of surgical wound closure'),
        )
    return csvDump(model, "c24")