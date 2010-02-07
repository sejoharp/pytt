from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template
from model.models import Property
import os

class PropertyHandler(webapp.RequestHandler):
    def post(self):
        property = self.__getProperty()
        form = PropertyForm(data=self.request.POST, instance=property)
        if form.is_valid():
            form.save(commit=True)
            self.redirect('/overview')
        else:
            self.__setOutput(form)


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

