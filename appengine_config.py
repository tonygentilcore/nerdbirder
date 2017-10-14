from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')

import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
