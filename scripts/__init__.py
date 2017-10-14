import os

import cloudstorage
from google.appengine.api import app_identity

import webapp2

bucket_name = os.environ.get(
        'BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
cloudstorage.set_default_retry_params(
    cloudstorage.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15
        ))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(bucket_name)
        filename = '/%s/birds.json' % bucket_name
        with cloudstorage.open(filename, 'w', content_type='application/json') as f:
            f.write('abcde\n')


app = webapp2.WSGIApplication([
    ('/regenerate', MainPage),
], debug=True)
