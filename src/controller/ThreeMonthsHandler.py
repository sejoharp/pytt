from controller.Helper import Converter, DataAccess, Other
from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.models import Time
import os

class Day():
    def __init__(self, date, worktime):
        self.date = date
        self.over = ""
        self.under = ""
        self.worktime = worktime
    
class ThreeMonthsHandler(webapp.RequestHandler):
    def get(self):
        user = DataAccess.getUser()
        times = DataAccess.getThreeMonthsTimes(user.key())
        days = []
        last_day = Day(times[0].start.date(),timedelta())
        for interval in times:
            if last_day.date != interval.start.date():
                days.append(self.generate_day(last_day))
                last_day = Day(interval.start.date(), timedelta())
           
            last_day.worktime += interval.stop - interval.start
        days.append(self.generate_day(last_day))
            
        path = os.path.join(os.path.dirname(__file__), '../view/three_months.html')
        self.response.out.write(template.render(path, {"days": days}))
        
    def generate_day(self, day):
        if day.worktime <= timedelta(hours=8):
            day.under = timedelta(hours=8) - day.worktime
            day.under = Converter.td_to_str2(day.under)
        elif day.worktime > timedelta(hours=8):
            day.over = day.worktime - timedelta(hours=8)
            day.over = Converter.td_to_str2(day.over)
        day.worktime = Converter.td_to_str2(day.worktime) 
        return day  
            