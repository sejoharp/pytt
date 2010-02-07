from controller.Helper import DataAccess
from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template
from model.models import Time
import os

class EditTimeHandler(webapp.RequestHandler):
    def get(self):
        timeID = self.request.get("timeID")
        time = DataAccess.getTime(timeID)
        timeForm = TimeForm(instance=time)
        values = {'timeForm':timeForm, 'timeID': timeID}
        path = os.path.join(os.path.dirname(__file__), '../view/editTime.html')
        self.response.out.write(template.render(path, values))

    def post(self):
        timeID = self.request.get("timeID")
        time = DataAccess.getTime(timeID)
        timeForm = TimeForm(data=self.request.POST, instance=time)
        if timeForm.is_valid():
            timeForm.save(commit=True)
            self.redirect('/overview')
        else:
            values = {'timeForm':timeForm, 'timeID': timeID}
            path = os.path.join(os.path.dirname(__file__), '../view/editTime.html')
            self.response.out.write(template.render(path, values))


class TimeForm(djangoforms.ModelForm):
    class Meta:
        model = Time
        exclude = ["userid"]
