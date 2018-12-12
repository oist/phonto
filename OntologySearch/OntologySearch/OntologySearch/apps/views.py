from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.finders import AppDirectoriesFinder
from os import path
from os import sep
import os
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

import smtplib
from django.core.mail import send_mail
from django.core import mail

from OntologySearch.apps import response_success
from OntologySearch.apps import response_successCORS
from OntologySearch.apps import response_forbidden
from OntologySearch.apps import response_notfound
from OntologySearch.apps import response_badrequest
from django.views.decorators.clickjacking import xframe_options_exempt

from django.conf import settings
import dber
import dbquerier
import sparqler
import spquerier
import requester
import auth

import cgitb
cgitb.enable()


# for autocomplete  return words array
def get_completesynonym (request , **options):
    queryString = requester.getQueryWord(request , options)

    if queryString is None or queryString == "":
        ret = []
    else:
        limitcnt = request.POST.get("limit")
        ret = spquerier.labelcomplete_synonym(queryString , limitcnt)

    return response_success(request, payload={
        'result' : ret,
    })

# return HierarchyData
def getowldata (request , **options):
    queryString = requester.getQueryWord(request , options)
    if queryString is None or queryString == "":
        ret = {}
    else:
        ret = sparqler.getHierarchyData(queryString)

    return response_success(request, payload={
        'result' : ret
    })

# return classes(classURI,name)
def getClasses (request , **options):
    queryString = requester.getQueryWord(request , options)
    if queryString is None or queryString == "":
        ret = []
    else:
        ret = []
        classes = spquerier.getClassByLabelSynonym(queryString)
        for row in classes:
            ret.append({
                "class":row.get("class")
                ,"name":row.get("label")
            })

    return response_success(request, payload={
        'result' : ret,
    })


def getContentsTest (request , **options):
    queryString = requester.getQueryWord(request , options)
    return response_success(request, payload={
        'result' : queryString,
    })


# return ontology contents()
def getContents (request , **options):
    queryString = requester.getQueryWord(request , options)

    return returnContents(request , queryString)

# return ontology contents(http)
def getContentsHttp (request , **options):
    queryString = requester.getQueryWord(request , options)
    queryString = 'http://' + queryString

    return returnContents(request , queryString)

# return ontology contents(https)
def getContentsHttps (request , **options):
    queryString = requester.getQueryWord(request , options)
    queryString = 'https://' + queryString

    return returnContents(request , queryString)

# return ontology contents
def returnContents (request , queryString):

    if queryString is None or queryString == "":
        ret = {}
    else:
        ret = spquerier.getContents(queryString)

    return response_success(request, payload={
        'result' : ret,
    })

# return ontology prefixes
def getPrefixes (request):
    ret = {'base':settings.BASEPREFIX,
           'owl':settings.OWLPREFIX
           }
    return response_success(request, payload={
        'result' : ret,
    })

