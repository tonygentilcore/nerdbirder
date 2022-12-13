#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''Generates json genus -> english family name for ebird checklist (clements).

Usage: ./ebird.py [language]
'''

import csv
import json
import os
import re
import sys
import time
import requests
from datetime import timedelta
import requests_cache

requests_cache.install_cache(
    'ebird',
    expire_after=timedelta(days=1),    # Otherwise expire responses after one day
)

language_to_languagename = {
  'es': 'español',
  'fr': 'français'
}

language_to_englishname = {
  'es': 'Spanish',
  'fr': 'French'
}

language = None
languagename = None
englishlanguagename = None
outfile = 'families.json'
if len(sys.argv) == 2:
    language = sys.argv[1]
    languagename = language_to_languagename[language]
    englishlanguagename = language_to_englishname[language]
    outfile = 'families-' + language + '.json'

TAXONOMY = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'ebird_taxonomy_v2022.csv')
JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', outfile)

def requestWikicommonsVernacular(sci_name):
    response = requests.get('https://commons.wikimedia.org/wiki/Category:' + sci_name)
    if response.status_code != 200:
        print('Wiki Commons HTTP Error for ' + sci_name, response.status_code)
        return None
    html = response.text
    m = re.search('<bdi class="vernacular" lang="' + language + '"><a href="[^"]+" class="extiw" title="[^"]+">([^<]+)</a></bdi>', html)
    if m:
        print('Wiki Commons:', m.group(1))
        return m.group(1)
    return None

def requestWikispeciesVernacular(sci_name):
    response = requests.get('https://species.wikimedia.org/wiki/' + sci_name)
    if response.status_code != 200:
        print('Wiki Species HTTP Error for ' + sci_name, response.status_code)
        return None
    html = response.text
    m = re.search('<b>' + languagename + ':</b>&#160;([^<]+)<br />', html)
    if m:
        print('Wiki Species:', m.group(1))
        return m.group(1)
    return None

def requestInaturalistVernacular(sci_name):
    time.sleep(2)
    response = requests.get('https://www.inaturalist.org/taxon_names.json?q=' + sci_name)
    if response.status_code != 200:
        print('iNaturalist HTTP Error for ' + sci_name, response.status_code)
        return None        
    response_json = response.json()
    if len(response_json) < 1:
        return None
    taxon_id = response_json[0]['taxon_id']
    time.sleep(2)
    response = requests.get('https://www.inaturalist.org/taxon_names.json?taxon_id=' + str(taxon_id))
    if response.status_code != 200:
        print('iNaturalist HTTP Error for ' + sci_name, response.status_code)
        return None
    response_json = response.json()
    for record in response_json:
        if record['lexicon'] == englishlanguagename:
            print('iNaturalist:', record['name'])
            return record['name']
    return None

sci_to_common_family_name = {}
def getCommonFamilyName(sci_name):
    if sci_name not in sci_to_common_family_name:
        common_name = requestInaturalistVernacular(sci_name)
        if not common_name:
            common_name = requestWikicommonsVernacular(sci_name)
        if not common_name:
            common_name = requestWikispeciesVernacular(sci_name)
        sci_to_common_family_name[sci_name] = common_name
    return sci_to_common_family_name[sci_name]

genus_to_family = {}
with open(TAXONOMY, 'r') as csvfile:
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
for genus, family in genus_to_family.items():
    iterable.append([genus, family])

with open(JSON_OUT, 'w') as f:
    f.write(json.dumps(iterable, separators=(',\n', ':')))
