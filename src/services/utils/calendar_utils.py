import calendar
import json

def _calculate_day_data(year, month, day):
    day_name = calendar.day_name[calendar.weekday(year, month, day)]
    return {"day": day_name, "event": ""}

def create_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    days_data = {}
    for week in cal:
        for day in week:
            if day != 0:
                days_data[day] = _calculate_day_data(year, month, day) 
    return json.dumps(days_data)

def append_event(day, event, calendar_data):
    calendar_dict = json.loads(calendar_data)  # Convert JSON string to dictionary
    if day in calendar_dict:
        calendar_dict[day]["event"] = event
    return json.dumps(calendar_dict)
