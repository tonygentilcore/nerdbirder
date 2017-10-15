import os
from xml.etree.cElementTree import iterparse

IOC_NAMES = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'master_ioc-names_xml.xml')

def getName(node):
    latin_name = node.findtext('latin_name')
    english_name = node.findtext('english_name')
    if english_name:
        return english_name.replace('and allies', 'et al').replace(' and ', ' & ')
    return latin_name

def isExtinct(node):
    return node.get('extinct') == 'yes'

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

    for event, elem in iterparse(IOC_NAMES):
        if elem.tag != 'order':
            continue
        order = elem

        if isExtinct(order):
            order.clear()
            continue
        num_orders += 1
        order_name = getName(order)
        order_result = {
          'name': order_name,
          'children': []
        }
        result['children'].append(order_result)
        # print(order_name)

        families = order.findall('family')
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

            genera = family.findall('genus')
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

                speciess = genus.findall('species')
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
        order.clear()

    print('%d orders, %d families, %d genera, %d species\n' % (num_orders, num_families, num_genera, num_species))

    if english_name_filter:
        print('ERROR: Couldn\'t match: %s' % ', '.join(english_name_filter.keys()))

    num_matched = num_filter - len(english_name_filter)

    print('\nPhotographed %d of %d species (%.2f%% complete)' % (num_matched, num_species, 100.0 * num_matched / num_species))

    return result
