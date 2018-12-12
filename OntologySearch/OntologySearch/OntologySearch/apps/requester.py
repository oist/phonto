import dber

def getParam(name , request , options):
    method = request.method
    queryString = None
    if options.get(name) is not None:
        queryString = options.get(name)

    elif method == 'POST':
        queryString = request.POST.get(name)

    else:
        queryString = request.GET.get(name)


    return queryString

def getParamList(name , request , options):
    method = request.method
    queryString = None
    if options.get(name) is not None:
        queryString = options.getlist(name)

    elif method == 'POST':
        queryString = request.POST.getlist(name)

    else:
        queryString = request.GET.getlist(name)


    return queryString

# get param from request or options
def getQueryWord(request , options):
    queryString = None
    if options.get("word") is not None:
        queryString = options.get("word")
    else:
        queryString = request.POST.get("query")

    return queryString

# get DBID by "dbname"
def getDbId(request , options):
    retid = None
    queryString = getParam("dbname" , request , options)

    if queryString is None :
        retid = "1"
    else:
        retid = dber.getDataBaseId(queryString)
        retid = str(retid)

    return retid

# get DBID and Word by request
# return{
#   "dbid":dbid or default(phdatabase)
#  ,"word":word
#  ,"wrongdb":true/false
# }
def getDbIdAndWord(request , options):
    retid = None
    retword = None
    wrongdb = False

    firstOP = getParam("dbname" , request , options)

    secondOP = getQueryWord(request , options)

    dbid =  dber.getDataBaseId(firstOP)
    if firstOP is not None:
        if secondOP is not None :
            # url: ...searchdb/{dbname}/{word}
            retword = secondOP
            if dbid is not None:
                # url: ...searchdb/{dbname(correct)}/{word}
                retid = str(dbid)
            else:
                # url: ...searchdb/{dbname(error)}/{word}
                retid = "1"
                wrongdb = True
        else:
            # url: ...searchdb/{dbname}  or ...searchdb/{word}
            if dbid is not None:
                # url: ...searchdb/{dbname(correct)}
                retid = str(dbid)
            else:
                # url: ...searchdb/{word}
                retid = "1"
                retword = firstOP

    else:
        retid = "1"
        if secondOP is not None :
            retword = secondOP

    return {"dbid":retid , "word":retword , "wrongdb":wrongdb}

# get dbname ,modelid , modelname , keyword , token
# by request
# return{
#    "dbname":dbname
#   ,"modelid":modelid
#   ,"modelname":modelname
#   ,"keyword":keyword
#   ,"token":token
# }
def getDbMargeParam(request , options):

    dbname = getParam("dbname" , request , options)
    modelid = getParam("modelid" , request , options)
    modelname = getParam("modelname" , request , options)
    keyword = getParam("keyword" , request , options)
    token = getParam("token" , request , options)

    return{
        "dbname":dbname
       ,"modelid":modelid
       ,"modelname":modelname
       ,"keyword":keyword
       ,"token":token
    }

# get auth param
# by request
# return{
#        "username":username
#       ,"password":password
#       ,"email":email
#       ,"token":token
#       ,"dbname":dbname
# }
def getAuthParam(request , options):

    username = getParam("username" , request , options)
    password = getParam("password" , request , options)
    email = getParam("email" , request , options)
    token = getParam("token" , request , options)
    dbname = getParam("dbname" , request , options)

    return{
        "username":username
       ,"password":password
       ,"email":email
       ,"token":token
       ,"dbname":dbname
    }
