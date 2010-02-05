from controller.Helper import Converter, UTC1
from datetime import date, datetime, timedelta
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.models import Property, Time
import os

class Overviewhandler(webapp.RequestHandler):
    def get(self):
        user = self.__getUser()
        last_time = self.__getLastTime(user.key())

        if last_time is None:
            """ never worked """
            # overtime und worktime koennten angezeigt werden
            self.__setNewUser()
        else:
            # data found
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            self.__times_today = self.__getTimes(user.key(), today)
            if last_time.stop is None:
                """ is still working """
                self.__buttonlabel = "stop"
                self.__times_today[len(self.__times_today) - 1].stop = datetime.now()
            else:
                """ is not working """
                self.__buttonlabel = "start"

            workedtime = self.__getWorkedtime(self.__times_today)
            workedtime_with_overtime = Converter.td_to_secs(workedtime) + user.overtime
            time_to_work = user.worktime - workedtime_with_overtime
            self.__finishing_time = datetime.now() + Converter.secs_to_td(time_to_work)
            if self.__buttonlabel == "stop":
                self.__times_today[len(self.__times_today) - 1].stop = None
            """ format output values """
            self.__worktime_str = Converter.secs_to_str(user.worktime)
            self.__time_to_work_str = Converter.secs_to_str(time_to_work)
            self.__workedtime_str = Converter.secs_to_str(Converter.td_to_secs(workedtime))
            self.__overtime_str = Converter.secs_to_str(user.overtime)

        output = self.__getOutput()
        path = os.path.join(os.path.dirname(__file__), '../view/overview.html')
        self.response.out.write(template.render(path, output))

    def post(self):
        user = self.__getUser()
        last_time = self.__getLastTime(user.key())
        self.__update_overtime(last_time, user)

        now = datetime.now()
        if last_time is not None and last_time.stop is None:
            last_time.stop = now
            last_time.put()
        else:
            new_time = Time(userid=user.key(), start=now)
            new_time.put()

        self.redirect('/overview')

    def __update_overtime(self, last_time, user):
        """ updates the overtime from the given user
        preconditions: last_time and last_time.stop are not None """
        if last_time is not None and last_time.stop is not None:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            times_today = self.__getTimes(user.key(), today)
            if len(times_today) == 0:
                last_day = last_time.start.replace(hour=0, minute=0, second=0, microsecond=0)
                times_last_day = self.__getTimes(user.key(), last_day)
                worked_time = self.__getWorkedtime(times_last_day)
                workedtime_with_overtime = Converter.td_to_secs(worked_time) + user.overtime
                user.overtime = workedtime_with_overtime - user.worktime
                user.put()

    def __getOutput(self):
        """ returns a dictionary with all output values """
        return {"times": self.__times_today,
                  "state": self.__buttonlabel,
                  "worktime": self.__worktime_str,
                  "overtime": self.__overtime_str,
                  "workedtime_today" : self.__workedtime_str,
                  "finishing_time" : self.__finishing_time,
                  "time_to_work": self.__time_to_work_str }

    def __setNewUser(self):
        """ sets the output values for a new user """
        self.__start = None
        self.__stop = None
        self.__buttonlabel = "start"
        self.__workedtime_today = None
        self.__finishing_time = None
        self.__worktime_str = None
        self.__overtime_str = None
        self.__finishing_time_str = None
        self.__time_to_work_str = None
        self.__workedtime_str = None

    def __getUser(self):
        """ returns the properties from the current user """
        return Property.gql("where email = :email",
                            email=users.get_current_user().email()).get()

    def __getLastTime(self, userid):
        """ returns the last time dataset from the given userid """
        last_time = Time.gql("where userid = :userid ORDER BY start DESC",
                            userid=userid).get()
        if last_time is not None:
            last_time.start = last_time.start.replace() #+ timedelta(hours=1)
            if last_time.stop is not None:
                last_time.stop = last_time.stop.replace()# + timedelta(hours=1)
        return last_time

    def __getTimes(self, userid, date):
        """ returns all time datasets from the given date
        from the given userid """
        times = Time.gql("where userid = :userid and start >= :date",
                                   userid=userid, date=date).fetch(100)
        for time in times:
            time.start = time.start.replace() #+ timedelta(hours=1)
            if time.stop is not None:
                time.stop = time.stop.replace() #+ timedelta(hours=1)
        return times

    def __getWorkedtime(self, times):
        """ returns the worked time from the given times """
        workedtime_today = timedelta()
        for time in times:
            workedtime_today += time.stop - time.start
        return workedtime_today




