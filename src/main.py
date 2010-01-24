from controller.IndexHandler import IndexHandler
from controller.OverviewHandler import Overviewhandler
from controller.PropertyHandler import PropertyHandler
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

application = webapp.WSGIApplication(
                                     [('/', IndexHandler),
                                      ('/properties', PropertyHandler),
                                      ('/overview', Overviewhandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
