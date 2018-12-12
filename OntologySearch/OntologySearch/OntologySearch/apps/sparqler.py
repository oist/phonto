'''
Created on 2015/06/17

@author: adminstrator
'''
import spquerier
from django.conf import settings

# get sparql column's value
def colValue(col):
    if col is None:
        return None

    coltype = col.get("type")
    if coltype is not None and coltype.lower() == "uri":
        ret = col.get("value")
    else:
        ret = col.get("value")

    return ret

# get namespace
def getNamespaceFromClass(classObj  ):
    if classObj is not None:
        classtype = classObj.get("type")
        if classtype is not None and classtype.lower() == "uri":
            namespace = classObj.get("value")
            return namespace

# get namespace
def getValue(fromObj , key  ):
    if fromObj is not None and isinstance(fromObj ,dict):
        targetObj = fromObj.get(key)
        if targetObj is not None:
            classtype = targetObj.get("type")
            if classtype is not None and classtype.lower() == "uri":
                ret = targetObj.get("value")
            else:
                ret = targetObj.get("value")

            return ret

# get parent chain
def getAncestor(namespace ,urls  ):

    #get myself
    urls.update({namespace:namespace})

    #get ancestor
    curns = namespace
    parents = []

    parentclasses = spquerier.getClassParent(curns )
    if len(parentclasses) == 0:
        return

    for row in parentclasses:
        rowpar = row.get("parent")
        if rowpar.get("type") == "uri":
            curns = rowpar.get("value")
            row.update({"class":curns})

            if urls.get(curns) is not None:
                row.update({"ommit":True})
                parents.append(row)
                continue

            urls.update({curns:curns})
            rowpar = getAncestor(curns ,urls)

            row.update({"parents":rowpar})

            parents.append(row)

    return parents


# get synonym (by class'es')
def getSynonymsAll(classUriArr):
    ret = []
    if classUriArr is None:
        return;

    uristep = 150
    curloop = 0
    cursum = 0
    curarr = []
    arrlen = len(classUriArr);
    if isinstance(classUriArr, list):
        startp = 0

        while startp < arrlen:
            endp = startp + uristep
            if endp > arrlen:
                endp = arrlen

            partArr = classUriArr[startp : endp]
            sret = spquerier.getSynonymsAllContents(partArr)
            if sret is not None and len(sret)>0:
                ret.extend(sret)

            startp = endp

    else:
        for row in classUriArr:
            curarr.append(row)
            curloop = curloop + 1
            cursum = cursum + 1
            if cursum == arrlen or curloop == uristep:
                sret = spquerier.getSynonymsAllContents(curarr)
                if sret is not None and len(sret)>0:
                    ret.extend(sret)
                curloop = 0
                curarr = []

    return ret


# get synonym (by class'es')
def getRelSynonymsAll(classUriArr):
    ret = []
    if classUriArr is None:
        return;

    uristep = 150
    curloop = 0
    cursum = 0
    curarr = []
    arrlen = len(classUriArr);
    if isinstance(classUriArr, list):
        startp = 0

        while startp < arrlen:
            endp = startp + uristep
            if endp > arrlen:
                endp = arrlen

            partArr = classUriArr[startp : endp]
            sret = spquerier.getRelSynonymsAllContents(partArr)
            if sret is not None and len(sret)>0:
                ret.extend(sret)

            startp = endp

    else:
        for row in classUriArr:
            curarr.append(row)
            curloop = curloop + 1
            cursum = cursum + 1
            if cursum == arrlen or curloop == uristep:
                sret = spquerier.getRelSynonymsAllContents(curarr)
                if sret is not None and len(sret)>0:
                    ret.extend(sret)
                curloop = 0
                curarr = []

    return ret



