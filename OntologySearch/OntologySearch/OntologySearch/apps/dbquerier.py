'''
Created on 2015/06/17

@author: adminstrator
'''
import MySQLdb
import sys
from django.conf import settings
from MySQLdb.cursors import DictCursor

def query(queryString , cursordict=False):
    return querycontents(queryString , cursordict , False)

def queryCommit(queryString , cursordict=False , connector=None):
    return querycontents(queryString , cursordict , True , connector)


def getConnector():
    dbconf = settings.SEARCH_TARGET_DB
    try:
        connector = MySQLdb.connect(host=dbconf.get("HOST") , db=dbconf.get("DATABASE") , user=dbconf.get("USER") , passwd=dbconf.get("PASSWD"), charset=dbconf.get("CHARSET"))
        return connector
    except:
        return None
#
# throw query
# return results array [ [col1,col2,col3,,,,],[col1,col2,col3,,,,],,,,, ]
def querycontents(queryString , cursordict , addcommit , defaultconnector=None):
    if queryString is None:
        return

    dbconf = settings.SEARCH_TARGET_DB
    chkq = queryString.strip().lower()
    try:
        if defaultconnector is not None:
            connector = defaultconnector
        else:
            connector = MySQLdb.connect(host=dbconf.get("HOST") , db=dbconf.get("DATABASE") , user=dbconf.get("USER") , passwd=dbconf.get("PASSWD"), charset=dbconf.get("CHARSET"))

        if cursordict:
            cursor = connector.cursor(DictCursor)
        else:
            cursor = connector.cursor()

        cursor.execute(queryString)
        result = cursor.fetchall()

        if addcommit and chkq[:6]!="select":
            connector.commit()

        ret = []
        for row in result:
            ret.append(row)

        cursor.close()

        if defaultconnector is None:
            connector.close()

        return ret

    except:
        print sys.exc_info()
        try:
            cursor.close()
        except:
            pass

        try:
            if defaultconnector is None:
                connector.close()
        except:
            pass

#
# throw query
# return first result [col1,col2,col3,,,,]
def firstrow(queryString, cursordict=False):

    result = query(queryString , cursordict)
    for row in result:
        return row;


#
# throw query without close (have to close at callee)
# return {"cursor":cursor , "connector" : connector}
def querycursor(queryString , cursordict , addcommit , defaultconnector=None):
    if queryString is None:
        return

    dbconf = settings.SEARCH_TARGET_DB
    chkq = queryString.strip().lower()
    try:
        if defaultconnector is not None:
            connector = defaultconnector
        else:
            connector = MySQLdb.connect(host=dbconf.get("HOST") , db=dbconf.get("DATABASE") , user=dbconf.get("USER") , passwd=dbconf.get("PASSWD"), charset=dbconf.get("CHARSET"))

        if cursordict:
            cursor = connector.cursor(DictCursor)
        else:
            cursor = connector.cursor()

        cursor.execute(queryString)

        if addcommit and chkq[:6]!="select":
            connector.commit()

        ret = {
             "cursor":cursor
            ,"connector":connector
        }
        return ret

    except:
        print sys.exc_info()
        try:
            cursor.close()
        except:
            pass

        try:
            if defaultconnector is None:
                connector.close()
        except:
            pass

        return {}

####
#### single table
####

##########################
## table'targetdb'
##

#
# return dbnames
#
def getDbNameList():


    sql =  "select dbname" \
           " from targetdb" \

    return query(sql)

#
# return dbid by dbname
#
def getDataBaseId(dbName):

    wherehit = MySQLdb.escape_string(dbName.encode("utf-8"))

    sql =  "select distinct dbid" \
           " from targetdb" \
           " where " \
           " lower(dbname) = '" + wherehit.lower() + "'"
#           " dbname = '" + wherehit + "'"

    return query(sql)

