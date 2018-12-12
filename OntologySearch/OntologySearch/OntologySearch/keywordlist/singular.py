'''
Created on 2015/06/23

@author: adminstrator
'''

import os
import sys
import glob
import re
from gettext import translation


#Illegal plurals
dicPlu ={
    'alumnus'    : 'alumni',
    'analysis'   : 'analyses',
    'axis'       : 'axes',
    'bacterium'  : 'bacteria',
    'basis'      : 'bases',
    'child'      : 'children',
    'crisis'     : 'crises',
    'crux'       : 'cruces',
    'datum'      : 'data',
    'ellipsis'   : 'ellipses',
    'foot'       : 'feet',
    'gentleman'  : 'gentlemen',
    'goose'      : 'geese',
    'knife'      : 'knives',
    'leaf'       : 'leaves',
    'louse'      : 'lice',
    'man'        : 'men',
    'medium'     : 'media',
    'mouse'      : 'mice',
    'oasis'      : 'oases',
    'ox'         : 'oxen',
    'person'     : 'people',
    'phenomenon' : 'phenomena',
    'seaman'     : 'seamen',
    'snowman'    : 'snowmen',
    'stimulus'   : 'stimuli',
    'tooth'      : 'teeth',
    'woman'      : 'women',

    'stemma'   : 'stemmata',
    ''   : '',
    ''   : '',
    ''   : '',
    ''   : '',


    #o
    'echo'   : 'echoes',
    'hero'   : 'heroes',
    'negro'  : 'negroes',
    'potato' : 'potatoes',
    'tomato' : 'tomatoes',
    'veto'   : 'vetoes',

    #f
    'calf'   : 'calves',
    'scarf'  : 'scarves',
    'half'   : 'halves',
    'elf'    : 'elves',
    'leaf'   : 'leaves',
    'loaf'   : 'loaves',
    'self'   : 'selves',
    'shelf'  : 'shelves',
    'wolf'   : 'wolves',

    #fe
    'knife'  : 'knives',
    'life'   : 'lives',
    'wife'   : 'wives',
    ''   : '',
}
dicNochange={
    'advice'     :'advice',
    'aircraft'   :'aircraft',
    'assistance' :'assistance',
    'baggage'    :'baggage',
    'cattle'     :'cattle',
    'clergy'     :'clergy',
    'data'       :'data',
    'deer'       :'deer',
    'damage'     :'damage',
    'economics'  :'economics',
    'equipment'  :'equipment',
    'ethics'     :'ethics',
    'evidence'   :'evidence',
    'experience' :'experience',
    'fun'        :'fun',
    'furniture'  :'furniture',
    'headquarters' :'headquarters',
    'homework'   :'homework',
    'hope'       :'hope',
    'information':'information',
    'knowledge'  :'knowledge',
    'news'       :'news',
    'mail'       :'mail',
    'machinery'  :'machinery',
    'mathematics':'mathematics',
    'means'      :'means',
    'measles'    :'measles',
    'media'      :'media',
    'milk'       :'milk',
    'money'      :'money',
    'labor'      :'labor',
    'luggage'    :'luggage',
    'people'     :'people',
    'poultry'    :'poultry',
    'police'     :'police',
    'physics'    :'physics',
    'series'     :'series',
    'sheep'      :'sheep',
    'soap'       :'soap',
    'software'   :'software',
    'species'    :'species',
    'trouble'    :'trouble',
    'technology' :'technology',
    'water'      :'water',
    'weather'    :'weather',
    'work'       :'work',
    'yen'        :'yen',

#    'fish'       :'fish',

    'japanese'   :'japanese',
    'chinese'    :'chinese',
    'portuguese' :'portuguese',
    'bengalese'  :'bengalese',
    'vietnamese' :'vietnamese',
    ''       :'',


}

def toPlural(name):
    if name is None:
        return
    name = name.strip().lower()

    #Illegal
    plural = dicPlu.get(name)
    if plural is not None:
        return plural

    #no change
    plural = dicNochange.get(name)
    if plural is not None:
        return plural

    # -y
    pattern = '[^aiueo]y$'
    result = re.search(pattern, name)
    if result is not None:
        plural = name[:-1] + "ies"
        return plural

    # -s,x,sh,ch
    pattern = '[s|x|sh|ch]$'  #z?
    result = re.search(pattern, name)
    if result is not None:
        plural = name + "es"
        return plural

    # o -1
    pattern = '[aiueo]o$'
    result = re.search(pattern, name)
    if result is not None:
        plural = name[:-1] + "s"
        return plural


    return name + 's'

#
