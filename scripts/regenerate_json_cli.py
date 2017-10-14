#!/usr/bin/python

'''Generates json for taxonomical visualization of nerdbirder instagram photos.

Usage: ./regenerate_json_cli.py
'''

import json
import os

import instagram
import taxonomy

JSON_OUT = os.path.join(os.path.dirname(__file__), os.pardir, 'site', 'birds.json')

def main():
    instagram_posts = instagram.getPostsByEnglishName()
    taxonomy_dict = taxonomy.getHierarchicalDict(english_name_filter=instagram_posts)

    with open(JSON_OUT, 'w') as f:
        f.write(json.dumps(taxonomy_dict, separators=(',\n', ':')))

if __name__ == '__main__':
    main()