#
# return db info by dbid
#
def getTargetDBbyId(targetId):

    wherehit = ""
    if isinstance(targetId, (int, long, float, complex)):
        wherehit = str(targetId)
    else:
        wherehit = MySQLdb.escape_string(targetId.encode("utf-8"))

    sql =  "select dbid , dbname ,urlformat, createdate " \
           " from targetdb" \
           " where " \
           " dbid = '" + wherehit + "'"

    return firstrow(sql)

#
# return db info by dbname
#
def getTargetDBbyName(targetName ,cursordict=False):

    wherehit = MySQLdb.escape_string(targetName.encode("utf-8"))

    sql =  "select dbid , dbname ,urlformat, createdate " \
           " from targetdb" \
           " where " \
           " lower(dbname) = '" + wherehit.lower() + "'"
#           " dbname = '" + wherehit + "'"

    return firstrow(sql , cursordict)

#
# return db info by dbname
#
def getTargetDBAll():

    sql =  "select *  from targetdb"

    return query(sql ,True)

# update
def updateTargetDB(dbid ,  dbinfo):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    urlformat = MySQLdb.escape_string(str(dbinfo.get("urlformat")).encode("utf-8"))

    sql =  "update targetdb set " \
           " urlformat =  '" + urlformat + "'" \
           " where " \
           " dbid = '" + dbid + "'"

    return queryCommit(sql)


##########################
## table'model'
##

#
# return model info by id
#
def getModelbyId(dbID , modelId):

    dbid = MySQLdb.escape_string(str(dbID).encode("utf-8"))

    modelid = MySQLdb.escape_string(str(modelId).encode("utf-8"))

    sql =  "select dbid , modelid ,name, createdate " \
           " from model" \
           " where " \
               " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'"

    return firstrow(sql ,True)

#
# return all model info
#
def getModelAll():

    sql =  "select * from model" \

    return query(sql ,True)

#insert
def insertmodel(dbid , modelid , modelname):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelid).encode("utf-8"))
    modelname = MySQLdb.escape_string(str(modelname).encode("utf-8"))

    sql =  "insert model("\
           " dbid"\
           ",modelid"\
           ",name"\
           ",createdate"\
           ")values(" \
           "'" + dbid + "'" \
           ",'" + modelid + "'" \
           ",'" + modelname + "'" \
           ",now()" \
           ")"

    return queryCommit(sql)

# update
def updatemodel(dbid , modelid , modelname):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelid).encode("utf-8"))
    modelname = MySQLdb.escape_string(str(modelname).encode("utf-8"))

    sql =  "update model set " \
           " name =  '" + modelname + "'" \
           " where " \
           " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'"

    return queryCommit(sql)

#delete
def deletemodel(dbid , modelid):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelid).encode("utf-8"))

    sql =  "delete from model"\
           " where " \
           " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'"

    return queryCommit(sql)

#delete whole models by dbid
def deleteallmodels(dbid):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))

    sql =  "delete from model"\
           " where " \
           " dbid = '" + dbid + "'" \

    return queryCommit(sql)


##########################
## table'keyword'
##

#
# return keyword list for each model
#
def getKeywordList(dbID , modelId):
    dbid = MySQLdb.escape_string(str(dbID).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelId).encode("utf-8"))

    sql =  "select * " \
           " from keyword" \
           " where " \
               " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'" \

    return query(sql ,True)

def getKeywordAll():

    sql =  "select * " \
           " from keyword" \

    return query(sql ,True)

#
# return keyword list for each model
#
def getKeywordListDistinct():

    sql =  "select distinct keyword from keyword"

    return query(sql ,True)

#
# return keyword list for each model
#
def getNewKeywordListDistinct():

    sql =  "select distinct keyword from keyword" \
           " where keyword not in (select srckeyword from sitelink_keyword)"

    return query(sql ,True)

