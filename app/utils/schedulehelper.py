from datetime import datetime, timezone, timedelta
from config import get_env
import json
import pytz
import os

utc=pytz.UTC

class ScheduleHelper:
    def __init__(self, bootcamp):
        path = get_env('SETTING_FILE').rsplit('/', 1)
        filename = os.path.join(path[0], bootcamp, path[1])
        
        with open(filename) as f:
            data = json.load(f)["schedule"]
        self.registration = data["registration_date"]
        for k in self.registration.keys():
            self.registration[k] = ScheduleHelper.to_time(self.registration[k])
        self.days = data["days_starting_date"]
        for k in self.days.keys():
            self.days[k] = ScheduleHelper.to_time(self.days[k])
        self.start = ScheduleHelper.to_time(data["start_date"])
        self.now = datetime.now(timezone.utc) + timedelta(hours=2)
    
    def __repr__(self):
        string = str(self.registration) + '\n'
        string += str(self.days) + '\n'
        string += str(self.start)
        return string

    def can_register(self):
        start = utc.localize(self.registration['start'])
        end = utc.localize(self.registration['end'])
        # Check if time is good
        if self.now > end or self.now < start:
            return False
        return True

    def can_fetchday(self, key):
        key = key.replace("day", "")
        # Check if key exist
        if key not in self.days:
            return False
        start = utc.localize(self.days[key])
        # Check if time is good
        if self.now < start:
            return False
        return True

    def event_has_started(self, key):
        start = utc.localize(self.start)
        # Check if time is good
        if self.now < start:
            return False
        return True


    @staticmethod
    def to_time(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

