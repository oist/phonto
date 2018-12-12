'''
Created on 2015/06/23

@author: adminstrator
'''

FILENAME_PHDBID_PUBMEDID = "phdbID_pipe_pubmedID.txt"
FILENAME_OUT      = "owllabels.txt"
FILENAME_OUT_RAW  = "owllabels_raw.txt"
FILENAME_RESULT   = "result.txt"

import os
import sys
import glob
import re
from xml.etree import ElementTree
import functions
import singular

def outOntoWord():
    print "start"
    argvs = sys.argv
    argc = len(argvs)

    if argc >1:
        targets=[argvs[1]]
    else:
        targets=glob.glob('target/*')

    owls = glob.glob('owl/*')
    outfile = 'out/' + FILENAME_OUT_RAW
    treeArr =[]
    treelobArr =[]
    nodesArr =[]
    contentsArr =[]
    firstlabelArr =[]
    filesArr =[]
    dicwords = {}  # {filename :{owlname:[word,word ,,,], owlname:[],,,} , filename:{},,,}
    dbid2pubmed={} # {dbid:[pubmedid,pubmedid,,,]}

    print "start parse owl"

    ElementTree.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    ElementTree.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    ElementTree.register_namespace('owl', 'http://www.w3.org/2002/07/owl#')
    for lob in owls:
        print 'parse : ' + lob + "(It may take time...)"
        tree = ElementTree.parse(lob)
        treeArr.append(tree)
        treelobArr.append(lob)
        firstlabelArr.append(True)

        # owl:Class/rdfs:label
        nodes =  tree.findall('.//{http://www.w3.org/2002/07/owl#}Class/{http://www.w3.org/2000/01/rdf-schema#}label')
        nodesArr.append(nodes)
        print 'end parse  : ' + lob

    outf = open(outfile ,'w')
    for i, nodes in enumerate(nodesArr):
        for node in nodes:
            text = node.text
            try:
                outtext = text.encode('utf-8')
            except:
                outtext = text

            functions.output(outtext , outf)
    outf.close()


def serchlabel(args):
    allLines = args.get("allLines")
    text = args.get("label")
    outf = args.get("outf")
    isfirstLabel = args.get("isfirstLabel")
    dicwords = args.get("dicwords")
    targetfilename = args.get("targetfile")
    cmopareowl =  args.get("compareowl")
    isplural = args.get("isPlural")
    dicwords.update({"hit" : False})

    if text is None or allLines is None:
        return

    u8 = text.encode('utf-8')
    if isfirstLabel:
        functions.output(u8 , outf)

    if u8=='heart' or u8=='vent':
        u8 = u8

    index = allLines.find(u8)
    if index>-1 :
#        pattern = '(^| +)' + u8 + '($| +)'
        pattern = '\\b' + u8 + '\\b'
        result = re.search(pattern, allLines)
        if result is not None:

            # for model***_pubmedid***
            ids = targetfilename.split('\\')
            filename = ids[len(ids)-1]

            if dicwords.get(filename):
                dicfile = dicwords.get(filename)
            else:
                dicfile = {}

            arrowl = dicfile.get(cmopareowl)
            if arrowl is None:
                arrowl = []
            else:
                pass

            arrowl.append(u8)
            dicfile.update({cmopareowl : arrowl})
            dicwords.update({filename : dicfile})
            dicwords.update({"hit" : True})

    return dicwords

#
# output filename owlname words
#
# args:
#     dicwords:{filename:{owlname:[word,word,,,]}}
#     resultf :output fileobj
def resultoutput_default(args):
    dicwords = args.get("dicwords")
    resultf = args.get("resultf")
    if dicwords is None:
        return

    for filename in dicwords:
        dicfile = dicwords.get(filename)
        if dicfile is None:
            continue

        wordparfile = ""
        for owlname in dicfile:
            arrwords = dicfile.get(owlname)
            if arrwords is None:
                continue

            wordparowl = ""
            for  word in arrwords:
                if word is None:
                    continue

                wordparowl = wordparowl + ',' + word
                wordparfile = wordparfile + ',' + word

            if len(wordparowl) > 0:
                wordparowl = wordparowl[1:]

