# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import translation
from report_forms.c13.forms import C13Form, C13Form_hungarian, TrendForm
from report_forms.c13.models import c13
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import csvDump, csvExport

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
        for i in range(len(one['jobs'][0])-1):
            jobs += [
                    {
                    'name': one['jobs'][i][0],
                    'first': [one['jobs'][i][1], two['jobs'][i][1]],
                    'second': [one['jobs'][i][2], two['jobs'][i][2]]
                },
            ]
        ZippedThat = {
            'overall': [ one['overall'], two['overall'] ],
            'removed': [ one['removed'], two['removed'] ],
            'counted': [ one['counted'], two['counted'] ],
            'jobs': jobs,
            'formdata': formStuff,
            }
    return ZippedThat