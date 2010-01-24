from google.appengine.ext import webapp
from datetime import datetime

class Overviewhandler(webapp.RequestHandler):
    def get(self):
        userdata = db(db.user.userid == session.auth.user.id).select().last()
        overtime = userdata.overtime
        worktime = userdata.worktime
        timedata = db(db.times.userid == session.auth.user.id).select().last()
        start = None
        stop = None
        diff = None
        finishing_time = None

        if timedata is not None:
            start = timedata.start
            stop = timedata.stop

        if request.vars.old_state is not None:
            now = datetime.now()
            if request.vars.old_state == "start":
                db.times.insert(start = now)
                if timedata is None:
                    timedata = db(db.times.userid == session.auth.user.id).select().last()
            elif request.vars.old_state == "stop":
                timedata.update_record(stop = now)
                stop = now
                overtime = __getUnix(timedata.stop) - __getUnix(timedata.start) - __getUnixTime(worktime) + overtime
                userdata.update_record(overtime = overtime)

        if timedata is None:
            # never used pytt
            statevalue = "start"
            start = ""
            stop = ""
            diff = ""
            finishing_time = ""
            datetime
        else:
            # used pytt before
            if stop is None:
                # is working
                diff = ""
                finishing_time = __getUnix(start) + __getUnixTime(worktime) - overtime
                finishing_time = datetime.fromtimestamp(finishing_time)
                statevalue = "stop"
            else:
                # is not working
                diff = stop - start
                finishing_time = ""
                statevalue = "start"

        return dict(overtime=overtime,
                    worktime= worktime,
                    start=start,
                    stop=stop,
                    diff=diff,
                    finishing_time = finishing_time,
                    statevalue = statevalue)