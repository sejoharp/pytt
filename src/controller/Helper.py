from datetime import timedelta, datetime, tzinfo
from google.appengine.api import users
from model.models import Property, Time
import math
import time

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
        return Converter.get_full_part(timestamp - (hour * 3600) , 60)

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
        return time.replace(tzinfo=UTC1()) + timedelta(hours=1)

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
            time.start = Converter.dt_to_UTC1(time.start)
            if time.stop is not None:
                time.stop = Converter.dt_to_UTC1(time.stop)
        return times

    @staticmethod
    def getLastTime(userid):
        """ returns the last time dataset from the given userid """
        last_time = Time.gql("where userid = :userid ORDER BY start DESC",
                            userid=userid).get()
        if last_time is not None:
            last_time.start = Converter.dt_to_UTC1(last_time.start)
            if last_time.stop is not None:
                last_time.stop = Converter.dt_to_UTC1(last_time.stop)
        return last_time

    @staticmethod
    def getTime(timeID):
        return Time.get(timeID)

class Other():
    @staticmethod
    def getTodayUTC1():
        return datetime.now(UTC1()).replace(hour=0, minute=0, second=0, microsecond=0)

class UTC1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1)

    def tzname(self, dt):
        return "UTC +1"

    def dst(self, dt):
        return timedelta(0)
