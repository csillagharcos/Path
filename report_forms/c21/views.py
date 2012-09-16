# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c21.forms import C21Form, FileUploadForm
from report_forms.c21.models import c21, c21CSV, Medicine

@login_required
def Display(request):
    if request.method == "POST":
        form = C21Form(request.POST)
        if form.is_valid():
            new_c21 = c21.objects.create(
                ### DATE TIME NINCS MÉG KÉSZ! ELSZÁLL MERT NINCS DATE TIME!
                case_id                         = form.cleaned_data['case_id'],
                hospital_registration_number    = form.cleaned_data['hospital_registration_number'],
                date_of_birth                   = datetime.strptime(form.cleaned_data['date_of_birth']),
                weight_of_patient               = form.cleaned_data['weight_of_patient'],
                principal_diagnoses_code        = form.cleaned_data['principal_diagnoses_code'],
                principal_procedure_code        = form.cleaned_data['principal_procedure_code'],
                procedure_planned               = form.cleaned_data['procedure_planned'],
                patient_allergy                 = form.cleaned_data['patient_allergy'],
                generic_name_of_drug            = form.cleaned_data['generic_name_of_drug'],
                penicilin_allergy               = form.cleaned_data['penicilin_allergy'],
                preoperative_infection          = form.cleaned_data['preoperative_infection'],
                type_of_infection               = form.cleaned_data['type_of_infection'],
                surgical_incision               = datetime.strptime(form.cleaned_data['surgical_incision']),
                antibiotic_given                = form.cleaned_data['antibiotic_given'],
                name_of_first_dose              = form.cleaned_data['name_of_first_dose'],
                first_dose                      = form.cleaned_data['first_dose'],
                name_of_second_dose             = form.cleaned_data['name_of_second_dose'],
                second_dose                     = form.cleaned_data['second_dose'],
                name_of_other_dose              = form.cleaned_data['name_of_other_dose'],
                other_dose                      = form.cleaned_data['other_dose'],
                route_of_admin                  = form.cleaned_data['route_of_admin'],
                date_of_first_dose              = datetime.strptime(form.cleaned_data['date_of_first_dose']),
                total_dose_in_24h               = form.cleaned_data['total_dose_in_24h'],
                date_of_last_dose               = datetime.strptime(form.cleaned_data['date_of_last_dose']),
                date_of_wound_close             = datetime.strptime(form.cleaned_data['date_of_wound_close']),
                added_by                        = request.user,
            )
            new_c21.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C21Form(request.POST)
            return render(request, 'c21.html', { 'form': form })

    form = C21Form()
    return render(request, 'c21.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        exists=()
        csv_file = request.FILES['file']
        imported_csv = c21CSV.import_data(data=csv_file)
        for line in imported_csv:
            try:
                new_c21 = c21.objects.create(
                    ### DATE TIME NINCS MÉG KÉSZ! ELSZÁLL MERT NINCS DATE TIME!
                    ### KÜLÖN KELL ÖSSZEADNI A DATE ÉS TIME MEZŐKET A CSV-BŐL!
                    case_id                         = parseInt(line.case_id),
                    hospital_registration_number    = line.hospital_registration_number,
                    date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                    weight_of_patient               = parseInt(line.weight_of_patient),
                    principal_diagnoses_code        = line.principal_diagnoses_code,
                    principal_procedure_code        = line.principal_procedure_code,
                    procedure_planned               = parseInt(line.procedure_planned),
                    patient_allergy                 = parseInt(line.patient_allergy),
                    generic_name_of_drug            = line.generic_name_of_drug,
                    penicilin_allergy               = parseInt(line.penicilin_allergy),
                    preoperative_infection          = parseInt(line.preoperative_infection),
                    type_of_infection               = line.type_of_infection,
                    surgical_incision               = datetime.strptime(line.surgical_incision, "%Y-%m-%d %H:%M:%S"),
                    antibiotic_given                = parseInt(line.antibiotic_given),
                    name_of_first_dose              = Medicine.objects.get(name = line.name_of_first_dose),
                    name_of_second_dose             = Medicine.objects.get(name = line.name_of_second_dose),
                    name_of_other_dose              = line.name_of_other_dose,
                    first_dose                      = float(line.first_dose),
                    second_dose                     = float(line.second_dose),
                    other_dose                      = float(line.other_dose),
                    route_of_admin                  = parseInt(line.route_of_admin),
                    date_of_first_dose              = datetime.strptime(line.date_of_first_dose, "%Y-%m-%d %H:%M:%S"),
                    total_dose_in_24h               = float(line.total_dose_in_24h),
                    date_of_last_dose               = datetime.strptime(line.date_of_last_dose, "%Y-%m-%d %H:%M:%S"),
                    date_of_wound_close             = datetime.strptime(line.date_of_wound_close, "%Y-%m-%d %H:%M:%S"),
                    added_by                        = request.user,
                )
                new_c21.save()
            except IntegrityError:
                exists += (line.case_id,)
        return HttpResponse(simplejson.dumps({"value" : exists}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c21.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    return render_to_response('base.html')
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
#    return render_to_response('statistics.html', context, context_instance=RequestContext(request))

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

def parseInt(integer):
    try:
        return int(integer)
    except ValueError:
        return ''

def parseFloat(integer):
    try:
        return float(integer)
    except ValueError:
        return ''