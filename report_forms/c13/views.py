# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import translation
from report_forms.c13.forms import C13Form, C13Form_hungarian, TrendForm, AnonymStatForm
from report_forms.c13.models import c13
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import csvDump, csvExport
from university.models import School

@login_required
def Display(request):
    if request.method == "POST":
        form = C13Form(request.POST)
        if form.is_valid():
            new_c13 = c13.objects.create(
                job                             = form.cleaned_data['job'],
                year                            = form.cleaned_data['year'],
                needlestick_injuries            = form.cleaned_data['needlestick_injuries'],
                staff_beginning                 = form.cleaned_data['staff_beginning'],
                staff_end                       = form.cleaned_data['staff_end'],
                working_hours_beginning         = form.cleaned_data['working_hours_beginning'],
                working_hours_end               = form.cleaned_data['working_hours_end'],
                added_by                        = request.user,
            )
            new_c13.save()
            return render_to_response('c13_filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C13Form(request.POST)
            return render(request, 'c13.html', { 'form': form })
    if request.LANGUAGE_CODE == "hu":
        form = C13Form_hungarian()
    else:
        form = C13Form()
    return render(request, 'c13.html', { 'form': form })

@login_required
def Statistics(request):
    context = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace) )
    return render_to_response('c13_statistics.html', context, context_instance=RequestContext(request))

def Trend(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            interval_one = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, year = form.cleaned_data['date1a']) )
            interval_two = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, year = form.cleaned_data['date2a']) )
            if form.cleaned_data['date3a']:
                interval_three = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, year = form.cleaned_data['date3a']) )
                context = ZipThat(interval_one, interval_two, form.cleaned_data, interval_three)
            else:
                interval_three = False
                context = ZipThat(interval_one, interval_two, form.cleaned_data)
            return render_to_response('c13_trend_diagram.html', context, context_instance=RequestContext(request))
        else:
            form = TrendForm(request.POST)
            return render(request, 'c13_trend.html', { 'form': form })
    else:
        form = TrendForm()
        return render(request, 'c13_trend.html', { 'form': form })

def Template(request):
    model = (
        _('Job'),
        _('Observed year'),
        _('Number of needle stick injuries in the observed year'),
        _('Total number of hospital staff at the beginning of the year (1st January)'),
        _('Total number of hospital staff at the end of the year (31st December)'),
        _('Total number of contracted working hours for the data at the beginning of the year/day (employee+ entrepreneur)'),
        _('Total number of contracted working hours for the data at the end of the year /day(employee+ entrepreneur)'),
        )
    return csvDump(model, "c13")

@login_required
def Export(request):
    model = ((
                 _('Job'),
                 _('Observed year'),
                 _('Number of needle stick injuries in the observed year'),
                 _('Total number of hospital staff at the beginning of the year (1st January)'),
                 _('Total number of hospital staff at the end of the year (31st December)'),
                 _('Total number of contracted working hours for the data at the beginning of the year/day (employee+ entrepreneur)'),
                 _('Total number of contracted working hours for the data at the end of the year /day(employee+ entrepreneur)'),
                 ),)
    cases = c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace)
    for case in cases:
        model += ((
                      str(case.job),
                      str(case.year),
                      str(case.needlestick_injuries),
                      str(case.staff_beginning),
                      str(case.staff_end),
                      str(case.working_hours_beginning),
                      str(case.working_hours_end),
                      ),)
    return csvExport(model, 'c13_export_'+datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"))

def CountStatistics(cases):
    countable_case=uncountable_case=()
    group = []
    for case in cases:
        if translation.get_language() == "hu":
            job_name = case.job.job_hungarian
        else:
            job_name = case.job.job_english
        try: first = float(float(case.needlestick_injuries) / ((float(case.staff_beginning) + float(case.staff_end))/2)*100)
        except: first = 0
        try: second = float(float(case.needlestick_injuries) / ((float(case.working_hours_beginning) + float(case.working_hours_end))*0.5 / 8) *100)
        except: second = 0
        group.append([
            job_name,
            first,
            second,
            ])
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "jobs" : group,
        }
    return context

