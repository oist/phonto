'''
Created on 2015/06/23

@author: adminstrator
'''

FILENAME_OUT      = "owllabels.txt"
FILENAME_RESULT   = "result.txt"


import os
import sys
import glob
from xml.etree import ElementTree

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter


def pdf2textsingle(args):
    fname = args.get("pdffile")
    outfile = args.get("outfile")

    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outtype = None
    imagewriter = None
    rotation = 0
    codec = 'utf-8'
    caching = True
    laparams = LAParams()

    # debug option
    debug = 0
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'

    if outfile:
        outfp = file(outfile, 'w')

    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)

    fp = file(fname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()

    device.close()
    outfp.close()
    return

def pdf2text():


    targets=glob.glob('target/*')
    for targetfile in targets:
        filename = os.path.basename(targetfile)
        outfilname = 'out/pubmed_' + filename[:-3] + "txt"
        args = { "pdffile": targetfile
                ,"outfile":outfilname
        }
        pdf2textsingle(args)
        print filename

#


