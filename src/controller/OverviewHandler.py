from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.models import UserProperty, Time
import os

class Overviewhandler(webapp.RequestHandler):
    def get(self):
        user = UserProperty.gql("where email = :email", email=users.get_current_user().email()).get()
        time = Time.gql("where userid = :userid ORDER BY height DESC", userid=user.key()).get()
        if time is None:
            # never worked
            start = None
            stop = None
            state = "start"
        else:
            # data found
            start = time.start
            stop = time.stop
            # alle time-Daten holen, bei dem die Startzeit dem aktuellen Datum entspricht.
            if time.stop is None:
                # is still working
                state = "stop"
                # beim letzten time-datensatz die stopzeit auf now setzen
            else:
                # is not working
                state = "start"
                        # finishing_time berechnen
            # alle Arbeiteszeiten von heute berücksichtigen, 
            # wenn gerade gearbeitet wird muss da auch mitberücksichtigt werden
            # könnte über eine Methode geschehen, die alle Zeiten ermittelt. Wirg gerade gearbeitet
            # wird beim letzten Datensatz die stopzeit auf now gesetzt.

        template_values = {"start": start,
                           "stop": stop,
                           "state": state,
                           "worktime": user.getWorktimedelta(),
                           "overtime": user.getOvertimedelta(), }
        path = os.path.join(os.path.dirname(__file__), '../view/overview.html')
        self.response.out.write(template.render(path, template_values))


        #timedata = db(db.times.userid == session.auth.user.id).select().last()
#        start = None
#        stop = None
#        diff = None
#        finishing_time = None
#
#        if timedata is not None:
#            start = timedata.start
#            stop = timedata.stop
#
#        if request.vars.old_state is not None:
#            now = datetime.now()
#            if request.vars.old_state == "start":
#                db.times.insert(start=now)
#                if timedata is None:
#                    timedata = db(db.times.userid == session.auth.user.id).select().last()
#            elif request.vars.old_state == "stop":
#                timedata.update_record(stop=now)
#                stop = now
#                overtime = __getUnix(timedata.stop) - __getUnix(timedata.start) - __getUnixTime(worktime) + overtime
#                userdata.update_record(overtime=overtime)
#
#        if timedata is None:
#            # never used pytt
#            statevalue = "start"
#            start = ""
#            stop = ""
#            diff = ""
#            finishing_time = ""
#            datetime
#        else:
#            # used pytt before
#            if stop is None:
#                # is working
#                diff = ""
#                finishing_time = __getUnix(start) + __getUnixTime(worktime) - overtime
#                finishing_time = datetime.fromtimestamp(finishing_time)
#                statevalue = "stop"
#            else:
#                # is not working
#                diff = stop - start
#                finishing_time = ""
#                statevalue = "start"
#
#        return dict(overtime=overtime,
#                    worktime=worktime,
#                    start=start,
#                    stop=stop,
#                    diff=diff,
#                    finishing_time=finishing_time,
#                    statevalue=statevalue)