#
# return keyword info by id
#
def getKeywordbyId(dbID , modelId , keyword):

    dbid = MySQLdb.escape_string(str(dbID).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelId).encode("utf-8"))
    keyword = MySQLdb.escape_string(str(keyword).encode("utf-8"))

    sql =  "select dbid , modelid ,keyword, createdate " \
           " from keyword" \
           " where " \
               " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'" \
           " and keyword = '" + keyword + "'"

    return firstrow(sql ,True)

#insert
def insertkeyword(dbid , modelid , keyword):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelid).encode("utf-8"))
    keyword = MySQLdb.escape_string(str(keyword).encode("utf-8"))

    sql =  "insert keyword("\
           " dbid"\
           ",modelid"\
           ",keyword"\
           ",createdate"\
           ")values(" \
           "'" + dbid + "'" \
           ",'" + modelid + "'" \
           ",'" + keyword + "'" \
           ",now()" \
           ")"

    return queryCommit(sql)

#delete
def deletekeyword(dbid , modelid , keyword ):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelid).encode("utf-8"))
    keyword = MySQLdb.escape_string(str(keyword).encode("utf-8"))

    sql =  "delete from keyword"\
           " where " \
           " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'" \
           " and keyword = '" + keyword + "'"

    return queryCommit(sql)

#delete keywords by modelid
def deletekeywords(dbid , modelid ):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))
    modelid = MySQLdb.escape_string(str(modelid).encode("utf-8"))

    sql =  "delete from keyword"\
           " where " \
           " dbid = '" + dbid + "'" \
           " and modelid = '" + modelid + "'" \

    return queryCommit(sql)

#delete keywords by db
def deleteallkeywords(dbid):

    dbid = MySQLdb.escape_string(str(dbid).encode("utf-8"))

    sql =  "delete from keyword"\
           " where " \
           " dbid = '" + dbid + "'" \

    return queryCommit(sql)

##########################
## table'token'
##

#
# return token info
#
def getEnabledToken(token ,dbname , ipaddress):

    token = MySQLdb.escape_string(str(token).encode("utf-8"))
    dbname = MySQLdb.escape_string(str(dbname).encode("utf-8"))
    ipaddress = MySQLdb.escape_string(str(ipaddress).encode("utf-8"))

    sql =  "select t.* " \
           " from token t , userdb ud ,targetdb td" \
           " where " \
               " t.userid = ud.userid " \
           " and ud.dbid = td.dbid " \
           " and t.token = '" + token + "'" \
           " and t.ipaddress = '" + ipaddress + "'"\
           " and lower(td.dbname) = '" + dbname.lower() + "'"
#           " and td.dbname = '" + dbname + "'"

    return firstrow(sql ,True)


#
# return user info by id
#
def getTakenToken(token):

    token = MySQLdb.escape_string(str(token).encode("utf-8"))

    sql =  "select * " \
           " from token" \
           " where " \
               " token = '" + token + "'"

    return firstrow(sql ,True)

#insert
def insertToken(token , userid ,ipaddress):

    token = MySQLdb.escape_string(str(token).encode("utf-8"))
    userid = MySQLdb.escape_string(str(userid).encode("utf-8"))
    ipaddress = MySQLdb.escape_string(str(ipaddress).encode("utf-8"))

    sql =  "insert into token("\
           " token " \
           ",userid " \
           ",ipaddress " \
           ",createdate " \
           ",expiredate " \
           ")values(" \
           " '" + token + "'" \
           ",'" + userid + "'" \
           ",'" + ipaddress + "'" \
           ", now()" \
           ", now() + INTERVAL 1 HOUR" \
           ")"

    return queryCommit(sql)

#delete expired token
def deleteExpiredToken():
    sql = "delete from token where expiredate < now()"
    return queryCommit(sql)


##########################
## table'sitelink','sitelink_keyword' ,'sitelink_word'
##
def getSitelink_word(queryArr):
    wordstr = ""
    for row in queryArr:
        wordstr += ",'" + MySQLdb.escape_string(str(row).encode("utf-8")) + "'"

    if wordstr:
        wordstr = wordstr[1:]

    sql = "select * " \
        " from sitelink_word " \
        " where srckeyword in(" + wordstr + ")" \
        " order by  linktype , dstdbname , dstmodelid , dstmodelname , srckeyword" \

    return query(sql , True)

