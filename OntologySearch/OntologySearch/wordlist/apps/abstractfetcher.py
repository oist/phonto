'''
Created on 2015/06/23

@author: adminstrator
'''

LIST_FILENAME = 'phdbID_pipe_pubmedID.txt'

import functions
import urllib2

def webfetch(args):
    modelid = args.get("modelid")
    pubmedid = args.get("pubmedid")
    absts = args.get("absts")

#    outfile = 'model' + modelid + '_pubmedid' + pubmedid
    outfile = 'pubmedid_' + pubmedid
    outfull = 'target/' + outfile

    print 'fetch ' + modelid + ' ' + pubmedid

    if absts.get(pubmedid):
        contents = absts.get(pubmedid)

#        outf = open(outfull , 'w')
#        functions.output(contents , outf)
#        outf.close()
    else:
        #fetch from web
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + pubmedid + '&retmode=text&rettype=abstract'
        response = urllib2.urlopen(url)
        res = response.read()
        absts.update({pubmedid : res })

        outf = open(outfull , 'w')
        functions.output(res , outf)
        outf.close()

    pass

def getabst(args):

    inf = open(LIST_FILENAME)
    lines = inf.readlines()
    inf.close()

    absts = {}
    for line in lines:
        if line is None or line.strip()=='':
            continue

        row = line.split("|")
        if len(row) <= 1:
            continue

        for i, col in enumerate(row):
            if i == 0:
                continue

            pubmedid = col.strip()
            if len(pubmedid) > 0:
                args={
                       "modelid":row[0].strip()
                      ,"pubmedid":pubmedid
                      ,"absts":absts
                }
                webfetch(args)

        #
    #

    pass


pass