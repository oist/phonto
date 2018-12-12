from django.conf.urls import patterns,  url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OntologySearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## for searchdb
    # auto complete
    url(r'^synonymcomplete$', 'OntologySearch.apps.views.get_completesynonym'),
    url(r'^complete/(?P<word>[^/]*)$','OntologySearch.apps.views.get_completesynonym'),

    # search db
    url(r'^searchdb$', 'OntologySearch.apps.views.searchdb'),
    url(r'^searchdb/(?P<dbname>[^/]*)$','OntologySearch.apps.views.searchdb'),
    url(r'^searchdb/(?P<dbname>[^/]*)/(?P<word>[^/]*)$','OntologySearch.apps.views.searchdb'),

    # search db all
    url(r'^searchdballexact/$','OntologySearch.apps.views.searchdballexact'),
    url(r'^searchdballexact/(?P<word>[^/]*)$','OntologySearch.apps.views.searchdballexact'),
    url(r'^searchdball/(?P<word>[^/]*)$','OntologySearch.apps.views.searchdball'),
    url(r'^searchdball/$','OntologySearch.apps.views.searchdball'),
    url(r'^searchneighbors/(?P<dbname>[^/]*)/(?P<identifier>[^/]*)$','OntologySearch.apps.views.searchneighbors'),
    url(r'^searchneighbors/$','OntologySearch.apps.views.searchneighbors'),

    # prefix
    url(r'^getprefixes$', 'OntologySearch.apps.views.getPrefixes'),
    url(r'^prefixes$', 'OntologySearch.apps.views.getPrefixes'),

    ## for db marge
    #
    url(r'^updatemodel/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<modelname>[^/]*)$', 'OntologySearch.apps.views.updatemodel'),
    url(r'^updatemodel/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<modelname>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.updatemodel'),
    url(r'^updatemodelname/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<modelname>[^/]*)$', 'OntologySearch.apps.views.updatemodel'),
    url(r'^updatemodelname/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<modelname>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.updatemodel'),

    #
    url(r'^deletemodel/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)$', 'OntologySearch.apps.views.deletemodel'),
    url(r'^deletemodel/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.deletemodel'),

    # keyword
    url(r'^insertkeyword/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<keyword>[^/]*)$', 'OntologySearch.apps.views.insertkeyword'),
    url(r'^insertkeyword/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<keyword>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.insertkeyword'),
    url(r'^deletekeyword/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<keyword>[^/]*)$', 'OntologySearch.apps.views.deletekeyword'),
    url(r'^deletekeyword/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<keyword>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.deletekeyword'),

    # tagetdb info
    url(r'^getdblist$', 'OntologySearch.apps.views.getdblist'),
    url(r'^getdbinfo/(?P<dbname>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.getdbinfo'),
    url(r'^updatedbinfo$', 'OntologySearch.apps.views.updatedbinfo'),

    # update model & keyword
    url(r'^updatebycsv$', 'OntologySearch.apps.views.updatebycsv'),
    url(r'^updatemodelandkeyword$', 'OntologySearch.apps.views.updatemodelandkeyword'),

    # get data
    url(r'^modellist/(?P<dbname>[^/]*)$', 'OntologySearch.apps.views.getmodellist'),
    url(r'^modellist/(?P<dbname>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.getmodellist'),
    url(r'^keywordlist/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)$', 'OntologySearch.apps.views.getkeywordlist'),
    url(r'^keywordlist/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)/(?P<token>[^/]*)$', 'OntologySearch.apps.views.getkeywordlist'),

    ## for ontology view
    # classes
    url(r'^classes/(?P<word>[^/]*)$','OntologySearch.apps.views.getClasses'),

    # contents
    url(r'^getcontents$', 'OntologySearch.apps.views.getContents'),
    #url(r'^contents/http/(?P<word>.*) *$','OntologySearch.apps.views.getContentsHttp'),
    #url(r'^contents/https/(?P<word>.*) *$','OntologySearch.apps.views.getContentsHttps'),
    url(r'^contents/(?P<word>.*) *$','OntologySearch.apps.views.getContents'),
    url(r'^contentstest/(?P<word>.*) *$','OntologySearch.apps.views.getContentsTest'),

    # hierarchy
    url(r'^getowldata$', 'OntologySearch.apps.views.getowldata'),
    url(r'^hierarchy/(?P<word>[^/]*)$','OntologySearch.apps.views.getowldata'),


    ## for auth
    url(r'^gettoken$', 'OntologySearch.apps.auth.gettoken'),
    url(r'^gettoken/(?P<dbname>[^/]*)/(?P<username>[^/]*)/(?P<password>[^/]*)$', 'OntologySearch.apps.auth.gettoken'),

    ## generate
    url(r'^regenerateonto$', 'OntologySearch.apps.views.regenerateonto'),
    url(r'^generateonto$', 'OntologySearch.apps.views.generateonto'),
    url(r'^generatedb$', 'OntologySearch.apps.views.generatedb'),

    ## deplicated urls
    url(r'^query$', 'OntologySearch.apps.views_dep.query'),
    url(r'^getcanditates$', 'OntologySearch.apps.views_dep.getCanditates'),
    url(r'^canditates/(?P<word>[^/]*)$','OntologySearch.apps.views_dep.getCanditates'),


    ## error responses
    # 404 response  (this should be last)
    url(r'^.*$','OntologySearch.apps.views.json404'),

)

