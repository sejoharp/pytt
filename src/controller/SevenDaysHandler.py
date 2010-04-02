from controller.Helper import DataAccess, Other
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import datetime
import os

class SevenDaysHandler(webapp.RequestHandler):
    def get(self):
        user = DataAccess.getUser()
        seven_days_ago = Other.getTodayUTC2() + datetime.timedelta(days= -7)
        times = DataAccess.getTimes(user.key(), seven_days_ago)

        output = {"times": times}
        path = os.path.join(os.path.dirname(__file__), '../view/sevenDays.html')
        self.response.out.write(template.render(path, output))

    def post(self):
        pass
