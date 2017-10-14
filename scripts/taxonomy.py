import os
from xml.dom import pulldom

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
    if english_name:
        return getText(english_name[0].childNodes).replace(' and ', ' & ')
    return latin_name

def isExtinct(node):
    return node.hasAttribute('extinct') and node.attributes['extinct'].value == 'yes'

def getHierarchicalDict(english_name_filter=None):
    num_orders = 0
    num_families = 0
    num_genera = 0
    num_species = 0
    num_filter = len(english_name_filter)
    result = {
      'name': 'aves',
      'children': []
    }

    events = pulldom.parse(IOC_NAMES)
    for event, node in events:
        if event != 'START_ELEMENT' or node.tagName != 'order':
            continue
        events.expandNode(node)
        order = node

        if isExtinct(order):
            order.unlink()
            continue
        num_orders += 1
        order_name = getName(order)
        order_result = {
          'name': order_name,
          'children': []
        }
        result['children'].append(order_result)
        # print(order_name)

        families = order.getElementsByTagName('family')
        for family in families:
            if isExtinct(family):
                continue
            num_families += 1
            family_name = getName(family)
            family_result = {
              'name': family_name,
              'children': []
            }
            order_result['children'].append(family_result)
            # print('\t%s' % family_name)

            genera = family.getElementsByTagName('genus')
            for genus in genera:
                if isExtinct(genus):
                    continue
                num_genera += 1
                genus_name = getName(genus)
                genus_result = {
                  'name': genus_name,
                  'children': []
                }
                family_result['children'].append(genus_result)
                # print('\t\t%s' % genus_name)

                speciess = genus.getElementsByTagName('species')
                for species in speciess:
                    if isExtinct(species):
                        continue
                    num_species += 1
                    species_name = getName(species)
                    size = 1000
                    images = {}
                    if english_name_filter:
                        search_name = species_name.replace("'", '').replace(' ', '').replace('-', '').lower()
                        post = english_name_filter.pop(search_name, None)
                        if post:
                            size = post['likes'] + 5 * post['num_comments']
                            images = post['images']
                        else:
                            continue
                    genus_result['children'].append({
                      'name': species_name,
                      'size': size,
                      'images': images
                    })
                    # print('\t\t\t%s' % species_name)
        order.unlink()

    print('%d orders, %d families, %d genera, %d species\n' % (num_orders, num_families, num_genera, num_species))

    if english_name_filter:
        print('ERROR: Couldn\'t match: %s' % ', '.join(english_name_filter.keys()))

    num_matched = num_filter - len(english_name_filter)

    print('\nPhotographed %d of %d species (%.2f%% complete)' % (num_matched, num_species, 100.0 * num_matched / num_species))

    return result
