from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from pathstatic.forms import LoginForm

def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            myProfile = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if myProfile is not None:
                login(request, myProfile)
                return HttpResponseRedirect(request.GET['next'])
            else:
                return render_to_response('login.html', { 'form': form }, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', { 'form': form }, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = { 'form' : form }
        return render_to_response('login.html', context, context_instance=RequestContext(request))

def homepage(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def knowledge_center(request):
    return render_to_response('knowledge_center.html', context_instance=RequestContext(request))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')