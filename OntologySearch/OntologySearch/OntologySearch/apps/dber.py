'''
Created on 2015/06/17

@author: adminstrator
'''
import sys
from django.conf import settings
import datetime
import dbquerier

# return model info with keyward info
# params:
#     dbid : dbid
#     hitconds : array of keyword
#
# return : [
#             {"id":modelid, "name":name, "url":url , keyword:[keyword]}
#          ]
#
def getModelAndKeyword(dbid , hitconds):
    if dbid is None or hitconds is None or len(hitconds) == 0:
        return {}

    #urlformat
    urlformat = ""
    dbinfo = getTargetDBbyID(dbid)
    if dbinfo is not None and dbinfo.get("urlformat") is not None:
        urlformat = dbinfo.get("urlformat")

    #mysql search
    result = dbquerier.getModelAndKeyword(dbid , hitconds)

    #adjust format
    #result = adjustKeyword(result , urlformat)
    result = adjustKeywordAllDB(result )

    return result

#
# like distinct...
#
# param
#   rowArr : [
#             {"dbname":dbname , "id":modelid, "name":name, "url":url , keyword:[keyword]}
#            ]
#
# return :
#            {dbname :[ {"id":modelid, "name":name,  "url":url , keyword:[keyword]}]
#            }
#
def translateForJS(rowArr):
    if rowArr is None:
        return

    urls ={}
    dataArr =[]
    curdbname = ""

    for row in rowArr:
        if row is None  or row.get("dbname") is None:
            continue

        if curdbname != row.get("dbname"):
            if curdbname :
                urls.update({ curdbname : dataArr })
            curdbname = row.get("dbname")
            dataArr =[]

        addData = {
                    "id":row.get("identifier")
                   ,"name":row.get("name")
                   ,"url":row.get("url")
                   ,"keywords":row.get("keywords")
                   }
        dataArr.extend([addData])

    if len(dataArr):
        urls.update({ curdbname : dataArr })



    return urls


# return model info with keyward info (All target)
# params:
#     dbid : dbid
#     hitconds : array of keyword
#
# return : [
#             {"id":modelid, "name":name, "url":url , keyword:[keyword]}
#          ]
#
def getModelAndKeywordAllDB(hitconds):
    if hitconds is None or len(hitconds) == 0:
        return {}

    #urlformat

    #mysql search
    result = dbquerier.getModelAndKeywordAllDB("", hitconds)

    #adjust format
    result = adjustKeywordAllDB(result)

    return result


#
# like distinct...
#
# param
#   rowArr : [
#             [dbid,modelid,name,keyword]
#            ]
#
# return : [
#             {"dbid":dbid , "identifier":modelid , "name":name , "url":url , keyword:[keyword]}
#          ]
#
def adjustKeywordAllDB(rowArr):
    if rowArr is None:
        return

    urlformat = ""
    curdbid = ""
    models={} #{id : {id, name , keywords:{} }
    modelids=[]
    for row in rowArr:
        if row is None or len(row)<4:
            continue

        if row[0] is not None and curdbid != row[0]:
            curdbid = row[0]
            dbinfo = getTargetDBbyID(curdbid)
            if dbinfo is not None and dbinfo.get("urlformat") is not None:
                urlformat = dbinfo.get("urlformat")
            else:
                urlformat = settings.SEARCH_TARGET_DB.get("URLFORMAT_DEFAULT")

        model = {}
        addkey = str(curdbid) + "_" + row[1]
        if models.get(addkey) is None:
            model = { "dbid":curdbid
                     ,"dbname":dbinfo.get("dbname")
                     ,"id":row[1]
                     ,"name":row[2]
                     ,"keywords":{row[3]:row[3]}
                     ,"url":urlformat.format(row[1])
                     }
            modelids.append(addkey)
        else:
            model = models.get(addkey)
            words = model.get("keywords")
            words.update({row[3]:row[3]})
            model.update({"keywords":words})

        models.update({addkey:model})

    ret = []
    for key in modelids:
        row = models.get(key)
        if row is None:
            continue
#        sngrow = [row.get("id"),row.get("name"),row.get("keywords")]
        keyArr = []
        keymap = row.get("keywords")
        if keymap:
            for keykey in keymap:
                keyArr.append(keykey)

        sngrow = { "dbid":row.get("dbid")
                  ,"dbname":row.get("dbname")
                  ,"identifier":row.get("id")
                  ,"name":row.get("name")
                  ,"url":row.get("url")
                  ,"keywords" : keyArr
                 }

        ret.append(sngrow)


    return ret

