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
            interval_one = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, surgical_incision__gte = form.cleaned_data['date1a'], surgical_incision__lte = form.cleaned_data['date1b'] ), False )
            interval_two = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, surgical_incision__gte = form.cleaned_data['date2a'], surgical_incision__lte = form.cleaned_data['date2b'] ), False )
            if form.cleaned_data['date3a'] and form.cleaned_data['date3b']:
                interval_three = CountStatistics(c13.objects.filter(added_by__personel__workplace = request.user.get_profile().workplace, surgical_incision__gte = form.cleaned_data['date3a'], surgical_incision__lte = form.cleaned_data['date3b'] ), False )
            else:
                interval_three = False
            return render_to_response('c13_trend_diagram.html', { 'one': interval_one, 'two': interval_two, 'three': interval_three, 'form': form.cleaned_data }, context_instance=RequestContext(request))
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