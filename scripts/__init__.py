import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('TODO!')


app = webapp2.WSGIApplication([
    ('/regenerate', MainPage),
], debug=True)
