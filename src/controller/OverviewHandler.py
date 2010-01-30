from datetime import date, datetime, timedelta
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.models import Property, Time
import os

class Overviewhandler(webapp.RequestHandler):
    def get(self):
        user = Property.gql("where email = :email",
                            email=users.get_current_user().email()).get()
        lastTime = Time.gql("where userid = :userid ORDER BY start DESC",
                            userid=user.key()).get()
        if lastTime is None:
            # never worked
            start = None
            stop = None
            state = "start"
            workedtime_today = None
            finishing_time = None
        else:
            # data found
            start = lastTime.start
            stop = lastTime.stop
            # alle lastTime-Daten holen, bei dem die Startzeit dem aktuellen Datum entspricht.
            times_today = Time.gql("where userid = :userid and start >= :heute",
                                   userid=user.key(), heute=date.today()).fetch(100)
            if lastTime.stop is None:
                # is still working
                state = "stop"
                # beim letzten lastTime-datensatz die stopzeit auf now setzen
                times_today[len(times_today) - 1].stop = datetime.now()
            else:
                # is not working
                state = "start"
            # finishing_time berechnen
            # alle Arbeiteszeiten von heute beruecksichtigen,
            workedtime_today = timedelta()
            for time in times_today:
                workedtime_today += time.stop - time.start

            workedtime_with_Overtime = workedtime_today + user.getOvertimedelta()
            time_to_work = user.getWorktimedelta() - workedtime_with_Overtime
            finishing_time = datetime.now() + time_to_work

        template_values = {"start": start,
                           "stop": stop,
                           "state": state,
                           "worktime": user.getWorktimedelta(),
                           "overtime": user.getOvertimedelta(),
                           "workedtime_today" : workedtime_today,
                           "finishing_time" : finishing_time,
                           "time_to_work": time_to_work,
                           }
        path = os.path.join(os.path.dirname(__file__), '../view/overview.html')
        self.response.out.write(template.render(path, template_values))
