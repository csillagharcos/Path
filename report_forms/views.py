# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

def list_report_forms(request):
    return render_to_response('list_of_report_forms.html', context_instance=RequestContext(request))