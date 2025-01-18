
import os
from icalendar import Calendar, Event
from datetime import datetime
import pytz

def create_ics_file(event_data):
    calendar = Calendar()

    event = Event()
    event.add('summary', event_data['summary'])
    event.add('description', event_data['description'])

    start_datetime_str = f"{event_data['start_date']} {event_data['start_time']}"
    end_datetime_str = f"{event_data['end_date']} {event_data['end_time']}"

    timezone = pytz.timezone(event_data['timezone'])

    start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone)
    end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone)

    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)

    calendar.add_component(event)

    return calendar.to_ical()

def save_ics_file(ics_data: bytes, save_path: str = "path") -> str:
    file_name = "event_created.ics"
    file_path = os.path.join(save_path, file_name)
    os.makedirs(save_path, exist_ok=True)
    
    with open(file_path, 'wb') as f:
        f.write(ics_data)
    
    return file_path
