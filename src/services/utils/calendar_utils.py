import calendar
import json

def create_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    days_data = []
    for week in cal:
        for day in week:
            if day != 0:
                day_name = calendar.day_name[calendar.weekday(year, month, day)]
                days_data.append({'day': day, 'dayname': day_name, 'events': []})
    return days_data

def append_event(calendar_data, day, event_data):
    day = int(day)  # Ensure day is an integer
    for day_data in calendar_data:
        for event in event_data:
            if day_data['day'] == day:
                day_data['events'].append(event.content)
                break
    return calendar_data