from controller.Helper import DataAccess, Other
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import os

class TodayHandler(webapp.RequestHandler):
    def get(self):
        user = DataAccess.getUser()
        times = DataAccess.getTimes(user.key(), Other.getTodayUTC1())

        output = {"times": times}
        path = os.path.join(os.path.dirname(__file__), '../view/today.html')
        self.response.out.write(template.render(path, output))

    def post(self):
        pass



