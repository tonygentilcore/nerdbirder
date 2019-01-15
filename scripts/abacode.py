#!/usr/bin/python

'''Generates json species -> ABA Code.

Usage: ./abacode.py
'''

import csv
import json
import os

CHECKLIST = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'ABA_Checklist-8.0.5.csv')
JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', 'abacodes.json')

FIELDNAMES = ['family', 'common name', 'scientific name', 'abbr', 'code']
iterable = []
with open(CHECKLIST, 'rU') as csvfile:
    rows = csv.DictReader(csvfile, fieldnames=FIELDNAMES)
    for row in rows:
        scientific_name = row['scientific name']
        code = row['code']
        if not code or int(code) < 3:
            continue
        iterable.append([scientific_name, code])

with open(JSON_OUT, 'w') as f:
    f.write(json.dumps(iterable, separators=(',\n', ':')))