# get DBID by dbname
def getDataBaseId(dbname):
    if dbname is None:
        return

    ids = dbquerier.getDataBaseId(dbname)
    retid = None
    for row in ids:
        retid = row[0]

    return retid


# get Target by dbid
# return{
#    "dbid"
#   ,"dbname"
#   ,"urlformat"
#   ,"createdate"
# }
def getTargetDBbyID(dbid):
    if dbid is None:
        return

    ret = None
    db =  dbquerier.getTargetDBbyId(dbid)
    if db is not None and len(db) > 3:
        ret = {
            "dbid" :     db[0]
           ,"dbname":    db[1]
           ,"urlformat" :db[2]
           ,"createdate":db[3]
        }
    return ret

# get Target by dbname
# return{
#    "dbid"
#   ,"dbname"
#   ,"urlformat"
#   ,"createdate"
# }
def getTargetDBbyName(dbname):
    if dbname is None:
        return

    ret = None
    db =  dbquerier.getTargetDBbyName(dbname)
    if db is not None and len(db) > 3:
        ret = {
            "dbid" :     db[0]
           ,"dbname":    db[1]
           ,"urlformat" :db[2]
           ,"createdate":db[3]
        }
    return ret

#
# return model list
#
def getModelList(dbID):
    qres = dbquerier.getModelList(dbID)
    ret={}

    curModelId = ""
    curKeywords=[]
    for row in qres:

        rowModelId = row["modelid"]
        if curModelId != rowModelId:
            curModelId = rowModelId

            addrow={}
            addrow["modelid"] = row["modelid"]
            addrow["name"] = row["name"]
            addrow["createdate"] = row["createdate"]
            curKeywords=[]
            addrow["keywords"] = curKeywords

            ret[rowModelId]=addrow

        if row["keyword"] is not None:
            keydic={ "keyword":row["keyword"]
                    ,"createdate":row["keyword_createdate"]
                    }
            curKeywords.append(keydic)

    return ret

#
# return keyword list for each model
#
def getKeywordList(dbID , modelId):
    qres = dbquerier.getKeywordList(dbID , modelId)
    ret=[]

    for row in qres:
        ret.append(row.get("keyword"))

    return ret

# insert or update model
def updatemodel(dbid , modelid , modelname):
    model = dbquerier.getModelbyId(dbid, modelid)

    if model is None:
        res = dbquerier.insertmodel(dbid , modelid , modelname)
    else:
        res = dbquerier.updatemodel(dbid , modelid , modelname)

    return res

# update models from csv string
def updatemodelsbylist(dbid , models):
    modelarr = models.split("\n")

    res = dbquerier.deleteallmodels(dbid)
    for row in modelarr:
        cmmindex = row.find(",")
        if cmmindex >= 0:
            modelid = row[0:cmmindex]
            name = row[cmmindex + 1:]

            updatemodel(dbid , modelid , name)

    return res

# update keywords from csv string
def updatekeywordsbylist(dbid , keywords):
    keyarr = keywords.split("\n")

    res = dbquerier.deleteallkeywords(dbid)
    for row in keyarr:
        cmmindex = row.find(",")
        if cmmindex >= 0:
            modelid = row[0:cmmindex]
            keyword = row[cmmindex + 1:]

            insertkeyword(dbid , modelid , keyword)

    return res

# insert keyword
def insertkeyword(dbid , modelid , keyword):
    res = []
    model = dbquerier.getModelbyId(dbid, modelid)
    if model is not None:
        keywordinfo = dbquerier.getKeywordbyId(dbid, modelid , keyword)
        if keywordinfo is None:
            res = dbquerier.insertkeyword(dbid , modelid , keyword)

    return res

# date object => date string
def dFormEach(obj,formatstr="%Y/%m/%d %H:%M:%S"):
    #print type(obj)

    if isinstance(obj, datetime.datetime):
        return obj .strftime('%Y/%m/%d %H:%M:%S')

    elif isinstance(obj, list):
        retobj = []
        for row in obj:
            retobj.append(dFormEach(row , formatstr))

        return retobj

    elif isinstance(obj, dict):
        retobj = {}
        for k, v in obj.iteritems():
            retobj[k] = dFormEach(v , formatstr)

        return retobj

    else:
        return obj


