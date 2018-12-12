# coding: UTF-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from OntologySearch.apps import requester ,dber
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt


# ontology search page
def index (request, **options):
    initword = ""
    if options.get("word") is not None:
        initword = options.get("word")

    return render_to_response('site/toppage.html', RequestContext(request, {
        'action_name': 'dashboard',
        'user'     : request.user,
        'initword'     : initword,
    }))

# dbsearch page
@xframe_options_exempt
def search (request , **options):
    initword=""
    initdbid=""
    initdbname=""

    idWords = requester.getDbIdAndWord(request , options)
    if idWords is not None:
        if idWords.get("word") is not None:
            initword = idWords.get("word")

        if idWords.get("dbid") is not None:
            initdbid = idWords.get("dbid")
        else:
            initdbid = "1"

        initdbinfo = dber.getTargetDBbyID(initdbid)
        if initdbinfo is not None:
            initdbname = initdbinfo.get("dbname")

        partlimit = settings.LIMIT_PARTIAL

    return render_to_response('site/search.html', RequestContext(request, {
        'user'       : request.user,
        'initword'   : initword,
        'initdbid'   : initdbid,
        'initdbname' : initdbname,
        'partlimit'  : partlimit,
    }))

# pilot version (sparqle page)
def wordcondition (request):
    return render_to_response('site/wordcondition.html', RequestContext(request, {
        'action_name': 'dashboard' ,
        'user'     : request.user,
    }))

# explanation
def navi (request):
    myhost = "http://phonto.unit.oist.jp/"
    test = ""
    return render_to_response('site/navi.html', RequestContext(request, {
         "myhost":myhost
        ,"test":test
    }))

# db update sample
def sampleupdate (request):
    myhost = "http://phonto.unit.oist.jp/"
    return render_to_response('site/sampleupdate.html', RequestContext(request, {
         "myhost":myhost
    }))

# model keyeord administrator page
def sampleadmin (request, **options):

    myhost = "http://phonto.unit.oist.jp/"

    return render_to_response('site/sampleadmin.html', RequestContext(request, {
         "myhost":myhost

    }))

# model keyeord administrator page
def samplecsvadmin (request, **options):
    myhost = "http://phonto.unit.oist.jp/"
    test = ""
    #password:"testpass"
    return render_to_response('site/samplecsvadmin.html', RequestContext(request, {
         "myhost":myhost
        ,"test":test
    }))

# sample info page
def samplemodel (request, **options):
    modelid = requester.getParam("modelid", request, options)
    return render_to_response('site/samplemodelinfo.html', RequestContext(request, {
         "modelid":modelid
    }))

def wrapper (request, **options):
    dbname = requester.getParam("dbname", request, options)
    modelid = requester.getParam("modelid", request, options)

    dbinfo = dber.getTargetDBbyName(dbname)
    urlformat = dbinfo.get("urlformat")
    src = urlformat.format(modelid)
    return render_to_response('site/wrapper.html', RequestContext(request, {
         "modelid":modelid
        ,"dbname":dbname
        ,"src":src
    }))


#javascrpit content
@xframe_options_exempt
def jslibcontent (request, **options):
    modelid = requester.getParam("modelid", request, options)
    return render_to_response('site/jslibcontent.html', RequestContext(request, {
         "modelid":modelid
    }))

def nvlc(obj):
    if obj is None:
        return "";
    else:
        return obj

