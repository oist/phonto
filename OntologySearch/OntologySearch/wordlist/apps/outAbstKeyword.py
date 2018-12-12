# coding:utf-8
'''
Created on 2015/06/23
for DBPF

@author: adminstrator
'''

FILE_DIR = "target_dbpf"
OUT_DIR = "target_dbpf/abst_dbpf"
TARGET_DIR = OUT_DIR
FILENAME_OUT = "dbpfkeywords.txt"
MODELID_OUT = "dbpfmodels.txt"
OWL_TEXT = "out/owllabels.txt"

from xml.etree import ElementTree
import functions
import os
import re

# main
def showSummary():
    files = os.listdir(FILE_DIR)
     
    for file in files:
        targetfile = FILE_DIR + os.sep + file
        if not os.path.isfile(targetfile):
            continue

        print targetfile
        tree = None
        try:    
            tree = ElementTree.parse(targetfile)
        except Exception as e:
            print 'error:' + str(e)
            continue

        oufilename, ext = os.path.splitext(targetfile)
        outfile = OUT_DIR + os.sep + os.path.basename(oufilename) +".txt"
        outf = open(outfile , "w")
        # get PubmedIds
        nodeKeywords =  tree.findall('.//keywords/keyword')
        
        for nodeKeyword in nodeKeywords:
            # get info for each Pubmed
            outf.write(nodeKeyword.text)
            outf.write(os.linesep)

        nodeAbstracts =  tree.findall('.//abstract')
        for nodeAbstract in nodeAbstracts:
            if nodeAbstract is None or nodeAbstract.text is None:
                continue
            outf.write(nodeAbstract.text)
            outf.write(os.linesep)

        outf.close()

    return

def setModelCSV():
    files = os.listdir(FILE_DIR)
    outf = open(MODELID_OUT , "w")
     
    for file in files:
        targetfile = FILE_DIR + os.sep + file
        if not os.path.isfile(targetfile):
            continue

        print targetfile
        tree = None
        try:    
            tree = ElementTree.parse(targetfile)
        except Exception as e:
            print 'error:' + str(e)
            continue

        modelid, ext = os.path.splitext(file)
        # get PubmedIds
        nodeKeywords =  tree.findall('.//titles/title')
        
        for nodeKeyword in nodeKeywords:
            # get info for each Pubmed
            outf.write(modelid + "," +nodeKeyword.text)
            outf.write(os.linesep)
            break

    outf.close()

    return

def setKeywordCSV():
    inf = open(OWL_TEXT , "r")
    owls = []
    cnt=0
    for line in inf:
#        row = line.replace('¥r¥n','¥n')
#        row = row.replace('¥r','¥n')
#        subowls = row.split('¥n')
        subowls = line.split('\r')
        owls.extend(subowls) 
    inf.close()

    outf = open(FILENAME_OUT , "w")

    files = os.listdir(TARGET_DIR)
    cnt = 1
    for file in files:
        targetfile = TARGET_DIR + os.sep + file
        tf = open(targetfile , "r")
        alllines = tf.read()

        for label in owls:
            if not label:
                continue
            
            u8 = label.encode('utf-8')
            index = alllines.find(u8)
            if index>-1 :
                pattern = '\\b' + u8 + '\\b'
                result = re.search(pattern, alllines)
                if result is not None:
                    outf.write(os.path.basename(file) + "," + u8)
                    outf.write(os.linesep)
            
        print cnt
        cnt += 1
    
    outf.close()
