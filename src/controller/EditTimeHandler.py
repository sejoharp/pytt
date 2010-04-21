from controller.Helper import DataAccess, Converter
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from Forms import TimeForm
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
            valid_time = timeForm.save(commit=False)
            Converter.model_to_UTC(valid_time)
            valid_time.put()
            self.redirect('/overview')
        else:
            values = {'timeForm':timeForm, 'timeID': timeID}
            path = os.path.join(os.path.dirname(__file__), '../view/editTime.html')
            self.response.out.write(template.render(path, values))