#generate sitelink_keyword
def genSitelink_keyword(srckey , conditions , linktype , alreadykeys):
    sepa="_,_"
    connector = dbquerier.getConnector()
    for hitcond in conditions:
        try:
            testkey = srckey + sepa + linktype + sepa + hitcond
            testkey = testkey.lower()
            if not alreadykeys.has_key(testkey):
                dbquerier.insertSitelink_keyword(connector ,srckey , linktype , hitcond)
                alreadykeys.update({testkey:testkey})
        except :
            print "Unexpected error:", sys.exc_info()[0]


def getDbinfo():
    sqldb = dbquerier.getTargetDBAll()
    dbinfo={}
    for row in sqldb:
        dbid = row.get("dbid")
        dbinfo.update({dbid:row})

    return dbinfo


def getDbModelinfo():
    dbmodelinfo ={}   #{dbid : { modelid : data}}
    sqlmodels = dbquerier.getModelAll()
    for row in sqlmodels:

        dbid = row.get("dbid")
        modelsinfo={}
        if dbmodelinfo.has_key(dbid):
            modelsinfo = dbmodelinfo.get(dbid)

        modelid = row.get("modelid")
        modelsinfo.update({modelid:row})

        dbmodelinfo.update({dbid:modelsinfo})

    return dbmodelinfo

#generate sitelink_keyword -> sitelink
def genSitelink(dbinfo , dbmodelinfo):
    res = dbquerier.deleteSitelink()
    sep = "_,_"

    keywordfromdb = dbquerier.getKeywordAll()
    keywordsInfo = {}
    for keyrow in keywordfromdb:
        keywordstr = keyrow.get("keyword")
        dbid = keyrow.get("dbid")
        modelid = keyrow.get("modelid")
        dbmodelid = str(dbid) + sep + modelid

        keywordData = keywordsInfo.get(keywordstr)
        if keywordData is None:
            keywordData = {dbmodelid : keyrow}
        else:
            keywordData.update({dbmodelid : keyrow})

        keywordsInfo.update({keywordstr : keywordData})

    keylinks = dbquerier.getSitelink_keywordAll()

    sitelink = {} # {type : { srcdbid_,_srcmodelid : {dstdbid_,_dstmodelid : data} # data = { ,,,,"keywords" : ...,...,...}
    for row in keylinks:
        if not row or not isinstance(row ,dict):
            continue

        linktype = keyrow.get("linktype")
        linkdata = sitelink.get(linktype)
        if linkdata is None:
            linkdata = {}

        srckeyword = keyrow.get("srckeyword")
        srckeywordedmodels = keywordsInfo(srckeyword)

        dstkeyword = keyrow.get("dstckeyword")
        dstkeywordedmodels = keywordsInfo(dstkeyword)

        if srckeywordedmodels is not None and dstkeywordedmodels is not None:
            for srckeywordedmodel in srckeywordedmodels:
                srcdbid = srckeywordedmodel.get("dbid")
                srcmodelid = srckeywordedmodel.get("modelid")

                srckey = str(srcdbid) + "_,_" + srcmodelid
                srcdata = linkdata.get(srckey)
                if srcdata is None:
                    srcdata = {}

                for dtskeywordedmodel in dstkeywordedmodels:
                    dstdbid = dtskeywordedmodel.get("dbid")
                    dstmodelid = dtskeywordedmodel.get("modelid")

                    dstkey = str(dstdbid) + "_,_" + dstmodelid
                    dstdata = srcdata.get(dstkey)
                    if dstdata is None:
                        dstdata = {}


