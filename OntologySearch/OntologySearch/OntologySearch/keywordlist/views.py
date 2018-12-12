import os
import sys
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.finders import AppDirectoriesFinder
from os import path
from os import sep
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings

from OntologySearch.apps import response_success
from OntologySearch.apps import response_forbidden
from OntologySearch.apps import response_notfound
from OntologySearch.apps import response_badrequest

from OntologySearch.apps import dber
from OntologySearch.apps import dbquerier
from OntologySearch.apps import sparqler
from OntologySearch.apps import spquerier
from OntologySearch.apps import requester
from OntologySearch.apps import auth

from OntologySearch.keywordlist import keyworddig
from OntologySearch.keywordlist import pdfutil
import traceback

import cgitb
cgitb.enable()


# for autocomplete  return words array
def getkeyfromarticle (request , **options):
    if request.method != 'POST':
        return response_badrequest(request)

    upfile = request.FILES['file']
    if upfile == None:
        return response_badrequest(request)

    upname = upfile.name.lower()
    if upname.endswith(".pdf") == False:
        return response_badrequest(request)

    savedir = os.path.dirname(os.path.abspath(__file__)) + sep + settings.ARTICLE_DIR
    now = datetime.datetime.now()
    filename = savedir + sep + now.strftime("%Y%m%d%H%M%S") + upfile.name

    fout = file (filename, 'wb')
    while 1:
        chunk = upfile.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()

    txtfilename = filename + ".txt"
    args = {
             "pdffile":filename
            ,"outfile":txtfilename
            }

    try:
        pdfutil.pdf2textsingle(args)

        ret = keyworddig.getOntoKeywords(txtfilename)
    except:
        print traceback.format_exc(sys.exc_info()[2])

    os.remove(txtfilename)
    os.remove(filename)

    return response_success(request, payload={
        'keyword' : ret,
    })


#
# error responses
#
def json404 (request):
    return response_notfound(request)

