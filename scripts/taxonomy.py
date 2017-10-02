#!/usr/bin/python

'''Prints extant avian taxonomy.

Usage: ./taxonomy.py
'''

import os
from xml.dom import minidom

IOC_NAMES = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'master_ioc-names_xml.xml')

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
    if not english_name:
        return latin_name
    return '%s (%s)' % (latin_name, getText(english_name[0].childNodes))

def isExtinct(node):
    return node.hasAttribute('extinct') and node.attributes['extinct'].value == 'yes'

num_orders = 0
num_families = 0
num_genera = 0
num_species = 0

list = minidom.parse(IOC_NAMES).getElementsByTagName('list')[0]
orders = list.getElementsByTagName('order')
for order in orders:
    if isExtinct(order):
        continue
    num_orders += 1
    print(getName(order))

    families = order.getElementsByTagName('family')
    for family in families:
        if isExtinct(family):
            continue
        num_families += 1
        print('\t%s' % getName(family))

        genera = family.getElementsByTagName('genus')
        for genus in genera:
            if isExtinct(genus):
                continue
            num_genera += 1
            print('\t\t%s' % getName(genus))

            speciess = genus.getElementsByTagName('species')
            for species in speciess:
                if isExtinct(species):
                    continue
                num_species += 1
                print('\t\t\t%s' % getName(species))

print('\n%d orders, %d families, %d genera, %d species' % (num_orders, num_families, num_genera, num_species))
