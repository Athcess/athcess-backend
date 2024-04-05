import calendar
import json


class CustomCalendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def _calculate_day_data(self, day):
        day_name = calendar.day_name[calendar.weekday(self.year, self.month, day)]
        return {"day": day_name, "event": ""}

    def create_calendar(self):
        cal = calendar.monthcalendar(self.year, self.month)
        days_data = {}
        for week in cal:
            for day in week:
                if day != 0:
                    days_data[day] = self._calculate_day_data(day)
        return json.dumps(days_data)
