from datetime import timedelta
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template
from model.models import Property
import os

class PropertyHandler(webapp.RequestHandler):
    def post(self):
        property = property = self.__getProperty()
        form = PropertyForm(data=self.request.POST, instance=property)
        if form.is_valid():
            property = form.save(commit=True)
            #property.email = user.email()
            #property.put()
            self.redirect('/overview')
        else:
            self.__setOutput(form)
#        query = Property.gql("WHERE userid = :userid ", userid=user.user_id())
#        userProperty = query.get()
#        if userProperty is None:
#            userProperty = Property(email=user.email(), worktime_sec=0, worktime_day=0, overtime_sec=0, overtime_day=0)
#        if self.request.get("worktime_min") is not None:
#            worktime = timedelta(0, 0, 0, 0,
#                                 int(self.request.get("worktime_min")),
#                                 int(self.request.get("worktime_hour")))
#            userProperty.setWorktimedelta(worktime)
#        if self.request.get("overtime_min") is not None:
#            overtime = timedelta(int(self.request.get("overtime_day")),
#                                 0, 0, 0,
#                              int(self.request.get("overtime_min")),
#                              int(self.request.get("overtime_hour")))
#            userProperty.setOvertimedelta(overtime)
#        userProperty.put()


    def get(self):
        property = self.__getProperty()
        self.__setOutput(PropertyForm(instance=property))

    def __setOutput(self, form):
        template_values = {"form" : form}
        path = os.path.join(os.path.dirname(__file__),
                            '../view/properties.html')
        self.response.out.write(template.render(path, template_values))

    def __getProperty(self):
        user = users.get_current_user()
        return Property.gql("where email = :email ",
                                email=user.email()).get()

class PropertyForm(djangoforms.ModelForm):
    class Meta:
        model = Property
        exclude = ["email"]

