#!/usr/bin/python

'''Generates json genus -> english family name for ebird checklist (clements).

Usage: ./ebird.py
'''

import csv
import json
import os

TAXONOMY = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'eBird_Taxonomy_v2017_18Aug2017.csv')
JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', 'families.json')

genus_to_family = {}

with open(TAXONOMY, 'rU') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if row['CATEGORY'] != 'species':
            continue
        genus, species = row['SCI_NAME'].split(' ')
        _, english_name = row['FAMILY'].split('(')
        genus_to_family[genus] = english_name[:-1].replace(', and Allies', ', et al.').replace(' and Allies', ', et al.').replace(', and ', ' & ').replace(' and ', ' & ')

iterable = []
for genus, family in genus_to_family.iteritems():
    iterable.append([genus, family])

with open(JSON_OUT, 'w') as f:
    f.write(json.dumps(iterable, separators=(',\n', ':')))
