from Forms import PropertyForm
from controller.Helper import DataAccess
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class PropertyHandler(webapp.RequestHandler):
    def get(self):
        property = DataAccess.getUser()
        self.__setOutput(PropertyForm(instance=property))

    def post(self):
        property = DataAccess.getUser()
        form = PropertyForm(data=self.request.POST, instance=property)
        if form.is_valid():
            form.save(commit=True)
            self.redirect('/overview')
        else:
            self.__setOutput(form)

    def __setOutput(self, form):
        template_values = {"form" : form}
        path = os.path.join(os.path.dirname(__file__),
                            '../view/properties.html')
        self.response.out.write(template.render(path, template_values))