#generate sitelink_keyword -> sitelink
def genSitelink_old(dbinfo , dbmodelinfo):
    res = dbquerier.deleteSitelink()

    keylinks = dbquerier.getGenerateSeed()

    cur_srcdbid = ""
    cur_srcdbname = ""
    cur_srcmodelid = ""
    cur_srcmodelname = ""
    cur_linktype = ""
    cur_dstdbid = ""
    cur_dstdbname = ""
    cur_dstmodelid = ""
    cur_dstmodelname = ""
    cur_dsturlformat = ""
    keywords = ""

    for row in keylinks:
        if not row or not isinstance(row ,dict):
            continue

        srcdbid = row.get("srcdbid")
        srcmodelid = row.get("srcmodelid")
        srckeyword = row.get("srckeyword")
        linktype = row.get("linktype")
        destkeyword = row.get("destkeyword")
        dstdbid = row.get("dstdbid")
        dstmodelid = row.get("dstmodelid")

        srcmodels={}
        if dbinfo.has_key(srcdbid):
            srcdbinfo = dbinfo.get(srcdbid)
            srcdbname = srcdbinfo.get("dbname")
            srcmodels = dbmodelinfo.get(srcdbid)

        if srcmodels.has_key(srcmodelid):
            srcmodelinfo = srcmodels.get(srcmodelid)
            srcmodelname = srcmodelinfo.get("name")

        dstmodels={}
        if dbinfo.has_key(dstdbid):
            dstdbinfo = dbinfo.get(dstdbid)
            dstdbname = dstdbinfo.get("dbname")
            dsturlformat = dstdbinfo.get("urlformat")
            dstmodels = dbmodelinfo.get(dstdbid)

        if dstmodels.has_key(dstmodelid):
            dstmodelinfo = dstmodels.get(dstmodelid)
            dstmodelname = dstmodelinfo.get("name")


        if    cur_srcdbid == srcdbid \
          and cur_srcmodelid == srcmodelid \
          and cur_linktype == linktype \
          and cur_dstdbid == dstdbid \
          and cur_dstmodelid == dstmodelid:
            keywords += "," + destkeyword

        else:
            if cur_srcdbid and cur_srcmodelid and cur_linktype and cur_dstdbid and cur_dstmodelid:
                if keywords:
                    keywords = keywords[1:]

                dbquerier.insertSitelink(
                    cur_srcdbid ,
                    cur_srcdbname ,
                    cur_srcmodelid ,
                    cur_srcmodelname ,
                    cur_linktype  ,
                    cur_dstdbid  ,
                    cur_dstdbname ,
                    cur_dstmodelid ,
                    cur_dstmodelname ,
                    keywords ,
                    cur_dsturlformat
                    )

            cur_srcdbid = srcdbid
            cur_srcdbname = srcdbname
            cur_srcmodelid = srcmodelid
            cur_srcmodelname = srcmodelname
            cur_linktype = linktype
            cur_dstdbid = dstdbid
            cur_dstdbname = dstdbname
            cur_dstmodelid = dstmodelid
            cur_dstmodelname = dstmodelname
            cur_dsturlformat = dsturlformat
            keywords = "," + destkeyword



    # insert last one
    if keywords:
        keywords = keywords[1:]

    dbquerier.insertSitelink(
        cur_srcdbid ,
        cur_srcdbname ,
        cur_srcmodelid ,
        cur_srcmodelname ,
        cur_linktype  ,
        cur_dstdbid  ,
        cur_dstdbname ,
        cur_dstmodelid ,
        cur_dstmodelname ,
        keywords ,
        cur_dsturlformat
        )


#generate sitelink_keyword -> sitelink_word
def genSitelink_word(dbinfo , dbmodelinfo):
    res = dbquerier.deleteSitelink_word()

    #keylinks = dbquerier.getGenerateSeed_word()
    keylinksCurdict = dbquerier.getGenerateSeed()
    if keylinksCurdict is None or keylinksCurdict.get("cursor") is not None:
        return

    cur_srckeyword = ""
    cur_dstkeyword = ""
    cur_linktype = ""
    cur_dstdbid = ""
    cur_dstdbname = ""
    cur_dstmodelid = ""
    cur_dstmodelname = ""
    cur_dsturlformat = ""
    keywords = ""

    #for row in keylinks:
    dbcursor  = keylinksCurdict.get("cursor")
    row = dbcursor.fetchone()
    while row is not None:
        if not row or not isinstance(row ,dict):
            continue

        srckeyword = row.get("srckeyword")
        linktype = row.get("linktype")
        destkeyword = row.get("destkeyword")
        dstdbid = row.get("dstdbid")
        dstmodelid = row.get("dstmodelid")

        dstmodels={}
        if dbinfo.has_key(dstdbid):
            dstdbinfo = dbinfo.get(dstdbid)
            dstdbname = dstdbinfo.get("dbname")
            dsturlformat = dstdbinfo.get("urlformat")
            dstmodels = dbmodelinfo.get(dstdbid)

        if dstmodels.has_key(dstmodelid):
            dstmodelinfo = dstmodels.get(dstmodelid)
            dstmodelname = dstmodelinfo.get("name")


        if    cur_dstkeyword == destkeyword \
          and cur_linktype == linktype \
          and cur_dstdbid == dstdbid \
          and cur_dstmodelid == dstmodelid:
            keywords += "," + destkeyword

        else:
            if cur_dstkeyword and cur_linktype and cur_dstdbid and cur_dstmodelid:
                if keywords:
                    keywords = keywords[1:]

                dbquerier.insertSitelink_word(
                    cur_dstkeyword ,
                    cur_linktype  ,
                    cur_dstdbid  ,
                    cur_dstdbname ,
                    cur_dstmodelid ,
                    cur_dstmodelname ,
                    cur_srckeyword ,
                    cur_dsturlformat
                    )

            cur_srckeyword = srckeyword
            cur_dstkeyword = destkeyword
            cur_linktype = linktype
            cur_dstdbid = dstdbid
            cur_dstdbname = dstdbname
            cur_dstmodelid = dstmodelid
            cur_dstmodelname = dstmodelname
            cur_dsturlformat = dsturlformat
            keywords = "," + destkeyword

        row = dbcursor.fetchone() #

    # insert last one
    if keywords:
        keywords = keywords[1:]

    dbquerier.insertSitelink_word(
        cur_dstkeyword ,
        cur_linktype  ,
        cur_dstdbid  ,
        cur_dstdbname ,
        cur_dstmodelid ,
        cur_dstmodelname ,
        cur_srckeyword ,
        cur_dsturlformat
        )



