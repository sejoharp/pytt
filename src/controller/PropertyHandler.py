from datetime import timedelta
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.models import UserProperty
import os

class PropertyHandler(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        query = UserProperty.gql("WHERE userid = :userid ", userid=user.user_id())
        userProperty = query.fetch()
        if self.request.get("worktime_min") is not None:
            worktime = timedelta(self.request.get("worktime_day"), self.request.get("worktime_sec"), 0, 0,
                              self.request.get("worktime_min"), self.request.get("worktime_hour"))
            userProperty.setWorktimedelta(worktime)
        if self.request.get("overtime_min") is not None:
            overtime = timedelta(self.request.get("overtime_day"), self.request.get("overtime_sec"), 0, 0,
                              self.request.get("overtime_min"), self.request.get("overtime_hour"))
            userProperty.setOvertimedelta(overtime)
        userProperty.put()
        self.redirect('/overview')

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), '../view/properties.html')
        self.response.out.write(template.render(path, template_values))



