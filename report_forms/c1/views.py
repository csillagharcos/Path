# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c1.forms import C1Form, FileUploadForm
from report_forms.c1.models import c1, c1CSV


def Display(request):
    form = C1Form()
    context = {'form' : form }
    return render_to_response('form.html', context, context_instance=RequestContext(request))

@login_required
def Import(request):
    if request.method == "POST":
        #upload data to database
        exists=()
        csv_file = request.FILES['file']
        imported_csv = c1CSV.import_data(data=csv_file)
        for line in imported_csv:
            try:
                new_c1 = c1.objects.create( patient_id=line.patient_id,
                                            case_id=line.case_id,
                                            date_of_birth=datetime.strptime(line.date_of_birth, "%Y-%m-%d"),
                                            date_of_delivery=datetime.strptime(line.date_of_delivery+' '+line.time_of_delivery, "%Y-%m-%d %H:%M:%S"),
                                            number_of_prev_deliveries = line.number_of_prev_deliveries,
                                            number_of_prev_deliveries_by_c = line.number_of_prev_deliveries_by_c,
                                            the_c_section = line.the_c_section,
                                            weight_of_the_newborn = line.weight_of_the_newborn,
                                            mother_illness = line.mother_illness,
                                            specify_mother_illness = line.specify_mother_illness,
                                            drg_code = line.drg_code,
                                            other_diagnoses = line.other_diagnoses,
                                            added_by = request.user,
                )
                new_c1.save()
            except IntegrityError:
                exists += (line.patient_id,)
                print "exists"
        return HttpResponse(simplejson.dumps({"value" : exists}), mimetype="application/json")
    else:
        form = FileUploadForm()
        context = { "form" : form }
        return render_to_response('form.html', context, context_instance=RequestContext(request))


@login_required
def Statistics(request):
    form = C1Form()
    context = {'form' : form }
    return render_to_response('form.html', context, context_instance=RequestContext(request))