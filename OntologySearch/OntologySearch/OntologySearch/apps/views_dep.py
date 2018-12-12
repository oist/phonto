## it's old
from OntologySearch.apps import response_success
import sparqler
import spquerier

import cgitb
cgitb.enable()

# get param from request or options
def getQueryWord(request , options):
    queryString = None
    if options.get("word") is not None:
        queryString = options.get("word")
    else:
        queryString = request.POST.get("query")

    return queryString


###############################
### deplicated functions
'''
def get_complete (request):
    queryString = request.POST["query"]

    limitcnt = request.POST.get("limit")
    ret = spquerier.labelcomplete(queryString , limitcnt)

    return response_success(request, payload={
        'result' : ret,
    })
'''
def query (request):
    queryString = request.POST["query"]

    ret = spquerier.query(queryString )

    return response_success(request, payload={
        'result' : ret,
    })

def getCanditates (request , **options):
    queryString = getQueryWord(request , options)

    if queryString is None or queryString == "":
        ret = {}
    else:
        ret = sparqler.getCandidate(queryString)

    return response_success(request, payload={
        'result' : ret,
    })

### deplicated functions end
###############################
'''
import rdfreader
def sync_owl (request):

    ret = rdfreader.syncowl();

    return response_success(request, payload={
        'result' : ret,
    })
'''

