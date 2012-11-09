# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from unidecode import unidecode
from report_forms.c1.forms import C1Form, FileUploadForm
from report_forms.c1.models import c1, c1CSV, c1OtherDiagnose
from report_forms.tools import calculate_age, csvDump, DateException, parseInt, parseFloat, csvExport
from django.utils.translation import ugettext_lazy as _

@login_required
def Display(request):
    if request.method == "POST":
        form = C1Form(request.POST)
        if form.is_valid():
            new_c1 = c1.objects.create(patient_id=form.cleaned_data['patient_id'],
                case_id=form.cleaned_data['case_id'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                date_of_delivery=form.cleaned_data['date_of_delivery'],
                number_of_prev_deliveries = form.cleaned_data['number_of_prev_deliveries'],
                number_of_prev_deliveries_by_c = form.cleaned_data['number_of_prev_deliveries_by_c'],
                the_c_section = form.cleaned_data['the_c_section'],
                weight_of_the_newborn = form.cleaned_data['weight_of_the_newborn'],
                mother_illness = form.cleaned_data['mother_illness'],
                specify_mother_illness = form.cleaned_data['specify_mother_illness'],
                drg_code = form.cleaned_data['drg_code'],
                added_by = request.user,
            )
            new_c1.save()
            return render_to_response('c1_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C1Form(request.POST)
            return render(request, 'c1.html', { 'form': form })

    form = C1Form()
    return render(request, 'c1.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        first = True
        try:
            csv_file = request.FILES['file']
            imported_csv = c1CSV.import_data(data=csv_file)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            try:
                if datetime.strptime(line.date_of_birth, "%Y-%m-%d") > datetime.strptime(line.date_of_delivery, "%Y-%m-%d"):
                    raise DateException(_("Born after date of delivery!"))
                new_c1 = c1.objects.create( patient_id=parseInt(line.patient_id),
                                            case_id=parseInt(line.case_id),
                                            date_of_birth=datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_delivery=datetime.strptime(line.date_of_delivery+' '+line.time_of_delivery, "%Y-%m-%d %H:%M"),
                                            number_of_prev_deliveries = parseInt(line.number_of_prev_deliveries),
                                            number_of_prev_deliveries_by_c = parseInt(line.number_of_prev_deliveries_by_c),
                                            the_c_section = parseInt(line.the_c_section),
                                            weight_of_the_newborn = parseFloat(line.weight_of_the_newborn),
                                            mother_illness = parseInt(line.mother_illness),
                                            specify_mother_illness = line.specify_mother_illness,
                                            drg_code = line.drg_code,
                                            added_by = request.user,
                )
                if not line.other_diagnoses == "":
                    od = line.other_diagnoses.split(",")
                    for o in od:
                        try:
                            obj = c1OtherDiagnose.objects.get(name=str(o))
                            new_c1.other_diagnoses.add(obj)
                        except ObjectDoesNotExist:
                            pass
                new_c1.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c1_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c1_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c1_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        if case.other_diagnoses.count() > 0:
            uncountable_case += (case,)
        else:
            countable_case += (case,)

    if len(countable_case) < 30:
        return render_to_response('c1_statistics.html', {"not_enough": True }, context_instance=RequestContext(request))

    ''' Working '''
    numerator = map(float,[0,0,0,0,0,0,0,0])
    agedenominator = [0,0,0]
    previousdenominator = [0,0]
    for case in countable_case:
        age = calculate_age(case.date_of_birth, case.date_of_delivery.date())
        if age < 20:
            agedenominator[0] += 1
        elif 20 <= age <= 35:
            agedenominator[1] += 1
        elif age > 35:
            agedenominator[2] += 1
        if not case.number_of_prev_deliveries:
            previousdenominator[0] += 1
        elif case.number_of_prev_deliveries >= 1:
            previousdenominator[1] += 1
        if case.drg_code == "671A" or case.drg_code == "671B":
            numerator[0] += 1                                               #indicator 1
            if not case.the_c_section:
                numerator[1] += 1                                           #subindicator 1
            else:
                numerator[2] += 1                                           #subindicator 2
            ''' Subindicator 3 '''
            if age < 20:
                numerator[3] += 1                                           #subindicator 3.1
            elif 20 <= age <= 35:
                numerator[4] += 1                                           #subindicator 3.2
            elif age > 35:
                numerator[5] += 1                                           #subindicator 3.3
            ''' Subindicator 4 '''
            if not case.number_of_prev_deliveries:
                numerator[6] += 1                                           #subindicator 4.1
            elif case.number_of_prev_deliveries >= 1:
                numerator[7] += 1                                           #subindicator 4.2

    ''' Counting '''
    try: indicator_one       = numerator[0] / len(countable_case)     * 100
    except: indicator_one    = 0
    try: subindicator_one    = numerator[1] / len(countable_case)     * 100
    except: subindicator_one = 0
    try: subindicator_two    = numerator[2] / len(countable_case)     * 100
    except: subindicator_two = 0
    try:
        subindicator_three_one  = numerator[3] / agedenominator[0]   * 100
    except ZeroDivisionError:
        subindicator_three_one  = 0

    try:
        subindicator_three_two  = numerator[4] / agedenominator[1]   * 100
    except ZeroDivisionError:
        subindicator_three_two  = 0

    try:
        subindicator_three_three= numerator[5] / agedenominator[2]   * 100
    except ZeroDivisionError:
        subindicator_three_three= 0

    try:
        subindicator_four_one   = numerator[6] / previousdenominator[0] * 100
    except ZeroDivisionError:
        subindicator_four_one   = 0

    try:
        subindicator_four_two   = numerator[7] / previousdenominator[1] * 100
    except ZeroDivisionError:
        subindicator_four_two   = 0

    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "indicator_one": indicator_one,
        "subindicator_one": subindicator_one,
        "subindicator_two": subindicator_two,
        "subindicator_three_one": subindicator_three_one,
        "subindicator_three_two": subindicator_three_two,
        "subindicator_three_three": subindicator_three_three,
        "subindicator_four_one": subindicator_four_one,
        "subindicator_four_two": subindicator_four_two,
    }
    return render_to_response('c1_statistics.html', context, context_instance=RequestContext(request))

def Template(request):
    model = (
        _('Patients ID'),
        _('Case ID'),
        _('Date of birth'),
        _('Date of delivery'),
        _('Time of delivery'),
        _('Number of previous deliveries'),
        _('Number of earlier deliveries by c-section'),
        _('The c-section'),
        _('Weight of newborn'),
        _('Mother illnes or risk'),
        _('Specify'),
        _('DRG Code'),
        _('Other diagnoses'),
        )
    return csvDump(model, "c1")

@login_required
def Export(request):
    model = ((
        _('Patients ID'),
        _('Case ID'),
        _('Date of birth'),
        _('Date of delivery'),
        _('Time of delivery'),
        _('Number of previous deliveries'),
        _('Number of earlier deliveries by c-section'),
        _('The c-section'),
        _('Weight of newborn'),
        _('Mother illnes or risk'),
        _('Specify'),
        _('DRG Code'),
        _('Other diagnoses'),
    ),)
    cases = c1.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        dob = str(case.date_of_delivery).split(' ')
        od = ""
        for other_diag in case.other_diagnoses.all():
            od += str(other_diag.name)+","
        model += ((str(case.patient_id), str(case.case_id), str(case.date_of_birth), str(dob[0]), str(dob[1])[:-3], str(case.number_of_prev_deliveries), str(case.number_of_prev_deliveries_by_c), str(case.the_c_section), str(case.weight_of_the_newborn), str(case.mother_illness), str(case.specify_mother_illness), str(case.drg_code), str(od)),)
    return csvExport(model, 'c1_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))
