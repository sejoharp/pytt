from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from controller import classes 

application = webapp.WSGIApplication(
                                     [('/', classes.MainPage),
                                      ('/sign', classes.Guestbook),
                                      ('/test', classes.DBTest)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
