# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.r1.forms import r1Form, FileUploadForm
from report_forms.r1.models import r1, r1CSV
from django.utils.translation import ugettext_lazy as _

@login_required
def Display(request):
    if request.method == "POST":
        form = r1Form(request.POST)
        if form.is_valid():
            new_r1 = r1.objects.create(
                patient_id                      = form.cleaned_data['patient_id'],
                case_id                         = form.cleaned_data['case_id'],
                date_of_birth                   = form.cleaned_data['date_of_birth'],


                added_by                        = request.user,
            )
            new_r1.save()
            return render_to_response('filled_out.html', {}, context_instance=RequestContext(request))
        else:
            form = r1Form(request.POST)
            return render(request, 'r1.html', { 'form': form })

    form = r1Form()
    return render(request, 'r1.html', { 'form': form })

@login_required
def Import(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        imported_csv = r1CSV.import_data(data=csv_file)
        for line in imported_csv:
            try:
                new_r1 = r1.objects.create(
                                            patient_id                      = line.patient_id,
                                            case_id                         = line.case_id,
                                            date_of_birth                   = datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_admission               = datetime.strptime(line.date_of_admission, "%Y-%m-%d"),


                                            added_by                        = request.user,
                )
                new_r1.save()
            except IntegrityError:
                #todo: testing for fail state
                pass
        return HttpResponse(simplejson.dumps({"value" : "okay."}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('r1.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    ''' Query '''
    countable_case=uncountable_case=()
    cases = r1.objects.all()
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
    return render_to_response('r1_statistics.html', context, context_instance=RequestContext(request))

def calculate_age(born, today = date.today()):
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return int(today.year - born.year - 1)
    else:
        return int(today.year - born.year)