#
# db search in detail
# return
#   'result' :
#      {
#         "hit":exacts
#       , "parents":
#       , "children":
#       , "sibling":
#       , "rels":
#       , "urlformat":
#       ,
#      }
def searchdb (request , **options):
    idWords = requester.getDbIdAndWord(request , options)
    queryString = idWords.get("word")
    dbid = idWords.get("dbid")
    if queryString is None or queryString == "" or dbid is None or dbid == "":
        return response_success(request, payload={
        'result' : {
             "hit":{}
           , "partialcnt":0
           , "partials":[]
           , "parents":{}
           , "children":{}
           , "siblings":{}
           , "rels":{}
           , "urlformat" : ""
          }
        })

    ##
    ## get words from fuseki
    ##
    # get candidate from owl
    candidates = sparqler.getCandidateDetail(queryString)
    #candidates = sparqler.getCandidate(queryString)

    # adjust result to set 'where' condition @sql
    exact = candidates.get("exact")
    hitconds = sparqler.toLabelSynonymArr(exact)

    synonym = candidates.get("synonym")
    synconds = sparqler.toLabelSynonymArr(synonym)
    if synconds is not None:
        hitconds.extend(synconds)

    parent = candidates.get("parent")
    parconds = sparqler.toLabelSynonymArr(parent ,"parentlabel")

    sibling = candidates.get("sibling")
    sibconds = sparqler.toLabelSynonymArr(sibling)

    child = candidates.get("child")
    chiconds = sparqler.toLabelSynonymArr(child)

    rel = candidates.get("rels")
    relconds = sparqler.toLabelSynonymArr(rel)

    partialcnt = candidates.get("partialcnt")
    partial = candidates.get("partials")
    partconds = sparqler.toLabelSynonymArr(partial)
    partsynmap = candidates.get("partsynmap")


    ## search from Mysql db

    # exact hit
    exacts = dber.getModelAndKeyword(dbid , hitconds)

    # parent
    pars = dber.getModelAndKeyword(dbid , parconds)

    # sibling
    sibs =  dber.getModelAndKeyword(dbid , sibconds)

    # children
    children = dber.getModelAndKeyword(dbid , chiconds)

    #other rels
    rels = dber.getModelAndKeyword(dbid , relconds)

    #partial hits
    partials = dber.getModelAndKeyword(dbid , partconds)

    return response_success(request, payload={
        'result' : {
             "hit":exacts
           , "parents":pars
           , "children":children
           , "siblings":sibs
           , "rels":rels
           , "partialcnt":partialcnt
           , "partials":partials
           , "partsynmap":partsynmap
          }
    })



@xframe_options_exempt
def searchdball (request , **options):
    queryString = requester.getParam("word" , request , options)
    if queryString is None or queryString == "":
        return response_successCORS(request, payload={
        'result' : {
             "hit":{}
           , "partialcnt":0
           , "partials":[]
           , "parents":{}
           , "children":{}
           , "siblings":{}
           , "rels":{}
           , "urlformat" : ""
          }
        })

    queryArr = queryString.split("_,_")
    res = dber.getSitelink_word(queryArr)
    if res:
        exacts = res.get("exact")

    return response_successCORS(request, payload={
          "hit":exacts

    })


@xframe_options_exempt
def searchneighbors (request , **options):
    dbname = requester.getParam("dbname" , request , options)
    identifier = requester.getParam("identifier" , request , options)
    if dbname is None or dbname == "" or identifier is None or identifier == "":
        return response_successCORS(request, payload={
        'result' : {
             "hit":{}
           , "partialcnt":0
           , "partials":[]
           , "parents":{}
           , "children":{}
           , "siblings":{}
           , "rels":{}
           , "urlformat" : ""
          }
        })

    res = dber.getNeighbors(dbname , identifier)

    exacts = {}
    parents = {}
    children = {}
    siblings = {}
    rels = {}
    if res:
        exacts = res.get("exact")
        parents = res.get("parent")
        children = res.get("child")
        siblings = res.get("sibling")
        rels = res.get("rels")

    return response_successCORS(request, payload={
          "hits":exacts
          ,"parents":parents
          ,"children":children
          ,"siblings":siblings
          ,"rels":rels
    })


@xframe_options_exempt
def searchdball_org (request , **options):
    queryString = requester.getParam("word" , request , options)

    if queryString is None or queryString == "":
        return response_successCORS(request, payload={
        'result' : {
             "hit":{}
           , "partialcnt":0
           , "partials":[]
           , "parents":{}
           , "children":{}
           , "siblings":{}
           , "rels":{}
           , "urlformat" : ""
          }
        })

    queryArr = queryString.split("_,_")
    queryString = ""
    for qstr in queryArr:
        if qstr:
            queryString += "|" + qstr

    if queryString:
        queryString = queryString[1:]

    ##
    ## get words from fuseki
    ##
    # get candidate from owl
    candidates = sparqler.getCandidate(queryString)

    # adjust result to set 'where' condition @sql
    exact = candidates.get("exact")
    hitconds = sparqler.toLabelSynonymArr(exact)

    synonym = candidates.get("synonym")
    synconds = sparqler.toLabelSynonymArr(synonym)
    if synconds is not None:
        hitconds.extend(synconds)

    ## search from Mysql db

    # exact hit
    exacts = dber.getModelAndKeywordAllDB( hitconds)


    exacts = dber.translateForJS(exacts)

    return response_successCORS(request, payload={
          "hit":exacts

    })






