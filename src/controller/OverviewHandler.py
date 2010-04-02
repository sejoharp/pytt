from controller.Helper import Converter, UTC2, DataAccess, Other
from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.models import Time
import os

class Overviewhandler(webapp.RequestHandler):
    def get(self):
        user = DataAccess.getUser()
        last_time = DataAccess.getLastTime(user.key())

        if last_time is None:
            """ never worked """
            # overtime und worktime koennten angezeigt werden
            self.__setNewUser()
        else:
            # data found
            today = Other.getTodayUTC1()
            self.__times_today = DataAccess.getTimes(user.key(), today)
            if last_time.stop is None:
                """ is still working """
                self.__buttonlabel = "stop"
                self.__times_today[len(self.__times_today) - 1].stop = datetime.now(UTC2())
            else:
                """ is not working """
                self.__buttonlabel = "start"

            workedtime = self.__getWorkedtime(self.__times_today)
            workedtime_with_overtime = Converter.td_to_secs(workedtime) + user.overtime
            time_to_work = user.worktime - workedtime_with_overtime

            """ format output values """
            self.__finishing_time = datetime.now(UTC2()) + Converter.secs_to_td(time_to_work)
            if self.__buttonlabel == "stop":
                self.__times_today[len(self.__times_today) - 1].stop = None
            self.__worktime_str = Converter.secs_to_str(user.worktime)
            self.__time_to_work_str = Converter.secs_to_str(time_to_work)
            self.__workedtime_str = Converter.secs_to_str(Converter.td_to_secs(workedtime))
            self.__overtime_str = Converter.secs_to_str(user.overtime)

        output = self.__getOutput()
        path = os.path.join(os.path.dirname(__file__), '../view/overview.html')
        self.response.out.write(template.render(path, output))

    def post(self):
        user = DataAccess.getUser()
        last_time = DataAccess.getLastTime(user.key())
        self.__update_overtime(last_time, user)

        now = datetime.now(UTC2())
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
            today = Other.getTodayUTC1()
            times_today = DataAccess.getTimes(user.key(), today)
            if len(times_today) == 0:
                last_day = last_time.start.replace(hour=0, minute=0, second=0, microsecond=0)
                times_last_day = DataAccess.getTimes(user.key(), last_day)
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
                  "time_to_work": self.__time_to_work_str,
                  "time": datetime.now(UTC2()) }

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


    def __getWorkedtime(self, times):
        """ returns the worked time from the given times """
        workedtime_today = timedelta()
        for time in times:
            workedtime_today += time.stop - time.start
        return workedtime_today




