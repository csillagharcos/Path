# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from csvImporter.model import CsvDataException
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c32.forms import C32Form, FileUploadForm, TrendForm, AnonymStatForm
from report_forms.c32.models import c32, c32CSV
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import calculate_age, parseInt, csvDump, DateException, csvExport
from university.models import School

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
            return render_to_response('c32_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C32Form(request.POST)
            return render(request, 'c32.html', { 'form': form })

    form = C32Form()
    return render(request, 'c32.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        date_errors=exists=errors=()
        first = True
        try:
            csv_file = request.FILES['file']
            imported_csv = c32CSV.import_data(data=csv_file)
        except CsvDataException:
            return render_to_response('error.html', {"message": _("You are not using the Template csv. The number of fields is different.") }, context_instance=RequestContext(request))
        for line in imported_csv:
            if first:
                first = False
                continue
            if datetime.strptime(line.date_of_birth, "%Y-%m-%d") > datetime.strptime(line.date_of_admission, "%Y-%m-%d"):
                raise DateException(_("Can't be born after admission!"))
            if datetime.strptime(line.date_of_discharge, "%Y-%m-%d") < datetime.strptime(line.date_of_admission, "%Y-%m-%d"):
                raise DateException(_("Can't be discharged before admission!"))
            try:
                new_c32 = c32.objects.create(
                                            patient_id                      = parseInt(line.patient_id),
                                            case_id                         = parseInt(line.case_id),
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_admission               = datetime.strptime(line.date_of_admission, "%Y-%m-%d"),
                                            patient_admission_status        = parseInt(line.patient_admission_status),
                                            date_of_discharge               = datetime.strptime(line.date_of_discharge, "%Y-%m-%d"),
                                            patient_discharge_status        = parseInt(line.patient_discharge_status),
                                            icd                             = line.icd,
                                            added_by                        = request.user,
                )
                new_c32.save()
            except IntegrityError:
                exists += (line.patient_id,)
            except DateException, (instance):
                date_errors += ((line.case_id,instance.parameter),)
            except:
                errors += (line.patient_id,)
        if exists or errors:
            return render_to_response('c32_error.html', {'exists': exists, 'errors': errors, 'date_errors': date_errors}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('c32_stat'))
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c32_file_upload.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    context = CountStatistics(c32.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace))
    if context:
        return render_to_response('c32_statistics.html', context, context_instance=RequestContext(request))
    else:
        return render(request, 'c32_statistics.html', {"not_enough": True})

@login_required
def Trend(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(c32.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date1a'], date_of_admission__lte = form.cleaned_data['date1b'] ), False )
            interval_two = CountStatistics(c32.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date2a'], date_of_admission__lte = form.cleaned_data['date2b'] ), False )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(c32.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, date_of_admission__gte = form.cleaned_data['date3a'], date_of_admission__lte = form.cleaned_data['date3b'] ), False )
            else:
                interval_three = False
            return render_to_response('c32_trend_diagram.html', { 'one': interval_one, 'two': interval_two, 'three': interval_three, 'form': form.cleaned_data }, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'c32_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'c32_trend.html', { 'form': form })

def Template(request):
    model = (
        _('Patients ID'),
        _('Case ID'),
        _('Date of birth'),
        _('Date of hospital admission'),
        _('Patient admission status'),
        _('Date of hospital discharge'),
        _('Patient discharge status'),
        _('ICD-10 at that departmental admission'),
        )
    return csvDump(model, "c32")

@login_required
def Export(request):
    model = ((
                 _('Patients ID'),
                 _('Case ID'),
                 _('Date of birth'),
                 _('Date of hospital admission'),
                 _('Patient admission status'),
                 _('Date of hospital discharge'),
                 _('Patient discharge status'),
                 _('ICD-10 at that departmental admission'),
                 ),)
    cases = c32.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.patient_id),
                      str(case.case_id),
                      str(case.date_of_birth),
                      str(case.date_of_admission),
                      str(case.patient_admission_status),
                      str(case.date_of_discharge),
                      str(case.patient_discharge_status),
                      str(case.icd),
                      ),)
    return csvExport(model, 'c32_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

def CountStatistics(cases, notView=True):
    ''' Query '''
    indicator_one_numerator = subindicator_one_30 = subindicator_two_2 = subindicator_one = 0
    countable_case=uncountable_case=()
    for case in cases:
        if calculate_age(case.date_of_birth, case.date_of_admission) <= 15 and (case.icd == "I61" or case.icd == "I62" or case.icd == "I63" or case.icd == "I64"):
            uncountable_case += (case,)
        else:
            countable_case += (case,)

    if len(countable_case) < 60 and notView:
        return False

    ''' Working '''
    for case in countable_case:
        if case.patient_discharge_status == 2 and (case.date_of_discharge - case.date_of_admission).days <= 30:
            indicator_one_numerator += 1
        if case.patient_discharge_status == 2 and (case.date_of_discharge - case.date_of_admission).days <= 30 and not case.patient_admission_status:
            subindicator_one += 1
        if not case.patient_admission_status and (case.patient_discharge_status == 0 or case.patient_discharge_status == 2):
            subindicator_one_30 += 1
        if case.patient_discharge_status == 2 and (case.date_of_discharge - case.date_of_admission).days <= 2:
            subindicator_two_2 += 1

    ''' Counting '''
    try: indicator_one = float( indicator_one_numerator ) / len(countable_case) * 100
    except ZeroDivisionError: indicator_one = 0
    try: subindicator_one = float( subindicator_one ) / float(subindicator_one_30)  * 100
    except ZeroDivisionError: subindicator_one = 0
    try: subindicator_two = float( subindicator_two_2 ) / len(countable_case) * 100
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
                stat = CountStatistics(c32.objects.filter(added_by__personel__workplace = workplace, date_of_admission__gte = start, date_of_admission__lte = end ), False )
                if stat['counted'] >= 30:
                    statistics += [{
                        "name" : workplace.codename,
                        "statistics" : stat
                    }]
            statistics = SortAndAddCountryAverage(statistics, start, end, request.user)
            return render_to_response('c31_anon.html', {'statistics': statistics}, context_instance=RequestContext(request))
        else:
            form = AnonymStatForm(request.POST)
            return render(request, 'c31.html', { 'form': form,'benchmarking': True })
    form = AnonymStatForm()
    return render(request, 'c31.html', { 'form': form,'benchmarking': True })

def SortAndAddCountryAverage(statistics, start, end, user):
    statistics = sorted(statistics, key=lambda x: x['name'])
    hospitals = []
    countryStat = []
    statis = []
    overall = removed = counted = indicator_one = subindicator_one = subindicator_two = 0
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
            query = c32.objects.filter(added_by__personel__workplace__codename = hospit, date_of_admission__gte = start, date_of_admission__lte = end )
            statis += [CountStatistics(query, False),]
        for stat in statis:
            overall += stat['overall']
            removed += stat['removed']
            counted += stat['counted']
            indicator_one += stat['indicator_one']
            subindicator_one += stat['subindicator_one']
            subindicator_two += stat['subindicator_two']
        counter = len(statis)
        stat = {
            "overall": overall,
            "removed": removed,
            "counted": counted,
            "indicator_one": (indicator_one/counter),
            "subindicator_one": (subindicator_one/counter),
            "subindicator_two": (subindicator_two/counter)
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