def genStatus():
    ret = False
    expiredHour = 1
    status = dbquerier.getGenStatus()
    if status is None:
        dbquerier.insertGenStatus('ON')
        ret = True
    else:
        if status.get("gen_status") != "ON" or status.get("gen_timediff") > expiredHour:
            dbquerier.updateGenStatus('ON')
            ret = True

    return ret


def getSitelink_word(queryArr):
    ret = {} #{linktype : {dbname:[data]} }  *{dbname:[data]} see 'translateForJS' return
    res = dbquerier.getSitelink_word(queryArr)

    for row in res:
        linktype = row.get("linktype")
        dstdbname = row.get("dstdbname")
        dsturlformat = row.get("dsturlformat")
        dstmodelid = row.get("dstmodelid")
        dstmodelname = row.get("dstmodelname")
        srckeyword = row.get("srckeyword")

        if not ret.get(linktype):
            ret.update({ linktype : {} })
        curtypes = ret.get(linktype)

        if not curtypes.get(dstdbname):
            curtypes.update({ dstdbname : {} })
        curdbs = curtypes.get(dstdbname)

        if not curdbs.get(dstmodelid):
            datarow = {
                       "id":dstmodelid
                       ,"name":dstmodelname
                       ,"url":dsturlformat.format(dstmodelid)
                       ,"keyword":{ srckeyword : srckeyword }
                       }
            curdbs.update({ dstmodelid : datarow})
        curmodel = curdbs.get(dstmodelid)

        curkeyword = curmodel.get("keyword")
        if  not curkeyword.get(srckeyword):
            curkeyword.update({ srckeyword : srckeyword })

    return ret


def getNeighbors(dbname , identifier):
    ret = {} #{linktype : {dbname:[data]} }  *{dbname:[data]} see 'translateForJS' return
    res = dbquerier.getNeighbors(dbname , identifier)

    for row in res:
        linktype = row.get("linktype")
        dstdbname = row.get("dstdbname")
        dsturlformat = row.get("dsturlformat")
        dstmodelid = row.get("dstmodelid")
        dstmodelname = row.get("dstmodelname")
        srckeyword = row.get("srckeyword")

        if not ret.get(linktype):
            ret.update({ linktype : {} })
        curtypes = ret.get(linktype)

        if not curtypes.get(dstdbname):
            curtypes.update({ dstdbname : {} })
        curdbs = curtypes.get(dstdbname)

        if not curdbs.get(dstmodelid):
            datarow = {
                       "id":dstmodelid
                       ,"name":dstmodelname
                       ,"url":dsturlformat.format(dstmodelid)
                       ,"keyword":{ srckeyword : srckeyword }
                       }
            curdbs.update({ dstmodelid : datarow})
        curmodel = curdbs.get(dstmodelid)

        curkeyword = curmodel.get("keyword")
        if  not curkeyword.get(srckeyword):
            curkeyword.update({ srckeyword : srckeyword })

    return ret