def getSitelink_keywordAll():

    sql = "select * " \
        " from sitelink_keyword " \

    return query(sql , True)

def getNeighbors(dbname , identifier):
    dbname = MySQLdb.escape_string(dbname.encode("utf-8"))
    identifier = MySQLdb.escape_string(identifier.encode("utf-8"))

    sql = "select * " \
        " from sitelink " \
        " where lower(srcdbname) = '" + dbname.lower() + "'" \
        "   and srcmodelid = '" + identifier + "'" \
        " order by  linktype , dstdbname , dstmodelid , dstmodelname " \

    return query(sql , True)

def deleteSitelink():

    sql =  "delete from sitelink"

    return queryCommit(sql)

def deleteSitelink_keyword():

    sql =  "delete from sitelink_keyword"

    return queryCommit(sql)

def deleteSitelink_word():

    sql =  "delete from sitelink_word"

    return queryCommit(sql)

#insert
def insertSitelink(
    srcdbid ,
    srcdbname ,
    srcmodelid ,
    srcmodelname ,
    linktype  ,
    dstdbid  ,
    dstdbname ,
    dstmodelid ,
    dstmodelname ,
    keywords ,
    dsturlformat
    ):

    srcdbid = MySQLdb.escape_string(str(srcdbid).encode("utf-8"))
    srcdbname = MySQLdb.escape_string(str(srcdbname).encode("utf-8"))
    srcmodelid = MySQLdb.escape_string(str(srcmodelid).encode("utf-8"))
    srcmodelname = MySQLdb.escape_string(str(srcmodelname).encode("utf-8"))
    linktype = MySQLdb.escape_string(str(linktype).encode("utf-8"))
    dstdbid = MySQLdb.escape_string(str(dstdbid).encode("utf-8"))
    dstdbname = MySQLdb.escape_string(str(dstdbname).encode("utf-8"))
    dstmodelid = MySQLdb.escape_string(str(dstmodelid).encode("utf-8"))
    dstmodelname = MySQLdb.escape_string(str(dstmodelname).encode("utf-8"))
    keywords = MySQLdb.escape_string(str(keywords).encode("utf-8"))
    dsturlformat = MySQLdb.escape_string(str(dsturlformat).encode("utf-8"))

    sql =  "insert into sitelink(" \
           " srcdbid ," \
           " srcdbname ," \
           " srcmodelid ," \
           " srcmodelname ," \
           " linktype  ," \
           " dstdbid  ," \
           " dstdbname ," \
           " dstmodelid ," \
           " dstmodelname ," \
           " keywords , " \
           " dsturlformat " \
           ")values(" \
           " '" + srcdbid + "'" \
           ",'" + srcdbname + "'" \
           ",'" + srcmodelid + "'" \
           ",'" + srcmodelname + "'" \
           ",'" + linktype + "'" \
           ",'" + dstdbid + "'" \
           ",'" + dstdbname + "'" \
           ",'" + dstmodelid + "'" \
           ",'" + dstmodelname + "'" \
           ",'" + keywords + "'" \
           ",'" + dsturlformat + "'" \
           ")"

    return queryCommit(sql)

def insertSitelink_keyword(connector , srckeyword , linktype ,destkeyword):

    srckeyword = MySQLdb.escape_string(str(srckeyword).encode("utf-8"))
    linktype = MySQLdb.escape_string(str(linktype).encode("utf-8"))
    destkeyword = MySQLdb.escape_string(str(destkeyword).encode("utf-8"))

    sql =  "insert into sitelink_keyword("\
           " srckeyword " \
           ",linktype " \
           ",destkeyword " \
           ")values(" \
           " '" + srckeyword + "'" \
           ",'" + linktype + "'" \
           ",'" + destkeyword + "'" \
           ")"

    return queryCommit(sql , False , connector)