# get HierarchyData (parentchain , brothers , children , synonym)
def getHierarchyData (name):
    queryString = name

    #get myselves
    myself = spquerier.getClassByLabelSynonym(queryString ,None)
    retarr = []
    if len(myself) == 0:
        return  ''

    else:
        for row in myself:
            myname = getValue(row , "label")
            mynamespace = getValue(row , "class")
            if mynamespace is not None:

                #
                mysynonyms = spquerier.getSynonyms(mynamespace)

                #ancestor
                urls={}
                reta = getAncestor(mynamespace ,urls )

                #brothers
                mewithparent = spquerier.getClassParent(mynamespace)
                parentname = ""
                parnamespace = ""
                retb =[]
                for parrow in mewithparent:
                    parentname = getValue(parrow, "parentlabel")
                    parnamespace = getValue(parrow, "parent")
                    if parnamespace is not None:
                        children = spquerier.getChildren(parnamespace)
                        retb.append({"parentns":parnamespace ,
                                     "parentname":parentname ,
                                     "brothers":children
                                     })

                #children
                mykids = spquerier.getChildren(mynamespace )

                retarr.append({'ancestor': reta,
                    'brothers':retb,
                    'children':mykids,
                    'myname':myname,
                    'myns':mynamespace,
                    'synonyms':mysynonyms,

                    })

    return retarr


#
# get search candidates
#
# param
#   name : classname or exact-synonym
#
# return (exact , synonym ,related)
#
def getCandidate(name):
    queryString = name

    ## get exact Hit (exact label or synonym )

    # myselves
    myselves = spquerier.getClassByLabelSynonym(queryString ,None)
    retdic ={}
    mynamespaces = {}
    if len(myselves) == 0:
        return  {"exact":{}
                ,"synonym":{}
                ,"related":{}
                }

    for myself in myselves:
        mynamespace = getValue(myself, "class")
        if mynamespace is not None:
            mynamespaces.update({mynamespace : mynamespace})

    #label & synonym
    synonyms = getSynonymsAll(mynamespaces)

    '''
    relatedlabels = []
    parnamespaces = {}
    relsynonyms = getRelSynonymsAll(mynamespaces)
    for rel in relsynonyms:
        relatedlabels.extend([{
             "label": rel.get("synonym")
        }])

    ## get related Hit

    # parents
    parents = spquerier.getClassParentAll(mynamespaces)
    for parentrow in parents:
        parnamespace = getValue(parentrow, "parent")
        if parnamespace is not None:
            parnamespaces.update({parnamespace : parnamespace})

    # brothers with synonym
    brothers = spquerier.getChildrenAllWithSynonym(parnamespaces)
    bronamespaces = {}
    brosynonyms = {}
    for brotherrow in brothers:
        bronamespace = getValue(brotherrow , "class")
        if bronamespace is not None and bronamespaces.get(bronamespace) is None:
            bronamespaces.update({bronamespace : bronamespace})

            relatedlabels.extend([{
                 "class": brotherrow.get("class")
                ,"label": brotherrow.get("label")
                ,"parent":brotherrow.get("parent")
                ,"parentlabel":brotherrow.get("parentlabel")
            }])

        brosynonym = brotherrow.get("synonym")
        if colValue(brosynonym) is not None:
            colval = colValue(brosynonym)

            if brosynonyms.get(colval) is None:
                brosynonyms.update({colval : colval})
                relatedlabels.extend([{"synonym":brosynonym}])

    retdic.update({"exact":myselves
                   ,"synonym":synonyms
                   ,"related":relatedlabels
                   })
    '''
    retdic.update({"exact":myselves
                   ,"synonym":synonyms
                   })

    return retdic
