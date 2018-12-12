'''
Created on 2015/06/17

@author: adminstrator
'''
import httplib
import urllib
import sys
import json
from django.conf import settings

exactSynonymListStr = "obo_annot:synonym,oboInOwl:hasExactSynonym,oboInOwl:hasBroadSynonym"
relatedSynonymListStr = "oboInOwl:hasRelatedSynonym"

#send query
#return json-like string
def query(queryString):

    fusekiurl = settings.FUSEKI_URL
    prot = fusekiurl.get("PROTOCOL").lower()
    hostname = fusekiurl.get("HOST")
    port = fusekiurl.get("PORT")
    sourceaddress = fusekiurl.get("SOURCE_ADDRESS")
    params = urllib.urlencode( { "query": queryString } )

    if prot == 'https':
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/sparql-results+json"}
        try:
            conn = httplib.HTTPSConnection(hostname, port)
            conn.request("POST", sourceaddress, params, headers)

            response = conn.getresponse()
            if response.status != 200:
                print response.status, response.reason

            #data(json string)
            data = response.read()
            conn.close()

            return jsonbindings(data)

        except:
            #print "Unexpected error:", sys.exc_info()[0]
            return {"queryError":sys.exc_info()[0]}

    else:
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/sparql-results+json"}
        try:
            conn = httplib.HTTPConnection(hostname, port)
            conn.request("POST", sourceaddress, params, headers)

            response = conn.getresponse()
            if response.status != 200:
                print response.status, response.reason

            #data(json string)
            data = response.read()
            conn.close()

            return jsonbindings(data)

        except:
            #print "Unexpected error:", sys.exc_info()[0]
            return {"queryError":sys.exc_info()[0]}

# translate sparqle result to json
def jsonbindings(queryresponce):
    if queryresponce is None:
        return None

    bindings = {}
    if queryresponce is not None:
        qresj = json.loads(queryresponce)
        if qresj is not None:
            jresults = qresj.get("results")
            if jresults is not None:
                bindings = jresults.get("bindings")

    return bindings

# return fuseki escape string
# "a'b" -> "a\\'b"
def fusekiC(srcChar):
    ret = srcChar.replace("'", "\\'")
    return ret

# retun constraint prefixes string(base)
def baseprefix():
    qarr = []
    for row in settings.BASEPREFIX:
        if row is not None and row.get("prefix") is not None and row.get("uri") is not None:
            qarr.append("prefix ")
            qarr.append(row.get("prefix"))
            qarr.append(":<")
            qarr.append(row.get("uri"))
            qarr.append("> ")

    qstring = "".join(qarr)
    return qstring

# retun constraint prefixes string(all)
def allprefix():
    qarr = []
    qarr.append(baseprefix())
    for row in settings.OWLPREFIX:
        if row is not None and row.get("prefix") is not None and row.get("uri") is not None:
            qarr.append("prefix ")
            qarr.append(row.get("prefix"))
            qarr.append(":<")
            qarr.append(row.get("uri"))
            qarr.append("> ")

    qstring = "".join(qarr)
    return qstring

# translate prefixed string if exists
# e.g. "http://purl.obolibrary.org/obo/UBERON_000210" -> "owl2:UBERON_0002101"
# e.g. "http://hoge.foga/baa" -> "<http://hoge.foga/baa>"
def prefixedString(url):
    ret = "<" + url + ">"
    curlen = 0
    for row in settings.BASEPREFIX:
        if row is not None and row.get("prefix") is not None and row.get("uri") is not None:
            testuri = row.get("uri")
            if url.startswith(testuri) and curlen < len(testuri):
                curlen = len(testuri)
                ret = row.get("prefix") + ":" + url[curlen :]
                ret = ret.replace("#", "\#")


    for row in settings.OWLPREFIX:
        if row is not None and row.get("prefix") is not None and row.get("uri") is not None:
            testuri = row.get("uri")
            if url.startswith(testuri) and curlen < len(testuri):
                curlen = len(testuri)
                ret = row.get("prefix") + ":" + url[curlen :]
                ret = ret.replace("#", "\#")

    return ret

####################################################################################################################
##
## sparqles autocomplete
##

# for autocomplete 1
# return array of names
def labelcomplete_synonym(namepart  , limitcnt):
    if limitcnt is None:
        limitcnt=settings.LIMIT_COMPLETE

    spq = []
    spq.append("SELECT DISTINCT ?synonym ")
    spq.append(" WHERE { ")
    spq.append("  ?class a owl:Class; ")
    spq.append("      rdfs:label ?classlabel; ")
    spq.append("      ?p ?synonym. ")
    spq.append("  filter (?p in(rdfs:label,")
    spq.append(exactSynonymListStr)
    spq.append(")) ")
    spq.append("  FILTER regex (?synonym,'^")
    spq.append(fusekiC(namepart))
    spq.append("','i')")
    spq.append(".} limit ")
    spq.append(str(limitcnt))

    spqstring = "".join(spq)
    qstring = allprefix() + spqstring
    print spqstring
    qres = query(qstring )

    ret = []
    if qres is not None:
        for row in qres:
            o = row.get("synonym")
            otype = o.get("type")
            if otype == "typed-literal" or otype == "literal":
                val = o.get("value")
                ret.append(val)

    return ret


