#!/usr/bin/python

'''Prints extant avian taxonomy.

Usage: ./taxonomy.py
'''

import json
import os
from xml.dom import minidom

IOC_NAMES = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'master_ioc-names_xml.xml')
JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', 'birds.json')

def getChildrenByTagName(node, tag_name):
    rc = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tag_name:
            rc.append(child)
    return rc

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getName(node):
    latin_name = getText(getChildrenByTagName(node, 'latin_name')[0].childNodes)
    english_name = getChildrenByTagName(node, 'english_name')
    if english_name:
        return getText(english_name[0].childNodes)
    return latin_name

def isExtinct(node):
    return node.hasAttribute('extinct') and node.attributes['extinct'].value == 'yes'

num_orders = 0
num_families = 0
num_genera = 0
num_species = 0
aves_json = {
  'name': 'aves',
  'children': []
}

list = minidom.parse(IOC_NAMES).getElementsByTagName('list')[0]
orders = list.getElementsByTagName('order')
for order in orders:
    if isExtinct(order):
        continue
    num_orders += 1
    order_name = getName(order)
    order_json = {
      'name': order_name,
      'children': []
    }
    aves_json['children'].append(order_json)
    print(order_name)

    families = order.getElementsByTagName('family')
    for family in families:
        if isExtinct(family):
            continue
        num_families += 1
        family_name = getName(family)
        family_json = {
          'name': family_name,
          'children': []
        }
        order_json['children'].append(family_json)
        print('\t%s' % family_name)

        genera = family.getElementsByTagName('genus')
        for genus in genera:
            if isExtinct(genus):
                continue
            num_genera += 1
            genus_name = getName(genus)
            genus_json = {
              'name': genus_name,
              'children': []
            }
            family_json['children'].append(genus_json)
            print('\t\t%s' % genus_name)

            speciess = genus.getElementsByTagName('species')
            for species in speciess:
                if isExtinct(species):
                    continue
                num_species += 1
                species_name = getName(species)
                genus_json['children'].append({
                  'name': species_name,
                  'size': 1000
                })
                print('\t\t\t%s' % species_name)

print('\n%d orders, %d families, %d genera, %d species' % (num_orders, num_families, num_genera, num_species))

with open(JSON_OUT, 'w') as f:
    f.write(json.dumps(aves_json))
