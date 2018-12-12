"""
Django settings for OntologySearch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import sep

#from django.conf.global_settings import STATIC_ROOT
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Telapate definition
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, "OntologySearch" , "templates"),
)
# Static definition
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, "OntologySearch" , "static"),
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$+dz-$(=3^uk*r7fsllw*#a&is&p)!+$i)5^h99$sw*i%oh1j8'

# SECURITY WARNING: don't run with debug turned on in production!
'''
DEBUG = True
TEMPLATE_DEBUG = True
'''
DEBUG = False
TEMPLATE_DEBUG = False
#'''

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rdflib_django',
    'OntologySearch',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OntologySearch.urls'

WSGI_APPLICATION = 'OntologySearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'utf-8'

TIME_ZONE = 'Asia/Tokyo'


USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'


##
## Ontollogy Search Conditions
##

# rdflib definition
RDFLIB_DIRS = (
    os.path.join(BASE_DIR, "rdflib"),
)

#test search target
SEARCH_TARGET_DB = {
    'HOST':"localhost",
    'DATABASE':"ontodb",
    'USER':"root",
    'PASSWD':"sbgnoist",
    'CHARSET':"utf8",
    'URLFORMAT_DEFAULT':"https://phdb.unit.oist.jp/modeldb/model/?mid={0}"
}
# setting for fuseki -ontology server-
FUSEKI_URL = {
     'PROTOCOL':'http'
    ,'HOST':'localhost'
    ,'PORT':'3030'
#    ,'SOURCE_ADDRESS':'/NIF'
    ,'SOURCE_ADDRESS':'/ds'
}
# setting for sparql prefix
BASEPREFIX = [
    {"prefix":"rdf"  ,"uri":"http://www.w3.org/1999/02/22-rdf-syntax-ns#"},
    {"prefix":"rdfs" ,"uri":"http://www.w3.org/2000/01/rdf-schema#"},
    {"prefix":"owl"  ,"uri":"http://www.w3.org/2002/07/owl#"},
    {"prefix":"swrl" ,"uri":"http://www.w3.org/2003/11/swrl#"},
    {"prefix":"swrlb","uri":"http://www.w3.org/2003/11/swrlb#"},
    {"prefix":"xsd"  ,"uri":"http://www.w3.org/2001/XMLSchema#"},
    {"prefix":"core" ,"uri":"http://www.w3.org/2004/02/skos/core#"},
    {"prefix":"foaf" ,"uri":"http://xmlns.com/foaf/0.1/"},
    {"prefix":"dc"   ,"uri":"http://purl.org/dc/elements/1.1/"}
            ]
OWLPREFIX = [
    {"prefix":"uberoncore"      ,"uri":"http://purl.obolibrary.org/obo/uberon/core#"},
    {"prefix":"PATO"            ,"uri":"http://purl.obolibrary.org/obo/PATO#"},
    {"prefix":"pato"            ,"uri":"http://purl.obolibrary.org/obo/pato#"},
    {"prefix":"obo"             ,"uri":"http://purl.obolibrary.org/obo/obo#"},
    {"prefix":"go"              ,"uri":"http://purl.obolibrary.org/obo/go#"},
    {"prefix":"owl2"            ,"uri":"http://purl.obolibrary.org/obo/"},

    {"prefix":"snap"            ,"uri":"http://www.ifomis.org/bfo/1.1/snap#"},
    {"prefix":"span"            ,"uri":"http://www.ifomis.org/bfo/1.1/span#"},
    {"prefix":"bfo"             ,"uri":"http://www.ifomis.org/bfo/1.1#"},

    {"prefix":"daml"            ,"uri":"http://www.daml.org/2001/03/daml+oil#"},
    {"prefix":"xsp"             ,"uri":"http://www.owl-ontologies.com/2005/08/07/xsp.owl#"},
    {"prefix":"Ontology1272057115","uri":"http://www.owl-ontologies.com/Ontology1272057115.owl#"},
    {"prefix":"oboInOwl"        ,"uri":"http://www.geneontology.org/formats/oboInOwl#"},

    {"prefix":"NIF"             ,"uri":"http://ontology.neuinfo.org/NIF/#"},
    {"prefix":"NIFstd"          ,"uri":"http://uri.neuinfo.org/nif/nifstd/"},
    {"prefix":"birn_annot"      ,"uri":"http://ontology.neuinfo.org/NIF/Backend/BIRNLex_annotation_properties.owl#"},
    {"prefix":"BIRNLex_OBO_UBO" ,"uri":"http://ontology.neuinfo.org/NIF/Backend/BIRNLex-OBO-UBO.owl#"},
    {"prefix":"obo_annot"       ,"uri":"http://ontology.neuinfo.org/NIF/Backend/OBO_annotation_properties.owl#"},

    {"prefix":"NIF_Quality"         ,"uri":"http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-Quality.owl#"},
    {"prefix":"NIF_Neuron_NT_Bridge","uri":"http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-Neuron-NT-Bridge.owl#"},
    {"prefix":"NIF_GrossAnatomy"    ,"uri":"http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-GrossAnatomy.owl#"},
    {"prefix":"NIF_Cell"            ,"uri":"http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-Cell.owl#"},
    {"prefix":"NIF_Organism"        ,"uri":"http://ontology.neuinfo.org/NIF/BiomaterialEntities/NIF-Organism.owl#"}
                ]

#save articlr dir
ARTICLE_DIR = 'target'

#ontology text file
ONTOLOGY_FILE = 'base' + sep + "owllabels.txt"

# sparql limit
LIMIT_COMPLETE = 10
LIMIT_SPARQL = 50
LIMIT_PARTIAL = 20