####################################################################################################################
##
## sparqles
##

# get child terms
def getChildren(parentns  ):
    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label ?parent ?parentlabel")
    qarr.append(" WHERE{")
    qarr.append("  ?class ")
    qarr.append("    a owl:Class; ")
    qarr.append("    rdfs:label ?label; ")
    qarr.append("    rdfs:subClassOf <")
    qarr.append(parentns)
    qarr.append(">. <")
    qarr.append(parentns)
    qarr.append("> rdfs:label ?parentlabel. ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get child terms (by class'es')
def getChildrenAll(classUriArr):
    if classUriArr is None:
        return;

    classList = []
    for classuri in classUriArr:
        classList.append(",")
        classList.append(prefixedString(classuri))

    classListStr = "".join(classList)
    if len(classListStr)>0:
        classListStr = classListStr[1:]

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label ?parent ?parentlabel")
    qarr.append(" WHERE{")
    qarr.append("  ?class ")
    qarr.append("    a owl:Class; ")
    qarr.append("    rdfs:label ?label; ")
    qarr.append("    rdfs:subClassOf ?parent .")
    qarr.append("  ?parent rdfs:label ?parentlabel. ")
    qarr.append("  filter (?parent in(")
    qarr.append(classListStr)
    qarr.append(")) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get child terms with synonym (by class'es')
def getChildrenAllWithSynonym(classUriArr):
    if classUriArr is None:
        return;

    classList = []
    for classuri in classUriArr:
        classList.append(",")
        classList.append(prefixedString(classuri))

    classListStr = "".join(classList)
    if len(classListStr)>0:
        classListStr = classListStr[1:]

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label ?parent ?parentlabel ?synonym ?relsyn ")
    qarr.append(" WHERE{")
    qarr.append("  ?class ")
    qarr.append("    a owl:Class; ")
    qarr.append("    rdfs:label ?label; ")
    qarr.append("    rdfs:subClassOf ?parent .")
    qarr.append("  optional{")
    qarr.append("    ?class ?p ?synonym .")
    qarr.append("    filter(?p in (")
    qarr.append(exactSynonymListStr)
    qarr.append("    ))")
    qarr.append("  }")

    qarr.append("  ?parent rdfs:label ?parentlabel. ")
    qarr.append("  filter (?parent in(")
    qarr.append(classListStr)
    qarr.append(")) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get class by label
def getClassByLabel(label  ):
    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label")
    qarr.append(" WHERE{")
    qarr.append("  ?class a owl:Class.")
    qarr.append("  ?class rdfs:label ?label.")
    qarr.append("  FILTER regex (?label, '^")
    qarr.append(fusekiC(label))
    qarr.append(" *$','i')")
    qarr.append(".} limit 10")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get class by label or synonym
def getClassByLabelSynonym(label ,limitcnt):
    if limitcnt is None:
        limitcnt=settings.LIMIT_SPARQL

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label ")
    qarr.append(" WHERE { ")
    qarr.append("  ?class a owl:Class; ")
    qarr.append("      rdfs:label ?label; ")
    qarr.append("      ?p ?synonym. ")
#    qarr.append("  filter (?p in(rdfs:label, obo_annot:synonym, core:example , oboInOwl:hasExactSynonym)) ")
    qarr.append("  filter (?p in(rdfs:label,")
    qarr.append(exactSynonymListStr)
    qarr.append(")) ")
    qarr.append("  FILTER regex (?synonym,'^")
    qarr.append(fusekiC(label))
    qarr.append(" *$','i')")
    qarr.append(".} limit ")
    qarr.append(str(limitcnt))

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get parent
def getClassParent(namespace):

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label ?parent ?parentlabel")
    qarr.append(" WHERE{<")
    qarr.append(namespace)
    qarr.append(">  a owl:Class; ")
    qarr.append("   rdfs:label ?label; ")
    qarr.append("   rdfs:subClassOf ?parent. ")
    qarr.append(" ?parent rdfs:label ?parentlabel. ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get parent (by class'es')
def getClassParentAll(classUriArr):
    if classUriArr is None:
        return;

    classList = []
    for classuri in classUriArr:
        classList.append(",")
        classList.append(prefixedString(classuri))

    classListStr = "".join(classList)
    if len(classListStr)>0:
        classListStr = classListStr[1:]

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?label ?parent ?parentlabel")
    qarr.append(" WHERE{")
    qarr.append("  ?class")
    qarr.append("    a owl:Class; ")
    qarr.append("   rdfs:label ?label; ")
    qarr.append("   rdfs:subClassOf ?parent. ")
    qarr.append(" ?parent rdfs:label ?parentlabel. ")
    qarr.append("  filter (?class in(")
    qarr.append(classListStr)
    qarr.append(")) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get contents
def getContents(namespace):
    if namespace is None:
        return;

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT *")
    qarr.append(" WHERE{ ?s ?p ?o .")
    qarr.append(" filter(?s = <")
    qarr.append(namespace)
    qarr.append(">) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get synonym
def getSynonyms(namespace):
    if namespace is None:
        return;

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?synonym ")
    qarr.append(" WHERE{ <")
    qarr.append(namespace)
    qarr.append("> ?p ?synonym; ")
    qarr.append(" rdfs:label ?classlabel. ")
    qarr.append("  filter (?p in(")
    qarr.append(exactSynonymListStr)
    qarr.append(")) ")
    qarr.append(" filter (?synonym != ?classlabel) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


#exact synonyms
def getSynonymsAllContents(classUriArr):
    if classUriArr is None:
        return;

    classList = []
    for classuri in classUriArr:
        classList.append(",")
        classList.append(prefixedString(classuri))

    classListStr = "".join(classList)
    if len(classListStr)>0:
        classListStr = classListStr[1:]

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?synonym ")
    qarr.append(" WHERE{")
    qarr.append("  ?class")
    qarr.append("   ?p ?synonym; ")
    qarr.append("   rdfs:label ?classlabel. ")
    qarr.append("  filter (?p in(")
    qarr.append(exactSynonymListStr)
    qarr.append(")) ")
    qarr.append("  filter (?class in(")
    qarr.append(classListStr)
    qarr.append(")) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# related synonyms
def getRelSynonymsAllContents(classUriArr):
    if classUriArr is None:
        return;

    classList = []
    for classuri in classUriArr:
        classList.append(",")
        classList.append(prefixedString(classuri))

    classListStr = "".join(classList)
    if len(classListStr)>0:
        classListStr = classListStr[1:]

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?synonym ")
    qarr.append(" WHERE{")
    qarr.append("  ?class")
    qarr.append("   ?p ?synonym; ")
    qarr.append("   rdfs:label ?classlabel. ")
    qarr.append("  filter (?p in(")
    qarr.append(relatedSynonymListStr)
    qarr.append(")) ")
    qarr.append("  filter (?class in(")
    qarr.append(classListStr)
    qarr.append(")) ")
    qarr.append("} ")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# exact synonyms
def synonymsExists(classUriArr):
    if classUriArr is None:
        return;

    classList = []
    for classuri in classUriArr:
        classList.append(",")
        classList.append(prefixedString(classuri))

    classListStr = "".join(classList)
    if len(classListStr)>0:
        classListStr = classListStr[1:]

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?synonym ")
    qarr.append(" WHERE{")
    qarr.append("  ?class")
    qarr.append("   ?p ?synonym; ")
    qarr.append("   rdfs:label ?classlabel. ")
    qarr.append("  filter (?p in(")
    qarr.append(exactSynonymListStr)
    qarr.append(")) ")
    qarr.append("  filter (?class in(")
    qarr.append(classListStr)
    qarr.append(")) ")
    qarr.append("} limit 1")

    qstring = "".join(qarr)
    qres = query(qstring )
    return qres


# get class , synonym  by label or synonym
#  ** class multiple
def getPartSynonymClass(criteria):
    limitcnt=settings.LIMIT_SPARQL

    qarr = []
    qarr.append(allprefix())
    qarr.append("SELECT DISTINCT ?class ?synonym ")
    qarr.append("WHERE {{")
    qarr.append("  ?class a owl:Class;")
    qarr.append("      ?p ?synonym.")
#    qarr.append("  filter (?p in(rdfs:label, obo_annot:synonym , oboInOwl:hasExactSynonym))")
    qarr.append("  filter (?p in(rdfs:label,")
    qarr.append(exactSynonymListStr)
    qarr.append("))")
    qarr.append("  FILTER regex (?synonym,'")
    qarr.append(criteria)
    qarr.append("' , 'i')")
    qarr.append("}union{")
    qarr.append("  ?class a owl:Class;")
    qarr.append("      ?p ?synonym;")
    qarr.append("      rdfs:label ?label.")
    qarr.append("  filter (?p in(")
    qarr.append(exactSynonymListStr)
    qarr.append("))")
    qarr.append("  FILTER regex (?label,'")
    qarr.append(criteria)
    qarr.append("' , 'i')")
    qarr.append(".}} limit ")
    qarr.append(str(limitcnt))

    qstring = "".join(qarr)
    qres = query( qstring )
    return qres

