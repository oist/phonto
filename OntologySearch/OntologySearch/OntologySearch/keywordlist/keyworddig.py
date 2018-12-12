'''
Created on 2015/06/23

@author: adminstrator
'''

FILENAME_PHDBID_PUBMEDID = "phdbID_pipe_pubmedID.txt"
FILENAME_OUT      = "owllabels.txt"
FILENAME_RESULT   = "result.txt"

import os
import sys
import glob
import re
from os import sep
from xml.etree import ElementTree
from django.conf import settings

from OntologySearch.keywordlist import singular


def getOntoKeywords(pdftext):
    print "start"

    #get ontology
    ontofile = os.path.dirname(os.path.abspath(__file__)) + sep + settings.ONTOLOGY_FILE
    ontf = open(ontofile, 'r')
    ontoarr=[]

    ontcontents = ontf.read()
    ontf.close
    if isinstance(ontcontents, unicode):
        ontcontents = ontcontents.encode('utf-8')

    ontcontents = ontcontents.replace("\r\n","\r")
    ontcontents = ontcontents.replace("\n","\r")
    ontcontents = ontcontents.replace("\r","\r\n")
    ontoarr = ontcontents.split("\r\n")

    #get article
    inf = open(pdftext, 'r')
    article = inf.read()
    if article == None or article == "":
        return []
    article = article.lower()

    inf.close()

    retarr=[]

    currow = 0
    progress = 0
    step = 10
    rows = len(ontoarr)
    for i, ontoLine in enumerate(ontoarr):
        currow +=1
        currest = (currow * 100) % (rows * step)
        curprog =  ((currow * 100) - currest) / (rows * step)
        if progress < curprog :
            print "..." + str(curprog * step) + "%"
            progress = curprog

        ontokey = ontoLine.lower()

        goplu = False
        addword = ""
        if article.find(ontokey) < 0:
            #plulal
            goplu = True

        else:
            #regex
            pattern = '\\b' + ontokey + '\\b'
            searc = re.search(pattern, article)
            if searc == None:
                goplu = True

        if goplu == True:
            plu = singular.toPlural(ontokey)
            if article.find(plu) >= 0:
                #regex
                pattern = '\\b' + plu + '\\b'
                searc = re.search(pattern, article)
                if searc != None:
                    addword = ontokey

        else:
            addword = ontokey
            pass

        if addword != "":
            print "hit : " + addword
            retarr.append(addword)

    return retarr


## output file or db or systemprint
def output(text , outfile):
    if outfile is None:
        return

    try:
        outfile.write(text.strip() + "\r")
    except:
        print "error text : " + text
        print sys.exc_info()
    pass
