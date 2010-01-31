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
            times_today = self.__getTimes(user.key(), date.today())
            if last_time.stop is None:
                """ is still working """
                self.__buttonlabel = "stop"
                times_today[len(times_today) - 1].stop = datetime.now(UTC1())
            else:
                """ is not working """
                self.__buttonlabel = "start"

            workedtime = self.__getWorkedtime(times_today)
            workedtime_with_overtime = Converter.td_to_secs(workedtime) + user.overtime
            time_to_work = user.worktime - workedtime_with_overtime
            finishing_time = datetime.now(UTC1()) + Converter.secs_to_td(time_to_work)

            """ format output values """
            self.__worktime_str = Converter.secs_to_str(user.worktime)
            self.__finishing_time_str = Converter.dt_to_str(finishing_time)
            self.__time_to_work_str = Converter.secs_to_str(time_to_work)
            self.__workedtime_str = Converter.secs_to_str(Converter.td_to_secs(workedtime))
            self.__start = Converter.dt_to_str(last_time.start)
            self.__stop = Converter.dt_to_str(last_time.stop)
            self.__overtime_str = Converter.secs_to_str(user.overtime)

        output = self.__getOutput()
        path = os.path.join(os.path.dirname(__file__), '../view/overview.html')
        self.response.out.write(template.render(path, output))

    def post(self):
        user = self.__getUser()
        last_time = self.__getLastTime(user.key())
        self.__update_overtime(last_time, user)

        if last_time is not None and last_time.stop is None:
            last_time.stop = datetime.now(UTC1())
            last_time.put()
        else:
            new_time = Time(userid=user.key(), start=datetime.now(UTC1()))
            new_time.put()

        self.redirect('/overview')

    def __update_overtime(self, last_time, user):
        """ updates the overtime from the given user
        preconditions: last_time and last_time.stop are not None """
        if last_time is not None and last_time.stop is not None:
            times_today = self.__getTimes(user.key(), date.today())
            if len(times_today) == 0:
                last_day = last_time.start.replace(hour=0, minute=0, second=0, microsecond=0)
                times_last_day = self.__getTimes(user.key(), last_day)
                worked_time = self.__getWorkedtime(times_last_day)
                workedtime_with_overtime = Converter.td_to_secs(worked_time) + user.overtime
                user.overtime = workedtime_with_overtime - user.worktime
                user.put()

    def __getOutput(self):
        """ returns a dictionary with all output values """
        return {"start": self.__start,
                  "stop": self.__stop,
                  "state": self.__buttonlabel,
                  "worktime": self.__worktime_str,
                  "overtime": self.__overtime_str,
                  "workedtime_today" : self.__workedtime_str,
                  "finishing_time" : self.__finishing_time_str,
                  "time_to_work": self.__time_to_work_str,
                  "time": Converter.dt_to_str(datetime.now(UTC1())), }

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
        return Time.gql("where userid = :userid ORDER BY start DESC",
                            userid=userid).get()

    def __getTimes(self, userid, date):
        """ returns all time datasets from the given date
        from the given userid """
        return Time.gql("where userid = :userid and start >= :date",
                                   userid=userid, date=date).fetch(100)

    def __getWorkedtime(self, times):
        """ returns the worked time from the given times """
        workedtime_today = timedelta()
        for time in times:
                workedtime_today += time.stop - time.start
        return workedtime_today