# insert or update model
#e.g. http://127.0.0.1:8000/apps/updatemodel/ipathwaysplus/199/modelname1/ptl30sm59fmqaMDmeka8q
def updatemodel (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    modelid = params.get("modelid")
    modelname = params.get("modelname")

    dbid = dber.getDataBaseId(dbname)

    res = dber.updatemodel( dbid , modelid , modelname)
    return response_success(request, payload={
         "params":params
        ,"result":res
    })

# delete model
#e.g. http://127.0.0.1:8000/apps/deletemodel/ipathwaysplus/199/ptl30sm59fmqaMDmeka8q
def deletemodel (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    modelid = params.get("modelid")

    dbid = dber.getDataBaseId(dbname)

    dbquerier.deletemodel(dbid, modelid)
    res = dbquerier.deletekeywords(dbid, modelid)
    return response_success(request, payload={
         "params":params
        ,"result":res
    })

# insert keyword
#e.g. http://127.0.0.1:8000/apps/insertkeyword/ipathwaysplus/199/signaling/ptl30sm59fmqaMDmeka8q
def insertkeyword (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    modelid = params.get("modelid")
    keyword = params.get("keyword")

    dbid = dber.getDataBaseId(dbname)

    res = dber.insertkeyword( dbid , modelid , keyword)
    return response_success(request, payload={
         "params":params
        ,"result":res
    })

# delete keyword
#e.g. http://127.0.0.1:8000/apps/deletekeyword/ipathwaysplus/199/keyword1/ptl30sm59fmqaMDmeka8q
def deletekeyword (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    modelid = params.get("modelid")
    keyword = params.get("keyword")

    dbid = dber.getDataBaseId(dbname)

    res = dbquerier.deletekeyword(dbid, modelid , keyword)
    return response_success(request, payload={
         "params":params
        ,"result":res
    })

#
# get db list
#e.g. http://127.0.0.1:8000/apps/getdblist/ptl30sm59fmqaMDmeka8q
def getdblist (request , **options):
    res = dbquerier.getDbNameList();
    return response_success(request, payload={
        "dblist":res
    })

#
# get db info
#e.g. http://127.0.0.1:8000/apps/getdbinfo/testdb/ptl30sm59fmqaMDmeka8q
def getdbinfo (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")

    res = dber.getTargetDBbyName(dbname);
    retinfo = {
            "dbid"     : res.get("dbid")
           ,"dbname"   : res.get("dbname")
           ,"urlformat": res.get("urlformat")
               }
    return response_success(request, payload={
        "dbinfo":retinfo
    })

#
# get db info
#e.g. http://127.0.0.1:8000/apps/getdbinfo/testdb/ptl30sm59fmqaMDmeka8q
def updatedbinfo (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    dbid = dber.getDataBaseId(dbname)
    urlformat = requester.getParam("urlformat" , request , options)

    res = dbquerier.updateTargetDB(dbid ,
                                   {
                                    "urlformat":urlformat
                                    })

    return response_success(request, payload={
        "result" : res
    })

#
# get model list
#e.g. http://127.0.0.1:8000/apps/modellist/testdb/ptl30sm59fmqaMDmeka8q
def getmodellist (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    dbid = dber.getDataBaseId(dbname)

    res = dber.getModelList(dbid)
    formatres = dber.dFormEach(res)
    return response_success(request, payload={
        "models":formatres
    })

#
# get keyword list
#e.g. http://127.0.0.1:8000/apps/keywordlist/testdb/1/ptl30sm59fmqaMDmeka8q
def getkeywordlist (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    modelid = params.get("modelid")
    dbid = dber.getDataBaseId(dbname)

    res = dber.getKeywordList(dbid , modelid)
    return response_success(request, payload={
        "keywords":res
    })


#
# update model list & keyword list
#
def updatebycsv (request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    dbid = dber.getDataBaseId(dbname)
    models = requester.getParam("modellist" , request , options)
    keywords = requester.getParam("keywordlist" , request , options)

    res = dber.updatemodelsbylist(dbid, models)
    res = dber.updatekeywordsbylist(dbid, keywords)

    return response_success(request, payload={
         "params":params
        ,"result":res
    })

#
# update 1model & relevant keyword list
# input params
#  token
#  dbname
#  modelid
#  modelname
#  keyword:[ keyword , keyword ,,,]
#
def updatemodelandkeyword(request , **options):
    authori = auth.checkTokenEnabledByRequest(request, options)
    if authori == False:
        return response_forbidden(request)

    params = requester.getDbMargeParam(request , options)
    dbname = params.get("dbname")
    dbid = dber.getDataBaseId(dbname)
    modelid = params.get("modelid")
    modelname = params.get("modelname")

    keyword = requester.getParamList("keyword[]" , request , options)

    res = dber.updatemodel( dbid , modelid , modelname)
    res = dbquerier.deletekeywords(dbid, modelid)

    if(isinstance(keyword , list)):
        for i, key in enumerate(keyword):
            res = dber.insertkeyword(dbid, modelid, key)

    return response_success(request, payload={
         "params":params
        ,"result":res
    })


def regenerateonto(request , **options):
    status = dber.genStatus()
    if not status:
        return response_success(request, payload={
             "msg":"skip generate"
        })

    # generate keyword relation
    dbquerier.deleteSitelink_keyword()

    return generateontoContents(request)


def generateonto(request , **options):
    status = dber.genStatus()
    if not status:
        return response_success(request, payload={
             "msg":"skip generate"
        })

    return generateontoContents(request)


def generateontoContents(request):
    # generate keyword relation
    keywords = dbquerier.getNewKeywordListDistinct()
    hitkeys={}
    parkeys={}
    sibkeys={}
    chikeys={}
    relkeys={}
    for keyword in keywords:
        queryString = keyword.get("keyword")
        candidates = sparqler.getCandidateDetail(queryString , True)
        # adjust result to set 'where' condition @sql
        exact = candidates.get("exact")
        hitconds = sparqler.toLabelSynonymArr(exact)

        synonym = candidates.get("synonym")
        synconds = sparqler.toLabelSynonymArr(synonym)
        if synconds is not None:
            hitconds.extend(synconds)

        dber.genSitelink_keyword(queryString , hitconds , "exact" , hitkeys)

        parent = candidates.get("parent")
        parconds = sparqler.toLabelSynonymArr(parent ,"parentlabel")
        if parconds is not None and len(parconds) > 0:
            dber.genSitelink_keyword(queryString , parconds , "parent" , parkeys)


        sibling = candidates.get("sibling")
        sibconds = sparqler.toLabelSynonymArr(sibling)
        if sibconds is not None and len(sibconds) > 0:
            dber.genSitelink_keyword(queryString , sibconds , "sibling" , sibkeys)

        child = candidates.get("child")
        chiconds = sparqler.toLabelSynonymArr(child)
        if chiconds is not None and len(chiconds) > 0:
            dber.genSitelink_keyword(queryString , chiconds , "child" , chikeys)

        rel = candidates.get("rels")
        relconds = sparqler.toLabelSynonymArr(rel)
        if relconds is not None and len(relconds) > 0:
            dber.genSitelink_keyword(queryString , relconds , "rel" , relkeys)

    dbquerier.updateGenStatus('FIN')

    return response_success(request, payload={
#         "params":params
#        ,"result":res
    })


def generatedb(request , **options):

    status = dber.genStatus()
    if not status:
        return response_success(request, payload={
             "msg":"skip generate"
        })

    # generate link
    dbinfo = dber.getDbinfo()
    dbmodelinfo = dber.getDbModelinfo()
    dber.genSitelink(dbinfo , dbmodelinfo)
    dber.genSitelink_word(dbinfo , dbmodelinfo)

    dbquerier.updateGenStatus('FIN')

    return response_success(request, payload={
#         "params":params
#        ,"result":res
    })


#
# error responses
#
def json404 (request):
    return response_notfound(request)

