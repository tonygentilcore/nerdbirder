import json
import os

import cloudstorage
from google.appengine.api import app_identity

import webapp2

import instagram
import taxonomy

BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
JSON_OUT = '/%s/birds.json' % BUCKET_NAME

cloudstorage.set_default_retry_params(
    cloudstorage.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15
        ))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(BUCKET_NAME)
        instagram_posts = instagram.getPostsByEnglishName()
        taxonomy_dict = taxonomy.getHierarchicalDict(english_name_filter=instagram_posts)

        with cloudstorage.open(
          JSON_OUT, 'w', content_type='application/json', options={'x-goog-acl': 'public-read'}) as f:
            f.write(json.dumps(taxonomy_dict, separators=(',\n', ':')))

app = webapp2.WSGIApplication([
    ('/regenerate_json', MainPage),
], debug=True)