def ZipThat(one,two,formStuff,three=False):
    jobs = []
    if three:
        for i in range(len(one['jobs'])):
            jobs += [
                    {
                    'name': one['jobs'][i][0],
                    'first': [one['jobs'][i][1],0,0],
                    'second': [one['jobs'][i][2],0,0]
                    },
                ]
        for i in range(len(two['jobs'])):
            setup = False
            for job in jobs:
                if job['name'] == two['jobs'][i][0]:
                    job['first'][1] = two['jobs'][i][1]
                    job['second'][1] = two['jobs'][i][2]
                    setup = True
                    break
            if setup is False:
                jobs += [{
                    'name': two['jobs'][i][0],
                    'first': [0,two['jobs'][i][1],0],
                    'second': [0,two['jobs'][i][2],0]
                },]
        for i in range(len(three['jobs'])):
            setup = False
            for job in jobs:
                if job['name'] == three['jobs'][i][0]:
                    job['first'][2] = three['jobs'][i][1]
                    job['second'][2] = three['jobs'][i][2]
                    setup = True
                    break
            if setup is False:
                jobs += [{
                    'name': three['jobs'][i][0],
                    'first': [0,0,three['jobs'][i][1]],
                    'second': [0,0,three['jobs'][i][2]]
                },]
        ZippedThat = {
            'overall': [ one['overall'], two['overall'], three['overall'] ],
            'removed': [ one['removed'], two['removed'], three['removed'] ],
            'counted': [ one['counted'], two['counted'], three['counted'] ],
            'jobs': jobs,
            'formdata': formStuff,
            }

    else:
        for i in range(len(one['jobs'])):
            for i in range(len(one['jobs'])):
                jobs += [
                        {
                        'name': one['jobs'][i][0],
                        'first': [one['jobs'][i][1],0],
                        'second': [one['jobs'][i][2],0]
                    },
                ]
        for i in range(len(two['jobs'])):
            setup = False
            for job in jobs:
                if job['name'] == two['jobs'][i][0]:
                    job['first'][1] = two['jobs'][i][1]
                    job['second'][1] = two['jobs'][i][2]
                    setup = True
                    break
            if setup is False:
                jobs += [{
                    'name': two['jobs'][i][0],
                    'first': [0,two['jobs'][i][1]],
                    'second': [0,two['jobs'][i][2]]
                },]
        ZippedThat = {
            'overall': [ one['overall'], two['overall'] ],
            'removed': [ one['removed'], two['removed'] ],
            'counted': [ one['counted'], two['counted'] ],
            'jobs': jobs,
            'formdata': formStuff,
            }
    return ZippedThat

def ZipForAnon(stats):
    name = []
    country = []
    first = True
    jobs = []
    item_codes = {}
    i = 0
    for stat in stats:
        item_codes[stat['name']] = i
        i += 1

    for stat in stats:
        name += [stat['name'],]
        this_workplace = School.objects.get(codename = stat['name'])
        print this_workplace.country.printable_name
        country += [this_workplace.country.printable_name,]
        for job in stat['statistics']['jobs']:
            if first:
                job_list_to_add = [job[0], job[1],]
                for i in range(len(stats)-1):
                    job_list_to_add += [0,]
                job_list_to_add += [job[2],]
                for i in range(len(stats)-1):
                    job_list_to_add += [0,]
                jobs += [job_list_to_add,]
                first = False
            else:
                for job_list in jobs:
                    if job_list[0] == job[0]:
                        first_in_table = item_codes[stat['name']] + 1
                        second_in_table = item_codes[stat['name']] + 1 + len(stats)
                        job_list[first_in_table] = job[1]
                        job_list[second_in_table] = job[2]
                        break
                    else:
                        job_list_to_add = [job[0]]
                        for i in range(len(stats)*2):
                            job_list_to_add += [0,]
                        jobs += [job_list_to_add,]
    return {
        'name': name,
        'country': country,
        'jobs': jobs
    }

@login_required
def AnonymStatistics(request):
    if request.method == "POST":
        form = AnonymStatForm(request.POST)
        statistics = []
        if form.is_valid():
            start = form.cleaned_data['endDate']
            workplaces = School.objects.all()
            for workplace in workplaces:
                stat = CountStatistics(c13.objects.filter(added_by__personel__workplace = workplace, year = start ))
                if stat['overall']:
                    statistics += [{
                        "name" : workplace.codename,
                        "country": workplace.country.printable_name,
                        "statistics" : stat
                    }]
            statistics = CreateUselessData(statistics)
            return render_to_response('c13_anon.html', {'statistics': statistics}, context_instance=RequestContext(request))
        else:
            form = AnonymStatForm(request.POST)
            return render(request, 'c13.html', { 'form': form,'benchmarking': True })
    form = AnonymStatForm()
    return render(request, 'c13.html', { 'form': form,'benchmarking': True })

def CreateUselessData(statistics):
    specialities = []
    for stat in statistics:
        for job in stat['statistics']['jobs']:
            if not job[0] in specialities:
                specialities.append(job[0])
    for stat in statistics:
        for speciality in specialities:
            found = False
            for job in stat['statistics']['jobs']:
                if job[0] == speciality:
                    found = True
            if not found:
                stat['statistics']['jobs'] += [[speciality,0,0],]
    return statistics

def SortAndAddCountryAverage(statistics, start, user):
    statistics = sorted(statistics, key=lambda x: x['name'])
    hospitals = []
    countryStat = []
    statis = []
    jobs = []
    overall = removed = counted = 0
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
            query = c13.objects.filter(added_by__personel__workplace__codename = hospit, year = start )
            statis += [CountStatistics(query),]
        for stat in statis:
            overall += stat['overall']
            removed += stat['removed']
            counted += stat['counted']
            first = second = counter = 0
            for job in stat['jobs']:
                jobname = job[0]
                first += job[1]
                second += job[2]
                counter += 1
                if counter:
                    jobs += [[jobname, (first/counter), (second/counter), counter],]
        stat = {
            "overall": overall,
            "removed": removed,
            "counted": counted,
            "jobs": jobs
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