#
# get search candidates indetail
#
# param
#   name : classname or exact-synonym
#   skippartial: true/false
#
# return { "exact":{}
#         ,"synonym":{}
#         ,"sibling":{}
#         ,"parent":{}
#         ,"child":{}
#         ,"rels":{}
#        }
#
def getCandidateDetail(name ,skippartial=False):
    queryString = name

    ## get exact Hit (exact label or synonym )

    # myselves
    myselves = spquerier.getClassByLabelSynonym(queryString ,None)
    retdic ={}
    relatedlabels = []
    siblinglabels = []
    synonyms = []
    parents = []
    mychildren=[]
    mynamespaces = {}
    parnamespaces = {}
    if len(myselves) > 0:

        for myself in myselves:
            mynamespace = getValue(myself, "class")
            if mynamespace is not None:
                mynamespaces.update({mynamespace : mynamespace})

        #synonym
        synonyms = getSynonymsAll(mynamespaces)

        relsynonyms = getRelSynonymsAll(mynamespaces)
        for rel in relsynonyms:
            if rel and (isinstance(rel,dict) ):
                relatedlabels.extend([{
                     "label": rel.get("synonym")
                }])

        ## get related Hit

        # parents
        parents = spquerier.getClassParentAll(mynamespaces)
        for parentrow in parents:
            parnamespace = getValue(parentrow, "parent")
            if parnamespace is not None:
                parnamespaces.update({parnamespace : parnamespace})

        # brothers with synonym
        brothers = spquerier.getChildrenAllWithSynonym(parnamespaces)
        bronamespaces = {}
        brosynonyms = {}
        for brotherrow in brothers:
            bronamespace = getValue(brotherrow , "class")
            if bronamespace is not None and bronamespaces.get(bronamespace) is None:
                bronamespaces.update({bronamespace : bronamespace})

                siblinglabels.extend([{
                     "class": brotherrow.get("class")
                    ,"label": brotherrow.get("label")
                    ,"parent":brotherrow.get("parent")
                    ,"parentlabel":brotherrow.get("parentlabel")
                }])

            if isinstance(brotherrow , dict):
                brosynonym = brotherrow.get("synonym")
                if colValue(brosynonym) is not None:
                    colval = colValue(brosynonym)

                    if brosynonyms.get(colval) is None:
                        brosynonyms.update({colval : colval})
                        siblinglabels.extend([{"synonym":brosynonym}])


        # children with synonym
        mychildren = spquerier.getChildrenAllWithSynonym(mynamespaces)

    # other related object

    # partial match
    partials = []
    partsynmap={}
    partialcnt = 0
    '''
    if not skippartial:
        partialwords = spquerier.getPartSynonymClass(queryString )
        partialcnt = len(partialwords)
        if partialcnt <= settings.LIMIT_PARTIAL:
            for i, wordobj in enumerate(partialwords):
                partclass = wordobj.get("class")
                if partclass is not None:
                    partval = colValue(partclass)
                    if partval is not None:
                        partns = [partval]
                        partsynonyms = getSynonymsAll(partns)
                        partsyn = []
                        partlabel = getValue(wordobj, "synonym")
                        for j, partobj in enumerate(partsynonyms):
                            synlabel = getValue(partobj, "synonym")
                            if partlabel != synlabel:
                                partsyn.append(",")
                                partsyn.append(synlabel)

                        if len(partsyn)>0:
                            partsyn = partsyn[1:]

                        partials.extend([{
                             "class": wordobj.get("class")
    #                                ,"label": wordobj.get("label")
                            ,"label": wordobj.get("synonym")
                        }])
                        partsynmap.update({partlabel : "".join(partsyn)})
    '''

    retdic.update({"exact":myselves
                   ,"synonym":synonyms
                   ,"sibling":siblinglabels
                   ,"parent":parents
                   ,"child":mychildren
                   ,"rels":relatedlabels
                   ,"partialcnt":partialcnt
                   ,"partials":partials
                   ,"partsynmap":partsynmap
                   })

    return retdic

#
# convert to [label or synonym ]array
#
# param
#   inarr : array of sparql result ('label' or 'synonym' needed)
#
def toLabelSynonymArr (inarr , labelkey="label" , synonymkey="synonym" ):
    retarr = []
    if inarr is None:
        return retarr

    for row in inarr:
        if not row or not isinstance(row ,dict):
            continue

        rowlabel = row.get(labelkey)
        if rowlabel is None:
            rowlabel = row.get(synonymkey)

        if rowlabel is None:
            continue

        rowlabeltype = rowlabel.get("type")
        if rowlabeltype =="typed-literal" or rowlabeltype =="literal":
            name = rowlabel.get("value")
            retarr.append(name)

    return retarr

