from django.conf.urls import patterns,  url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OntologySearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## for searchdb
    # auto complete
    url(r'^getkeyfromarticle$', 'OntologySearch.keywordlist.views.getkeyfromarticle'),

    ## error responses
    # 404 response  (this should be last)
    url(r'^.*$','OntologySearch.keywordlist.views.json404'),

)

