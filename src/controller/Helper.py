import math
import time

from datetime import datetime
from datetime import timedelta
from datetime import tzinfo
from google.appengine.api import users
from model.models import Property
from model.models import Time

class Converter():
    @staticmethod
    def td_to_secs(delta):
        return delta.seconds + delta.days * 24 * 3600

    @staticmethod
    def secs_to_td(seconds):
        return timedelta(seconds=seconds)

    @staticmethod
    def dt_to_str(dt):
        if dt is not None:
            ret = dt.strftime("%H:%M:%S %d.%m.%Y")
        else:
            ret = ""
        return ret

    @staticmethod
    def secs_to_str(secs):
        hour = Converter.get_full_part(secs, 3600)
        min = Converter.get_min_from_timestamp(secs, hour)
        sec = Converter.get_sec_from_timestamp(secs, hour, min)
        return str(hour) + "h " + str(min) + "m " + str(sec) + "s"

    @staticmethod
    def td_to_str(delta):
        day = delta.days
        hour = Converter.get_full_part(delta.seconds, 3600)
        min = Converter.get_min_from_timestamp(delta.seconds, hour)
        sec = Converter.get_sec_from_timestamp(delta.seconds, hour, min)
        return str(day) + "d " + str(hour) + "h " + str(min) + "m " + str(sec) + "s"

    @staticmethod
    def td_to_str2(delta):
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return str(hours) + ":" + str(minutes) + ":" + str(seconds)
    
    @staticmethod
    def dt_to_secs(value):
        return time.mktime(value.timetuple())

    @staticmethod
    def get_sec_from_timestamp(timestamp, hour, mins):
        return Converter.get_full_part(timestamp - (hour * 3600 + mins * 60), 60)

    @staticmethod
    def get_hour_from_timestamp(timestamp):
        return Converter.get_full_part(timestamp, 3600)

    @staticmethod
    def get_min_from_timestamp(timestamp, hour):
        return Converter.get_full_part(timestamp - (hour * 3600), 60)

    @staticmethod
    def secs_to_dt(secs):
        return datetime.fromtimestamp(secs)

    @staticmethod
    def get_full_part(value, divisor):
        if value < 0:
            negative = True
            value = int(math.fabs(value))
        else:
            negative = False

        full = value / divisor
        if negative == True:
            full = full * -1
        return full

    @staticmethod
    def dt_to_UTC1(time):
        return Converter.dt_to_tz(time, UTC(), UTC1())

    @staticmethod
    def dt_to_tz(time, from_tz, to_tz):
        return time.replace(tzinfo=from_tz).astimezone(to_tz)

    @staticmethod
    def model_to_UTC1(time_model):
        Converter.model_to_tz(time_model, UTC(), UTC1())

    @staticmethod
    def model_to_UTC(time_model):
        Converter.model_to_tz(time_model, UTC1(), UTC())

    @staticmethod
    def model_to_tz(time_model, from_tz, to_tz):
        time_model.start = Converter.dt_to_tz(time_model.start, from_tz, to_tz)
        if time_model.stop is not None:
            time_model.stop = Converter.dt_to_tz(time_model.stop, from_tz, to_tz)

class DataAccess():
    @staticmethod
    def getUser():
        """ returns the properties from the current user """
        return Property.gql("where email = :email", email=users.get_current_user().email()).get()

    @staticmethod
    def getTimes(userid, date):
        """ returns all time datasets from the given date
        from the given userid """
        times = Time.gql("where userid = :userid and start >= :date",
                         userid=userid, date=date).fetch(1000)
        for time in times:
            Converter.model_to_UTC1(time)
        return times

    @staticmethod
    def getTimesFromTo(userid, startdate, enddate):
        """ returns all time datasets from the given date
        from the given userid """
        times = Time.gql("where userid = :userid and start > :startdate and start < :enddate order by start",
                         userid=userid, startdate=startdate, enddate=enddate).fetch(1000)
        for time in times:
            Converter.model_to_UTC1(time)
        return times

    @staticmethod
    def getThreeMonthsTimes(userid):
        """ returns all time datasets from the given date from the given userid """
        times = Time.gql("where userid = :userid and start > datetime(2010,12,31) and start < datetime(2011,4,1) order by start",
                         userid=userid).fetch(1000)
        for time in times:
            Converter.model_to_UTC1(time)
        return times
        
    @staticmethod
    def getLastTime(userid):
        """ returns the last time dataset from the given userid """
        last_time = Time.gql("where userid = :userid ORDER BY start DESC",
                             userid=userid).get()
        if last_time is not None:
            Converter.model_to_UTC1(last_time)
        return last_time

    @staticmethod
    def getTime(timeID):
        time = Time.get(timeID)
        Converter.model_to_UTC1(time)
        return time

class Other():
    @staticmethod
    def getTodayUTC1():
        return Other.getNowUTC1().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def getNowUTC1():
        return datetime.now(UTC1())

class UTC1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def first_sunday_on_or_after(self, dt):
        days_to_go = 6 - dt.weekday()
        if days_to_go:
            dt += timedelta(days_to_go)
        return dt

    def dst(self, dt):
        """daylight saving time"""

        if self.dst_start(dt.year) <= dt.replace(tzinfo=None) < self.dst_end(dt.year):
            return timedelta(hours=1)
        else:
            return timedelta(hours=0)

    def tzname(self, dt):
        if self.dst(dt) == timedelta(hours=0):
            # Central European Time
            return "CET"
        else:
            # Central European Summer Time
            return "CEST"

    def dst_start(self, year):
        # european summer time starts 1 am (utc) on the last Sunday of March
        return self.first_sunday_on_or_after(datetime(year, 3, 25, 1))

    def dst_end(self, year):
        # european summer time ends 1 am (utc) on the last Sunday of October
        return self.first_sunday_on_or_after(datetime(year, 10, 25, 1))

class UTC(tzinfo):
    def utcoffset(self, dt):
        return self.dst(dt)

    def dst(self, dt):
        """daylight saving time"""
        return timedelta(hours=0)


    def tzname(self, dt):
        return "UTC"
    
