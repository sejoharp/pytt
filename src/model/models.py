from google.appengine.ext import db
import datetime

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class UserProperty(db.Model):
    email = db.StringProperty()
    worktime_sec = db.IntegerProperty()
    worktime_day = db.IntegerProperty()
    overtime_sec = db.IntegerProperty()
    overtime_day = db.IntegerProperty()

    def getOvertimedelta(self):
        return datetime.timedelta(self.overtime_day,
                                  self.__getSecs(self.overtime_sec),
                                  0, 0,
                                  self.__getMins(self.overtime_sec),
                                  self.__getHours(self.overtime_sec))

    def setOvertimedelta(self, delta):
        self.overtime_sec = delta.seconds
        self.overtime_day = delta.days

    def getWorktimedelta(self):
        return datetime.timedelta(self.worktime_day,
                                  self.__getSecs(self.worktime_sec),
                                  0, 0,
                                  self.__getMins(self.worktime_sec),
                                  self.__getHours(self.worktime_sec))

    def setWorktimedelta(self, delta):
        self.worktime_sec = delta.seconds
        self.worktime_day = delta.days

    def __getMins(self, secs):
        return (secs % 3600) / 60

    def __getHours(self, secs):
        return secs / 3600

    def __getSecs(self, secs):
        return secs % 60

class Time(db.Model):
    userid = db.ReferenceProperty(UserProperty)
    start = db.DateTimeProperty()
    stop = db.DateTimeProperty()
