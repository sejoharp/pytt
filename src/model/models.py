from google.appengine.ext import db
import datetime

class Property(db.Model):
    email = db.StringProperty()
    # worktime in seconds
    worktime = db.IntegerProperty()
    # overtime in seconds
    overtime = db.IntegerProperty()

    def getOvertimedelta(self):
        return datetime.timedelta(seconds=self.overtime)

    def getWorktimedelta(self):
        return datetime.timedelta(seconds=self.worktime)

    def setOvertimedelta(self, delta):
        self.overtime = delta.seconds + delta.days * 24 * 3600

    def setWorktimedelta(self, delta):
        self.worktime = delta.seconds + delta.days * 24 * 3600

class Time(db.Model):
    userid = db.ReferenceProperty(Property)
    start = db.DateTimeProperty()
    stop = db.DateTimeProperty()
