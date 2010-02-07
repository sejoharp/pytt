from controller.DBInit import DBInit
from controller.IndexHandler import IndexHandler
from controller.OverviewHandler import Overviewhandler
from controller.PropertyHandler import PropertyHandler
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from controller.TodayHandler import TodayHandler
from controller.EditTimeHandler import EditTimeHandler

application = webapp.WSGIApplication(
                                     [('/', IndexHandler),
                                      ('/properties', PropertyHandler),
                                      ('/overview', Overviewhandler),
                                      ('/today', TodayHandler),
                                      ('/editTime', EditTimeHandler)],
                                     debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
