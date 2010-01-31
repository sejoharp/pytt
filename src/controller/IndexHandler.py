from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
import os

class IndexHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        query = db.GqlQuery("select * from Property where email = :email"
                            , email=user.email())
        amount = query.count(10)

        if amount != 1:
            self.response.out.write("You do not have the permission to use pytt.")
#            path = os.path.join(os.path.dirname(__file__), '../view/error.html')
#            self.response.out.write(template.render(path, template_values))
        else:
            property = query.get()
            if property.worktime == None:
                self.redirect('/properties')
            else:
                self.redirect('/overview')
