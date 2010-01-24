from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from model.models import User
import datetime

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

class DBTest(webapp.RequestHandler):
    def get(self):
        user = User()
        user.userid ="der neue"
        user.worktime = datetime.time(8,0)
        user.setTimedelta(datetime.timedelta(1,1,0,0,1,1))
        self.response.out.write(" hour: " + str(user.overtime_hour))
        self.response.out.write(" min: " + str(user.overtime_min))
        self.response.out.write(" sec: " + str(user.overtime_sec))
        self.response.out.write(" day: " + str(user.overtime_day))
        user.put()
        dbuser = db.get(user.key())
        self.response.out.write("<br> result: ")
        self.response.out.write(dbuser.getTimedelta())

class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            self.response.out.write(users.get_current_user().user_id())
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), '../view/index.html')
        self.response.out.write(template.render(path, template_values))


