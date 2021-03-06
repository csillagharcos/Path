# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from report_forms.c24.forms import C24Form, FileUploadForm, TrendForm, AnonymStatForm
from report_forms.c24.models import c24, c24CSV, Medicine, diagCode
from report_forms.tools import parseInt, parseFloat, csvDump, calculate_age, DateException, csvExport
from django.utils.translation import ugettext_lazy as _
from university.models import School

@login_required
def Display(request):
    if request.method == "POST":
        form = C24Form(request.POST)
        if form.is_valid():
            new_c24 = c24.objects.create(
                case_id                         = form.cleaned_data['case_id'],
                hospital_registration_number    = form.cleaned_data['hospital_registration_number'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],
                weight_of_patient               = form.cleaned_data['weight_of_patient'],
                principal_diagnoses_code        = form.cleaned_data['principal_diagnoses_code'],
                principal_procedure_code        = form.cleaned_data['principal_procedure_code'],
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
                route_of_admin                  = form.cleaned_data['route_of_admin'],
                date_of_first_dose              = form.cleaned_data['date_of_first_dose'],
                total_dose_in_24h               = form.cleaned_data['total_dose_in_24h'],
                date_of_last_dose               = form.cleaned_data['date_of_last_dose'],
                date_of_wound_close             = form.cleaned_data['date_of_wound_close'],
                added_by                        = request.user,
            )
            new_c24.save()
            return render_to_response('c24_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C24Form(request.POST)
            return render(request, 'c24.html', { 'form': form, 'medicines': Medicine.objects.all() })

    form = C24Form()
    return render(request, 'c24.html', { 'form': form, 'medicines': Medicine.objects.all() })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=errors=()
        first = True
        try:
            csv_file = request.FILES['file']
            imported_csv = c24CSV.import_data(data=csv_file)
        except UnicodeDecodeError:
            return render_to_response('error.html', {"message": _("You probably forgot to delete the first row of the csv file, please recheck.") }, context_instance=RequestContext(request))
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            try:
                try: si = datetime.strptime(line.surgical_incision+" "+line.surgical_incision_time, "%Y-%m-%d %H:%M")
                except ValueError: raise DateException(_("Date format is unaccaptable! YYYY-MM-DD is the only acceptable format."))
                try: dofd = datetime.strptime(line.date_of_first_dose+" "+line.time_of_first_dose, "%Y-%m-%d %H:%M")
                except ValueError: raise DateException(_("Date format is unaccaptable! YYYY-MM-DD is the only acceptable format."))
                try: dold =datetime.strptime(line.date_of_last_dose+" "+line.time_of_last_dose, "%Y-%m-%d %H:%M")
                except ValueError: raise DateException(_("Date format is unaccaptable! YYYY-MM-DD is the only acceptable format."))
                try: dowc =datetime.strptime(line.date_of_wound_close+" "+line.time_of_wound_close, "%Y-%m-%d %H:%M")
                except ValueError: raise DateException(_("Date format is unaccaptable! YYYY-MM-DD is the only acceptable format."))
                if dofd > dold and dofd is not None and dold is not None:
                    raise DateException(_("Date of last dose happened before date of first dose!"))
                if si > dowc and si is not None and dowc is not None:
                    raise DateException(_("Can't close the wound before the incision!"))
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
                    name_of_first_dose              = line.name_of_first_dose,
                    name_of_second_dose             = line.name_of_second_dose,
                    first_dose                      = parseFloat(line.first_dose),
                    second_dose                     = parseFloat(line.second_dose),
                    route_of_admin                  = parseInt(line.route_of_admin),
                    date_of_first_dose              = dofd,
                    total_dose_in_24h               = parseFloat(line.total_dose_in_24h),
                    date_of_last_dose               = dold,
                    date_of_wound_close             = dowc,
                    added_by                        = request.user,
                )
                new_c24.save()
            except IntegrityError:
                date_errors += ((line.case_id,_("This case is already in the database!")),)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.case_id,)
        if errors or date_errors:
            return render_to_response('c24_error.html', {'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c24_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c24_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    context = CountStatistics( c24.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace), True, request.LANGUAGE_CODE )
    if context:
        return render_to_response('c24_statistics.html', context, context_instance=RequestContext(request))
    else:
        return render(request, 'c24_statistics.html', {"not_enough": True})

@login_required
def Trend(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(c24.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, surgical_incision__gte = form.cleaned_data['date1a'], surgical_incision__lte = form.cleaned_data['date1b'] ), False, request.LANGUAGE_CODE )
            interval_two = CountStatistics(c24.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, surgical_incision__gte = form.cleaned_data['date2a'], surgical_incision__lte = form.cleaned_data['date2b'] ), False, request.LANGUAGE_CODE )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(c24.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, surgical_incision__gte = form.cleaned_data['date3a'], surgical_incision__lte = form.cleaned_data['date3b'] ), False, request.LANGUAGE_CODE )
            else:
                interval_three = False
            if not interval_one and not interval_two and not interval_three:
                return render(request, 'c24_statistics.html', {"not_enough": True})
            else:
                return render_to_response('c24_trend_diagram.html', { 'one': interval_one, 'two': interval_two, 'three': interval_three, 'form': form.cleaned_data }, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'c24_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'c24_trend.html', { 'form': form })

def Template(request):
    model = (
        _('Case ID'),
        _('Hospital registration number'),
        _('Date of birth'),
        _('Weight of patient'),
        _('Principal diagnosis code (ICD-10)'),
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
        _('First dose'),
        _('Second dose'),
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

@login_required
def Export(request):
    model = ((
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
                 _('First dose'),
                 _('Second dose'),
                 _('Route of administration of first dose'),
                 _('Date of first dose'),
                 _('Time of first dose'),
                 _('Total doses in 24 hours'),
                 _('Date of last dose'),
                 _('Time of last dose'),
                 _('Date of surgical wound closure'),
                 _('Time of surgical wound closure'),
                 ),)
    cases = c24.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        si   = str(case.surgical_incision).split(' ')
        dofd = str(case.date_of_first_dose).split(' ')
        dold = str(case.date_of_last_dose).split(' ')
        dswc = str(case.date_of_wound_close).split(' ')
        model += ((
                      str(case.case_id),
                      str(case.hospital_registration_number),
                      str(case.date_of_birth),
                      str(case.weight_of_patient),
                      str(case.principal_diagnoses_code),
                      str(case.principal_procedure_code),
                      str(case.procedure_planned),
                      str(case.patient_allergy),
                      str(case.generic_name_of_drug),
                      str(case.penicilin_allergy),
                      str(case.preoperative_infection),
                      str(case.type_of_infection),
                      str(si[0]),
                      str(si[1])[:-3],
                      str(case.antibiotic_given),
                      str(case.name_of_first_dose),
                      str(case.name_of_second_dose),
                      str(case.first_dose),
                      str(case.second_dose),
                      str(case.route_of_admin),
                      str(dofd[0]),
                      str(dofd[1])[:-3],
                      str(case.total_dose_in_24h),
                      str(dold[0]),
                      str(dold[1])[:-3],
                      str(dswc[0]),
                      str(dswc[1])[:-3],
                      ),)
    return csvExport(model, 'c24_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

def CountStatistics(cases, notView=True, language_code="hu"):
    ''' Query '''
    countable_case=uncountable_case=()
    medicines=()
    acceptable_diagnoses = diagCode.objects.filter( language = language_code )
    for medicine in Medicine.objects.all():
        medicines += (medicine.name,)
    for case in cases:
        exists = False
        for diag in acceptable_diagnoses:
            if case.principal_diagnoses_code in diag.code:
                exists = True
            if case.principal_procedure_code in diag.code:
                exists = True
        if exists and case.procedure_planned and calculate_age(case.date_of_birth) >= 18 and not case.preoperative_infection and not case.generic_name_of_drug in medicines:
            countable_case += (case,)
        else:
            uncountable_case += (case,)

    if len(countable_case) < 30 and notView:
        return False

    ''' Working '''
    indicator_one = indicator_twoa = indicator_twob = indicator_three = indicator_four = indicator_five = indicator_six = indicator_seven = indicator_eight = indicator_nine = indicator_ten = 0
    for case in countable_case:
        indicator_tracker = 0
        try: first_med_dose = Medicine.objects.get(name = case.name_of_first_dose).dose
        except: first_med_dose = 0
        try: second_med_dose = Medicine.objects.get(name = case.name_of_second_dose).dose
        except: second_med_dose = 0
        try: first_med_doseUnder = Medicine.objects.get(name = case.name_of_first_dose).doseUnder
        except: first_med_doseUnder = 0
        try: second_med_doseUnder = Medicine.objects.get(name = case.name_of_second_dose).doseUnder
        except: second_med_doseUnder = 0
        #indicator one
        acceptable = False
        if case.name_of_first_dose in medicines or case.name_of_second_dose in medicines:
            if (case.name_of_first_dose == "Cefazolin" or case.name_of_first_dose == "Cefuroxim" or case.name_of_first_dose == "Cefotaxim" or case.name_of_first_dose == "Ceftriaxon") and (case.name_of_second_dose == "Metronidazol" or case.name_of_second_dose == "Clindamycin"):
                indicator_one += 1
                indicator_tracker += 1
                acceptable = True
            elif (case.name_of_second_dose == "Cefazolin" or case.name_of_second_dose == "Cefuroxim" or case.name_of_second_dose == "Cefotaxim" or case.name_of_second_dose == "Ceftriaxon") and (case.name_of_first_dose == "Metronidazol" or case.name_of_first_dose == "Clindamycin"):
                indicator_one += 1
                indicator_tracker += 1
                acceptable = True
            elif case.name_of_first_dose == "Cefazolin" or case.name_of_first_dose == "Cefotaxim" or case.name_of_first_dose == "Cefuroxim" or case.name_of_first_dose == "Ceftriaxon" or case.name_of_first_dose == "Clindamycin" or case.name_of_first_dose == "Amoxy/clav":
                indicator_one += 1
                indicator_tracker += 1
                acceptable = True
            elif case.name_of_second_dose == "Cefazolin" or case.name_of_second_dose == "Cefotaxim" or case.name_of_second_dose == "Cefuroxim" or case.name_of_second_dose == "Ceftriaxon" or case.name_of_second_dose == "Clindamycin" or case.name_of_second_dose == "Amoxy/clav":
                indicator_one += 1
                indicator_tracker += 1
                acceptable = True

        #indicator two A
        if case.weight_of_patient >= 60:
            if (first_med_dose == case.first_dose or second_med_dose == case.second_dose) and acceptable:
                indicator_twoa += 1
                indicator_tracker += 1
        elif case.weight_of_patient < 60:
            if (first_med_dose == case.first_dose or second_med_dose == case.second_dose) or (first_med_doseUnder == case.first_dose or second_med_doseUnder == case.second_dose) and acceptable:
                indicator_twoa += 1
                indicator_tracker += 1

        #indicator two B
        if case.weight_of_patient >= 60:
            if first_med_dose == case.first_dose and (second_med_dose == case.second_dose or case.second_dose is None) and acceptable:
                indicator_twob += 1
        else:
            if (first_med_doseUnder == case.first_dose and second_med_doseUnder == case.second_dose) and acceptable:
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
        if indicator_tracker < 4:
            indicator_six += 1
        else:
            indicator_ten += 1

        #indicator eight
        if not case.antibiotic_given:
            indicator_eight += 1

        #indicator nine
        if case.first_dose is None: fd = 0
        else: fd = case.first_dose
        if case.second_dose is None: sd = 0
        else: sd = case.second_dose
        if case.date_of_first_dose == case.date_of_last_dose and case.total_dose_in_24h == fd + sd:
            indicator_nine += 1


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
    return context


@login_required
def AnonymStatistics(request):
    if request.method == "POST":
        form = AnonymStatForm(request.POST)
        statistics = []
        if form.is_valid():
            start = form.cleaned_data['endDate'] - timedelta(days=365)
            end = form.cleaned_data['endDate']
            workplaces = School.objects.filter(country__printable_name = request.user.get_profile().country)
            for workplace in workplaces:
                stat = CountStatistics(c24.objects.filter(added_by__personel__workplace = workplace, surgical_incision__gte = start, surgical_incision__lte = end ), False )
                if stat['counted'] >= 30:
                    statistics += [{
                        "name" : workplace.codename,
                        "statistics" : stat
                    }]
            statistics = SortAndAddCountryAverage(statistics, start, end, request.user)
            return render_to_response('c24_anon.html', {'statistics': statistics}, context_instance=RequestContext(request))
        else:
            form = AnonymStatForm(request.POST)
            return render(request, 'c24.html', { 'form': form,'benchmarking': True })
    form = AnonymStatForm()
    return render(request, 'c24.html', { 'form': form,'benchmarking': True })

def SortAndAddCountryAverage(statistics, start, end, user):
    statistics = sorted(statistics, key=lambda x: x['name'])
    hospitals = []
    countryStat = []
    statis = []
    overall = removed = counted = one = twoa = twob = three = four = five = six = seven = eight = nine = ten = 0
    for workplace in statistics:
        foundCountry = False
        hospital = School.objects.get(codename=workplace['name'])
        if not hospitals:
            hospitals += [{ 'country': hospital.country.printable_name, 'hospitals': [hospital.codename,]},]
        else:
            for hos in hospitals:
                if hos['country'] == hospital.country.printable_name:
                    hos['hospitals'] += [hospital.codename,]
                    foundCountry = True
                    break
            if not foundCountry:
                hospitals += [{ 'country': hospital.country.printable_name, 'hospitals': [hospital.codename,]},]

    for country in hospitals:
        name = country['country']
        for hospit in country['hospitals']:
            query = c24.objects.filter(added_by__personel__workplace__codename = hospit, surgical_incision__gte = start, surgical_incision__lte = end )
            statis += [CountStatistics(query, False),]
        for stat in statis:
            overall += stat['overall']
            removed += stat['removed']
            counted += stat['counted']
            one += stat['one']
            twoa += stat['twoa']
            twob += stat['twob']
            three += stat['three']
            four += stat['four']
            five += stat['five']
            six += stat['six']
            seven += stat['seven']
            eight += stat['eight']
            nine += stat['nine']
            ten += stat['ten']
        counter = len(statis)
        stat = {
            "overall": overall,
            "removed": removed,
            "counted": counted,
            "one": (one/counter),
            "twoa": (twoa/counter),
            "twob": (twob/counter),
            "three": (three/counter),
            "four": (four/counter),
            "five": (five/counter),
            "six": (six/counter),
            "seven": (seven/counter),
            "eight": (eight/counter),
            "nine": (nine/counter),
            "ten": (ten/counter),
            }
        countryStat += [{
            'name': name,
            'statistics': stat
        },]
    combined_results = countryStat + statistics
    ci = wi = 0
    coi = woi = None
    yourCountry = yourHospital = [{},]

    for result in combined_results:
        if user.get_profile().workplace.country.printable_name == result['name']:
            coi = ci
        ci += 1
    if coi is not None:
        yourCountry = combined_results.pop(coi)

    for result in combined_results:
        if user.get_profile().workplace.codename == result['name']:
            woi = wi
        wi += 1
    if woi is not None:
        yourHospital =  combined_results.pop(woi)

    if coi is not None and woi is not None:
        combined_results = [yourCountry,] + [yourHospital,] + combined_results
    elif coi is not None:
        combined_results = [yourCountry,] + combined_results
    elif woi is not None:
        combined_results = [yourHospital,] + combined_results

    return combined_results