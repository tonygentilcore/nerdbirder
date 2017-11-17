#!/usr/bin/python

'''Generates json species -> redlist category.

Usage: ./redlist.py
'''

import csv
import json
import os

REDLIST = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'species_20171108_5576.csv')
JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', 'redlist.json')

genus_to_family = {}

iterable = []
with open(REDLIST, 'rU') as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        iterable.append([row['Scientific name'], row['Global IUCN Red List Category'][:2]])

with open(JSON_OUT, 'w') as f:
    f.write(json.dumps(iterable, separators=(',\n', ':')))