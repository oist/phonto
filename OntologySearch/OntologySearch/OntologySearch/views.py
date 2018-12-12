from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt

import settings

def index (request):
    return render_to_response('site/toppage.html', RequestContext(request, {
        'action_name': 'dashboard',
        'user'     : request.user,
    }))

@xframe_options_exempt
def jslib (request):
    return render_to_response('site/ontologicalneighbors.js', RequestContext(request, {
        'action_name': 'dashboard',
        'user'     : request.user,
    }))

@xframe_options_exempt
def jslibcss (request):
    return render_to_response('site/ontologicalneighbors.css', RequestContext(request, {
#    return render_to_response('static/css/common.css', RequestContext(request, {
        'action_name': 'dashboard',
        'user'     : request.user,
    }))