def insertSitelink_word(
    srckeyword ,
    linktype  ,
    dstdbid  ,
    dstdbname ,
    dstmodelid ,
    dstmodelname ,
    basekeyword ,
    dsturlformat
    ):

    srckeyword = MySQLdb.escape_string(str(srckeyword).encode("utf-8"))
    linktype = MySQLdb.escape_string(str(linktype).encode("utf-8"))
    dstdbid = MySQLdb.escape_string(str(dstdbid).encode("utf-8"))
    dstdbname = MySQLdb.escape_string(str(dstdbname).encode("utf-8"))
    dstmodelid = MySQLdb.escape_string(str(dstmodelid).encode("utf-8"))
    dstmodelname = MySQLdb.escape_string(str(dstmodelname).encode("utf-8"))
    basekeyword = MySQLdb.escape_string(str(basekeyword).encode("utf-8"))
    dsturlformat = MySQLdb.escape_string(str(dsturlformat).encode("utf-8"))

    sql =  "insert into sitelink_word(" \
           " srckeyword ," \
           " linktype  ," \
           " dstdbid  ," \
           " dstdbname ," \
           " dstmodelid ," \
           " dstmodelname, " \
           " basekeyword ," \
           " dsturlformat " \
           ")values(" \
           " '" + srckeyword + "'" \
           ",'" + linktype + "'" \
           ",'" + dstdbid + "'" \
           ",'" + dstdbname + "'" \
           ",'" + dstmodelid + "'" \
           ",'" + dstmodelname + "'" \
           ",'" + basekeyword + "'" \
           ",'" + dsturlformat + "'" \
           ")"

    return queryCommit(sql)

# for sitelink_ctl
def getGenStatus():
    sql =  "select * " \
        " ,TIMESTAMPDIFF(HOUR, gen_date ,now()) gen_timediff " \
        " from sitelink_ctl where row_id = 0 "

    return firstrow(sql ,True)

def insertGenStatus(status):
    sql =  "insert into sitelink_ctl(row_id , gen_status , gen_date) "\
        "values( 0 , '" + status + "' , now() )"

    return queryCommit(sql)

def updateGenStatus(status):
    sql =  "update sitelink_ctl set "\
        " gen_status = '" + status + "'"\
        ",gen_date = now() " \
        " where row_id = 0"

    return queryCommit(sql)


####
#### queries
####

#
# keyword search
#
# param
#   keywordArr : array of keyword
#
# return m.modelid,m.name
#
def getModelByKeyword(keywordArr):
    qarr = []
    for row in keywordArr:
        if row is None:
            continue

        rowvar = MySQLdb.escape_string(row.lower().encode("utf-8"))

        qarr.append(",'")
        qarr.append(rowvar)
        qarr.append("'")

    wherehit = "".join(qarr)
    if len(wherehit) > 0:
        wherehit = wherehit[1:]


    sql =  "select distinct m.modelid,m.name"
    sql += " from model m "
    sql += "  ,keyword k "
    sql += " where "
    sql += " m.modelid = k.modelid "
    sql += " and lower(k.keyword) in (" +  wherehit + ")"

    return query(sql)


#
# keyword search
#
# param
#   dbid  : where is a target
#   keywordArr : array of keyword
#
# return m.modelid,m.name
#
def getModelAndKeyword(dbid , keywordArr):
    qarr = []
    for row in keywordArr:
        if row is None:
            continue

        rowvar = MySQLdb.escape_string(row.lower().encode("utf-8"))

        qarr.append(",'")
        qarr.append(rowvar)
        qarr.append("'")

    wherehit = "".join(qarr)
    if len(wherehit) > 0:
        wherehit = wherehit[1:]

    dbcond = MySQLdb.escape_string(dbid)

    #sql =  "select distinct m.modelid,m.name , k.keyword"
    sql =  "select distinct m.dbid, m.modelid,m.name , k.keyword"
    sql += " from model m "
    sql += "  ,keyword k "
    sql += " where "
    sql += " m.dbid = " + dbcond
    sql += " and m.modelid = k.modelid "
    sql += " and lower(k.keyword) in (" +  wherehit + ")"
    sql += " order by m.modelid "

    return query(sql)

