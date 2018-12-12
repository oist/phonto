'''
Created on 2015/06/17

@author: adminstrator
'''

from OntologySearch.apps import response_success
from OntologySearch.apps import response_badrequest
from OntologySearch.apps import response_forbidden

import dbquerier
import requester
import datetime
import random

#
# param
#     request{
#             "username":username ,
#             "dbname":dbname ,
#             "password":password (MD5 nize)
#            }
#
def gettoken (request , **options):
    dbquerier.deleteExpiredToken()

    params = requester.getAuthParam(request , options)
    username = params.get("username")
    password = params.get("password")
    dbname = params.get("dbname")
    remaddr = request.META.get("REMOTE_ADDR")

    if username is None or password is None or dbname is None:
        return response_badrequest(request)

    #confirm DB exists
    qualified = False
    dbinfo = dbquerier.getTargetDBbyName(dbname ,True)
    if dbinfo is not None and dbinfo.get("dbid") is not None:
        dbid = dbinfo.get("dbid")
        #confirm user exists
        userinfo = dbquerier.getUserByDB(dbid , username , password)
        if userinfo is not None and userinfo.get("userid") is not None:
            qualified = True
            userid = userinfo.get("userid")
            curdate = datetime.datetime.now()
            expiredate = curdate + datetime.timedelta(hours=1)
            #insert
            token = newToken()
            dbquerier.insertToken(token, userid, remaddr)

    if qualified == False:
        return response_forbidden(request)

    request.session['username'] = username
    request.session['token'] = token
    request.session['dbname'] = dbname

    return response_success(request, payload={
        'token' : token ,
        'expiredate':expiredate.strftime('%Y/%m/%d %H:%M')
    })

#
#
#
def newToken ():
    repeat = True
    outstr = ""
    while repeat:
        outstr = randomstr(20)
        takentoken = dbquerier.getTakenToken(outstr)
        if(takentoken is None):
            repeat = False

    return outstr

#
#
#
def randomstr (maxlen = 1 , strtype=0):
    ret = ""
    randomstr = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    if strtype==1:
        randomstr = "0123456789"
    elif strtype==2:
        randomstr = "0123456789abcdef"

    retlen = 0
    while retlen< maxlen :
        ret += random.choice(randomstr)
        retlen = len(ret)

    return ret

#
#
#
def checkTokenEnabledByRequest (request , options):
    params = requester.getAuthParam(request , options)
    token = params.get("token")
    dbname = params.get("dbname")
    remaddr = request.META.get("REMOTE_ADDR")

    return checkTokenEnabled(token , dbname , remaddr)

#
#
#
def checkTokenEnabled (token , dbname , ipaddres):
    dbquerier.deleteExpiredToken()
    tokeninfo = dbquerier.getEnabledToken(token , dbname , ipaddres)
    if tokeninfo is not None:
        return True
    else:
        return False