#            line_fileowl = filename + '|' + os.path.basename(owlname) + '|' + wordparowl
#            print line_fileowl
#            functions.output(line_fileowl , resultf)

        if len(wordparfile) > 0:
            wordparfile = wordparfile[1:]
        line_file = filename + '|' + wordparfile
        functions.output(line_file , resultf)
        functions.output(" " , resultf)

#
# output dbid pubmedid words
#
def resultoutput_fordbid_pubmedid(args):
    dicwords = args.get("dicwords")
    resultf = args.get("resultf")
    if dicwords is None:
        return

    for filename in dicwords:
        dicfile = dicwords.get(filename)
        if dicfile is None:
            continue

        ids = filename.split('_')
        modelid = ids[0]
        dbid = modelid[5 : len(modelid)]
        pubmed = ids[1]
        pubmedid = pubmed[8 : len(pubmed)]


        wordstr = ""
        for owlname in dicfile:
            arrwords = dicfile.get(owlname)
            if arrwords is None:
                continue

            for  word in arrwords:
                if word is None:
                    continue

                wordstr = wordstr + ',' + word


        if len(wordstr) > 0:
            wordstr = wordstr[1:]

        line = dbid + '|' + pubmedid + '|' + wordstr
        print line
        functions.output(line , resultf)

#
# output dbid pubmedid words
#
def resultoutput_dbid_pubmedid_words(args):
    dicwords = args.get("dicwords")
    resultf = args.get("resultf")
    dicrels = args.get("dicrelation")
    if dicwords is None:
        return

    for dbid in dicrels:
        arr = dicrels.get(dbid)
        if arr is None:
            line = dbid + '|'
            print line
            functions.output(line , resultf)
            continue

        for pubmedid in arr:
            pubmedwords = {}
            filename = "pubmed_" + pubmedid
            dicfile = dicwords.get(filename)

            if dicfile is None:
                line = dbid + '|' + pubmedid + '|'
                print line
                functions.output(line , resultf)
                continue

            wordstr = ""
            for owlname in dicfile:
                arrwords = dicfile.get(owlname)
                if arrwords is None:
                    continue

                for  word in arrwords:
                    if word is None:
                        continue

                    elif pubmedwords.get(word.strip()) is not None:
                        continue

                    pubmedwords.update({word.strip() : word.strip()})
                    wordstr = wordstr + ',' + word

            if len(wordstr) > 0:
                wordstr = wordstr[1:]

            line = dbid + '|' + pubmedid + '|' + wordstr
            print line
            functions.output(line , resultf)

#
# output pubmedid words
#
def resultoutput_pubmedid_words(args):
    dicwords = args.get("dicwords")
    resultf = args.get("resultf")
    dicrels = args.get("dicrelation")
    pubmedtemp = {}
    if dicwords is None:
        return

    for dbid in dicrels:
        arr = dicrels.get(dbid)
        if arr is None:
            line = dbid + '|'
            print line
            functions.output(line , resultf)
            continue

        for pubmedid in arr:
            already = pubmedtemp.get(pubmedid)
            if already is None:
                pubmedtemp.update({pubmedid : pubmedid})
            else:
                continue

            pubmedwords = {}
            filename = "pubmed_" + pubmedid
            dicfile = dicwords.get(filename)

            if dicfile is None:
                continue

            for owlname in dicfile:
                arrwords = dicfile.get(owlname)
                if arrwords is None:
                    continue

                for  word in arrwords:
                    if word is None:
                        continue

                    elif pubmedwords.get(word.strip()) is not None:
                        continue

                    pubmedwords.update({word.strip() : word.strip()})

                    line = 'insert into pubmed_word values(\'' + pubmedid + '\',\'' + word.strip() + '\');'
                    print line
                    functions.output(line , resultf)


#
# output dbid pubmedid
#
def resultoutput(args):
    dicwords = args.get("dicwords")
    resultf = args.get("resultf")
    dicrels = args.get("dicrelation")
    db_pubmedtemp = {} #key -> dbid + '_' + pubmedid
    if dicwords is None:
        return

    for dbid in dicrels:
        arr = dicrels.get(dbid)
        if arr is None:
            continue

        for pubmedid in arr:
            tempkey = dbid + '_' + pubmedid
            already =  db_pubmedtemp.get(tempkey)

            if already is not None:
                continue

            db_pubmedtemp.update({tempkey:tempkey})
            line = 'insert into db_pubmed values(\'' + dbid + '\',\'' + pubmedid + '\');'
            print line
            functions.output(line , resultf)

