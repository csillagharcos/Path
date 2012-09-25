# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import translation
from report_forms.c13.forms import C13Form, C13Form_hungarian
from report_forms.c13.models import c13, joblist
from django.utils.translation import ugettext_lazy as _
from report_forms.tools import csvDump

@login_required
def Display(request):
    if request.method == "POST":
        form = C13Form(request.POST)
        if form.is_valid():
            new_c13 = c13.objects.create(
                job                             = joblist.objects.get(pk=1),
                year                            = form.cleaned_data['year'],
                needlestick_injuries            = form.cleaned_data['needlestick_injuries'],
                staff_beginning                 = form.cleaned_data['staff_beginning'],
                staff_end                       = form.cleaned_data['staff_end'],
                working_hours_beginning         = form.cleaned_data['working_hours_beginning'],
                working_hours_end               = form.cleaned_data['working_hours_end'],
                added_by                        = request.user,
            )
            new_c13.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            if request.LANGUAGE_CODE == "hu":
                form = C13Form_hungarian(request.POST)
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
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c13.objects.all()
    group = []
    print
    for case in cases:
        if translation.get_language() == "hu":
            job_name = case.job.job_hungarian
        else:
            job_name = case.job.job_english
        group.append([
                  job_name,
                  (case.staff_beginning + case.staff_end)/2,
                  ((case.working_hours_beginning + case.working_hours_end)*0.5)/8,
                  case.needlestick_injuries / (case.staff_beginning + case.staff_end)/2 *100,
                  case.needlestick_injuries / ((case.working_hours_beginning + case.working_hours_end)*0.5)/8 *100,
        ])

    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
        "stuff" : group,
#        "indicator_one": indicator_one,
#        "subindicator_one": subindicator_one,
#        "subindicator_two": subindicator_two,
    }
    return render_to_response('c13_statistics.html', context, context_instance=RequestContext(request))

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