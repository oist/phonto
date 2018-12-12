'''
Created on 2015/06/17

@author: adminstrator
'''
import rdflib
from rdflib import OWL, RDFS
from os import path
from os import sep
import shelve
import pickle

def getS(queryString , filepath):
    g = pickle.load(open("pickle.dump", "rb"))

    if g is None:
        print "no cache"
        print "parse start"
        g = rdflib.ConjunctiveGraph()
        g.parse(filepath)
        print "parse end"

    # query: sparql
    qarr = []
    qarr.append("""SELECT * WHERE{?s ?p ?o """)

    qarr.append("""FILTER regex (?o, '^""")
    qarr.append(queryString)
    qarr.append("""', "i")""")

    qarr.append(""".} limit 10""")
    qstring = "".join(qarr)
    print qstring
    qres = g.query(qstring)
#    qres = g.query(qstring,initNs={"em": em})
    print "query end"

    ret = []
    for s, p, o in qres:
        ret.append(o)

    return ret


def syncowl():
    # use rdflib
    filepath = path.dirname( path.abspath( __file__ ) ) + sep + ".."+ sep + "static" + sep + "data" + sep +"ext.owl"
    g = rdflib.ConjunctiveGraph()
    g.parse(filepath)

    #
    pickle.dump(g, open("pickle.dump", "wb"))

    return True








###################################################################################################################
### runnable command ###
'''
#move to D:\job\java_stand\eclipse_luna_py\OntologySearch\OntologySearch\static\data

import rdflib
from rdflib import OWL,RDFS

g = rdflib.ConjunctiveGraph()
#g.parse("install.rdf")
g.parse("obi.owl")
print("graph has %s statements." % len(g))
"""
for s, p, o in g:
    print((s, p, o))
"""
em = rdflib.Namespace("http://www.mozilla.org/2004/em-rdf#")
qstring = """
    SELECT * WHERE
    {
      ?s ?p ?o.
    }"""
qres = g.query(qstring)
#qres = g.query(qstring,initNs={"em": em})
"""
qres = g.query("""
    SELECT * WHERE
    {
      ?s ?p ?o
      FILTER regex (?o, '^dfdu', "i")
    .}""")
"""
print("%s results exist." % len(qres))
for s, p, o in qres:
    print((s, p, o))

'''

