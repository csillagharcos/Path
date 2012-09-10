# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from report_forms.c1.forms import C1Form, FileUploadForm
from report_forms.c1.models import c1, c1CSV, c1OtherDiagnose

def list_report_forms(request):
    return render_to_response('list_of_report_forms.html', context_instance=RequestContext(request))