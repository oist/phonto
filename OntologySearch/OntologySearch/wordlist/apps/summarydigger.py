# coding:utf-8
'''
Created on 2015/06/23

@author: adminstrator
'''

SUMMARY_FILE = "esummary.fcgi.xml"
FILENAME_RESULT   = "summary.txt"

from xml.etree import ElementTree
import functions
import os

# main
def showSummary():

    summaryfile = SUMMARY_FILE
    dicouts = {}  # {filename :{owlname:[word,word ,,,], owlname:[],,,} , filename:{},,,}

    tree = ElementTree.parse(summaryfile)

    # get PubmedIds
    nodeDocSums =  tree.findall('.//DocSum')

    for nodeDocSum in nodeDocSums:
        # get info for each Pubmed
        nodeId = nodeDocSum.find('.Id')
        pubmedid = nodeId.text
        dicpub = dicouts.get(pubmedid)
        if dicpub is None:
            dicpub = {}

        #find articles
        subnodes =  nodeDocSum.find(".Item[@Name='ArticleIds']")
        for subnode in subnodes:
            idtype = subnode.attrib["Name"]
            idValue = subnode.text
            if idValue == pubmedid:
                continue

            urlcanditate =""
            if str(idtype) == "pmc":
                urlcanditate = "http://www.ncbi.nlm.nih.gov/pmc/articles/" + idValue
            elif str(idtype) == "doi":
                urlcanditate = "http://link.springer.com/article/" + idValue + "/fulltext.html"

            strout = "pubmed : " + pubmedid + "\t type : " + idtype + "\t id : " + idValue
            if len(urlcanditate) > 0:
                strout += "\t url : " + urlcanditate

            print strout

            #pool dic
            arrref = dicpub.get("ref")
            if arrref is None:
                arrref = []

            dicref = { "type":idtype
                      ,"id":idValue
                      ,"url":str(urlcanditate)
                      }
            arrref.append(dicref)
            dicpub.update({"ref":arrref})

        #find ELocationID
        locnode =  nodeDocSum.find(".Item[@Name='ELocationID']")
        if locnode is not None and locnode.text is not None:
            loc = locnode.text
            print "pubmed : " + pubmedid + "\t ELocatioID  \t  " + loc

            dicpub.update({"locatioid":loc})

        dicouts.update({pubmedid:dicpub})

        #mkdir
        path = pubmedid
        if not os.path.exists(path):
            os.mkdir(path)

    #

pass