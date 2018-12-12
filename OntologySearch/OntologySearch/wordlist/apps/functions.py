'''
Created on 2015/06/16

@author: adminstrator
'''
import sys


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

