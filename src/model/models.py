from google.appengine.ext import db

class Property(db.Model):
    email = db.StringProperty()
    # worktime in seconds
    worktime = db.IntegerProperty()
    # overtime in seconds
    overtime = db.IntegerProperty()

class Time(db.Model):
    userid = db.ReferenceProperty(Property)
    start = db.DateTimeProperty()
    stop = db.DateTimeProperty()
