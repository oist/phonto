'''
Created on 2015/06/23

@author: adminstrator
'''


from apps import searchonto
from apps import abstractfetcher
from apps import summarydigger
from apps import pdfer
from apps import singular

from apps import outAbstKeyword

# main
if __name__ == '__main__':


    args = {}
### for dbpf    
#    abstractfetcher.getabst(args)

#    summarydigger.showSummary()

#    searchonto.ontSearch()
#    searchonto.outOntoWord()

#    pdfer.pdf2text()

#    print singular.toPlural('study')
###

###
#    outAbstKeyword.showSummary()
#    outAbstKeyword.setKeywordCSV()
    outAbstKeyword.setModelCSV()
    
###

    print "fin."
pass