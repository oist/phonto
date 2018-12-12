from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OntologySearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'OntologySearch.site.views.navi'),
    url(r'^ontology$', 'OntologySearch.site.views.index', name='ontology'),
    url(r'^ontology/(?P<word>[^/]*)$', 'OntologySearch.site.views.index'),

    url(r'^search$','OntologySearch.site.views.search', name='search'),
    url(r'^search/(?P<dbname>[^/]*)$','OntologySearch.site.views.search'),
    url(r'^search/(?P<dbname>[^/]*)/(?P<word>[^/]*)$','OntologySearch.site.views.search'),

    url(r'^navi$', 'OntologySearch.site.views.navi', name='navi'),

    url(r'^csvadmin','OntologySearch.site.views.samplecsvadmin'),
    url(r'^sampleadmin','OntologySearch.site.views.sampleadmin'),
    url(r'^sampleupdate','OntologySearch.site.views.sampleupdate'),
    url(r'^samplemodel/(?P<modelid>[^/]*)','OntologySearch.site.views.samplemodel'),

    url(r'^wrapper/(?P<dbname>[^/]*)/(?P<modelid>[^/]*)$','OntologySearch.site.views.wrapper'),

    #js library
    url(r'^ontologicalneighbors.js$', 'OntologySearch.views.jslib'),
    url(r'^ontologicalneighbors.css$', 'OntologySearch.views.jslibcss'),

    url(r'^apps/', include('OntologySearch.apps.urls') ,name='apps'),
    url(r'^[^/]*/apps/', include('OntologySearch.apps.urls')),

    url(r'^keywordlist/', include('OntologySearch.keywordlist.urls')),

    url(r'^admin/', include(admin.site.urls)),

    #old page
    url(r'^word$', 'OntologySearch.site.views.wordcondition', name='wordcondition'),

)
