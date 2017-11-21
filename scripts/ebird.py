#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Generates json genus -> english family name for ebird checklist (clements).

Usage: ./ebird.py [language]
'''

import csv
import json
import os
import re
import sys
import urllib2

language_to_languagename = {
  'es': 'español'
}

language = None
languagename = None
outfile = 'families.json'
if len(sys.argv) == 2:
    language = sys.argv[1]
    languagename = language_to_languagename[language]
    outfile = 'families-' + language + '.json'

TAXONOMY = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'eBird_Taxonomy_v2017_18Aug2017.csv')
JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', outfile)

def requestWikicommonsVernacular(sci_name):
    try:
        response = urllib2.urlopen('https://commons.wikimedia.org/wiki/Category:' + sci_name)
        html = response.read()
    except urllib2.HTTPError:
        print 'HTTP Error for ' + sci_name
        return None
    m = re.search('<bdi class="vernacular" lang="' + language + '"><a href="[^"]+" class="extiw" title="[^"]+">([^<]+)</a></bdi>', html)
    if m:
        print 'commons', m.group(1)
        return m.group(1)
    return None

def requestWikispeciesVernacular(sci_name):
    try:
        response = urllib2.urlopen('https://species.wikimedia.org/wiki/' + sci_name)
        html = response.read()
    except urllib2.HTTPError:
        print 'HTTP Error for ' + sci_name
        return None
    m = re.search('<b>' + languagename + ':</b>&#160;([^<]+)<br />', html)
    if m:
        print 'species', m.group(1)
        return m.group(1)
    return None

sci_to_common_family_name = {}
def getCommonFamilyName(sci_name):
    if sci_name not in sci_to_common_family_name:
        common_name = requestWikicommonsVernacular(sci_name)
        if not common_name:
            common_name = requestWikispeciesVernacular(sci_name)
        sci_to_common_family_name[sci_name] = common_name
    return sci_to_common_family_name[sci_name]

genus_to_family = {}
with open(TAXONOMY, 'rU') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if row['CATEGORY'] != 'species':
            continue
        genus, species = row['SCI_NAME'].split(' ')
        sci_family_name, english_name = row['FAMILY'].split('(')
        sci_family_name = sci_family_name.strip()
        english_name = english_name[:-1].replace(', and Allies', ', et al.').replace(' and Allies', ', et al.').replace(', and ', ' & ').replace(' and ', ' & ')
        if language:
            genus_to_family[genus] = getCommonFamilyName(sci_family_name) or sci_family_name
        else:
            genus_to_family[genus] = english_name

iterable = []
for genus, family in genus_to_family.iteritems():
    iterable.append([genus, family])

with open(JSON_OUT, 'w') as f:
    f.write(json.dumps(iterable, separators=(',\n', ':')))