#
# keyword search
#
# param
#   dbid  : where is a target
#   keywordArr : array of keyword
#
# return m.modelid,m.name
#
def getModelAndKeywordAllDB(dbid ,keywordArr):
    qarr = []
    for row in keywordArr:
        if row is None:
            continue

        rowvar = MySQLdb.escape_string(row.lower().encode("utf-8"))

        qarr.append(",'")
        qarr.append(rowvar)
        qarr.append("'")

    wherehit = "".join(qarr)
    if len(wherehit) > 0:
        wherehit = wherehit[1:]

    sql =  "select distinct m.dbid , m.modelid,m.name , k.keyword"
    sql += " from model m "
    sql += "  ,keyword k "
    sql += " where true "
    if dbid :
        dbcond = MySQLdb.escape_string(dbid)
        sql += " and m.dbid = " + dbcond

    sql += " and m.modelid = k.modelid "
    sql += " and lower(k.keyword) in (" +  wherehit + ")"
    sql += " order by m.modelid "

    return query(sql)

#
# return user info by user, db ,id
#
def getUserByDB(dbID , userName , password):

    dbid = MySQLdb.escape_string(str(dbID).encode("utf-8"))
    username = MySQLdb.escape_string(str(userName).encode("utf-8"))
    password = MySQLdb.escape_string(str(password).encode("utf-8"))

    sql =  "select u.* " \
           " from user u , userdb ud" \
           " where " \
               " u.userid = ud.userid" \
           " and ud.dbid = '" + dbid + "'" \
           " and u.username = '" + username + "'" \
           " and u.password = '" + password + "'"

    return firstrow(sql ,True)

#
# return model list (with keywordlist)
#
def getModelList(dbID):

    dbid = MySQLdb.escape_string(str(dbID).encode("utf-8"))

    sql =  "select m.* ,k.keyword , k.createdate keyword_createdate " \
           " from model m " \
           " left join  keyword k " \
             " on  m.dbid=k.dbid " \
             " and m.modelid = k.modelid " \
           " where m.dbid = '" + dbid + "'" \
           " order by m.dbid , m.modelid "

    return query(sql ,True)

# for generate
def getGenerateSeed():
    sql =  "select " \
            " srck.dbid srcdbid " \
            ",srck.modelid srcmodelid " \
            ",srck.keyword srckeyword " \
            ",sk.linktype " \
            ",sk.destkeyword " \
            ",dstk.dbid dstdbid " \
            ",dstk.modelid dstmodelid " \
          " from " \
                " sitelink_keyword sk " \
                ",keyword srck " \
                ",keyword dstk " \
          " where  srck.keyword = sk.srckeyword " \
               " and dstk.keyword = sk.destkeyword " \
               " and !(    dstk.dbid = srck.dbid " \
                     " and dstk.modelid = srck.modelid " \
                     " ) "
#          " order by sk.linktype , srck.dbid , srck.modelid , dstk.dbid , dstk.modelid , sk.srckeyword ,sk.destkeyword "

    #return query(sql ,True)
    return querycursor(sql ,False , False)


def getGenerateSeed_word():
    sql =  "select distinct" \
            " sk.srckeyword " \
            ",sk.linktype " \
            ",sk.destkeyword " \
            ",dstk.dbid dstdbid " \
            ",dstk.modelid dstmodelid " \
        " from " \
            " sitelink_keyword sk " \
            " ,keyword dstk  " \
        " where  dstk.keyword = sk.destkeyword " \
        " order by sk.linktype , sk.srckeyword, dstk.dbid , dstk.modelid " \

    #return query(sql ,True)
    return querycursor(sql ,True , False)


