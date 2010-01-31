from datetime import timedelta, datetime
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
            ret = dt
        return ret

    @staticmethod
    def secs_to_str(secs):
        hour = secs / 3600
        min = (secs % 3600) / 60
        sec = secs % 60
        return str(hour) + "h " + str(min) + "m " + str(sec) + "s"

    @staticmethod
    def td_to_str(delta):
        day = delta.days
        hour = delta.seconds / 3600
        min = (delta.seconds % 3600) / 60
        sec = delta.seconds % 60
        return str(day) + "d " + str(hour) + "h " + str(min) + "m " + str(sec) + "s"

    @staticmethod
    def dt_to_secs(value):
        return time.mktime(value.timetuple())

    @staticmethod
    def secs_to_dt(secs):
        return datetime.fromtimestamp(secs)
