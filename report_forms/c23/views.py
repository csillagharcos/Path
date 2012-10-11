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
from report_forms.c23.forms import C23Form, FileUploadForm
from report_forms.c23.models import c23, c23CSV, Medicine
from report_forms.tools import parseFloat, parseInt, csvDump, calculate_age, DateException
from django.utils.translation import ugettext_lazy as _

@login_required
def Display(request):
    if request.method == "POST":
        form = C23Form(request.POST)
        if form.is_valid():
            new_c23 = c23.objects.create(
                case_id                         = form.cleaned_data['case_id'],
                hospital_registration_number    = form.cleaned_data['hospital_registration_number'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],
                weight_of_patient               = form.cleaned_data['weight_of_patient'],
                principal_diagnoses_code        = form.cleaned_data['principal_diagnoses_code'],
                principal_procedure_code        = form.cleaned_data['principal_procedure_code'],
                principal_diagnoses_code_other  = form.cleaned_data['principal_diagnoses_code_other'],
                procedure_planned               = form.cleaned_data['procedure_planned'],
                patient_allergy                 = form.cleaned_data['patient_allergy'],
                generic_name_of_drug            = form.cleaned_data['generic_name_of_drug'],
                penicilin_allergy               = form.cleaned_data['penicilin_allergy'],
                preoperative_infection          = form.cleaned_data['preoperative_infection'],
                type_of_infection               = form.cleaned_data['type_of_infection'],
                surgical_incision               = form.cleaned_data['surgical_incision'],
                antibiotic_given                = form.cleaned_data['antibiotic_given'],
                name_of_first_dose              = form.cleaned_data['name_of_first_dose'],
                first_dose                      = form.cleaned_data['first_dose'],
                name_of_second_dose             = form.cleaned_data['name_of_second_dose'],
                second_dose                     = form.cleaned_data['second_dose'],
                name_of_other_dose              = form.cleaned_data['name_of_other_dose'],
                other_dose                      = form.cleaned_data['other_dose'],
                route_of_admin                  = form.cleaned_data['route_of_admin'],
                date_of_first_dose              = form.cleaned_data['date_of_first_dose'],
                total_dose_in_24h               = form.cleaned_data['total_dose_in_24h'],
                date_of_last_dose               = form.cleaned_data['date_of_last_dose'],
                date_of_wound_close             = form.cleaned_data['date_of_wound_close'],
                added_by                        = request.user,
            )
            new_c23.save()
            return render_to_response('c23_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C23Form(request.POST)
            return render(request, 'c23.html', { 'form': form, 'medicines': Medicine.objects.all() })

    form = C23Form()
    return render(request, 'c23.html', { 'form': form, 'medicines': Medicine.objects.all() })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=errors=exists=()
        try:
            csv_file = request.FILES['file']
            imported_csv = c23CSV.import_data(data=csv_file)
        except UnicodeDecodeError:
            return render_to_response('error.html', {"message": _("You probably forgot to delete the first row of the csv file, please recheck.") }, context_instance=RequestContext(request))
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            try:
                try: si = datetime.strptime(line.surgical_incision+" "+line.surgical_incision_time, "%Y-%m-%d %H:%M")
                except ValueError: si = None
                try: dofd = datetime.strptime(line.date_of_first_dose+" "+line.time_of_first_dose, "%Y-%m-%d %H:%M")
                except ValueError: dofd = None
                try: dold =datetime.strptime(line.date_of_last_dose+" "+line.time_of_last_dose, "%Y-%m-%d %H:%M")
                except ValueError: dold = None
                try: dowc =datetime.strptime(line.date_of_wound_close+" "+line.time_of_wound_close, "%Y-%m-%d %H:%M")
                except ValueError: dowc = None
                if dofd >= dold and dofd is not None and dold is not None:
                    raise DateException(_("Date of last dose happened before date of first dose!"))
                if si > dowc and si is not None and dowc is not None:
                    raise DateException(_("Can't close the wound before the incision!"))
                if not parseInt(line.penicilin_allergy):
                    pa = 1
                else:
                    pa = parseInt(line.penicilin_allergy)

                new_c23 = c23.objects.create(
                    case_id                         = parseInt(line.case_id),
                    hospital_registration_number    = line.hospital_registration_number,
                    date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                    weight_of_patient               = parseInt(line.weight_of_patient),
                    principal_diagnoses_code        = line.principal_diagnoses_code,
                    principal_diagnoses_code_other  = line.principal_diagnoses_code_other,
                    principal_procedure_code        = line.principal_procedure_code,
                    procedure_planned               = parseInt(line.procedure_planned),
                    patient_allergy                 = parseInt(line.patient_allergy),
                    generic_name_of_drug            = line.generic_name_of_drug,
                    penicilin_allergy               = pa,
                    preoperative_infection          = parseInt(line.preoperative_infection),
                    type_of_infection               = line.type_of_infection,
                    surgical_incision               = si,
                    antibiotic_given                = parseInt(line.antibiotic_given),
                    name_of_first_dose              = line.name_of_first_dose,
                    name_of_second_dose             = line.name_of_second_dose,
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
                new_c23.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (inst):
                date_errors += (line.patient_id,)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c23_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c23_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c23_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    accepted_diagnose_codes = ("S70.0", "S70.1", "S70.2")
    countable_case=uncountable_case=()
    cases = c23.objects.all()
    medicines=()
    for medicine in Medicine.objects.all():
        medicines += (medicine.name,)
    for case in cases:
        if case.principal_diagnoses_code in accepted_diagnose_codes and case.procedure_planned and calculate_age(case.date_of_birth) >= 18 and not case.preoperative_infection and not case.generic_name_of_drug in medicines:
            countable_case += (case,)
        else:
            uncountable_case += (case,)

    ''' Working '''
    indicator_one = indicator_twoa = indicator_twob = indicator_three = indicator_four = indicator_five = indicator_six = indicator_seven = indicator_eight = indicator_nine = indicator_ten = 0
    for case in countable_case:
        indicator_tracker = 0
        try: first_med_dose = Medicine.objects.get(name = case.name_of_first_dose).dose
        except: first_med_dose = -1
        try: second_med_dose = Medicine.objects.get(name = case.name_of_second_dose).dose
        except: second_med_dose = -1
        try: first_med_doseUnder = Medicine.objects.get(name = case.name_of_first_dose).doseUnder
        except: first_med_doseUnder = -1
        try: second_med_doseUnder = Medicine.objects.get(name = case.name_of_second_dose).doseUnder
        except: second_med_doseUnder = -1
        #indicator one
        if case.name_of_first_dose in medicines and case.name_of_second_dose in medicines:
            if case.name_of_first_dose == "Cefazolin" or case.name_of_first_dose == "Cefuroxim" or case.name_of_first_dose == "Vancomycin":
                indicator_one += 1
                indicator_tracker += 1
            elif case.name_of_second_dose == "Cefazolin" or case.name_of_second_dose == "Cefuroxim" or case.name_of_second_dose == "Cefuroxim":
                indicator_one += 1
                indicator_tracker += 1

        #indicator two A
        if first_med_dose == case.first_dose and second_med_dose == case.second_dose:
            indicator_twoa += 1
            indicator_tracker += 1

        #indicator two B
        if case.weight_of_patient > 60:
            if first_med_dose == case.first_dose and second_med_dose == case.second_dose:
                indicator_twob += 1
        else:
            if first_med_doseUnder == case.first_dose and second_med_doseUnder == case.second_dose:
                indicator_twob += 1

        #indicator three
        if case.route_of_admin == 1:
            indicator_three += 1
            indicator_tracker += 1

        #indicator four
        try:
            if (case.surgical_incision - case.date_of_first_dose).seconds <= 3600:
                indicator_four += 1
                indicator_tracker += 1
        except:
            pass

        #indicator ten
        if not indicator_tracker == 4:
            indicator_ten += 1

        #indicator five
        try:
            if (case.date_of_wound_close - case.date_of_last_dose).seconds <= 86400:
                indicator_five += 1
            #indicator seven
            else:
                indicator_seven += 1
        except:
            indicator_seven += 1

        #indicator six
        if not indicator_tracker == 4:
            indicator_six += 1

        #indicator eight
        if not case.antibiotic_given:
            indicator_eight += 1

        #indicator nine
        if case.date_of_first_dose == case.date_of_last_dose and case.total_dose_in_24h == case.first_dose + case.second_dose:
            indicator_nine += 1


    print indicator_nine
    ''' Counting '''
    try: one = float(indicator_one) / len(countable_case) * 100
    except: one = 0
    try: twoa = float(indicator_twoa) / len(countable_case) * 100
    except: twoa = 0
    try: twob = float(indicator_twob) / len(countable_case) * 100
    except: twob = 0
    try: three = float(indicator_three) / len(countable_case) * 100
    except: three = 0
    try: four = float(indicator_four) / len(countable_case) * 100
    except: four = 0
    try: five = float(indicator_five) / len(countable_case) * 100
    except: five = 0
    try: six = float(indicator_six) / len(countable_case) * 100
    except: six = 0
    try: seven = float(indicator_seven) / len(countable_case) * 100
    except: seven = 0
    try: eight = float(indicator_eight) / len(countable_case) * 100
    except: eight = 0
    try: nine = float(indicator_nine) / len(countable_case) * 100
    except: nine = 0
    try: ten = float(indicator_ten) / len(countable_case) * 100
    except: ten = 0

    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "one": one,
        "twoa": twoa,
        "twob": twob,
        "three": three,
        "four": four,
        "five": five,
        "six": six,
        "seven": seven,
        "eight": eight,
        "nine": nine,
        "ten": ten,
        }
    return render_to_response('c23_statistics.html', context, context_instance=RequestContext(request))

def Template(request):
    model = (
        _('Case ID'),
        _('Hospital registration number'),
        _('Date of birth'),
        _('Weight of patient'),
        _('Principal diagnosis code (ICD-10 or DRG)'),
        _('Other principal diagnosis code (ICD-10 or DRG)'),
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
    return csvDump(model, "c23")