# -*- coding: utf-8 -*-
from datetime import datetime
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from report_forms.c1.forms import C1Form, FileUploadForm
from report_forms.c1.models import c1, c1CSV, c1OtherDiagnose
from report_forms.tools import calculate_age, csvDump
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
        exists=errors=()
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
                parsed_diagnoses=()
                print parsed_diagnoses
                new_c1 = c1.objects.create( patient_id=line.patient_id,
                                            case_id=line.case_id,
                                            date_of_birth=datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_delivery=datetime.strptime(line.date_of_delivery+' '+line.time_of_delivery, "%Y-%m-%d %H:%M"),
                                            number_of_prev_deliveries = line.number_of_prev_deliveries,
                                            number_of_prev_deliveries_by_c = line.number_of_prev_deliveries_by_c,
                                            the_c_section = line.the_c_section,
                                            weight_of_the_newborn = line.weight_of_the_newborn,
                                            mother_illness = line.mother_illness,
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
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c1_error.html', {'exists': exists, 'errors': errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c1_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c1_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c1.objects.all()
    for case in cases:
        if case.other_diagnoses.count() > 0:
            uncountable_case += (case,)
        else:
            countable_case += (case,)

    ''' Working '''
    numerator = map(float,[0,0,0,0,0,0,0,0])
    agedenominator = [0,0,0]
    previousdenominator = [0,0]
    for case in countable_case:
        age = calculate_age(case.date_of_birth)
        if age <= 20:
            agedenominator[0] += 1
        elif 20 < age < 35:
            agedenominator[1] += 1
        elif age >= 35:
            agedenominator[2] += 1
        if case.number_of_prev_deliveries == 0:
            previousdenominator[0] += 1
        elif case.number_of_prev_deliveries >= 2:
            previousdenominator[1] += 1
        if case.drg_code == "671A" or case.drg_code == "671B":
            numerator[0] += 1                                               #indicator 1
            if not case.the_c_section:
                numerator[1] += 1                                           #subindicator 1
            else:
                numerator[2] += 1                                           #subindicator 2
            ''' Subindicator 3 '''
            if age <= 20:
                numerator[3] += 1                                           #subindicator 3.1
            elif 20 < age < 35:
                numerator[4] += 1                                           #subindicator 3.2
            elif age >= 35:
                numerator[5] += 1                                           #subindicator 3.3
            ''' Subindicator 4 '''
            if case.number_of_prev_deliveries == 0:
                numerator[6] += 1                                           #subindicator 4.1
            elif case.number_of_prev_deliveries >= 2:
                numerator[7] += 1                                           #subindicator 4.2

    ''' Counting '''
    indicator_one               = numerator[0] / len(countable_case)     * 100
    subindicator_one            = numerator[1] / len(countable_case)     * 100
    subindicator_two            = numerator[2] / len(countable_case)     * 100

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