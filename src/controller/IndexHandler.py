from datetime import timedelta
from google.appengine.api import users
from google.appengine.ext import webapp
from model.models import UserProperty

class IndexHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        query = UserProperty.gql("WHERE userid = :userid ",
                  userid=user.user_id())
        userProperty = query.fetch()

        if userProperty.__len__() != 1:
            template_values = {"message": "You do not have the permission to use pytt.", }
            path = os.path.join(os.path.dirname(__file__), '../view/error.html')
        elif self.request.get("worktime") is not None:
            userProperty.worktime = self.request.get("worktime");
            userProperty.setTimedeta(
                                     datetime.timedelta(
                                                        self.request.get("day"),
                                                        self.overtime_sec, 0, 0,
                                                        self.overtime_min,
                                                        self.overtime_hour))
        elif userProperty.worktime == None:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), '../view/index.html')
        else:
            self.redirect('/overview')

        self.response.out.write(template.render(path, template_values))