# main
def ontSearch():
    print "start"
    argvs = sys.argv
    argc = len(argvs)

    if argc >1:
        targets=[argvs[1]]
    else:
        targets=glob.glob('target/*')

    owls = glob.glob('owl/*')
    outfile = 'out/' + FILENAME_OUT
    resfile = 'out/' + FILENAME_RESULT
    linkfile = FILENAME_PHDBID_PUBMEDID
    treeArr =[]
    treelobArr =[]
    nodesArr =[]
    contentsArr =[]
    firstlabelArr =[]
    filesArr =[]
    dicwords = {}  # {filename :{owlname:[word,word ,,,], owlname:[],,,} , filename:{},,,}
    dbid2pubmed={} # {dbid:[pubmedid,pubmedid,,,]}

    print "1/5 get link phdbid-pubmedid"
    inf = open(linkfile,'r')
    for line in inf:
        contents = line.split('|')
        if len(contents) > 1:
            dbid = contents[0].strip()

            if dbid is None:
                continue

            for i, col in enumerate(contents):
                col = col.strip()
                if i == 0 :
                    continue

                pubarr = dbid2pubmed.get(dbid)
                if pubarr is None:
                    pubarr = []

                if col != '':
                    pubarr.append(col)

                dbid2pubmed.update({dbid:pubarr})

    inf.close()

    print "2/5 parse owl"

    ElementTree.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    ElementTree.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
    ElementTree.register_namespace('owl', 'http://www.w3.org/2002/07/owl#')
    for lob in owls:
        print 'parse : ' + lob + "(It may take time...)"
        tree = ElementTree.parse(lob)
        treeArr.append(tree)
        treelobArr.append(lob)
        firstlabelArr.append(True)

        # owl:Class/rdfs:label
        nodes =  tree.findall('.//{http://www.w3.org/2002/07/owl#}Class/{http://www.w3.org/2000/01/rdf-schema#}label')
        nodesArr.append(nodes)
        print 'end parse  : ' + lob
    print "3/5 get target file"

    for targetfile in targets:
        inf = open(targetfile)
        allLines = inf.read()
        contentsArr.append(allLines)
        filesArr.append(targetfile)
        inf.close()

    print "4/5 search words"

    outf = open(outfile, 'w')

    currow = 0
    progress = 0
    step = 10
    rows = len(contentsArr)
    for i, allLines in enumerate(contentsArr):
        currow +=1
        currest = (currow * 100) % (rows * step)
        curprog =  ((currow * 100) - currest) / (rows * step)
        if progress < curprog :
            print "..." + str(curprog * step) + "%"
            progress = curprog

        targetfile = filesArr[i]
        for j, tree in enumerate(treeArr):
            lob = treelobArr[j]
            if firstlabelArr[j]:
                functions.output("### " + lob + "'s labels start" , outf)

            # owl:Class/rdfs:label
            #nodes =  tree.findall('.//{http://www.w3.org/2002/07/owl#}Class/{http://www.w3.org/2000/01/rdf-schema#}label')
            nodes = nodesArr[j]

            for node in nodes:
                args={
                       "allLines":allLines
                      ,"label":node.text
                      ,"outf":outf
                      ,"isfirstLabel":firstlabelArr[j]
                      ,"dicwords":dicwords
                      ,"targetfile":filesArr[i]
                      ,"compareowl":treelobArr[j]
                      ,"isPlural":False
                }
                dicwords = serchlabel(args)
                if not dicwords.get("hit"):
                    newlabel = singular.toPlural(node.text)
                    if newlabel != node.text:
                        args.update({"label" : newlabel , "isPlural" :True})
                        dicwords = serchlabel(args)
            #
            if firstlabelArr[j]:
                functions.output("### end of "+ lob +"'s labels" , outf)
            firstlabelArr[j] = False
        #
    #

    print "5/5 result output"
    resultf = open(resfile, 'w')
    args={
           "dicwords":dicwords
          ,"resultf":resultf
          ,"dicrelation":dbid2pubmed
    }
    resultoutput(args)
#    resultoutput_default(args)

    resultf.close()
    outf.close()

pass