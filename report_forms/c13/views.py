# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c13.forms import C13Form, FileUploadForm
from report_forms.c13.models import c13, c13CSV
from django.utils.translation import ugettext_lazy as _

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
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = C13Form(request.POST)
            return render(request, 'c13.html', { 'form': form })

    form = C13Form()
    return render(request, 'c13.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        imported_csv = c13CSV.import_data(data=csv_file)
        for line in imported_csv:
            try:
                new_c13 = c13.objects.create(
                                            job                             = line.job,
                                            year                            = line.year,
                                            needlestick_injuries            = line.needlestick_injuries,
                                            staff_beginning                 = line.staff_beginning,
                                            staff_end                       = line.staff_end,
                                            working_hours_beginning         = line.working_hours_beginning,
                                            working_hours_end               = line.working_hours_end,
                                            added_by                        = request.user,
                )
                new_c13.save()
            except IntegrityError:
                #todo: testing for fail state
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('c13.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = c13.objects.all()
    for case in cases:
        pass

    ''' Working '''

    ''' Counting '''

    ''' Displaying '''
    context = {
        "overall": len(cases),
        "removed": len(uncountable_case),
        "counted": len(countable_case),
#        "indicator_one": indicator_one,
#        "subindicator_one": subindicator_one,
#        "subindicator_two": subindicator_two,
    }
    return render_to_response('c13_statistics.html', context, context_instance=RequestContext(request))

def calculate_age(born, today = date.today()):
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return int(today.year - born.year - 1)
    else:
        return int(today.year - born.year)